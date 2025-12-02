import uvicorn
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add parent of project root to path (to allow 'import dealflow')
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Add A2A stub to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "a2a_stub"))

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from dealflow.agents.a2a_wrapper import DealFlowAgentExecutor

def main():
    # 1. Configure Agent Card
    skill = AgentSkill(
        id='sponsorship_outreach',
        name='Sponsorship Outreach',
        description='Autonomously researches and contacts potential sponsors.',
        tags=['sales', 'marketing', 'autonomous'],
        examples=['Find sponsors for my hackathon', 'Contact Stripe for sponsorship'],
    )

    agent_card = AgentCard(
        name='DealFlow Agent',
        description='Autonomous Sponsorship Swarm',
        url='http://localhost:8000/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,
            input_modes=['text'],
            output_modes=['text'],
        ),
        skills=[skill],
    )

    # 2. Create task store and request handler
    task_store = InMemoryTaskStore()
    request_handler = DefaultRequestHandler(
        agent_executor=DealFlowAgentExecutor(),
        task_store=task_store,
    )

    # 3. Create A2A application
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    print("Starting DealFlow A2A Server on port 8000...")
    
    # 4. Start server
    uvicorn.run(
        server.build(), 
        host='0.0.0.0', 
        port=8000
    )

if __name__ == '__main__':
    main()
