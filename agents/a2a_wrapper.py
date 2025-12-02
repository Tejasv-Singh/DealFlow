import asyncio
from typing import AsyncIterable
from a2a.server.agent_execution import AgentExecutor
from a2a.types import (
    RequestContext, 
    EventQueue, 
    TaskStatusUpdateEvent, 
    TaskStatus, 
    TaskState, 
    TaskArtifactUpdateEvent, 
    new_text_artifact, 
    new_agent_text_message
)
from dealflow.agents.campaign_manager import CampaignManager

class DealFlowAgent:
    """
    Internal agent class that supports streaming.
    """
    def __init__(self):
        self.manager = CampaignManager()

    async def stream(self, query: str) -> AsyncIterable[dict]:
        """Stream responses from your agent."""
        
        # 1. Report start
        yield {
            'is_task_complete': False,
            'require_user_input': False,
            'content': f"Starting DealFlow cycle for query: {query}"
        }

        # 2. Run the actual logic (blocking, so run in executor)
        loop = asyncio.get_event_loop()
        # We capture stdout or logs in a real system, here we just wait for it to finish
        await loop.run_in_executor(None, self.manager.run_cycle)

        # 3. Report completion
        yield {
            'is_task_complete': True,
            'require_user_input': False,
            'content': 'DealFlow cycle completed successfully. Check the dashboard for updates.'
        }

class DealFlowAgentExecutor(AgentExecutor):
    """
    A2A Wrapper for the DealFlow Campaign Manager.
    """
    def __init__(self):
        self.agent = DealFlowAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        task = context.current_task

        async for event in self.agent.stream(query):
            if event['is_task_complete']:
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        append=False,
                        context_id=task.context_id,
                        task_id=task.id,
                        last_chunk=True,
                        artifact=new_text_artifact(
                            name='current_result',
                            description='Agent response result.',
                            text=event['content'],
                        ),
                    )
                )
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(state=TaskState.completed),
                        final=True,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )
            elif event['require_user_input']:
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.input_required,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id,
                            ),
                        ),
                        final=True,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )
            else:
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        append=True,
                        status=TaskStatus(
                            state=TaskState.working,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id,
                            ),
                        ),
                        final=False,
                        context_id=task.context_id,
                        task_id=task.id,
                    )
                )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass
