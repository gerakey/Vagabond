import enum

class APObjectType(enum.Enum):
    NOTE = 'Note'
    PERSON = 'Person'
    OBJECT = 'Object'
    CREATE = 'Create'
    DELETE = 'Delete'
    FOLLOW = 'Follow'
    ACTIVITY = 'Activity'