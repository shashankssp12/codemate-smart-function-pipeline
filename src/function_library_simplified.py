"""
Simplified Function Library Module
Contains 10 core functions focused on practical functionality.
"""

import json
import smtplib
import math
import os
import re
import hashlib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any
import random
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FunctionLibrary:
    """Registry of 10 core functions with their metadata."""
    
    def __init__(self):
        self.functions = {}
        self._register_functions()
    
    def _register_functions(self):
        """Register the 10 core functions with their metadata."""
        
        # 1. Invoice Management
        self.register_function(
            name="get_invoices",
            func=self.get_invoices,
            description="Retrieve invoices for a specific month",
            inputs={"month": "str"},
            outputs={"invoices": "List[Dict]", "count": "int"}
        )
        
        # 2. Invoice Summarization
        self.register_function(
            name="summarize_invoices",
            func=self.summarize_invoices,
            description="Create a summary of invoice data with totals and statistics",
            inputs={"invoices": "List[Dict]"},
            outputs={"summary": "Dict", "total_amount": "float", "count": "int"}
        )
        
        # 3. Email Sending
        self.register_function(
            name="send_email",
            func=self.send_email,
            description="Send an email with given content to a recipient",
            inputs={"content": "Any", "recipient": "str", "subject": "str"},
            outputs={"status": "str", "recipient": "str", "subject": "str"}
        )
        
        # 4. Email Validation
        self.register_function(
            name="validate_email",
            func=self.validate_email,
            description="Validate if an email address is properly formatted",
            inputs={"email": "str"},
            outputs={"is_valid": "bool", "email": "str"}
        )
        
        # 5. Mathematical Operations
        self.register_function(
            name="add_numbers",
            func=self.add_numbers,
            description="Add two numbers together",
            inputs={"a": "float", "b": "float"},
            outputs={"result": "float", "operation": "str"}
        )
        
        # 6. Current Time
        self.register_function(
            name="get_current_time",
            func=self.get_current_time,
            description="Get the current date and time",
            inputs={},
            outputs={"current_time": "str", "timestamp": "str", "formatted": "str"}
        )
        
        # 7. Random Number Generation
        self.register_function(
            name="generate_random_number",
            func=self.generate_random_number,
            description="Generate a random number between min and max values",
            inputs={"min_val": "float", "max_val": "float"},
            outputs={"random_number": "float", "range": "str"}
        )
        
        # 8. String Processing
        self.register_function(
            name="uppercase_string",
            func=self.uppercase_string,
            description="Convert a string to uppercase",
            inputs={"text": "str"},
            outputs={"uppercase_text": "str", "original": "str"}
        )
        
        # 9. Prime Number Checking
        self.register_function(
            name="check_prime",
            func=self.check_prime,
            description="Check if a number is prime",
            inputs={"number": "int"},
            outputs={"is_prime": "bool", "number": "int", "explanation": "str"}
        )
        
        # 10. Calculate Total
        self.register_function(
            name="calculate_total",
            func=self.calculate_total,
            description="Calculate the total of a specific field in a list of items",
            inputs={"items": "List[Dict]", "field": "str"},
            outputs={"total": "float", "count": "int", "field": "str"}
        )
    
    def register_function(self, name: str, func: callable, description: str, 
                         inputs: Dict[str, str], outputs: Dict[str, str]):
        """Register a function with its metadata."""
        self.functions[name] = {
            "function": func,
            "description": description,
            "inputs": inputs,
            "outputs": outputs
        }
    
    def get_function_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all functions."""
        metadata = {}
        for name, info in self.functions.items():
            metadata[name] = {
                "description": info["description"],
                "inputs": info["inputs"],
                "outputs": info["outputs"]
            }
        return metadata
    
    def execute_function(self, name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function by name with given inputs."""
        if name not in self.functions:
            return {"error": f"Function '{name}' not found"}
        
        try:
            function = self.functions[name]["function"]
            result = function(**inputs)
            return result
        except Exception as e:
            return {"error": f"Error executing function '{name}': {str(e)}"}
    
    # =============================================================================
    # FUNCTION IMPLEMENTATIONS
    # =============================================================================
    
    def get_invoices(self, month: str) -> Dict[str, Any]:
        """Retrieve invoices for a specific month."""
        # Simulate invoice data for the given month
        sample_invoices = [
            {
                "invoice_id": f"INV-{month.upper()}-001",
                "amount": 5000.00,
                "status": "paid",
                "date": f"2024-{self._get_month_number(month)}-15",
                "client": "Acme Corp"
            },
            {
                "invoice_id": f"INV-{month.upper()}-002",
                "amount": 7500.00,
                "status": "paid",
                "date": f"2024-{self._get_month_number(month)}-20",
                "client": "Tech Solutions"
            },
            {
                "invoice_id": f"INV-{month.upper()}-003",
                "amount": 3000.00,
                "status": "pending",
                "date": f"2024-{self._get_month_number(month)}-25",
                "client": "StartUp Inc"
            }        ]
        
        return {
            "invoices": sample_invoices,
            "count": len(sample_invoices)
        }
    
    def summarize_invoices(self, invoices: List[Dict]) -> Dict[str, Any]:
        """Create a summary of invoice data."""
        if not invoices:
            return {
                "summary": "No invoices found",
                "total_amount": 0.0,
                "count": 0
            }
        
        total_amount = sum(invoice.get("amount", 0) for invoice in invoices)
        paid_count = len([inv for inv in invoices if inv.get("status") == "paid"])
        pending_count = len([inv for inv in invoices if inv.get("status") == "pending"])
        
        summary = {
            "total_invoices": len(invoices),
            "total_amount": total_amount,
            "paid_invoices": paid_count,
            "pending_invoices": pending_count,
            "average_amount": total_amount / len(invoices) if invoices else 0
        }
        
        return {
            "summary": summary,
            "total_amount": total_amount,
            "count": len(invoices)
        }
    
    def send_email(self, content: Any, recipient: str, subject: str = "Automated Report") -> Dict[str, str]:
        """Send an email with given content using real SMTP."""
        try:
            # Format content based on type
            if isinstance(content, dict):
                formatted_content = self._format_dict_for_email(content)
            elif isinstance(content, list):
                formatted_content = self._format_list_for_email(content)
            else:
                formatted_content = str(content)
            
            # Get email configuration from environment variables
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            email_username = os.getenv('EMAIL_USERNAME')
            email_password = os.getenv('EMAIL_PASSWORD')
            
            # Validate email configuration
            if not email_username or not email_password:
                return {
                    "status": "Error: Email credentials not configured in .env file",
                    "recipient": recipient,
                    "subject": subject
                }
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_username
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body to email
            body = f"""
Hello,

Here is your automated report:

{formatted_content}

--
This email was sent automatically by the Smart Function Pipeline System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(email_username, email_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(email_username, recipient, text)
            server.quit()
            
            print(f"✅ Real Email sent successfully to {recipient}")
            print(f"📧 Subject: {subject}")
            print("-" * 50)
            
            return {
                "status": "Email sent successfully",
                "recipient": recipient,
                "subject": subject
            }
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "SMTP Authentication failed. Please check email credentials."
            print(f"❌ {error_msg}")
            return {
                "status": f"Error: {error_msg}",
                "recipient": recipient,
                "subject": subject
            }
        except smtplib.SMTPRecipientsRefused:
            error_msg = f"Recipient email address '{recipient}' was refused by the server."
            print(f"❌ {error_msg}")
            return {
                "status": f"Error: {error_msg}",
                "recipient": recipient,
                "subject": subject
            }
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "status": f"Error: {error_msg}",
                "recipient": recipient,
                "subject": subject
            }
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """Validate if an email address is properly formatted."""
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(email_pattern, email))
        
        return {
            "is_valid": is_valid,
            "email": email
        }
    
    def add_numbers(self, a: float, b: float) -> Dict[str, Any]:
        """Add two numbers together."""
        result = a + b
        return {
            "result": result,
            "operation": f"{a} + {b} = {result}"
        }
    
    def get_current_time(self) -> Dict[str, str]:
        """Get the current date and time."""
        now = datetime.now()
        return {
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": str(now.timestamp()),
            "formatted": now.strftime("%A, %B %d, %Y at %I:%M:%S %p")
        }
    
    def generate_random_number(self, min_val: float, max_val: float) -> Dict[str, Any]:
        """Generate a random number between min and max values."""
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        
        random_num = random.uniform(min_val, max_val)
        return {
            "random_number": round(random_num, 2),
            "range": f"between {min_val} and {max_val}"
        }
    
    def uppercase_string(self, text: str) -> Dict[str, str]:
        """Convert a string to uppercase."""
        return {
            "uppercase_text": text.upper(),
            "original": text
        }
    
    def check_prime(self, number: int) -> Dict[str, Any]:
        """Check if a number is prime."""
        if number < 2:
            return {
                "is_prime": False,
                "number": number,
                "explanation": f"{number} is not prime (less than 2)"
            }
        
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return {
                    "is_prime": False,
                    "number": number,
                    "explanation": f"{number} is not prime (divisible by {i})"
                }
        
        return {
            "is_prime": True,
            "number": number,
            "explanation": f"{number} is prime"
        }
    
    def calculate_total(self, items: List[Dict], field: str) -> Dict[str, Any]:
        """Calculate the total of a specific field in a list of items."""
        try:
            total = sum(item.get(field, 0) for item in items if isinstance(item.get(field), (int, float)))
            return {
                "total": total,
                "count": len(items),
                "field": field
            }
        except Exception as e:
            return {
                "total": 0,
                "count": 0,
                "field": field,
                "error": str(e)
            }
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _get_month_number(self, month: str) -> str:
        """Convert month name to number."""
        months = {
            "january": "01", "february": "02", "march": "03", "april": "04",
            "may": "05", "june": "06", "july": "07", "august": "08",
            "september": "09", "october": "10", "november": "11", "december": "12"
        }
        return months.get(month.lower(), "01")
    
    def _format_dict_for_email(self, data: dict) -> str:
        """Format dictionary data for email content."""
        def format_value(value, indent=0):
            spaces = "  " * indent
            if isinstance(value, dict):
                result = "{\n"
                for k, v in value.items():
                    result += f"{spaces}  {k}: {format_value(v, indent + 1)}\n"
                result += f"{spaces}}}"
                return result
            elif isinstance(value, list):
                if not value:
                    return "[]"
                result = "[\n"
                for item in value:
                    result += f"{spaces}  {format_value(item, indent + 1)}\n"
                result += f"{spaces}]"
                return result
            else:
                return str(value)
        
        return format_value(data)
    
    def _format_list_for_email(self, data: list) -> str:
        """Format list data for email content."""
        if not data:
            return "No items found."
        
        result = f"List of {len(data)} items:\n\n"
        for i, item in enumerate(data, 1):
            result += f"{i}. {self._format_dict_for_email(item) if isinstance(item, dict) else str(item)}\n"
        
        return result
