# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class ChatInviteLinkMember(BaseObject):
    """
    Describes a chat member joined a chat via an invite link
    
    :param user_id: User identifier
    :type user_id: :class:`int`
    
    :param joined_chat_date: Point in time (Unix timestamp) when the user joined the chat
    :type joined_chat_date: :class:`int`
    
    :param approver_user_id: User identifier of the chat administrator, approved user join request
    :type approver_user_id: :class:`int`
    
    """

    ID: str = Field("chatInviteLinkMember", alias="@type")
    user_id: int
    joined_chat_date: int
    approver_user_id: int

    @staticmethod
    def read(q: dict) -> ChatInviteLinkMember:
        return ChatInviteLinkMember.construct(**q)
