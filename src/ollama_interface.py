"""
AI Model Interface for Ollama
Handles communication with local Ollama instance running Mistral 7B
"""

import json
import ollama
from typing import Dict, List, Any, Optional
import re


class OllamaInterface:
    """Interface for communicating with Ollama local LLM."""
    
    def __init__(self, model_name: str = "mistral:7b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.client = ollama.Client(host=host)
    
    def parse_user_query(self, user_query: str, available_functions: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Parse user query and return a structured function call flow.
        
        Args:
            user_query: The natural language query from the user
            available_functions: Dictionary of available functions with their metadata
            
        Returns:
            List of function calls with inputs
        """
        
        # Create the prompt for function planning
        prompt = self._create_function_planning_prompt(user_query, available_functions)
        
        try:
            # Call Ollama model
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a function planning AI. Analyze user queries and return a JSON array of function calls."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.1,  # Low temperature for more deterministic output
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            )
            
            # Extract function calls from response
            function_calls = self._extract_function_calls(response['message']['content'])
            return function_calls
            
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return []
    
    def _create_function_planning_prompt(self, user_query: str, available_functions: Dict[str, Dict]) -> str:
        """Create a detailed prompt for function planning."""
        
        # Create function documentation
        function_docs = []
        for func_name, metadata in available_functions.items():
            inputs_str = ", ".join([f"{k}: {v}" for k, v in metadata["inputs"].items()])
            outputs_str = ", ".join([f"{k}: {v}" for k, v in metadata["outputs"].items()])
            
            func_doc = f"""
Function: {func_name}
Description: {metadata["description"]}
Inputs: {inputs_str}
Outputs: {outputs_str}
"""
            function_docs.append(func_doc)
        
        prompt = f"""
You are a function planning AI that converts natural language queries into structured function call sequences.

AVAILABLE FUNCTIONS:
{chr(10).join(function_docs)}

USER QUERY: "{user_query}"

TASK: Analyze the user query and create a sequence of function calls to fulfill the request.

RULES:
1. Return ONLY a valid JSON array of function calls
2. Each function call must have: {{"function": "function_name", "inputs": {{"param": "value"}}}}
3. Use variable references like "$output_0", "$output_1" to chain function outputs
4. The first function's output becomes $output_0, second becomes $output_1, etc.
5. Be specific with parameter values when possible
6. If the user doesn't specify an email, use "user@example.com"

EXAMPLE FORMAT:
[
  {{"function": "get_invoices", "inputs": {{"month": "March"}}}},
  {{"function": "summarize_invoices", "inputs": {{"invoices": "$output_0.invoices"}}}},
  {{"function": "send_email", "inputs": {{"content": "$output_1.summary", "recipient": "user@example.com", "subject": "Invoice Summary"}}}}
]

RESPONSE (JSON only):
"""
        return prompt
    
    def _extract_function_calls(self, response_text: str) -> List[Dict[str, Any]]:
        """Extract function calls from the model response."""
        try:
            # Look for JSON array in the response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                function_calls = json.loads(json_str)
                
                # Validate the structure
                if isinstance(function_calls, list):
                    validated_calls = []
                    for call in function_calls:
                        if isinstance(call, dict) and "function" in call and "inputs" in call:
                            validated_calls.append(call)
                    return validated_calls
                    
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
        
        # Fallback: try to extract function names and create basic calls
        return self._fallback_extraction(response_text)
    
    def _fallback_extraction(self, response_text: str) -> List[Dict[str, Any]]:
        """Fallback method to extract function calls if JSON parsing fails."""
        # This is a simple fallback - in production you might want more sophisticated parsing
        fallback_calls = []
        
        # Look for common patterns
        if "invoice" in response_text.lower():
            fallback_calls.append({"function": "get_invoices", "inputs": {"month": "March"}})
        
        if "summar" in response_text.lower():
            fallback_calls.append({"function": "summarize_invoices", "inputs": {"invoices": "$output_0.invoices"}})
        
        if "email" in response_text.lower() or "send" in response_text.lower():
            fallback_calls.append({
                "function": "send_email", 
                "inputs": {
                    "content": "$output_1.summary" if len(fallback_calls) > 0 else "No content available",
                    "recipient": "user@example.com",
                    "subject": "Automated Report"
                }
            })
        
        return fallback_calls
    
    def test_connection(self) -> bool:
        """Test if Ollama is accessible and the model is available."""
        try:
            # Try to list models
            models = self.client.list()
            model_names = [model['name'] for model in models['models']]
            return self.model_name in model_names
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def generate_summary(self, data: Any, context: str = "") -> str:
        """Generate a natural language summary of data."""
        prompt = f"""
Generate a clear, concise summary of the following data:

Context: {context}
Data: {json.dumps(data, indent=2)}

Provide a human-readable summary in 2-3 sentences.
"""
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data analyst that creates clear, concise summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.3,
                    "max_tokens": 200
                }
            )
            return response['message']['content']
        except Exception as e:
            return f"Summary generation failed: {e}"
