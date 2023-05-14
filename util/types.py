
from dataclasses import dataclass
from enum import Enum

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class Message:
    role: Role
    content: str
    
    def toMap(self):
        return {
            "role": self.role.value,
            "content": self.content
        }

Messages = list[Message]

def messagesToMap(messages: Messages):
    return [message.toMap() for message in messages]


@dataclass
class DatabaseEntry:
    id: str
    question: str
    answer: str
    