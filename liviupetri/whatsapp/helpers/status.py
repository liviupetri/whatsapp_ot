from enum import Enum


class Status(Enum):
    INITIAL_STATUS = 'initial status'
    SETUP = 'click'
    ONLINE = 'online'
    OFFLINE = 'offline'
    TYPING = 'typing'
    RECORDING = 'recording'
    NOT_DEFINED = 'not defined'
    LAST_SEEN = 'last seen'
    USER_CHANGED = 'User has changed! Not tracking!'

