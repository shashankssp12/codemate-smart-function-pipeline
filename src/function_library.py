"""
Function Library Module
Contains all the predefined functions that can be called by the MCP server.
"""

import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional
import random


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
        except Exception as e:
            return {"filepath": f"Error saving file: {str(e)}"}
    
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
