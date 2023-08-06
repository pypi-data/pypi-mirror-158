# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import PublicChatType


class CheckCreatedPublicChatsLimit(BaseObject):
    """
    Checks whether the maximum number of owned public chats has been reached. Returns corresponding error if the limit was reached. The limit can be increased with Telegram Premium
    
    :param type_: Type of the public chats, for which to check the limit
    :type type_: :class:`PublicChatType`
    
    """

    ID: str = Field("checkCreatedPublicChatsLimit", alias="@type")
    type_: PublicChatType = Field(..., alias='type')

    @staticmethod
    def read(q: dict) -> CheckCreatedPublicChatsLimit:
        return CheckCreatedPublicChatsLimit.construct(**q)
