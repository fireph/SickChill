# coding=utf-8
# Author: Idan Gutman
# Modified by jkaberg, https://github.com/jkaberg for SceneAccess
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
import re
import time

# Third Party Imports
from requests.compat import quote, urljoin
from requests.utils import dict_from_cookiejar

# First Party Imports
import sickbeard
from sickbeard import logger, tvcache
from sickbeard.bs4_parser import BS4Parser
from sickbeard.common import cpu_presets
from sickchill.helper.common import convert_size, try_int
from sickchill.providers.media.torrent import TorrentProvider


class SCCProvider(TorrentProvider):

    def __init__(self):

        super().__init__('SceneAccess', extra_options=tuple([]))

        self.urls = {
            'base_url': 'https://sceneaccess.eu',
            'login': 'https://sceneaccess.eu/login',
            'detail': 'https://www.sceneaccess.eu/details?id=%s',
            'search': 'https://sceneaccess.eu/all?search=%s&method=1&%s',
            'download': 'https://www.sceneaccess.eu/%s'
        }

        self.url = self.urls['base_url']

        self.categories = {
            'Season': 'c26=26&c44=44&c45=45',  # Archive, non-scene HD, non-scene SD; need to include non-scene because WEB-DL packs get added to those categories
            'Episode': 'c17=17&c27=27&c33=33&c34=34&c44=44&c45=45',  # TV HD, TV SD, non-scene HD, non-scene SD, foreign XviD, foreign x264
            'RSS': 'c17=17&c26=26&c27=27&c33=33&c34=34&c44=44&c45=45'  # Season + Episode
        }

    def login(self):
        if any(dict_from_cookiejar(self.session.cookies).values()):
            return True

        login_params = {
            'username': self.config('username'),
            'password': self.config('password'),
            'submit': 'come on in'
        }

        response = self.get_url(self.urls['login'], post_data=login_params, returns='text')
        if not response:
            logger.warning("Unable to connect to provider")
            return False

        if re.search(r'Username or password incorrect', response) \
                or re.search(r'<title>SceneAccess \| Login</title>', response):
            logger.warning("Invalid username or password. Check your settings")
            return False

        return True

    @staticmethod
    def _isSection(section, text):
        title = r'<title>.+? \| {0}</title>'.format(section)
        return re.search(title, text, re.I)

    def search(self, search_strings, ep_obj=None) -> list:
        results = []
        if not self.login():
            return results

        for mode in search_strings:
            items = []
            if mode != 'RSS':
                logger.debug("Search Mode: {0}".format(mode))
            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    logger.debug("Search string: {0}".format(search_string))

                search_url = self.urls['search'] % (quote(search_string), self.categories[mode])

                try:
                    data = self.get_url(search_url, returns='text')
                    time.sleep(cpu_presets[sickbeard.CPU_PRESET])
                except Exception as e:
                    logger.warning("Unable to fetch data. Error: {0}".format(repr(e)))

                if not data:
                    continue

                with BS4Parser(data, 'html5lib') as html:
                    torrent_table = html.find('table', id='torrents-table')
                    torrent_rows = torrent_table('tr') if torrent_table else []

                    # Continue only if at least one Release is found
                    if len(torrent_rows) < 2:
                        logger.debug("Data returned from provider does not contain any torrents")
                        continue

                    for result in torrent_table('tr')[1:]:

                        try:
                            link = result.find('td', class_='ttr_name').find('a')
                            url = result.find('td', class_='td_dl').find('a')

                            title = link.string
                            if re.search(r'\.\.\.', title):
                                data = self.get_url(urljoin(self.url, link['href']), returns='text')
                                if data:
                                    with BS4Parser(data) as details_html:
                                        title = re.search('(?<=").+(?<!")', details_html.title.string).group(0)
                            download_url = self.urls['download'] % url['href']
                            seeders = int(result.find('td', class_='ttr_seeders').string)
                            leechers = int(result.find('td', class_='ttr_leechers').string)
                            torrent_size = result.find('td', class_='ttr_size').contents[0]

                            size = convert_size(torrent_size) or -1
                        except (AttributeError, TypeError):
                            continue

                        if not all([title, download_url]):
                            continue

                        # Filter unseeded torrent
                        if seeders < self.config('minseed') or leechers < self.config('minleech'):
                            if mode != 'RSS':
                                logger.debug(
                                    "Discarding torrent because it doesn't meet the minimum seeders or leechers: {0} (S:{1} L:{2})".format(title, seeders, leechers))
                            continue

                        item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers, 'hash': ''}
                        if mode != 'RSS':
                            logger.debug("Found result: {0} with {1} seeders and {2} leechers".format(title, seeders, leechers))

                        items.append(item)

            # For each search mode sort all the items by seeders if available
            items.sort(key=lambda d: try_int(d.get('seeders', 0)), reverse=True)

            results += items

        return results


