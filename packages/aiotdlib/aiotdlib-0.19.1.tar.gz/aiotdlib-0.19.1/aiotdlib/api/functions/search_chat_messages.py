# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import MessageSender
from ..types import SearchMessagesFilter


class SearchChatMessages(BaseObject):
    """
    Searches for messages with given words in the chat. Returns the results in reverse chronological order, i.e. in order of decreasing message_id. Cannot be used in secret chats with a non-empty query (searchSecretMessages must be used instead), or without an enabled message database. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
    
    :param chat_id: Identifier of the chat in which to search messages
    :type chat_id: :class:`int`
    
    :param query: Query to search for
    :type query: :class:`str`
    
    :param sender_id: Identifier of the sender of messages to search for; pass null to search for messages from any sender. Not supported in secret chats
    :type sender_id: :class:`MessageSender`
    
    :param from_message_id: Identifier of the message starting from which history must be fetched; use 0 to get results from the last message
    :type from_message_id: :class:`int`
    
    :param offset: Specify 0 to get results from exactly the from_message_id or a negative offset to get the specified message and some newer messages
    :type offset: :class:`int`
    
    :param limit: The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, the limit must be greater than -offset. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
    :type limit: :class:`int`
    
    :param filter_: Additional filter for messages to search; pass null to search for all messages
    :type filter_: :class:`SearchMessagesFilter`
    
    :param message_thread_id: If not 0, only messages in the specified thread will be returned; supergroups only
    :type message_thread_id: :class:`int`
    
    """

    ID: str = Field("searchChatMessages", alias="@type")
    chat_id: int
    query: str
    sender_id: MessageSender
    from_message_id: int
    offset: int
    limit: int
    filter_: SearchMessagesFilter = Field(..., alias='filter')
    message_thread_id: int

    @staticmethod
    def read(q: dict) -> SearchChatMessages:
        return SearchChatMessages.construct(**q)
