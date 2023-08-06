# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class EnableProxy(BaseObject):
    """
    Enables a proxy. Only one proxy can be enabled at a time. Can be called before authorization
    
    :param proxy_id: Proxy identifier
    :type proxy_id: :class:`int`
    
    """

    ID: str = Field("enableProxy", alias="@type")
    proxy_id: int

    @staticmethod
    def read(q: dict) -> EnableProxy:
        return EnableProxy.construct(**q)
