from langgraph.graph import Node
from app.ai.tools.base_tool import ToolNodeInput

class HITLManager:
    @classmethod
    def create_node(cls) -> Node:
        async def hitl_gate(state: ToolNodeInput) -> dict:
            if state.context.get('confidence', 1.0) < 0.7:
                return {"status": "PAUSED", **state.dict()}
            return {"status": "CONTINUE", **state.dict()}
        
        return Node(
            name="HITL_Gate",
            description="Human approval checkpoint",
            func=hitl_gate
        )