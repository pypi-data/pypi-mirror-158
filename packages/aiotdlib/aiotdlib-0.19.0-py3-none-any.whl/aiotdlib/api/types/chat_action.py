# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class ChatAction(BaseObject):
    """
    Describes the different types of activity in a chat
    
    """

    ID: str = Field("chatAction", alias="@type")


class ChatActionCancel(ChatAction):
    """
    The user has canceled the previous action
    
    """

    ID: str = Field("chatActionCancel", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionCancel:
        return ChatActionCancel.construct(**q)


class ChatActionChoosingContact(ChatAction):
    """
    The user is picking a contact to send
    
    """

    ID: str = Field("chatActionChoosingContact", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionChoosingContact:
        return ChatActionChoosingContact.construct(**q)


class ChatActionChoosingLocation(ChatAction):
    """
    The user is picking a location or venue to send
    
    """

    ID: str = Field("chatActionChoosingLocation", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionChoosingLocation:
        return ChatActionChoosingLocation.construct(**q)


class ChatActionChoosingSticker(ChatAction):
    """
    The user is picking a sticker to send
    
    """

    ID: str = Field("chatActionChoosingSticker", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionChoosingSticker:
        return ChatActionChoosingSticker.construct(**q)


class ChatActionRecordingVideo(ChatAction):
    """
    The user is recording a video
    
    """

    ID: str = Field("chatActionRecordingVideo", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionRecordingVideo:
        return ChatActionRecordingVideo.construct(**q)


class ChatActionRecordingVideoNote(ChatAction):
    """
    The user is recording a video note
    
    """

    ID: str = Field("chatActionRecordingVideoNote", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionRecordingVideoNote:
        return ChatActionRecordingVideoNote.construct(**q)


class ChatActionRecordingVoiceNote(ChatAction):
    """
    The user is recording a voice note
    
    """

    ID: str = Field("chatActionRecordingVoiceNote", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionRecordingVoiceNote:
        return ChatActionRecordingVoiceNote.construct(**q)


class ChatActionStartPlayingGame(ChatAction):
    """
    The user has started to play a game
    
    """

    ID: str = Field("chatActionStartPlayingGame", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionStartPlayingGame:
        return ChatActionStartPlayingGame.construct(**q)


class ChatActionTyping(ChatAction):
    """
    The user is typing a message
    
    """

    ID: str = Field("chatActionTyping", alias="@type")

    @staticmethod
    def read(q: dict) -> ChatActionTyping:
        return ChatActionTyping.construct(**q)


class ChatActionUploadingDocument(ChatAction):
    """
    The user is uploading a document
    
    :param progress: Upload progress, as a percentage
    :type progress: :class:`int`
    
    """

    ID: str = Field("chatActionUploadingDocument", alias="@type")
    progress: int

    @staticmethod
    def read(q: dict) -> ChatActionUploadingDocument:
        return ChatActionUploadingDocument.construct(**q)


class ChatActionUploadingPhoto(ChatAction):
    """
    The user is uploading a photo
    
    :param progress: Upload progress, as a percentage
    :type progress: :class:`int`
    
    """

    ID: str = Field("chatActionUploadingPhoto", alias="@type")
    progress: int

    @staticmethod
    def read(q: dict) -> ChatActionUploadingPhoto:
        return ChatActionUploadingPhoto.construct(**q)


class ChatActionUploadingVideo(ChatAction):
    """
    The user is uploading a video
    
    :param progress: Upload progress, as a percentage
    :type progress: :class:`int`
    
    """

    ID: str = Field("chatActionUploadingVideo", alias="@type")
    progress: int

    @staticmethod
    def read(q: dict) -> ChatActionUploadingVideo:
        return ChatActionUploadingVideo.construct(**q)


class ChatActionUploadingVideoNote(ChatAction):
    """
    The user is uploading a video note
    
    :param progress: Upload progress, as a percentage
    :type progress: :class:`int`
    
    """

    ID: str = Field("chatActionUploadingVideoNote", alias="@type")
    progress: int

    @staticmethod
    def read(q: dict) -> ChatActionUploadingVideoNote:
        return ChatActionUploadingVideoNote.construct(**q)


class ChatActionUploadingVoiceNote(ChatAction):
    """
    The user is uploading a voice note
    
    :param progress: Upload progress, as a percentage
    :type progress: :class:`int`
    
    """

    ID: str = Field("chatActionUploadingVoiceNote", alias="@type")
    progress: int

    @staticmethod
    def read(q: dict) -> ChatActionUploadingVoiceNote:
        return ChatActionUploadingVoiceNote.construct(**q)


class ChatActionWatchingAnimations(ChatAction):
    """
    The user is watching animations sent by the other party by clicking on an animated emoji
    
    :param emoji: The animated emoji
    :type emoji: :class:`str`
    
    """

    ID: str = Field("chatActionWatchingAnimations", alias="@type")
    emoji: str

    @staticmethod
    def read(q: dict) -> ChatActionWatchingAnimations:
        return ChatActionWatchingAnimations.construct(**q)
