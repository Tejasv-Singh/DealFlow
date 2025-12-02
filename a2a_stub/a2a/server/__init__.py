class AgentExecutor:
    async def execute(self, context, event_queue) -> None:
        raise NotImplementedError

    async def cancel(self, context, event_queue) -> None:
        pass

class A2AServer:
    def __init__(self, agent_executor, port, host):
        self.agent_executor = agent_executor
        self.port = port
        self.host = host

    async def start(self):
        print(f"Mock A2A Server started on {self.host}:{self.port}")
        # Keep running
        import asyncio
        while True:
            await asyncio.sleep(3600)
