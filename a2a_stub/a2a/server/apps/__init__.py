class A2AStarletteApplication:
    def __init__(self, agent_card, http_handler):
        self.agent_card = agent_card
        self.http_handler = http_handler

    def build(self):
        # Return a dummy ASGI app
        async def app(scope, receive, send):
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', b'text/plain'],
                ],
            })
            await send({
                'type': 'http.response.body',
                'body': b'Mock A2A Server Running',
            })
        return app
