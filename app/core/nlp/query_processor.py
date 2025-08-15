# Natural language query processor
from typing import Dict, Any, Optional, List, Tuple
import logging
from datetime import datetime
from app.models.task import Task, TaskStatus, TaskState
from app.db.repositories.task_repository import TaskRepository
from app.core.marc1.execution_engine import ExecutionEngine
from app.core.nlp.intent_parser import IntentParser
from app.core.marc1.protocol import Marc1Intent
from app.core.marc1.tool_registry import get_tool_registry

logger = logging.getLogger(__name__)

class NLPQueryProcessor:
    """
    Processes natural language queries and converts them to executable tasks
    
    This class handles the initial processing of natural language queries,
    extracting intent, parameters, and determining the appropriate tools
    to execute the request.
    """
    
    def __init__(self, db_session, execution_engine: Optional[ExecutionEngine] = None):
        self.db_session = db_session
        self.task_repo = TaskRepository(db_session)
        self.execution_engine = execution_engine or ExecutionEngine()
        self.intent_parser = IntentParser()
        self.tool_registry = get_tool_registry()
        
    async def process_query(self, task_id: str) -> Task:
        """
        Process a natural language query task
        
        Args:
            task_id: The ID of the task to process
            
        Returns:
            The updated task with processed parameters
        """
        # Get the task from the database
        task = await self.task_repo.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return None
            
        try:
            # Update task status to processing
            task.current_state = TaskState(
                task_id=task.id,
                status=TaskStatus.RUNNING,
                updated_at=datetime.now().isoformat()
            )
            await self.task_repo.update_task(task)
            
            # Extract intent and parameters from the query using the intent parser
            intent, suggested_tools = self.intent_parser.parse_query(task.query)
            
            # Update task with extracted parameters
            task.parameters = intent.parameters
            task.context["intent"] = intent.intent_name
            task.context["confidence"] = intent.confidence
            
            # Store the full intent object for reference
            task.context["marc1_intent"] = intent.dict()
            
            # Determine appropriate tools based on intent
            task.tools = self._prepare_tools_for_intent(intent)
            
            # Validate tool parameters
            validation_errors = self._validate_tool_parameters(task.tools, task.parameters)
            if validation_errors:
                print (f"Validation errors: {validation_errors}")
                #Add diagnostic information
                diagnostic_message = Validator.diagnose_tool_validation_error(validation_errors)
                logger.error(f"Tool validation error: {diagnostic_message}")
                task.current_state.error = diagnostic_message
                task.context["validation_errors"] = validation_errors
                task.current_state.status = TaskStatus.PAUSED
                task.current_state.requires_approval = True
                task.current_state.metadata["pause_reason"] = "Parameter validation failed"
                task.current_state.metadata["validation_errors"] = validation_errors
                logger.info(f"Task {task_id} paused due to parameter validation errors")
            else:
                # Update task status based on confidence
                if intent.confidence < 0.9:
                    # Low confidence - require human approval
                    task.current_state.status = TaskStatus.PAUSED
                    task.current_state.requires_approval = True
                    task.current_state.metadata["pause_reason"] = "Low confidence in intent detection"
                    task.current_state.metadata["confidence"] = intent.confidence
                    logger.info(f"Task {task_id} paused for human approval due to low confidence: {intent.confidence}")
                else:
                    # Good confidence - queue for execution
                    task.current_state.status = TaskStatus.QUEUED
                    logger.info(f"Task {task_id} queued for execution with intent: {intent.intent_name}")
            
            # Save the updated task
            await self.task_repo.update_task(task)
            
            # If confidence is high enough and no validation errors, start execution
            if intent.confidence >= 0.9 and not validation_errors:
                # This would typically be done by a background worker
                # For now, we'll just log that it would happen
                logger.info(f"Task {task_id} would now be executed by background worker")
                print(f"Task {task_id} would now be executed by background worker")
                # In a real implementation, you would start the execution here
                await self.start_execution(task)
            
            return task
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            # Update task status to failed
            if task and task.current_state:
                task.current_state.status = TaskStatus.FAILED
                task.current_state.error = str(e)
                await self.task_repo.update_task(task)
            return task
    
    def _prepare_tools_for_intent(self, intent: Marc1Intent) -> List[Dict[str, Any]]:
        """
        Prepare tool configurations based on the extracted intent
        
        Args:
            intent: The extracted intent
            
        Returns:
            A list of tool configurations
        """
        # Get suggested tools from the tool registry
        suggested_tools = self.tool_registry.get_tools_for_intent(intent.intent_name)
        
        # If no tools found, try to dynamically determine tools
        if not suggested_tools:
            logger.info(f"No predefined tools for intent {intent.intent_name}, using dynamic tool selection")
            suggested_tools = self._dynamically_select_tools(intent)
            
                # Fill in parameters from intent
        for tool in suggested_tools:
            for param_name, param_value in tool.get("parameters", {}).items():
                # Check if this is a template parameter (${param})
                if isinstance(param_value, str) and param_value.startswith("${") and param_value.endswith("}"):
                    # Extract parameter name from template
                    intent_param_name = param_value[2:-1]
                    if intent_param_name in intent.parameters:
                        # Replace with actual value from intent
                        tool["parameters"][param_name] = intent.parameters[intent_param_name]
        
        return suggested_tools
    
    def _validate_tool_parameters(self, tools: List[Dict[str, Any]], parameters: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate parameters for all tools in a workflow
        
        Args:
            tools: List of tool configurations
            parameters: Parameters extracted from the query
            
        Returns:
            Dictionary of validation errors, or empty dict if valid
        """
        all_errors = {}
        
        for tool in tools:
            tool_name = tool.get("name")
            if not tool_name:
                continue
                
            # Get parameters for this tool
            tool_params = tool.get("parameters", {})
            
            # Validate using the tool registry
            errors = self.tool_registry.validate_tool_parameters(tool_name, tool_params)
            if errors:
                all_errors[tool_name] = errors
                
        return all_errors
    
    def _dynamically_select_tools(self, intent: Marc1Intent) -> List[Dict[str, Any]]:
        """
        Dynamically select tools based on intent when no predefined workflow exists
        
        Args:
            intent: The extracted intent
            
        Returns:
            A list of tool configurations
        """
        # In Phase 1, this is a simple fallback mechanism
        # In Phase 2, this will use LLM to dynamically determine tools
        
        # Basic mapping of common verbs to tools
        verb_to_tool = {
            "login": [{"name": "cargowise_login", "parameters": {}}],
            "search": [{"name": "cargowise_search_booking", "parameters": {}}],
            "find": [{"name": "cargowise_search_booking", "parameters": {}}],
           
            "create": [{"name": "cargowise_create_order", "parameters": {}}],
            "track": [{"name": "cargowise_track_shipment", "parameters": {}}],
            "update": [{"name": "cargowise_update_booking", "parameters": {}}],
            "modify": [{"name": "cargowise_update_booking", "parameters": {}}],
            "generate": [{"name": "cargowise_generate_report", "parameters": {}}],
            "report": [{"name": "cargowise_generate_report", "parameters": {}}]
        }
        
        # Extract verb from intent name
        intent_parts = intent.intent_name.split('_')
        if not intent_parts:
            return []
            
        verb = intent_parts[0].lower()
        
        # Get tools for this verb
        tools = verb_to_tool.get(verb, [])
        
        # Fill in parameters from intent
        for tool in tools:
            for param_name, param_value in intent.parameters.items():
                if param_name not in tool["parameters"]:
                    tool["parameters"][param_name] = param_value
        
        # If we need to login first, add login tool
        if tools and tools[0]["name"] != "cargowise_login":
            login_tool = {
                "name": "cargowise_login",
                "parameters": {
                    "username": intent.parameters.get("username", "${username}"),
                    "password": intent.parameters.get("password", "${password}"),
                    "environment": intent.parameters.get("environment", "desktop")
                }
            }
            tools.insert(0, login_tool)
            
        return tools
    
    async def start_execution(self, task: Task) -> None:
        """
        Start execution of a processed task
        
        Args:
            task: The task to execute
        """
        logger.info(f"Starting execution of task {task.id}")
        print(f"Starting execution of task {task.id} with tools: {[tool['name'] for tool in task.tools]}")
        # Update task status
        task.current_state.status = TaskStatus.RUNNING
        await self.task_repo.update_task(task)
        
        try:
            # Execute the task using the execution engine
            async for state in self.execution_engine.execute_task(task):
                # Update task state
                
                print(f"Task state updated: {state.status}")
                task.current_state = state
                await self.task_repo.update_task(task)
                
                # If execution paused or completed, break
                if state.status in [TaskStatus.PAUSED, TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    break
            # After execution completes, ensure completed_at is set if status is COMPLETED
            if task.current_state.status == TaskStatus.COMPLETED and not task.completed_at:
                task.completed_at = datetime.utcnow()
                await self.task_repo.update_task(task)
                    
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {str(e)}")
            print(f"Error executing task {task.id}: {str(e)}")
            # Update task status to failed
            task.current_state.status = TaskStatus.FAILED
            task.current_state.error = str(e)
            await self.task_repo.update_task(task)