# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class CheckPhoneNumberVerificationCode(BaseObject):
    """
    Checks the phone number verification code for Telegram Passport
    
    :param code: Verification code to check
    :type code: :class:`str`
    
    """

    ID: str = Field("checkPhoneNumberVerificationCode", alias="@type")
    code: str

    @staticmethod
    def read(q: dict) -> CheckPhoneNumberVerificationCode:
        return CheckPhoneNumberVerificationCode.construct(**q)
