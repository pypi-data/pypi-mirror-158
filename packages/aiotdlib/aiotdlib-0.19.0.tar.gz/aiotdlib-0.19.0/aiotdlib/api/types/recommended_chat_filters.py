# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from .recommended_chat_filter import RecommendedChatFilter
from ..base_object import BaseObject


class RecommendedChatFilters(BaseObject):
    """
    Contains a list of recommended chat filters
    
    :param chat_filters: List of recommended chat filters
    :type chat_filters: :class:`list[RecommendedChatFilter]`
    
    """

    ID: str = Field("recommendedChatFilters", alias="@type")
    chat_filters: list[RecommendedChatFilter]

    @staticmethod
    def read(q: dict) -> RecommendedChatFilters:
        return RecommendedChatFilters.construct(**q)
