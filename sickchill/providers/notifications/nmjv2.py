# coding=utf-8
# Author: Jasper Lanting
# Based on nmj.py by Nico Berlee: http://nico.berlee.nl/
# URL: https://sickchill.github.io
#
# This file is part of SickChill.
#
# SickChill is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickChill is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickChill. If not, see <http://www.gnu.org/licenses/>.
# Stdlib Imports
import time
# noinspection PyUnresolvedReferences
import urllib.request

from xml.dom.minidom import parseString

# First Party Imports
import sickbeard
from sickbeard import logger

from xml.etree import ElementTree

# Local Folder Imports
# Local Folder Imports
from .base import AbstractNotifier


class Notifier(AbstractNotifier):
    def notify_snatch(self, name):
        return False
        # Not implemented: Start the scanner when snatched does not make any sense

    def notify_download(self, name):
        self._notifyNMJ()

    def notify_subtitle_download(self, name, lang):
        self._notifyNMJ()

    def notify_git_update(self, new_version):
        return False
        # Not implemented, no reason to start scanner.

    def notify_login(self, ipaddress=""):
        return False

    def test_notify(self, host):
        return self._sendNMJ(host)

    def notify_settings(self, host, dbloc, instance):
        """
        Retrieves the NMJv2 database location from Popcorn hour

        host: The hostname/IP of the Popcorn Hour server
        dbloc: 'local' for PCH internal hard drive. 'network' for PCH network shares
        instance: Allows for selection of different DB in case of multiple databases

        Returns: True if the settings were retrieved successfully, False otherwise
        """
        try:
            url_loc = "http://{0}:8008/file_operation?arg0=list_user_storage_file&arg1=&arg2={1}&arg3=20&arg4=true&arg5=true&arg6=true&arg7=all&arg8=name_asc&arg9=false&arg10=false".format(host, instance)
            req = urllib.request.Request(url_loc)
            handle1 = urllib.request.urlopen(req)
            response1 = handle1.read()
            xml = parseString(response1)
            time.sleep(300.0 / 1000.0)
            for node in xml.getElementsByTagName('path'):
                xmlTag = node.toxml()
                xmlData = xmlTag.replace('<path>', '').replace('</path>', '').replace('[=]', '')
                url_db = "http://" + host + ":8008/metadata_database?arg0=check_database&arg1=" + xmlData
                reqdb = urllib.request.Request(url_db)
                handledb = urllib.request.urlopen(reqdb)
                responsedb = handledb.read()
                xmldb = parseString(responsedb)
                returnvalue = xmldb.getElementsByTagName('returnValue')[0].toxml().replace('<returnValue>', '').replace(
                    '</returnValue>', '')
                if returnvalue == "0":
                    DB_path = xmldb.getElementsByTagName('database_path')[0].toxml().replace(
                        '<database_path>', '').replace('</database_path>', '').replace('[=]', '')
                    if dbloc == "local" and DB_path.find("localhost") > -1:
                        sickbeard.NMJv2_HOST = host
                        sickbeard.NMJv2_DATABASE = DB_path
                        return True
                    if dbloc == "network" and DB_path.find("://") > -1:
                        sickbeard.NMJv2_HOST = host
                        sickbeard.NMJv2_DATABASE = DB_path
                        return True

        except IOError as e:
            logger.warning("Warning: Couldn't contact popcorn hour on host {0}: {1}".format(host, e))
            return False
        return False

    def _sendNMJ(self, host):
        """
        Sends a NMJ update command to the specified machine

        host: The hostname/IP to send the request to (no port)
        database: The database to send the request to
        mount: The mount URL to use (optional)

        Returns: True if the request succeeded, False otherwise
        """

        # if a host is provided then attempt to open a handle to that URL
        try:
            url_scandir = "http://" + host + ":8008/metadata_database?arg0=update_scandir&arg1=" + self.config('database') + "&arg2=&arg3=update_all"
            logger.debug("NMJ scan update command sent to host: {0}".format(host))
            url_updatedb = "http://" + host + ":8008/metadata_database?arg0=scanner_start&arg1=" + self.config('database') + "&arg2=background&arg3="
            logger.debug("Try to mount network drive via url: {0}".format(host))
            prereq = urllib.request.Request(url_scandir)
            req = urllib.request.Request(url_updatedb)
            handle1 = urllib.request.urlopen(prereq)
            response1 = handle1.read()
            time.sleep(300.0 / 1000.0)
            handle2 = urllib.request.urlopen(req)
            response2 = handle2.read()
        except IOError as e:
            logger.warning("Warning: Couldn't contact popcorn hour on host {0}: {1}".format(host, e))
            return False
        try:
            et = ElementTree.fromstring(response1)
            result1 = et.findtext("returnValue")
        except SyntaxError as e:
            logger.exception("Unable to parse XML returned from the Popcorn Hour: update_scandir, {0}".format(e))
            return False
        try:
            et = ElementTree.fromstring(response2)
            result2 = et.findtext("returnValue")
        except SyntaxError as e:
            logger.exception("Unable to parse XML returned from the Popcorn Hour: scanner_start, {0}".format(e))
            return False

        # if the result was a number then consider that an error
        error_codes = ["8", "11", "22", "49", "50", "51", "60"]
        error_messages = ["Invalid parameter(s)/argument(s)",
                          "Invalid database path",
                          "Insufficient size",
                          "Database write error",
                          "Database read error",
                          "Open fifo pipe failed",
                          "Read only file system"]
        if int(result1) > 0:
            index = error_codes.index(result1)
            logger.exception("Popcorn Hour returned an error: {0}".format((error_messages[index])))
            return False
        else:
            if int(result2) > 0:
                index = error_codes.index(result2)
                logger.exception("Popcorn Hour returned an error: {0}".format((error_messages[index])))
                return False
            else:
                logger.info("NMJv2 started background scan")
                return True

    def _notifyNMJ(self, host=None, force=False):
        """
        Sends a NMJ update command based on the SB config settings

        host: The host to send the command to (optional, defaults to the host in the config)
        database: The database to use (optional, defaults to the database in the config)
        mount: The mount URL (optional, defaults to the mount URL in the config)
        force: If True then the notification will be sent even if NMJ is disabled in the config
        """
        if not self.config('enabled') and not force:
            logger.debug("Notification for NMJ scan update not enabled, skipping this notification")
            return False

        # fill in omitted parameters
        if not host:
            host = sickbeard.NMJv2_HOST

        logger.debug("Sending scan command for NMJ ")

        return self._sendNMJ(host)
