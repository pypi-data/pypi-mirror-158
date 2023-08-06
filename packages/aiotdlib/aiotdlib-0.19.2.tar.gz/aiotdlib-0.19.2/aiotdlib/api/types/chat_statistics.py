# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from .chat_statistics_administrator_actions_info import ChatStatisticsAdministratorActionsInfo
from .chat_statistics_inviter_info import ChatStatisticsInviterInfo
from .chat_statistics_message_interaction_info import ChatStatisticsMessageInteractionInfo
from .chat_statistics_message_sender_info import ChatStatisticsMessageSenderInfo
from .date_range import DateRange
from .statistical_graph import StatisticalGraph
from .statistical_value import StatisticalValue
from ..base_object import BaseObject


class ChatStatistics(BaseObject):
    """
    Contains a detailed statistics about a chat
    
    """

    ID: str = Field("chatStatistics", alias="@type")


class ChatStatisticsChannel(ChatStatistics):
    """
    A detailed statistics about a channel chat
    
    :param period: A period to which the statistics applies
    :type period: :class:`DateRange`
    
    :param member_count: Number of members in the chat
    :type member_count: :class:`StatisticalValue`
    
    :param mean_view_count: Mean number of times the recently sent messages was viewed
    :type mean_view_count: :class:`StatisticalValue`
    
    :param mean_share_count: Mean number of times the recently sent messages was shared
    :type mean_share_count: :class:`StatisticalValue`
    
    :param enabled_notifications_percentage: A percentage of users with enabled notifications for the chat
    :type enabled_notifications_percentage: :class:`float`
    
    :param member_count_graph: A graph containing number of members in the chat
    :type member_count_graph: :class:`StatisticalGraph`
    
    :param join_graph: A graph containing number of members joined and left the chat
    :type join_graph: :class:`StatisticalGraph`
    
    :param mute_graph: A graph containing number of members muted and unmuted the chat
    :type mute_graph: :class:`StatisticalGraph`
    
    :param view_count_by_hour_graph: A graph containing number of message views in a given hour in the last two weeks
    :type view_count_by_hour_graph: :class:`StatisticalGraph`
    
    :param view_count_by_source_graph: A graph containing number of message views per source
    :type view_count_by_source_graph: :class:`StatisticalGraph`
    
    :param join_by_source_graph: A graph containing number of new member joins per source
    :type join_by_source_graph: :class:`StatisticalGraph`
    
    :param language_graph: A graph containing number of users viewed chat messages per language
    :type language_graph: :class:`StatisticalGraph`
    
    :param message_interaction_graph: A graph containing number of chat message views and shares
    :type message_interaction_graph: :class:`StatisticalGraph`
    
    :param instant_view_interaction_graph: A graph containing number of views of associated with the chat instant views
    :type instant_view_interaction_graph: :class:`StatisticalGraph`
    
    :param recent_message_interactions: Detailed statistics about number of views and shares of recently sent messages
    :type recent_message_interactions: :class:`list[ChatStatisticsMessageInteractionInfo]`
    
    """

    ID: str = Field("chatStatisticsChannel", alias="@type")
    period: DateRange
    member_count: StatisticalValue
    mean_view_count: StatisticalValue
    mean_share_count: StatisticalValue
    enabled_notifications_percentage: float
    member_count_graph: StatisticalGraph
    join_graph: StatisticalGraph
    mute_graph: StatisticalGraph
    view_count_by_hour_graph: StatisticalGraph
    view_count_by_source_graph: StatisticalGraph
    join_by_source_graph: StatisticalGraph
    language_graph: StatisticalGraph
    message_interaction_graph: StatisticalGraph
    instant_view_interaction_graph: StatisticalGraph
    recent_message_interactions: list[ChatStatisticsMessageInteractionInfo]

    @staticmethod
    def read(q: dict) -> ChatStatisticsChannel:
        return ChatStatisticsChannel.construct(**q)


class ChatStatisticsSupergroup(ChatStatistics):
    """
    A detailed statistics about a supergroup chat
    
    :param period: A period to which the statistics applies
    :type period: :class:`DateRange`
    
    :param member_count: Number of members in the chat
    :type member_count: :class:`StatisticalValue`
    
    :param message_count: Number of messages sent to the chat
    :type message_count: :class:`StatisticalValue`
    
    :param viewer_count: Number of users who viewed messages in the chat
    :type viewer_count: :class:`StatisticalValue`
    
    :param sender_count: Number of users who sent messages to the chat
    :type sender_count: :class:`StatisticalValue`
    
    :param member_count_graph: A graph containing number of members in the chat
    :type member_count_graph: :class:`StatisticalGraph`
    
    :param join_graph: A graph containing number of members joined and left the chat
    :type join_graph: :class:`StatisticalGraph`
    
    :param join_by_source_graph: A graph containing number of new member joins per source
    :type join_by_source_graph: :class:`StatisticalGraph`
    
    :param language_graph: A graph containing distribution of active users per language
    :type language_graph: :class:`StatisticalGraph`
    
    :param message_content_graph: A graph containing distribution of sent messages by content type
    :type message_content_graph: :class:`StatisticalGraph`
    
    :param action_graph: A graph containing number of different actions in the chat
    :type action_graph: :class:`StatisticalGraph`
    
    :param day_graph: A graph containing distribution of message views per hour
    :type day_graph: :class:`StatisticalGraph`
    
    :param week_graph: A graph containing distribution of message views per day of week
    :type week_graph: :class:`StatisticalGraph`
    
    :param top_senders: List of users sent most messages in the last week
    :type top_senders: :class:`list[ChatStatisticsMessageSenderInfo]`
    
    :param top_administrators: List of most active administrators in the last week
    :type top_administrators: :class:`list[ChatStatisticsAdministratorActionsInfo]`
    
    :param top_inviters: List of most active inviters of new members in the last week
    :type top_inviters: :class:`list[ChatStatisticsInviterInfo]`
    
    """

    ID: str = Field("chatStatisticsSupergroup", alias="@type")
    period: DateRange
    member_count: StatisticalValue
    message_count: StatisticalValue
    viewer_count: StatisticalValue
    sender_count: StatisticalValue
    member_count_graph: StatisticalGraph
    join_graph: StatisticalGraph
    join_by_source_graph: StatisticalGraph
    language_graph: StatisticalGraph
    message_content_graph: StatisticalGraph
    action_graph: StatisticalGraph
    day_graph: StatisticalGraph
    week_graph: StatisticalGraph
    top_senders: list[ChatStatisticsMessageSenderInfo]
    top_administrators: list[ChatStatisticsAdministratorActionsInfo]
    top_inviters: list[ChatStatisticsInviterInfo]

    @staticmethod
    def read(q: dict) -> ChatStatisticsSupergroup:
        return ChatStatisticsSupergroup.construct(**q)
