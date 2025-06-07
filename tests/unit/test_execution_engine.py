import pytest
from app.core.marc1.execution_engine import ExecutionEngine
from app.models.task import Task

@pytest.mark.asyncio
async def test_linear_workflow_execution():
    # Setup
    sample_task = Task(
        id="test-001",
        tools=["ClickButtonTool", "TypeTextTool"],  # Mock registry
        parameters={"text": "Hello World"}
    )
    
    engine = ExecutionEngine(task_registry={})
    
    # Execute
    states = []
    async for state in engine.execute_task(sample_task):
        states.append(state)
    
    # Validate
    assert len(states) > 0
    final_state = states[-1]
    assert final_state.status == "COMPLETED"