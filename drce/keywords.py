from enum import Enum


class Argument(Enum):
    ACTION = 'action'
    WHERE = 'where'
    TYPE = 'type'
    TARGET = 'target'
    TO = 'to'


class ActionType(Enum):
    USER = 'user'
    ROLE = 'role'
    CHANNEL = 'channel'
    CATEGORY = 'category'
    WRAPPED = 'wrapped'


class Action(Enum):
    BAN = 'ban'
    KICK = 'kick'
    UNBAN = 'unban'
    DELETE = 'delete'
    RESET = 'reset'
    EDIT = 'edit'
    ADD = 'add'
    USE = 'use'
    GIVE = 'give'
    DEFCON = 'defcon'
    RED_BUTTON = 'red_button'
    SILENT_GUILD = 'silent_guild'
    SPAM = 'spam'
