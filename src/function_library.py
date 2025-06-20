"""
Function Library Module
Contains all the predefined functions that can be called by the MCP server.
"""

import json
import smtplib
import math
import os
import re
import hashlib
import base64
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional
import random
import requests


class FunctionLibrary:
    """Registry of all available functions with their metadata."""
    
    def __init__(self):
        self.functions = {}
        self._register_functions()
    
    def _register_functions(self):
        """Register all available functions with their metadata."""
        
        # Invoice Functions
        self.register_function(
            name="get_invoices",
            func=self.get_invoices,
            description="Retrieve invoices for a specific month",
            inputs={"month": "str"},
            outputs={"invoices": "List[Dict]"}
        )
        
        self.register_function(
            name="filter_invoices_by_amount",
            func=self.filter_invoices_by_amount,
            description="Filter invoices by minimum amount",
            inputs={"invoices": "List[Dict]", "min_amount": "float"},
            outputs={"filtered_invoices": "List[Dict]"}
        )
        
        self.register_function(
            name="summarize_invoices",
            func=self.summarize_invoices,
            description="Create a summary of invoice data",
            inputs={"invoices": "List[Dict]"},
            outputs={"summary": "Dict"}
        )
        
        # Email Functions
        self.register_function(
            name="send_email",
            func=self.send_email,
            description="Send an email with given content",
            inputs={"content": "str", "recipient": "str", "subject": "str"},
            outputs={"status": "str"}
        )
        
        # Data Processing Functions
        self.register_function(
            name="calculate_total",
            func=self.calculate_total,
            description="Calculate total amount from a list of items",
            inputs={"items": "List[Dict]", "field": "str"},
            outputs={"total": "float"}
        )
        
        self.register_function(
            name="group_by_field",
            func=self.group_by_field,
            description="Group data by a specific field",
            inputs={"data": "List[Dict]", "field": "str"},
            outputs={"grouped_data": "Dict"}
        )
        
        # Date Functions
        self.register_function(
            name="filter_by_date_range",
            func=self.filter_by_date_range,
            description="Filter data by date range",
            inputs={"data": "List[Dict]", "date_field": "str", "start_date": "str", "end_date": "str"},
            outputs={"filtered_data": "List[Dict]"}
        )
        
        # File Functions
        self.register_function(
            name="save_to_file",
            func=self.save_to_file,
            description="Save data to a JSON file",
            inputs={"data": "Any", "filename": "str"},
            outputs={"filepath": "str"}
        )
        
        self.register_function(
            name="read_from_file",
            func=self.read_from_file,
            description="Read data from a JSON file",
            inputs={"filename": "str"},
            outputs={"data": "Any"}
        )
          # Conversion Functions
        self.register_function(
            name="convert_currency",
            func=self.convert_currency,
            description="Convert amount between currencies",
            inputs={"amount": "float", "from_currency": "str", "to_currency": "str"},
            outputs={"converted_amount": "float"}
        )
        
        # Mathematical Functions
        self.register_function(
            name="add_numbers",
            func=self.add_numbers,
            description="Add two numbers",
            inputs={"a": "float", "b": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="subtract_numbers",
            func=self.subtract_numbers,
            description="Subtract two numbers",
            inputs={"a": "float", "b": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="multiply_numbers",
            func=self.multiply_numbers,
            description="Multiply two numbers",
            inputs={"a": "float", "b": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="divide_numbers",
            func=self.divide_numbers,
            description="Divide two numbers",
            inputs={"a": "float", "b": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="power",
            func=self.power,
            description="Calculate a number raised to a power",
            inputs={"base": "float", "exponent": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="square_root",
            func=self.square_root,
            description="Calculate square root of a number",
            inputs={"number": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="factorial",
            func=self.factorial,
            description="Calculate factorial of a number",
            inputs={"number": "int"},
            outputs={"result": "int"}
        )
        
        self.register_function(
            name="logarithm",
            func=self.logarithm,
            description="Calculate natural logarithm of a number",
            inputs={"number": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="sine",
            func=self.sine,
            description="Calculate sine of an angle in radians",
            inputs={"angle": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="cosine",
            func=self.cosine,
            description="Calculate cosine of an angle in radians",
            inputs={"angle": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="tangent",
            func=self.tangent,
            description="Calculate tangent of an angle in radians",
            inputs={"angle": "float"},
            outputs={"result": "float"}
        )
        
        self.register_function(
            name="absolute_value",
            func=self.absolute_value,
            description="Get absolute value of a number",
            inputs={"number": "float"},
            outputs={"result": "float"}
        )
        
        # String Functions
        self.register_function(
            name="uppercase_string",
            func=self.uppercase_string,
            description="Convert string to uppercase",
            inputs={"text": "str"},
            outputs={"result": "str"}
        )
        
        self.register_function(
            name="lowercase_string",
            func=self.lowercase_string,
            description="Convert string to lowercase",
            inputs={"text": "str"},
            outputs={"result": "str"}
        )
        
        self.register_function(
            name="reverse_string",
            func=self.reverse_string,
            description="Reverse a string",
            inputs={"text": "str"},
            outputs={"result": "str"}
        )
        
        self.register_function(
            name="count_words",
            func=self.count_words,
            description="Count words in a string",
            inputs={"text": "str"},
            outputs={"count": "int"}
        )
        
        self.register_function(
            name="remove_spaces",
            func=self.remove_spaces,
            description="Remove all spaces from a string",
            inputs={"text": "str"},
            outputs={"result": "str"}
        )
        
        self.register_function(
            name="replace_text",
            func=self.replace_text,
            description="Replace text in a string",
            inputs={"text": "str", "old": "str", "new": "str"},
            outputs={"result": "str"}
        )
        
        # List Functions
        self.register_function(
            name="sort_list",
            func=self.sort_list,
            description="Sort a list of numbers",
            inputs={"numbers": "List[float]"},
            outputs={"sorted_list": "List[float]"}
        )
        
        self.register_function(
            name="find_max",
            func=self.find_max,
            description="Find maximum value in a list",
            inputs={"numbers": "List[float]"},
            outputs={"max_value": "float"}
        )
        
        self.register_function(
            name="find_min",
            func=self.find_min,
            description="Find minimum value in a list",
            inputs={"numbers": "List[float]"},
            outputs={"min_value": "float"}
        )
        
        self.register_function(
            name="calculate_average",
            func=self.calculate_average,
            description="Calculate average of a list of numbers",
            inputs={"numbers": "List[float]"},
            outputs={"average": "float"}
        )
        
        self.register_function(
            name="calculate_median",
            func=self.calculate_median,
            description="Calculate median of a list of numbers",
            inputs={"numbers": "List[float]"},
            outputs={"median": "float"}
        )
        
        self.register_function(
            name="sum_list",
            func=self.sum_list,
            description="Calculate sum of a list of numbers",
            inputs={"numbers": "List[float]"},
            outputs={"sum": "float"}
        )
        
        # Web Functions
        self.register_function(
            name="web_summarizer",
            func=self.web_summarizer,
            description="Fetch and summarize content from a web URL",
            inputs={"url": "str"},
            outputs={"summary": "str", "content": "str"}
        )
        
        self.register_function(
            name="download_file",
            func=self.download_file,
            description="Download a file from a URL",
            inputs={"url": "str", "filename": "str"},
            outputs={"status": "str", "filepath": "str"}
        )
        
        self.register_function(
            name="check_url_status",
            func=self.check_url_status,
            description="Check if a URL is accessible",
            inputs={"url": "str"},
            outputs={"status_code": "int", "is_accessible": "bool"}
        )
        
        # Date and Time Functions
        self.register_function(
            name="get_current_time",
            func=self.get_current_time,
            description="Get current date and time",
            inputs={},
            outputs={"current_time": "str"}
        )
        
        self.register_function(
            name="add_days",
            func=self.add_days,
            description="Add days to a date",
            inputs={"date": "str", "days": "int"},
            outputs={"new_date": "str"}
        )
        
        self.register_function(
            name="date_difference",
            func=self.date_difference,
            description="Calculate difference between two dates in days",
            inputs={"date1": "str", "date2": "str"},
            outputs={"difference_days": "int"}
        )
        
        self.register_function(
            name="format_date",
            func=self.format_date,
            description="Format a date string",
            inputs={"date": "str", "format": "str"},
            outputs={"formatted_date": "str"}
        )
        
        # Utility Functions
        self.register_function(
            name="generate_random_number",
            func=self.generate_random_number,
            description="Generate a random number between min and max",
            inputs={"min_val": "float", "max_val": "float"},
            outputs={"random_number": "float"}
        )
        
        self.register_function(
            name="generate_uuid",
            func=self.generate_uuid,
            description="Generate a UUID string",
            inputs={},
            outputs={"uuid": "str"}
        )
        
        self.register_function(
            name="hash_string",
            func=self.hash_string,
            description="Generate SHA256 hash of a string",
            inputs={"text": "str"},
            outputs={"hash": "str"}
        )
        
        self.register_function(
            name="encode_base64",
            func=self.encode_base64,
            description="Encode string to base64",
            inputs={"text": "str"},
            outputs={"encoded": "str"}
        )
        
        self.register_function(
            name="decode_base64",
            func=self.decode_base64,
            description="Decode base64 string",
            inputs={"encoded": "str"},
            outputs={"decoded": "str"}
        )
        
        self.register_function(
            name="validate_email",
            func=self.validate_email,
            description="Validate email address format",
            inputs={"email": "str"},
            outputs={"is_valid": "bool"}
        )
        
        self.register_function(
            name="extract_domain",
            func=self.extract_domain,
            description="Extract domain from URL",
            inputs={"url": "str"},
            outputs={"domain": "str"}
        )
        
        self.register_function(
            name="count_characters",
            func=self.count_characters,
            description="Count characters in a string",
            inputs={"text": "str"},
            outputs={"count": "int"}
        )
        
        self.register_function(
            name="celsius_to_fahrenheit",
            func=self.celsius_to_fahrenheit,
            description="Convert temperature from Celsius to Fahrenheit",
            inputs={"celsius": "float"},
            outputs={"fahrenheit": "float"}
        )
        
        self.register_function(
            name="fahrenheit_to_celsius",
            func=self.fahrenheit_to_celsius,
            description="Convert temperature from Fahrenheit to Celsius",
            inputs={"fahrenheit": "float"},
            outputs={"celsius": "float"}
        )
        
        self.register_function(
            name="calculate_percentage",
            func=self.calculate_percentage,
            description="Calculate percentage of a value",
            inputs={"value": "float", "total": "float"},
            outputs={"percentage": "float"}
        )
        
        self.register_function(
            name="round_number",
            func=self.round_number,
            description="Round a number to specified decimal places",
            inputs={"number": "float", "decimals": "int"},
            outputs={"rounded": "float"}
        )
        
        self.register_function(
            name="check_prime",
            func=self.check_prime,
            description="Check if a number is prime",
            inputs={"number": "int"},
            outputs={"is_prime": "bool"}
        )
        
        self.register_function(
            name="fibonacci_sequence",
            func=self.fibonacci_sequence,
            description="Generate fibonacci sequence up to n terms",
            inputs={"n": "int"},
            outputs={"sequence": "List[int]"}
        )
        
        self.register_function(
            name="greatest_common_divisor",
            func=self.greatest_common_divisor,
            description="Find GCD of two numbers",
            inputs={"a": "int", "b": "int"},
            outputs={"gcd": "int"}
        )
        
        self.register_function(
            name="least_common_multiple",
            func=self.least_common_multiple,
            description="Find LCM of two numbers",
            inputs={"a": "int", "b": "int"},
            outputs={"lcm": "int"}
        )
        
        self.register_function(
            name="palindrome_check",
            func=self.palindrome_check,
            description="Check if a string is a palindrome",
            inputs={"text": "str"},
            outputs={"is_palindrome": "bool"}
        )
        
        self.register_function(
            name="remove_duplicates",
            func=self.remove_duplicates,
            description="Remove duplicates from a list",
            inputs={"items": "List[Any]"},
            outputs={"unique_items": "List[Any]"}
        )
    
    def register_function(self, name: str, func: callable, description: str, 
                         inputs: Dict[str, str], outputs: Dict[str, str]):
        """Register a function with its metadata."""
        self.functions[name] = {
            "func": func,
            "description": description,
            "inputs": inputs,
            "outputs": outputs
        }
    
    def get_function_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all functions (without the actual function objects)."""
        return {
            name: {
                "description": meta["description"],
                "inputs": meta["inputs"],
                "outputs": meta["outputs"]
            }
            for name, meta in self.functions.items()
        }
    
    def execute_function(self, name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function by name with given inputs."""
        if name not in self.functions:
            raise ValueError(f"Function '{name}' not found")
        
        func = self.functions[name]["func"]
        return func(**inputs)
    
    # Function Implementations
    def get_invoices(self, month: str) -> Dict[str, List[Dict]]:
        """Mock function to retrieve invoices for a specific month."""
        # Simulate invoice data
        mock_invoices = [
            {"id": "INV-001", "date": f"2024-{month}-01", "amount": 1500.00, "client": "ABC Corp", "status": "paid"},
            {"id": "INV-002", "date": f"2024-{month}-15", "amount": 2300.00, "client": "XYZ Ltd", "status": "pending"},
            {"id": "INV-003", "date": f"2024-{month}-20", "amount": 890.00, "client": "Tech Solutions", "status": "paid"},
            {"id": "INV-004", "date": f"2024-{month}-28", "amount": 3200.00, "client": "Global Inc", "status": "overdue"},
        ]
        return {"invoices": mock_invoices}
    
    def filter_invoices_by_amount(self, invoices: List[Dict], min_amount: float) -> Dict[str, List[Dict]]:
        """Filter invoices by minimum amount."""
        filtered = [inv for inv in invoices if inv.get("amount", 0) >= min_amount]
        return {"filtered_invoices": filtered}
    
    def summarize_invoices(self, invoices: List[Dict]) -> Dict[str, Dict]:
        """Create a summary of invoice data."""
        total_amount = sum(inv.get("amount", 0) for inv in invoices)
        total_count = len(invoices)
        
        status_counts = {}
        for inv in invoices:
            status = inv.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        summary = {
            "total_amount": total_amount,
            "total_count": total_count,
            "status_breakdown": status_counts,
            "average_amount": total_amount / total_count if total_count > 0 else 0
        }
        return {"summary": summary}
    
    def send_email(self, content: str, recipient: str, subject: str = "Automated Report") -> Dict[str, str]:
        """Mock function to send an email."""
        # In a real implementation, this would actually send an email
        print(f"Mock Email Sent:")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Content: {content}")
        return {"status": "Email sent successfully"}
    
    def calculate_total(self, items: List[Dict], field: str) -> Dict[str, float]:
        """Calculate total amount from a list of items."""
        total = sum(item.get(field, 0) for item in items)
        return {"total": total}
    
    def group_by_field(self, data: List[Dict], field: str) -> Dict[str, Dict]:
        """Group data by a specific field."""
        grouped = {}
        for item in data:
            key = item.get(field, "unknown")
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)
        return {"grouped_data": grouped}
    
    def filter_by_date_range(self, data: List[Dict], date_field: str, 
                           start_date: str, end_date: str) -> Dict[str, List[Dict]]:
        """Filter data by date range."""
        filtered_data = []
        for item in data:
            item_date = item.get(date_field)
            if item_date and start_date <= item_date <= end_date:
                filtered_data.append(item)
        return {"filtered_data": filtered_data}
    
    def save_to_file(self, data: Any, filename: str) -> Dict[str, str]:
        """Save data to a JSON file."""
        filepath = f"data/{filename}"
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return {"filepath": filepath}
        except Exception as e:            return {"filepath": f"Error saving file: {str(e)}"}
    
    def read_from_file(self, filename: str) -> Dict[str, Any]:
        """Read data from a JSON file."""
        filepath = f"data/{filename}"
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return {"data": data}
        except Exception as e:
            return {"data": f"Error reading file: {str(e)}"}
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, float]:
        """Mock currency conversion function."""
        # Mock exchange rates
        rates = {
            ("USD", "EUR"): 0.85,
            ("EUR", "USD"): 1.18,
            ("USD", "GBP"): 0.73,
            ("GBP", "USD"): 1.37,
            ("EUR", "GBP"): 0.86,
            ("GBP", "EUR"): 1.16
        }
        
        rate = rates.get((from_currency, to_currency), 1.0)
        converted_amount = amount * rate
        return {"converted_amount": converted_amount}

    # Mathematical Functions
    def add_numbers(self, a: float, b: float) -> Dict[str, float]:
        """Add two numbers."""
        return {"result": a + b}
    
    def subtract_numbers(self, a: float, b: float) -> Dict[str, float]:
        """Subtract two numbers."""
        return {"result": a - b}
    
    def multiply_numbers(self, a: float, b: float) -> Dict[str, float]:
        """Multiply two numbers."""
        return {"result": a * b}
    
    def divide_numbers(self, a: float, b: float) -> Dict[str, float]:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return {"result": a / b}
    
    def power(self, base: float, exponent: float) -> Dict[str, float]:
        """Calculate a number raised to a power."""
        return {"result": math.pow(base, exponent)}
    
    def square_root(self, number: float) -> Dict[str, float]:
        """Calculate square root of a number."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return {"result": math.sqrt(number)}
    
    def factorial(self, number: int) -> Dict[str, int]:
        """Calculate factorial of a number."""
        if number < 0:
            raise ValueError("Cannot calculate factorial of negative number")
        return {"result": math.factorial(number)}
    
    def logarithm(self, number: float) -> Dict[str, float]:
        """Calculate natural logarithm of a number."""
        if number <= 0:
            raise ValueError("Cannot calculate logarithm of non-positive number")
        return {"result": math.log(number)}
    
    def sine(self, angle: float) -> Dict[str, float]:
        """Calculate sine of an angle in radians."""
        return {"result": math.sin(angle)}
    
    def cosine(self, angle: float) -> Dict[str, float]:
        """Calculate cosine of an angle in radians."""
        return {"result": math.cos(angle)}
    
    def tangent(self, angle: float) -> Dict[str, float]:
        """Calculate tangent of an angle in radians."""
        return {"result": math.tan(angle)}
    
    def absolute_value(self, number: float) -> Dict[str, float]:
        """Get absolute value of a number."""
        return {"result": abs(number)}
    
    # String Functions
    def uppercase_string(self, text: str) -> Dict[str, str]:
        """Convert string to uppercase."""
        return {"result": text.upper()}
    
    def lowercase_string(self, text: str) -> Dict[str, str]:
        """Convert string to lowercase."""
        return {"result": text.lower()}
    
    def reverse_string(self, text: str) -> Dict[str, str]:
        """Reverse a string."""
        return {"result": text[::-1]}
    
    def count_words(self, text: str) -> Dict[str, int]:
        """Count words in a string."""
        words = text.split()
        return {"count": len(words)}
    
    def remove_spaces(self, text: str) -> Dict[str, str]:
        """Remove all spaces from a string."""
        return {"result": text.replace(" ", "")}
    
    def replace_text(self, text: str, old: str, new: str) -> Dict[str, str]:
        """Replace text in a string."""
        return {"result": text.replace(old, new)}
    
    # List Functions
    def sort_list(self, numbers: List[float]) -> Dict[str, List[float]]:
        """Sort a list of numbers."""
        return {"sorted_list": sorted(numbers)}
    
    def find_max(self, numbers: List[float]) -> Dict[str, float]:
        """Find maximum value in a list."""
        if not numbers:
            raise ValueError("Cannot find max of empty list")
        return {"max_value": max(numbers)}
    
    def find_min(self, numbers: List[float]) -> Dict[str, float]:
        """Find minimum value in a list."""
        if not numbers:
            raise ValueError("Cannot find min of empty list")
        return {"min_value": min(numbers)}
    
    def calculate_average(self, numbers: List[float]) -> Dict[str, float]:
        """Calculate average of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        return {"average": sum(numbers) / len(numbers)}
    
    def calculate_median(self, numbers: List[float]) -> Dict[str, float]:
        """Calculate median of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate median of empty list")
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            median = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            median = sorted_numbers[n//2]
        return {"median": median}
    
    def sum_list(self, numbers: List[float]) -> Dict[str, float]:
        """Calculate sum of a list of numbers."""
        return {"sum": sum(numbers)}
    
    # Web Functions
    def web_summarizer(self, url: str) -> Dict[str, str]:
        """Fetch and summarize content from a web URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text
            
            # Simple text extraction (remove HTML tags)
            import re
            clean_text = re.sub(r'<[^>]+>', '', content)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            # Simple summarization (first 500 characters)
            summary = clean_text[:500] + "..." if len(clean_text) > 500 else clean_text
            
            return {"summary": summary, "content": clean_text[:2000]}
        except Exception as e:
            return {"summary": f"Error fetching URL: {str(e)}", "content": ""}
    
    def download_file(self, url: str, filename: str) -> Dict[str, str]:
        """Download a file from a URL."""
        try:
            # Ensure downloads directory exists
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            
            filepath = os.path.join(downloads_dir, filename)
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return {"status": "File downloaded successfully", "filepath": filepath}
        except Exception as e:
            return {"status": f"Error downloading file: {str(e)}", "filepath": ""}
    
    def check_url_status(self, url: str) -> Dict[str, Any]:
        """Check if a URL is accessible."""
        try:
            response = requests.head(url, timeout=10)
            return {"status_code": response.status_code, "is_accessible": response.status_code == 200}
        except Exception as e:
            return {"status_code": 0, "is_accessible": False}
    
    # Date and Time Functions
    def get_current_time(self) -> Dict[str, str]:
        """Get current date and time."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"current_time": current_time}
    
    def add_days(self, date: str, days: int) -> Dict[str, str]:
        """Add days to a date."""
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            new_date_obj = date_obj + timedelta(days=days)
            return {"new_date": new_date_obj.strftime("%Y-%m-%d")}
        except ValueError:
            return {"new_date": "Invalid date format. Use YYYY-MM-DD"}
    
    def date_difference(self, date1: str, date2: str) -> Dict[str, int]:
        """Calculate difference between two dates in days."""
        try:
            date1_obj = datetime.strptime(date1, "%Y-%m-%d")
            date2_obj = datetime.strptime(date2, "%Y-%m-%d")
            diff = (date2_obj - date1_obj).days
            return {"difference_days": diff}
        except ValueError:
            return {"difference_days": 0}
    
    def format_date(self, date: str, format: str) -> Dict[str, str]:
        """Format a date string."""
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted = date_obj.strftime(format)
            return {"formatted_date": formatted}
        except ValueError:
            return {"formatted_date": "Invalid date format"}
    
    # Utility Functions
    def generate_random_number(self, min_val: float, max_val: float) -> Dict[str, float]:
        """Generate a random number between min and max."""
        return {"random_number": random.uniform(min_val, max_val)}
    
    def generate_uuid(self) -> Dict[str, str]:
        """Generate a UUID string."""
        import uuid
        return {"uuid": str(uuid.uuid4())}
    
    def hash_string(self, text: str) -> Dict[str, str]:
        """Generate SHA256 hash of a string."""
        hash_object = hashlib.sha256(text.encode())
        return {"hash": hash_object.hexdigest()}
    
    def encode_base64(self, text: str) -> Dict[str, str]:
        """Encode string to base64."""
        encoded = base64.b64encode(text.encode()).decode()
        return {"encoded": encoded}
    
    def decode_base64(self, encoded: str) -> Dict[str, str]:
        """Decode base64 string."""
        try:
            decoded = base64.b64decode(encoded).decode()
            return {"decoded": decoded}
        except Exception:
            return {"decoded": "Invalid base64 string"}
    
    def validate_email(self, email: str) -> Dict[str, bool]:
        """Validate email address format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        return {"is_valid": is_valid}
    
    def extract_domain(self, url: str) -> Dict[str, str]:
        """Extract domain from URL."""
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0]
            return {"domain": domain}
        except Exception:
            return {"domain": "Invalid URL"}
    
    def count_characters(self, text: str) -> Dict[str, int]:
        """Count characters in a string."""
        return {"count": len(text)}
    
    def celsius_to_fahrenheit(self, celsius: float) -> Dict[str, float]:
        """Convert temperature from Celsius to Fahrenheit."""
        fahrenheit = (celsius * 9/5) + 32
        return {"fahrenheit": fahrenheit}
    
    def fahrenheit_to_celsius(self, fahrenheit: float) -> Dict[str, float]:
        """Convert temperature from Fahrenheit to Celsius."""
        celsius = (fahrenheit - 32) * 5/9
        return {"celsius": celsius}
    
    def calculate_percentage(self, value: float, total: float) -> Dict[str, float]:
        """Calculate percentage of a value."""
        if total == 0:
            raise ValueError("Total cannot be zero")
        percentage = (value / total) * 100
        return {"percentage": percentage}
    
    def round_number(self, number: float, decimals: int) -> Dict[str, float]:
        """Round a number to specified decimal places."""
        return {"rounded": round(number, decimals)}
    
    def check_prime(self, number: int) -> Dict[str, bool]:
        """Check if a number is prime."""
        if number < 2:
            return {"is_prime": False}
        for i in range(2, int(math.sqrt(number)) + 1):
            if number % i == 0:
                return {"is_prime": False}
        return {"is_prime": True}
    
    def fibonacci_sequence(self, n: int) -> Dict[str, List[int]]:
        """Generate fibonacci sequence up to n terms."""
        if n <= 0:
            return {"sequence": []}
        elif n == 1:
            return {"sequence": [0]}
        elif n == 2:
            return {"sequence": [0, 1]}
        
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        return {"sequence": sequence}
    
    def greatest_common_divisor(self, a: int, b: int) -> Dict[str, int]:
        """Find GCD of two numbers."""
        while b:
            a, b = b, a % b
        return {"gcd": abs(a)}
    
    def least_common_multiple(self, a: int, b: int) -> Dict[str, int]:
        """Find LCM of two numbers."""
        gcd = self.greatest_common_divisor(a, b)["gcd"]
        lcm = abs(a * b) // gcd
        return {"lcm": lcm}
    
    def palindrome_check(self, text: str) -> Dict[str, bool]:
        """Check if a string is a palindrome."""
        clean_text = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
        is_palindrome = clean_text == clean_text[::-1]
        return {"is_palindrome": is_palindrome}
    
    def remove_duplicates(self, items: List[Any]) -> Dict[str, List[Any]]:
        """Remove duplicates from a list."""
        unique_items = list(dict.fromkeys(items))  # Preserves order
        return {"unique_items": unique_items}
