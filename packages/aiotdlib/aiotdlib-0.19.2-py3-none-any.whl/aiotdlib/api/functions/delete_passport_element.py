# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import PassportElementType


class DeletePassportElement(BaseObject):
    """
    Deletes a Telegram Passport element
    
    :param type_: Element type
    :type type_: :class:`PassportElementType`
    
    """

    ID: str = Field("deletePassportElement", alias="@type")
    type_: PassportElementType = Field(..., alias='type')

    @staticmethod
    def read(q: dict) -> DeletePassportElement:
        return DeletePassportElement.construct(**q)
