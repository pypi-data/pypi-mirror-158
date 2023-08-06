# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import PassportElementType


class GetPassportElement(BaseObject):
    """
    Returns one of the available Telegram Passport elements
    
    :param type_: Telegram Passport element type
    :type type_: :class:`PassportElementType`
    
    :param password: Password of the current user
    :type password: :class:`str`
    
    """

    ID: str = Field("getPassportElement", alias="@type")
    type_: PassportElementType = Field(..., alias='type')
    password: str

    @staticmethod
    def read(q: dict) -> GetPassportElement:
        return GetPassportElement.construct(**q)
