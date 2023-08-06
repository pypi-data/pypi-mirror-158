# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class CloseSecretChat(BaseObject):
    """
    Closes a secret chat, effectively transferring its state to secretChatStateClosed
    
    :param secret_chat_id: Secret chat identifier
    :type secret_chat_id: :class:`int`
    
    """

    ID: str = Field("closeSecretChat", alias="@type")
    secret_chat_id: int

    @staticmethod
    def read(q: dict) -> CloseSecretChat:
        return CloseSecretChat.construct(**q)
