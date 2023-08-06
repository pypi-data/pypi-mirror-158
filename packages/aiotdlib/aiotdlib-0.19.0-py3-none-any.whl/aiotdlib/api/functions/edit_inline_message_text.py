# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import InputMessageContent
from ..types import ReplyMarkup


class EditInlineMessageText(BaseObject):
    """
    Edits the text of an inline text or game message sent via a bot; for bots only
    
    :param inline_message_id: Inline message identifier
    :type inline_message_id: :class:`str`
    
    :param reply_markup: The new message reply markup; pass null if none
    :type reply_markup: :class:`ReplyMarkup`
    
    :param input_message_content: New text content of the message. Must be of type inputMessageText
    :type input_message_content: :class:`InputMessageContent`
    
    """

    ID: str = Field("editInlineMessageText", alias="@type")
    inline_message_id: str
    reply_markup: ReplyMarkup
    input_message_content: InputMessageContent

    @staticmethod
    def read(q: dict) -> EditInlineMessageText:
        return EditInlineMessageText.construct(**q)
