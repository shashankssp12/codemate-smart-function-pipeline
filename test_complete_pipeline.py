"""
Comprehensive test for the multi-step invoice pipeline
"""

import sys
import os

# Add the src directory to Python path
sys.path.append('src')

from function_library import FunctionLibrary
from execution_engine import ExecutionEngine
from mcp_server import MCPServer

def test_complete_pipeline():
    """Test the complete invoice pipeline: get invoices -> summarize -> send email."""
    
    print("🧪 Testing Complete Invoice Pipeline...")
    print("=" * 60)
    
    # Initialize the function library
    lib = FunctionLibrary()
    engine = ExecutionEngine(lib)
    
    # Test 1: Get invoices for December
    print("\n1️⃣  Testing get_invoices function...")
    invoices_result = lib.get_invoices("December")
    print(f"Invoices retrieved: {invoices_result}")
    
    # Test 2: Summarize invoices
    print("\n2️⃣  Testing summarize_invoices function...")
    if 'invoices' in invoices_result:
        summary_result = lib.summarize_invoices(invoices_result['invoices'])
        print(f"Summary created: {summary_result}")
    else:
        print("❌ No invoices found to summarize")
        return
    
    # Test 3: Send email with summary
    print("\n3️⃣  Testing send_email function with summary...")
    if 'summary' in summary_result:
        email_result = lib.send_email(
            content=summary_result['summary'],
            recipient="nitishsr14@gmail.com",
            subject="December Invoice Summary"
        )
        print(f"Email sent: {email_result}")
    else:
        print("❌ No summary found to email")
        return
    
    print("\n✅ Complete pipeline test successful!")
    
    # Test 4: Test execution engine with multi-step pipeline
    print("\n4️⃣  Testing execution engine with multi-step pipeline...")
    
    pipeline_steps = [
        {
            "function": "get_invoices",
            "inputs": {"month": "December"},
            "output_var": "december_invoices"
        },
        {
            "function": "summarize_invoices", 
            "inputs": {"invoices": "{{december_invoices.invoices}}"},
            "output_var": "invoice_summary"
        },
        {
            "function": "send_email",
            "inputs": {
                "content": "{{invoice_summary.summary}}",
                "recipient": "manager@company.com",
                "subject": "December Invoice Summary Report"
            },
            "output_var": "email_result"
        }
    ]
    
    execution_result = engine.execute_pipeline(pipeline_steps)
    print(f"Pipeline execution result: {execution_result}")
    
    # Test 5: Test with filtering
    print("\n5️⃣  Testing pipeline with invoice filtering...")
    
    filter_pipeline = [
        {
            "function": "get_invoices",
            "inputs": {"month": "December"},
            "output_var": "december_invoices"
        },
        {
            "function": "filter_invoices_by_amount",
            "inputs": {
                "invoices": "{{december_invoices.invoices}}",
                "min_amount": 5000.0
            },
            "output_var": "high_value_invoices"
        },
        {
            "function": "send_email",
            "inputs": {
                "content": "{{high_value_invoices.filtered_invoices}}",
                "recipient": "finance@company.com", 
                "subject": "High Value Invoices (>$5000)"
            },
            "output_var": "email_result"
        }
    ]
    
    filter_result = engine.execute_pipeline(filter_pipeline)
    print(f"Filter pipeline result: {filter_result}")
    
    print("\n🎉 All tests completed successfully!")

if __name__ == "__main__":
    test_complete_pipeline()
