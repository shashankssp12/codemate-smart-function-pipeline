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

CORE FUNCTIONS AVAILABLE:
- get_invoices(month) - Get invoices for a month
- summarize_invoices(invoices) - Summarize invoice data
- send_email(content, recipient, subject) - Send email
- validate_email(email) - Check if email is valid
- add_numbers(a, b) - Add two numbers
- get_current_time() - Get current time
- generate_random_number(min_val, max_val) - Random number
- uppercase_string(text) - Convert to uppercase
- check_prime(number) - Check if number is prime
- calculate_total(items, field) - Calculate total of field

COMMON QUERY PATTERNS:
- "is this email valid [email]" → use validate_email function
- "add/sum [numbers]" → use add_numbers function  
- "what time is it" → use get_current_time function
- "convert [text] to uppercase" → use uppercase_string function
- "is [number] prime" → use check_prime function
- "random number between [min] and [max]" → use generate_random_number function
- "get invoices for [month]" → use get_invoices function
- "summarize invoices" → use summarize_invoices function after get_invoices
- "send email" → use send_email function

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
        fallback_calls = []
        
        # Convert to lowercase for case-insensitive matching
        lower_text = response_text.lower()
        
        # Email validation check
        if "valid" in lower_text and "email" in lower_text:
            # Extract email from the query if possible
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, response_text)
            email = emails[0] if emails else "test@example.com"
            fallback_calls.append({"function": "validate_email", "inputs": {"email": email}})
            return fallback_calls
        
        # Mathematical operations
        if any(word in lower_text for word in ["add", "plus", "+", "sum"]):
            fallback_calls.append({"function": "add_numbers", "inputs": {"a": 5, "b": 3}})
            return fallback_calls
        
        if any(word in lower_text for word in ["subtract", "minus", "-"]):
            fallback_calls.append({"function": "subtract_numbers", "inputs": {"a": 10, "b": 3}})
            return fallback_calls
        
        if any(word in lower_text for word in ["multiply", "times", "*"]):
            fallback_calls.append({"function": "multiply_numbers", "inputs": {"a": 4, "b": 5}})
            return fallback_calls
        
        if any(word in lower_text for word in ["divide", "÷", "/"]):
            fallback_calls.append({"function": "divide_numbers", "inputs": {"a": 20, "b": 4}})
            return fallback_calls
        
        # String operations
        if "uppercase" in lower_text or "upper" in lower_text:
            fallback_calls.append({"function": "uppercase_string", "inputs": {"text": "hello world"}})
            return fallback_calls
        
        if "lowercase" in lower_text or "lower" in lower_text:
            fallback_calls.append({"function": "lowercase_string", "inputs": {"text": "HELLO WORLD"}})
            return fallback_calls
        
        if "reverse" in lower_text:
            fallback_calls.append({"function": "reverse_string", "inputs": {"text": "hello"}})
            return fallback_calls
        
        # Web operations
        if "download" in lower_text and "url" in lower_text:
            fallback_calls.append({"function": "download_file", "inputs": {"url": "https://example.com/file.txt", "filename": "downloaded_file.txt"}})
            return fallback_calls
        
        if "summarize" in lower_text and "web" in lower_text:
            fallback_calls.append({"function": "web_summarizer", "inputs": {"url": "https://example.com"}})
            return fallback_calls
        
        # Time operations
        if "current time" in lower_text or "time now" in lower_text:
            fallback_calls.append({"function": "get_current_time", "inputs": {}})
            return fallback_calls
        
        # Random number
        if "random number" in lower_text:
            fallback_calls.append({"function": "generate_random_number", "inputs": {"min_val": 1, "max_val": 100}})
            return fallback_calls
        
        # Prime check
        if "prime" in lower_text:
            fallback_calls.append({"function": "check_prime", "inputs": {"number": 17}})
            return fallback_calls
        
        # Default invoice operations (only if explicitly mentioned)
        if "invoice" in lower_text:
            fallback_calls.append({"function": "get_invoices", "inputs": {"month": "March"}})
            if "summary" in lower_text or "summarize" in lower_text:
                fallback_calls.append({"function": "summarize_invoices", "inputs": {"invoices": "$output_0.invoices"}})
        
        # Send email (only if explicitly sending something)
        if "send email" in lower_text and len(fallback_calls) > 0:
            fallback_calls.append({
                "function": "send_email", 
                "inputs": {
                    "content": f"$output_{len(fallback_calls)-1}",
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
