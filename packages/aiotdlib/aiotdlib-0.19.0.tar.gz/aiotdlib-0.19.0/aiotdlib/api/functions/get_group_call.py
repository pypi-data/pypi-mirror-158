# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class GetGroupCall(BaseObject):
    """
    Returns information about a group call
    
    :param group_call_id: Group call identifier
    :type group_call_id: :class:`int`
    
    """

    ID: str = Field("getGroupCall", alias="@type")
    group_call_id: int

    @staticmethod
    def read(q: dict) -> GetGroupCall:
        return GetGroupCall.construct(**q)
