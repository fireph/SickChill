# coding=utf-8
# Author: Nic Wolfe <nic@wolfeden.ca>
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
import json
# noinspection PyUnresolvedReferences
import urllib

# First Party Imports
import sickbeard
from sickbeard import logger

# Local Folder Imports
from .base import AbstractNotifier


class Notifier(AbstractNotifier):

    def _notify_emby(self, message, host=None, emby_apikey=None):
        """Handles notifying Emby host via HTTP API

        Returns:
            Returns True for no issue or False if there was an error

        """

        # fill in omitted parameters
        if not host:
            host = sickbeard.EMBY_HOST
        if not emby_apikey:
            emby_apikey = sickbeard.EMBY_APIKEY

        url = '{0}/emby/Notifications/Admin'.format(host)
        values = {'Name': 'SickChill', 'Description': message, 'ImageUrl': sickbeard.LOGO_URL}
        data = json.dumps(values)

        try:
            req = urllib.request.Request(url, data)
            req.add_header('X-MediaBrowser-Token', emby_apikey)
            req.add_header('Content-Type', 'application/json')

            response = urllib.request.urlopen(req)
            result = response.read()
            response.close()

            logger.debug('EMBY: HTTP response: ' + result.replace('\n', ''))
            return True

        except (urllib.error.URLError, IOError) as e:
            logger.warning('EMBY: Warning: Couldn\'t contact Emby at ' + url + ' ' + str(e))
            return False


##############################################################################
# Public functions
##############################################################################

    def test_notify(self, host, emby_apikey):
        return self._notify_emby('This is a test notification from SickChill', host, emby_apikey)

    def update_library(self, show=None):
        """Handles updating the Emby Media Server host via HTTP API

        Returns:
            Returns True for no issue or False if there was an error

        """

        if self.config('enabled'):
            if not sickbeard.EMBY_HOST:
                logger.debug('EMBY: No host specified, check your settings')
                return False

            if show:
                if show.indexer == 1:
                    provider = 'tvdb'
                elif show.indexer == 2:
                    logger.warning('EMBY: TVRage Provider no longer valid')
                    return False
                else:
                    logger.warning('EMBY: Provider unknown')
                    return False
                query = '?{0}id={1}'.format(provider, show.indexerid)
            else:
                query = ''

            url = '{0}/emby/Library/Series/Updated{1}'.format(sickbeard.EMBY_HOST, query)

            values = {}
            data = urllib.parse.urlencode(values)
            try:
                req = urllib.request.Request(url, data)
                req.add_header('X-MediaBrowser-Token', sickbeard.EMBY_APIKEY)

                response = urllib.request.urlopen(req)
                result = response.read()
                response.close()

                logger.debug('EMBY: HTTP response: ' + result.replace('\n', ''))
                return True

            except (urllib.error.URLError, IOError) as e:
                logger.warning('EMBY: Warning: Couldn\'t contact Emby at ' + url + ' ' + str(e))
                return False