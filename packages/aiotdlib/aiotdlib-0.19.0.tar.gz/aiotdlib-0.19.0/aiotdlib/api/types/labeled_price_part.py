# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class LabeledPricePart(BaseObject):
    """
    Portion of the price of a product (e.g., "delivery cost", "tax amount")
    
    :param label: Label for this portion of the product price
    :type label: :class:`str`
    
    :param amount: Currency amount in the smallest units of the currency
    :type amount: :class:`int`
    
    """

    ID: str = Field("labeledPricePart", alias="@type")
    label: str
    amount: int

    @staticmethod
    def read(q: dict) -> LabeledPricePart:
        return LabeledPricePart.construct(**q)
