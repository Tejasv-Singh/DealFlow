from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List

class TaskState(Enum):
    working = "working"
    completed = "completed"
    input_required = "input_required"

@dataclass
class TaskStatus:
    state: TaskState
    message: Optional[Any] = None

@dataclass
class Task:
    id: str
    context_id: str

class RequestContext:
    def __init__(self, task: Task, user_input: str):
        self.current_task = task
        self.user_input = user_input

    def get_user_input(self):
        return self.user_input

class EventQueue:
    async def enqueue_event(self, event):
        print(f"[A2A Event] {event}")

@dataclass
class TaskStatusUpdateEvent:
    status: TaskStatus
    final: bool
    context_id: str
    task_id: str
    append: bool = False

@dataclass
class TaskArtifactUpdateEvent:
    context_id: str
    task_id: str
    last_chunk: bool
    artifact: Any
    append: bool = False

def new_text_artifact(name, description, text):
    return {"name": name, "description": description, "text": text}

def new_agent_text_message(text, context_id, task_id):
    return {"text": text, "context_id": context_id, "task_id": task_id}

@dataclass
class AgentCapabilities:
    streaming: bool
    input_modes: List[str]
    output_modes: List[str]

@dataclass
class AgentSkill:
    id: str
    name: str
    description: str
    tags: List[str]
    examples: List[str]

@dataclass
class AgentCard:
    name: str
    description: str
    url: str
    version: str
    default_input_modes: List[str]
    default_output_modes: List[str]
    capabilities: AgentCapabilities
    skills: List[AgentSkill]
