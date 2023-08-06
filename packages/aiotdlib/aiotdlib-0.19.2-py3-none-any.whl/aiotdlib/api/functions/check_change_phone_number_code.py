# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class CheckChangePhoneNumberCode(BaseObject):
    """
    Checks the authentication code sent to confirm a new phone number of the user
    
    :param code: Authentication code to check
    :type code: :class:`str`
    
    """

    ID: str = Field("checkChangePhoneNumberCode", alias="@type")
    code: str

    @staticmethod
    def read(q: dict) -> CheckChangePhoneNumberCode:
        return CheckChangePhoneNumberCode.construct(**q)
