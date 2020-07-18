# coding=utf-8
# Author: Dieter Blomme <dieterblomme@gmail.com>
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
# First Party Imports
import sickbeard
import sickchill
from sickbeard import logger
from sickchill.providers.notifications.base import AbstractNotifier

# Local Folder Imports
from .api import TraktAPI
from .exceptions import traktAuthException, traktException, traktServerBusy


class Notifier(AbstractNotifier):
    """
    A "notifier" for trakt.tv which keeps track of what has and hasn't been added to your library.
    """
    def __init__(self):
        super().__init__('Trakt')

    def notify_snatch(self, name):
        pass

    def notify_download(self, name):
        pass

    def notify_subtitle_download(self, name, lang):
        pass

    def notify_git_update(self, new_version):
        pass

    def notify_login(self, ipaddress=""):
        pass

    def notify_postprocess(self, name):
        pass

    def update_library(self, ep_obj):
        """
        Sends a request to trakt indicating that the given episode is part of our library.

        ep_obj: The TVEpisode object to add to trakt
        """

        trakt_api = TraktAPI(self.config('timeout'))

        if self.config('enabled'):
            try:
                # URL parameters
                data = {
                    'shows': [
                        {
                            'title': ep_obj.show.name,
                            'year': ep_obj.show.startyear,
                            'ids': {ep_obj.idxr.slug: ep_obj.show.indexerid},
                        }
                    ]
                }

                if self.config('sync_watchlist') and self.config('remove_from_serieslist'):
                        trakt_api.traktRequest("sync/watchlist/remove", data, method='POST')

                # Add Season and Episode + Related Episodes
                data['shows'][0]['seasons'] = [{'number': ep_obj.season, 'episodes': []}]

                for relEp_Obj in [ep_obj] + ep_obj.relatedEps:
                    data['shows'][0]['seasons'][0]['episodes'].append({'number': relEp_Obj.episode})

                if self.config('sync_watchlist') and self.config('remove_from_watchlist'):
                    trakt_api.traktRequest("sync/watchlist/remove", data, method='POST')

                # update library
                trakt_api.traktRequest("sync/collection", data, method='POST')

            except (traktException, traktAuthException, traktServerBusy) as e:
                logger.warning("Could not connect to Trakt service: {0}".format(str(e)))

    def update_watchlist(self, show_obj=None, s=None, e=None, data_show=None, data_episode=None, update="add"):

        """
        Sends a request to trakt indicating that the given episode is part of our library.

        show_obj: The TVShow object to add to trakt
        s: season number
        e: episode number
        data_show: structured object of shows trakt type
        data_episode: structured object of episodes trakt type
        update: type o action add or remove
        """

        trakt_api = TraktAPI(self.config('timeout'))

        if self.config('enabled'):

            data = {}
            try:
                # URL parameters
                if show_obj is not None:
                    data = {
                        'shows': [
                            {
                                'title': show_obj.name,
                                'year': show_obj.startyear,
                                'ids': {show_obj.idxr.slug: show_obj.indexerid},
                            }
                        ]
                    }
                elif data_show is not None:
                    data.update(data_show)
                else:
                    logger.warning("there's a coding problem contact developer. It's needed to be provided at lest one of the two: data_show or show_obj")
                    return False

                if data_episode is not None:
                    data['shows'][0].update(data_episode)

                elif s is not None:
                    # trakt URL parameters
                    season = {
                        'season': [
                            {
                                'number': s,
                            }
                        ]
                    }

                    if e is not None:
                        # trakt URL parameters
                        episode = {
                            'episodes': [
                                {
                                    'number': e
                                }
                            ]
                        }

                        season['season'][0].update(episode)

                    data['shows'][0].update(season)

                trakt_url = "sync/watchlist"
                if update == "remove":
                    trakt_url += "/remove"

                trakt_api.traktRequest(trakt_url, data, method='POST')

            except (traktException, traktAuthException, traktServerBusy) as e:
                logger.warning("Could not connect to Trakt service: {0}".format(str(e)))
                return False

        return True

    @staticmethod
    def trakt_show_data_generate(data):

        showList = []
        # TODO: is indexer and indexerid swapped here or in traktChecker:591? !Important
        for indexer, indexerid, title, year in data:
            show = {'title': title, 'year': year, 'ids': {sickchill.indexer.slug(indexer): indexerid}}
            showList.append(show)

        post_data = {'shows': showList}

        return post_data

    @staticmethod
    def trakt_episode_data_generate(data):

        # Find how many unique season we have
        uniqueSeasons = []
        for season, episode in data:
            if season not in uniqueSeasons:
                uniqueSeasons.append(season)

        # build the query
        seasonsList = []
        for searchedSeason in uniqueSeasons:
            episodesList = []
            for season, episode in data:
                if season == searchedSeason:
                    episodesList.append({'number': episode})
            seasonsList.append({'number': searchedSeason, 'episodes': episodesList})

        post_data = {'seasons': seasonsList}

        return post_data

    @staticmethod
    def test_notify(username, blacklist_name=None):
        """
        Sends a test notification to trakt with the given authentication info and returns a boolean
        representing success.

        api: The api string to use
        username: The username to use
        blacklist_name: slug of trakt list used to hide not interested show

        Returns: True if the request succeeded, False otherwise
        """
        try:
            trakt_api = TraktAPI(self.config('timeout'))
            trakt_api.validateAccount()
            if blacklist_name and blacklist_name is not None:
                trakt_lists = trakt_api.traktRequest("users/" + username + "/lists")
                found = False
                for trakt_list in trakt_lists:
                    if trakt_list['ids']['slug'] == blacklist_name:
                        return "Test notice sent successfully to Trakt"
                if not found:
                    return "Trakt blacklist doesn't exists"
            else:
                return "Test notice sent successfully to Trakt"
        except (traktException, traktAuthException, traktServerBusy) as e:
            logger.warning("Could not connect to Trakt service: {0}".format(str(e)))
            return "Test notice failed to Trakt: {0}".format(str(e))