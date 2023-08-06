# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class CheckPasswordRecoveryCode(BaseObject):
    """
    Checks whether a 2-step verification password recovery code sent to an email address is valid
    
    :param recovery_code: Recovery code to check
    :type recovery_code: :class:`str`
    
    """

    ID: str = Field("checkPasswordRecoveryCode", alias="@type")
    recovery_code: str

    @staticmethod
    def read(q: dict) -> CheckPasswordRecoveryCode:
        return CheckPasswordRecoveryCode.construct(**q)
