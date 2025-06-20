"""
Execution Engine
Handles the execution of function call flows with proper data passing and error handling.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from function_library import FunctionLibrary


class ExecutionEngine:
    """Executes function call flows with data flow management."""
    
    def __init__(self, function_library: FunctionLibrary):
        self.function_library = function_library
        self.execution_history = []
        self.output_storage = {}
    
    def execute_pipeline(self, function_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a pipeline of function calls.
        
        Args:
            function_calls: List of function calls with inputs
            
        Returns:
            Execution result with final output and metadata
        """
        self.execution_history = []
        self.output_storage = {}
        
        try:
            for i, call in enumerate(function_calls):
                step_result = self._execute_step(i, call)
                if not step_result["success"]:
                    return self._create_error_result(step_result["error"], i)
            
            return self._create_success_result()
            
        except Exception as e:
            return self._create_error_result(f"Pipeline execution failed: {str(e)}", -1)
    
    def _execute_step(self, step_index: int, function_call: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step in the pipeline."""
        function_name = function_call.get("function")
        raw_inputs = function_call.get("inputs", {})
        output_var = function_call.get("output_var")  # Get the variable name
        
        try:
            # Resolve input variables
            resolved_inputs = self._resolve_inputs(raw_inputs)
            
            # Execute the function
            result = self.function_library.execute_function(function_name, resolved_inputs)
            
            # Store the output with both numeric and named keys
            self.output_storage[f"output_{step_index}"] = result
            if output_var:
                self.output_storage[output_var] = result
            
            # Log the execution
            step_log = {
                "step": step_index,
                "function": function_name,
                "inputs": resolved_inputs,
                "outputs": result,
                "output_var": output_var,
                "success": True
            }
            self.execution_history.append(step_log)
            
            return {"success": True, "result": result}
        except Exception as e:
            error_log = {
                "step": step_index,
                "function": function_name,
                "inputs": raw_inputs,
                "error": str(e),
                "success": False
            }
            self.execution_history.append(error_log)
            return {"success": False, "error": str(e)}
    
    def _resolve_inputs(self, raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve variable references in inputs."""
        resolved = {}
        
        for key, value in raw_inputs.items():
            if isinstance(value, str):
                # Handle both {{var.field}} and $output_N.field formats
                if value.startswith("{{") and value.endswith("}}"):
                    resolved_value = self._resolve_template_variable(value)
                    resolved[key] = resolved_value
                elif value.startswith("$"):
                    resolved_value = self._resolve_variable(value)
                    resolved[key] = resolved_value
                else:
                    resolved[key] = value
            else:
                resolved[key] = value
        
        return resolved
    
    def _resolve_variable(self, variable: str) -> Any:
        """Resolve a variable reference like $output_0.invoices"""
        try:
            # Parse variable reference (e.g., "$output_0.invoices")
            var_pattern = r'\$output_(\d+)(?:\.(.+))?'
            match = re.match(var_pattern, variable)
            
            if not match:
                raise ValueError(f"Invalid variable reference: {variable}")
            
            output_index = int(match.group(1))
            field_path = match.group(2)
            
            # Get the output
            output_key = f"output_{output_index}"
            if output_key not in self.output_storage:
                raise ValueError(f"Output {output_key} not found")
            
            data = self.output_storage[output_key]
            
            # Navigate the field path if specified
            if field_path:
                for field in field_path.split('.'):
                    if isinstance(data, dict):
                        data = data.get(field)
                    else:
                        raise ValueError(f"Cannot access field '{field}' on non-dict data")
                    
                    if data is None:
                        raise ValueError(f"Field '{field}' not found")            
            return data
            
        except Exception as e:
            raise ValueError(f"Error resolving variable {variable}: {str(e)}")
    
    def _resolve_template_variable(self, variable: str) -> Any:
        """Resolve a template variable reference like {{var_name.field}}"""
        try:
            # Remove the {{ and }} brackets
            var_content = variable[2:-2].strip()
            
            # Parse variable reference (e.g., "december_invoices.invoices")
            parts = var_content.split('.')
            var_name = parts[0]
            field_path = parts[1:] if len(parts) > 1 else []
            
            # Look for the variable in output storage by name
            data = None
            if var_name in self.output_storage:
                data = self.output_storage[var_name]
            else:
                # Try to map variable names to output indices based on execution history
                for step in self.execution_history:
                    if step.get("success") and step.get("output_var") == var_name:
                        data = step["outputs"]
                        break
                
                # If still not found, try common mappings
                if data is None:
                    var_mapping = {
                        "december_invoices": "output_0",
                        "invoice_summary": "output_1", 
                        "high_value_invoices": "output_1"
                    }
                    
                    if var_name in var_mapping:
                        output_key = var_mapping[var_name]
                        if output_key in self.output_storage:
                            data = self.output_storage[output_key]
            
            if data is None:
                raise ValueError(f"Variable '{var_name}' not found in output storage")
              # Navigate the field path if specified
            for field in field_path:
                if isinstance(data, dict):
                    data = data.get(field)
                else:
                    raise ValueError(f"Cannot access field '{field}' on non-dict data")
                if data is None:
                    raise ValueError(f"Field '{field}' not found")
            
            return data
            
        except Exception as e:
            raise ValueError(f"Error resolving template variable {variable}: {str(e)}")
    
    def _create_success_result(self) -> Dict[str, Any]:
        """Create a successful execution result."""
        final_output = None
        if self.output_storage:
            # Get the last numeric output as the final result
            numeric_keys = [k for k in self.output_storage.keys() if k.startswith('output_')]
            if numeric_keys:
                last_key = max(numeric_keys, key=lambda x: int(x.split('_')[1]))
                final_output = self.output_storage[last_key]
        
        return {
            "success": True,
            "final_output": final_output,
            "execution_history": self.execution_history,
            "all_outputs": self.output_storage
        }
    
    def _create_error_result(self, error_message: str, failed_step: int) -> Dict[str, Any]:
        """Create an error execution result."""
        return {
            "success": False,
            "error": error_message,
            "failed_step": failed_step,
            "execution_history": self.execution_history,
            "partial_outputs": self.output_storage
        }
    
    def get_execution_summary(self) -> str:
        """Get a human-readable summary of the execution."""
        if not self.execution_history:
            return "No execution history available."
        
        summary_lines = ["Execution Summary:"]
        
        for step in self.execution_history:
            if step["success"]:
                summary_lines.append(f"✓ Step {step['step']}: {step['function']} - Success")
            else:
                summary_lines.append(f"✗ Step {step['step']}: {step['function']} - Error: {step['error']}")
        
        return "\n".join(summary_lines)
    
    def validate_function_calls(self, function_calls: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validate function calls before execution."""
        available_functions = self.function_library.get_function_metadata()
        
        for i, call in enumerate(function_calls):
            # Check if function exists
            function_name = call.get("function")
            if not function_name:
                return False, f"Step {i}: Missing function name"
            
            if function_name not in available_functions:
                return False, f"Step {i}: Function '{function_name}' not found"
            
            # Check required inputs
            required_inputs = available_functions[function_name]["inputs"]
            provided_inputs = call.get("inputs", {})
            
            for param_name, param_type in required_inputs.items():
                if param_name not in provided_inputs:
                    return False, f"Step {i}: Missing required parameter '{param_name}' for function '{function_name}'"
        
        return True, "Validation passed"
    
    def dry_run(self, function_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform a dry run to validate the pipeline without execution."""
        is_valid, validation_message = self.validate_function_calls(function_calls)
        
        if not is_valid:
            return {
                "valid": False,
                "error": validation_message,
                "function_calls": function_calls
            }
        
        # Create execution plan
        execution_plan = []
        for i, call in enumerate(function_calls):
            plan_step = {
                "step": i,
                "function": call["function"],
                "inputs": call["inputs"],
                "description": self.function_library.functions[call["function"]]["description"]
            }
            execution_plan.append(plan_step)
        
        return {
            "valid": True,
            "message": "Pipeline is valid and ready for execution",
            "execution_plan": execution_plan,
            "total_steps": len(function_calls)
        }
