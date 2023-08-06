# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import FormattedText


class ParseMarkdown(BaseObject):
    """
    Parses Markdown entities in a human-friendly format, ignoring markup errors. Can be called synchronously
    
    :param text: The text to parse. For example, "__italic__ ~~strikethrough~~ ||spoiler|| **bold** `code` ```pre``` __[italic__ text_url](telegram.org) __italic**bold italic__bold**"
    :type text: :class:`FormattedText`
    
    """

    ID: str = Field("parseMarkdown", alias="@type")
    text: FormattedText

    @staticmethod
    def read(q: dict) -> ParseMarkdown:
        return ParseMarkdown.construct(**q)
