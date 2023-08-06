# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import InputSticker


class UploadStickerFile(BaseObject):
    """
    Uploads a file with a sticker; returns the uploaded file
    
    :param user_id: Sticker file owner; ignored for regular users
    :type user_id: :class:`int`
    
    :param sticker: Sticker file to upload
    :type sticker: :class:`InputSticker`
    
    """

    ID: str = Field("uploadStickerFile", alias="@type")
    user_id: int
    sticker: InputSticker

    @staticmethod
    def read(q: dict) -> UploadStickerFile:
        return UploadStickerFile.construct(**q)
