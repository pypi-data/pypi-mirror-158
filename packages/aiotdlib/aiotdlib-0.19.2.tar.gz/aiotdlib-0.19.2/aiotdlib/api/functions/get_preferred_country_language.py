# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class GetPreferredCountryLanguage(BaseObject):
    """
    Returns an IETF language tag of the language preferred in the country, which must be used to fill native fields in Telegram Passport personal details. Returns a 404 error if unknown
    
    :param country_code: A two-letter ISO 3166-1 alpha-2 country code
    :type country_code: :class:`str`
    
    """

    ID: str = Field("getPreferredCountryLanguage", alias="@type")
    country_code: str

    @staticmethod
    def read(q: dict) -> GetPreferredCountryLanguage:
        return GetPreferredCountryLanguage.construct(**q)
