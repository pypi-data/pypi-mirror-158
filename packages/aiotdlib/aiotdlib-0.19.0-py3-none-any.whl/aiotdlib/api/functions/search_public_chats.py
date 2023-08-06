# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class SearchPublicChats(BaseObject):
    """
    Searches public chats by looking for specified query in their username and title. Currently, only private chats, supergroups and channels can be public. Returns a meaningful number of results. Excludes private chats with contacts and chats from the chat list from the results
    
    :param query: Query to search for
    :type query: :class:`str`
    
    """

    ID: str = Field("searchPublicChats", alias="@type")
    query: str

    @staticmethod
    def read(q: dict) -> SearchPublicChats:
        return SearchPublicChats.construct(**q)
