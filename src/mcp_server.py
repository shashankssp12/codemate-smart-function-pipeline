"""
MCP Server - Model Context Protocol Server
Main orchestrator that integrates AI model with function execution pipeline.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, render_template, send_from_directory
from function_library import FunctionLibrary
from ollama_interface import OllamaInterface
from execution_engine import ExecutionEngine


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPServer:
    """Main MCP Server class that orchestrates the entire pipeline."""
    
    def __init__(self, model_name: str = "mistral:7b", ollama_host: str = "http://localhost:11434"):
        self.function_library = FunctionLibrary()
        self.ollama_interface = OllamaInterface(model_name, ollama_host)
        self.execution_engine = ExecutionEngine(self.function_library)
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self._setup_routes()
        
        # Test Ollama connection on startup
        if self.ollama_interface.test_connection():
            logger.info(f"Successfully connected to Ollama with model: {model_name}")
        else:
            logger.warning(f"Could not connect to Ollama. Model: {model_name}, Host: {ollama_host}")
    
    def _setup_routes(self):
        """Setup Flask routes for the MCP server."""
        
        @self.app.route('/', methods=['GET'])
        def index():
            """Serve the main chat interface."""
            return render_template('index.html')
        
        @self.app.route('/static/<path:filename>')
        def static_files(filename):
            """Serve static files."""
            return send_from_directory('../static', filename)
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            ollama_status = self.ollama_interface.test_connection()
            return jsonify({
                "status": "healthy" if ollama_status else "degraded",
                "ollama_connected": ollama_status,
                "functions_available": len(self.function_library.functions),
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/functions', methods=['GET'])
        def list_functions():
            """List all available functions."""
            return jsonify({
                "functions": self.function_library.get_function_metadata(),
                "count": len(self.function_library.functions)
            })
        
        @self.app.route('/execute', methods=['POST'])
        def execute_query():
            """Main endpoint to execute user queries."""
            try:
                data = request.get_json()
                if not data or 'query' not in data:
                    return jsonify({"error": "Missing 'query' in request body"}), 400
                
                result = self.process_user_query(data['query'])
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                return jsonify({"error": f"Internal server error: {str(e)}"}), 500
        
        @self.app.route('/plan', methods=['POST'])
        def plan_query():
            """Endpoint to get execution plan without running it."""
            try:
                data = request.get_json()
                if not data or 'query' not in data:
                    return jsonify({"error": "Missing 'query' in request body"}), 400
                
                result = self.plan_user_query(data['query'])
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Error planning query: {str(e)}")
                return jsonify({"error": f"Internal server error: {str(e)}"}), 500
        
        @self.app.route('/execute-plan', methods=['POST'])
        def execute_plan():
            """Execute a predefined function call plan."""
            try:
                data = request.get_json()
                if not data or 'function_calls' not in data:
                    return jsonify({"error": "Missing 'function_calls' in request body"}), 400
                
                result = self.execute_function_calls(data['function_calls'])
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Error executing plan: {str(e)}")
                return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    def process_user_query(self, user_query: str) -> Dict[str, Any]:
        """
        Complete pipeline: parse query, plan execution, and execute.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Complete execution result
        """
        logger.info(f"Processing user query: {user_query}")
        
        # Step 1: Parse the query using AI model
        available_functions = self.function_library.get_function_metadata()
        function_calls = self.ollama_interface.parse_user_query(user_query, available_functions)
        
        if not function_calls:
            return {
                "success": False,
                "error": "Could not parse user query into function calls",
                "user_query": user_query,
                "timestamp": datetime.now().isoformat()
            }
        
        logger.info(f"Generated function calls: {function_calls}")
        
        # Step 2: Validate the plan
        try:
            is_valid, validation_message = self.execution_engine.validate_function_calls(function_calls)
            if not is_valid:
                return {
                    "success": False,
                    "error": f"Invalid execution plan: {validation_message}",
                    "function_calls": function_calls,
                    "user_query": user_query,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Validation error: {str(e)}",
                "function_calls": function_calls,
                "user_query": user_query,
                "timestamp": datetime.now().isoformat()
            }
        
        # Step 3: Execute the plan
        try:
            execution_result = self.execution_engine.execute_pipeline(function_calls)
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "function_calls": function_calls,
                "user_query": user_query,
                "timestamp": datetime.now().isoformat()
            }
        
        # Step 4: Generate summary
        try:
            summary = self._generate_result_summary(execution_result, user_query)
        except Exception as e:
            summary = f"Summary generation failed: {str(e)}"
        
        return {
            "success": execution_result.get("success", False),
            "user_query": user_query,
            "function_calls": function_calls,
            "execution_result": execution_result,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    
    def plan_user_query(self, user_query: str) -> Dict[str, Any]:
        """
        Plan execution without running it.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Execution plan and validation result
        """
        logger.info(f"Planning user query: {user_query}")
        
        # Parse the query using AI model
        available_functions = self.function_library.get_function_metadata()
        function_calls = self.ollama_interface.parse_user_query(user_query, available_functions)
        
        if not function_calls:
            return {
                "success": False,
                "error": "Could not parse user query into function calls",
                "user_query": user_query
            }
        
        # Perform dry run
        dry_run_result = self.execution_engine.dry_run(function_calls)
        
        return {
            "user_query": user_query,
            "function_calls": function_calls,
            "dry_run_result": dry_run_result,
            "timestamp": datetime.now().isoformat()
        }
    
    def execute_function_calls(self, function_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a predefined list of function calls.
        
        Args:
            function_calls: List of function calls to execute
            
        Returns:
            Execution result
        """
        logger.info(f"Executing function calls: {function_calls}")
        
        execution_result = self.execution_engine.execute_pipeline(function_calls)
        summary = self._generate_result_summary(execution_result)
        
        return {
            "success": execution_result["success"],            "function_calls": function_calls,
            "execution_result": execution_result,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_result_summary(self, execution_result: Dict[str, Any], 
                                user_query: str = None) -> str:
        """Generate a human-readable summary of the execution result."""
        if not execution_result.get("success", False):
            return f"Execution failed: {execution_result.get('error', 'Unknown error')}"
        
        # Get the final output
        final_output = execution_result.get("final_output", {})
        
        # Create a simple summary without AI if Ollama is unavailable
        if user_query and "email" in user_query.lower() and "valid" in user_query.lower():
            # Email validation summary
            is_valid = final_output.get("is_valid", False)
            return f"Email validation result: {'Valid' if is_valid else 'Invalid'}"
        
        # Try to use AI for summary generation
        try:
            context = f"User query: {user_query}" if user_query else "Direct function execution"
            ai_summary = self.ollama_interface.generate_summary(final_output, context)
            return ai_summary
        except Exception as e:
            # Fallback to basic summary
            steps_completed = len(execution_result.get("execution_history", []))
            if final_output:
                key_results = []
                for key, value in final_output.items():
                    key_results.append(f"{key}: {value}")
                result_summary = ", ".join(key_results)
                return f"Successfully completed {steps_completed} steps. Results: {result_summary}"
            else:
                return f"Successfully completed {steps_completed} steps."
    
    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """Run the Flask server."""
        logger.info(f"Starting MCP Server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_app() -> Flask:
    """Factory function to create Flask app."""
    mcp_server = MCPServer()
    return mcp_server.app


if __name__ == "__main__":
    # Create and run the MCP server
    server = MCPServer()
    server.run(debug=True)
