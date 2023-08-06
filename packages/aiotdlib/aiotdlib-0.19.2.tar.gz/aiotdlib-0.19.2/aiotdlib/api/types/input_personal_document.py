# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from .input_file import InputFile
from ..base_object import BaseObject


class InputPersonalDocument(BaseObject):
    """
    A personal document to be saved to Telegram Passport
    
    :param files: List of files containing the pages of the document
    :type files: :class:`list[InputFile]`
    
    :param translation: List of files containing a certified English translation of the document
    :type translation: :class:`list[InputFile]`
    
    """

    ID: str = Field("inputPersonalDocument", alias="@type")
    files: list[InputFile]
    translation: list[InputFile]

    @staticmethod
    def read(q: dict) -> InputPersonalDocument:
        return InputPersonalDocument.construct(**q)
