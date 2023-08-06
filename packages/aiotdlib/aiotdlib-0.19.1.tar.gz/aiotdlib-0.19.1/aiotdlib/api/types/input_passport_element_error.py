# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from .input_passport_element_error_source import InputPassportElementErrorSource
from .passport_element_type import PassportElementType
from ..base_object import BaseObject


class InputPassportElementError(BaseObject):
    """
    Contains the description of an error in a Telegram Passport element; for bots only
    
    :param type_: Type of Telegram Passport element that has the error
    :type type_: :class:`PassportElementType`
    
    :param message: Error message
    :type message: :class:`str`
    
    :param source: Error source
    :type source: :class:`InputPassportElementErrorSource`
    
    """

    ID: str = Field("inputPassportElementError", alias="@type")
    type_: PassportElementType = Field(..., alias='type')
    message: str
    source: InputPassportElementErrorSource

    @staticmethod
    def read(q: dict) -> InputPassportElementError:
        return InputPassportElementError.construct(**q)
