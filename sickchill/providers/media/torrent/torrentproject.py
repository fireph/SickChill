# coding=utf-8
# Author: Gonçalo M. (aka duramato/supergonkas) <supergonkas@gmail.com>
#
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
# Third Party Imports
import validators

# First Party Imports
from sickbeard import logger, tvcache
from sickchill.helper.common import convert_size, try_int
from sickchill.providers.media.torrent import TorrentProvider


class TorrentProjectProvider(TorrentProvider):

    def __init__(self):

        # Provider Init
        super().__init__('TorrentProject', extra_options=tuple([]))

        # URLs
        self.url = 'https://torrentproject.se/'

        self.ability_status = self.PROVIDER_BACKLOG

        # Cache
        self.cache_search_params = {'RSS': ['0day']}

    def search(self, search_strings, ep_obj=None) -> list:
        results = []

        search_params = {
            'out': 'json',
            'filter': 2101,
            'showmagnets': 'on',
            'num': 50
        }

        for mode in search_strings:  # Mode = RSS, Season, Episode
            items = []
            logger.debug("Search Mode: {0}".format(mode))

            for search_string in search_strings[mode]:

                if mode != 'RSS':
                    logger.debug("Search string: {0}".format(search_string))

                search_params['s'] = search_string

                if self.config('custom_url'):
                    if not validators.url(self.config('custom_url')):
                        logger.warning("Invalid custom url set, please check your settings")
                        return results
                    search_url = self.config('custom_url')
                else:
                    search_url = self.url

                torrents = self.get_url(search_url, params=search_params, returns='json')
                if not (torrents and "total_found" in torrents and int(torrents["total_found"]) > 0):
                    logger.debug("Data returned from provider does not contain any torrents")
                    continue

                del torrents["total_found"]

                results = []
                for i in torrents:
                    title = torrents[i]["title"]
                    seeders = try_int(torrents[i]["seeds"], 1)
                    leechers = try_int(torrents[i]["leechs"], 0)
                    if seeders < self.config('minseed') or leechers < self.config('minleech'):
                        if mode != 'RSS':
                            logger.debug("Torrent doesn't meet minimum seeds & leechers not selecting : {0}".format(title))
                        continue

                    t_hash = torrents[i]["torrent_hash"]
                    torrent_size = torrents[i]["torrent_size"]
                    if not all([t_hash, torrent_size]):
                        continue
                    download_url = torrents[i]["magnet"] + self._custom_trackers
                    size = convert_size(torrent_size) or -1

                    if not all([title, download_url]):
                        continue

                    item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers, 'hash': t_hash}

                    if mode != 'RSS':
                        logger.debug("Found result: {0} with {1} seeders and {2} leechers".format
                                   (title, seeders, leechers))

                    items.append(item)

            # For each search mode sort all the items by seeders if available
            items.sort(key=lambda d: try_int(d.get('seeders', 0)), reverse=True)
            results += items

        return results


