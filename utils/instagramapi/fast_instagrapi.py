import time
from typing import Set

from instagrapi import MediaMixin, Client
from instagrapi.exceptions import ClientError
from instagrapi.extractors import extract_user_short
from instagrapi.utils import json_value


class FastClient(Client):
    def tagged_users_id(self, user_id: int, amount: int = 0) -> Set[str]:
        """
        Get followers id that tagged the main user

        Parameters
        ----------
        user_id: int
        amount: int, optional
            Maximum number of media to return, default is 0 (all medias)

        Returns
        -------
        List[Media]
            A list of objects of Media
        """
        amount = int(amount)
        user_id = int(user_id)
        try:
            medias = self.fast_usertag_medias_gql(user_id, amount)
        except ClientError:
            medias = self.fast_usertag_medias_v1(user_id, amount)
        return medias

    def fast_usertag_medias_v1(self, user_id: int, amount: int = 0) -> Set[str]:
        """
        Get medias where a user is tagged (by Private Mobile API)
        Parameters
        ----------
        user_id: int
        amount: int, optional
            Maximum number of media to return, default is 0 (all medias)
        Returns
        -------
        List[Media]
            A list of objects of Media
        """
        amount = int(amount)
        user_id = int(user_id)
        medias = []
        next_max_id = ""
        while True:
            try:
                items = self.private_request(f"usertags/{user_id}/feed/", params={"max_id": next_max_id})["items"]
            except Exception as e:
                self.logger.exception(e)
                break
            medias.extend(items)
            if not self.last_json.get("more_available"):
                break
            if amount and len(medias) >= amount:
                break
            next_max_id = self.last_json.get("next_max_id", "")
        if amount:
            medias = medias[:amount]

        tagged_users = set()
        for media in medias:
            try:
                tagged_users.add(str(media["user"]["pk"]))

            # TODO override errors (loggers)
            except KeyError as e:
                self.logger.exception(e)
            except TypeError as e:
                self.logger.exception(e)

        return tagged_users

    def fast_usertag_medias_gql(self,
                           user_id: int, amount: int = 0, sleep: int = 2
                           ) -> Set[str]:
        """
        Get medias where a user is tagged (by Public GraphQL API)
        Parameters
        ----------
        user_id: int
        amount: int, optional
            Maximum number of media to return, default is 0 (all medias)
        sleep: int, optional
            Timeout between pages iterations, default is 2
        Returns
        -------
        List[Media]
            A list of objects of Media
        """
        amount = int(amount)
        user_id = int(user_id)
        medias = []
        end_cursor = None
        variables = {
            "id": user_id,
            "first": 50 if not amount or amount > 50 else amount,
            # These are Instagram restrictions, you can only specify <= 50
        }
        while True:
            if end_cursor:
                variables["after"] = end_cursor
            data = self.public_graphql_request(
                variables, query_hash="be13233562af2d229b008d2976b998b5"
            )
            page_info = json_value(
                data, "user", "edge_user_to_photos_of_you", "page_info", default={}
            )
            edges = json_value(
                data, "user", "edge_user_to_photos_of_you", "edges", default=[]
            )
            for edge in edges:
                medias.append(edge["node"])
            end_cursor = page_info.get("end_cursor")
            if not page_info.get("has_next_page") or not end_cursor:
                break
            if amount and len(medias) >= amount:
                break
            time.sleep(sleep)
        if amount:
            medias = medias[:amount]

        tagged_users = set()
        for media in medias:
            try:
                tagged_users.add(str(media["owner"]["id"]))

            # TODO override errors (loggers)
            except KeyError as e:
                self.logger.exception(e)
            except TypeError as e:
                self.logger.exception(e)

        return tagged_users