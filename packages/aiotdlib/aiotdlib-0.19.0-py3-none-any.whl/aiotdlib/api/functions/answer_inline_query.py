# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import InputInlineQueryResult


class AnswerInlineQuery(BaseObject):
    """
    Sets the result of an inline query; for bots only
    
    :param inline_query_id: Identifier of the inline query
    :type inline_query_id: :class:`int`
    
    :param is_personal: Pass true if results may be cached and returned only for the user that sent the query. By default, results may be returned to any user who sends the same query
    :type is_personal: :class:`bool`
    
    :param results: The results of the query
    :type results: :class:`list[InputInlineQueryResult]`
    
    :param cache_time: Allowed time to cache the results of the query, in seconds
    :type cache_time: :class:`int`
    
    :param next_offset: Offset for the next inline query; pass an empty string if there are no more results
    :type next_offset: :class:`str`
    
    :param switch_pm_text: If non-empty, this text must be shown on the button that opens a private chat with the bot and sends a start message to the bot with the parameter switch_pm_parameter
    :type switch_pm_text: :class:`str`
    
    :param switch_pm_parameter: The parameter for the bot start message
    :type switch_pm_parameter: :class:`str`
    
    """

    ID: str = Field("answerInlineQuery", alias="@type")
    inline_query_id: int
    is_personal: bool
    results: list[InputInlineQueryResult]
    cache_time: int
    next_offset: str
    switch_pm_text: str
    switch_pm_parameter: str

    @staticmethod
    def read(q: dict) -> AnswerInlineQuery:
        return AnswerInlineQuery.construct(**q)
