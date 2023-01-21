import os
from enum import Enum

from pathlib import Path
from typing import Iterable, Set


# Create and configure logger
# from core.settings import INSTAGRAM_LOG_PATH
from utils.instagramapi.fast_instagrapi import FastClient

# logging.basicConfig(filename=INSTAGRAM_LOG_PATH,
#                     format='%(asctime)s %(message)s',
#                     filemode='w')
#
# logger = logging.getLogger()
#
# logger.setLevel(logging.DEBUG)


class Mentions(str, Enum):
    MEDIA = "usertags"
    HISTORY = "mentions"


class InstagramLogin:
    def __init__(self, username, password, file_path: Path = None):
        self.client = FastClient()
        self._username = username
        self._password = password
        self._file_path = file_path
        self.login()

    def perform_credential_login(self) -> None:
        self.client.login(self._username, self._password)

    def login(self) -> None:
        """
        Authenticate to Instagram account

        Basically there are two cases:
            1. When we are signing in for the first time
            2. When we have already signed in and want to use other times through sessions we've created

        Returns:
            None
        """
        if not self.is_dump_exists:
            self.perform_credential_login()
            self.client.dump_settings(self._file_path)

        else:
            self.client.load_settings(self._file_path)
            self.perform_credential_login()

    @property
    def is_dump_exists(self) -> bool:
        return os.path.exists(self._file_path)

    def get_client(self):
        return self.client


class InstagramBaseParser:
    def __init__(self, client: InstagramLogin):
        self.client = client.get_client()
        self.user_id = str(self.client.user_id)

    def _is_following(self, follower_user_id: str) -> bool:
        """
        Indicates whether particular user (NOT MAIN) is following MAIN USER.

        Parameters
        ----------
        follower_user_id: str
            User id of expected follower

        Returns
        -------
        bool
            Is user following MAIN USER
        """
        if follower_user_id in self.client.user_followers(self.user_id, amount=20):
            return True
        return False

    def _is_tagged(self, follower_user_id: str):
        return follower_user_id in self.tagged_users

    def find(self, posts: Iterable, attribute: Mentions) -> bool:
        """
        If mention of user is found

                Parameters
        ----------
        posts: Iterable
            Posts are medias or histories.

        attribute: str
            Attribute is needed, because instagrapi has two different keys to access mentions
            There are only two options:
                - "usertags" for medias
                - "mentions" for histories
        """
        for post in posts:
            for mention in getattr(post, attribute):
                try:
                    if mention.user.pk == self.user_id:
                        return True
                except AttributeError as error:
                    # TODO Errors should pass silently, release logging here...
                    pass
        return False

    @property
    def tagged_users(self) -> Set[str]:
        return self.client.tagged_users_id(int(self.user_id))


class ParseOneUserInstagram(InstagramBaseParser):
    def __init__(self, follower_username: str, client: InstagramLogin):
        super().__init__(client)
        self.follower_user_id = self.client.user_id_from_username(follower_username)

    def is_following(self):
        return self._is_following(
            follower_user_id=self.follower_user_id
        )

    def is_tagged(self):
        return self._is_tagged(self.follower_user_id)

    # def is_in_story_mentions(self):
    #     return self.find(
    #         posts=self._get_histories(int(self.follower_user_id)),
    #         attribute=Mentions.HISTORY
    #     )
    #
    # def is_in_all_posts(self):
    #     """
    #     Parses all medias and histories and tries to find mention
    #     """
    #     return any((self.is_in_story_mentions(), self.is_in_media_mentions()))


class ParseMultipleInstagram(InstagramBaseParser):
    def get_follower_id(self, username):
        return self.client.user_id_from_username(username)

    def is_following(self, follower_username):
        return self._is_following(
            follower_user_id=self.get_follower_id(follower_username)
        )

    def is_tagged(self, follower_username):
        return self._is_tagged(self.get_follower_id(follower_username))

    # def is_in_story_mentions(self, follower_username):
    #     return self.find(
    #         posts=self._get_histories(int(self.get_follower_id(follower_username))),
    #         attribute=Mentions.HISTORY
    #     )
    #
    # def is_in_all_posts(self, follower_username):
    #     """
    #     Parses all medias and histories and tries to find mention
    #     """
    #     return any((self.is_in_story_mentions(follower_username), self.is_in_media_mentions(follower_username)))
