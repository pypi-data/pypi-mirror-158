# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class CheckEmailAddressVerificationCode(BaseObject):
    """
    Checks the email address verification code for Telegram Passport
    
    :param code: Verification code to check
    :type code: :class:`str`
    
    """

    ID: str = Field("checkEmailAddressVerificationCode", alias="@type")
    code: str

    @staticmethod
    def read(q: dict) -> CheckEmailAddressVerificationCode:
        return CheckEmailAddressVerificationCode.construct(**q)
