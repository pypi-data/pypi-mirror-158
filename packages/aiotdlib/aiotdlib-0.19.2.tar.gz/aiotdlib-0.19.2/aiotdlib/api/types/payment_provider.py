# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class PaymentProvider(BaseObject):
    """
    Contains information about a payment provider
    
    """

    ID: str = Field("paymentProvider", alias="@type")


class PaymentProviderOther(PaymentProvider):
    """
    Some other payment provider, for which a web payment form must be shown
    
    :param url: Payment form URL
    :type url: :class:`str`
    
    """

    ID: str = Field("paymentProviderOther", alias="@type")
    url: str

    @staticmethod
    def read(q: dict) -> PaymentProviderOther:
        return PaymentProviderOther.construct(**q)


class PaymentProviderSmartGlocal(PaymentProvider):
    """
    Smart Glocal payment provider
    
    :param public_token: Public payment token
    :type public_token: :class:`str`
    
    """

    ID: str = Field("paymentProviderSmartGlocal", alias="@type")
    public_token: str

    @staticmethod
    def read(q: dict) -> PaymentProviderSmartGlocal:
        return PaymentProviderSmartGlocal.construct(**q)


class PaymentProviderStripe(PaymentProvider):
    """
    Stripe payment provider
    
    :param publishable_key: Stripe API publishable key
    :type publishable_key: :class:`str`
    
    :param need_country: True, if the user country must be provided
    :type need_country: :class:`bool`
    
    :param need_postal_code: True, if the user ZIP/postal code must be provided
    :type need_postal_code: :class:`bool`
    
    :param need_cardholder_name: True, if the cardholder name must be provided
    :type need_cardholder_name: :class:`bool`
    
    """

    ID: str = Field("paymentProviderStripe", alias="@type")
    publishable_key: str
    need_country: bool
    need_postal_code: bool
    need_cardholder_name: bool

    @staticmethod
    def read(q: dict) -> PaymentProviderStripe:
        return PaymentProviderStripe.construct(**q)
