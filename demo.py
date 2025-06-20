#!/usr/bin/env python3
"""
Demonstration script showing the MCP server capabilities without requiring Ollama
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.function_library import FunctionLibrary
from src.execution_engine import ExecutionEngine


def demo_basic_pipeline():
    """Demo a basic invoice processing pipeline."""
    print("🚀 Demo: Basic Invoice Processing Pipeline")
    print("=" * 50)
    
    # Initialize components
    lib = FunctionLibrary()
    engine = ExecutionEngine(lib)
    
    # Define a function call pipeline
    function_calls = [
        {"function": "get_invoices", "inputs": {"month": "March"}},
        {"function": "summarize_invoices", "inputs": {"invoices": "$output_0.invoices"}},
        {"function": "send_email", "inputs": {
            "content": "$output_1.summary", 
            "recipient": "finance@company.com", 
            "subject": "March Invoice Summary"
        }}
    ]
    
    print("\n📋 Planned Function Calls:")
    for i, call in enumerate(function_calls, 1):
        print(f"   {i}. {call['function']}({call['inputs']})")
    
    # Execute the pipeline
    print("\n🚀 Executing Pipeline...")
    result = engine.execute_pipeline(function_calls)
    
    if result["success"]:
        print("✅ Pipeline executed successfully!")
        print(f"\n📊 Final Result:")
        final_output = result["final_output"]
        print(f"   Status: {final_output.get('status', 'N/A')}")
        
        print(f"\n📈 Execution Summary:")
        for step in result["execution_history"]:
            if step["success"]:
                print(f"   ✓ Step {step['step']}: {step['function']} - Success")
            else:
                print(f"   ✗ Step {step['step']}: {step['function']} - Error: {step['error']}")
    else:
        print(f"❌ Pipeline failed: {result['error']}")


def demo_data_processing():
    """Demo data processing capabilities."""
    print("\n\n🔄 Demo: Data Processing Capabilities")
    print("=" * 50)
    
    lib = FunctionLibrary()
    engine = ExecutionEngine(lib)
    
    # More complex pipeline
    function_calls = [
        {"function": "get_invoices", "inputs": {"month": "March"}},
        {"function": "filter_invoices_by_amount", "inputs": {
            "invoices": "$output_0.invoices", 
            "min_amount": 1000.0
        }},
        {"function": "group_by_field", "inputs": {
            "data": "$output_1.filtered_invoices", 
            "field": "status"
        }},
        {"function": "save_to_file", "inputs": {
            "data": "$output_2.grouped_data", 
            "filename": "invoice_analysis.json"
        }}
    ]
    
    print("\n📋 Planned Function Calls:")
    for i, call in enumerate(function_calls, 1):
        print(f"   {i}. {call['function']}")
        for key, value in call['inputs'].items():
            print(f"      {key}: {value}")
    
    # Execute
    result = engine.execute_pipeline(function_calls)
    
    if result["success"]:
        print("\n✅ Data Processing Pipeline completed!")
        
        # Show some intermediate results
        print("\n📊 Intermediate Results:")
        for key, output in result["all_outputs"].items():
            print(f"   {key}:")
            if isinstance(output, dict):
                for k, v in output.items():
                    if isinstance(v, list):
                        print(f"     {k}: {len(v)} items")
                    elif isinstance(v, dict):
                        print(f"     {k}: {len(v)} keys")
                    else:
                        print(f"     {k}: {v}")
    else:
        print(f"❌ Pipeline failed: {result['error']}")


def demo_function_validation():
    """Demo function call validation."""
    print("\n\n🔍 Demo: Function Call Validation")
    print("=" * 50)
    
    lib = FunctionLibrary()
    engine = ExecutionEngine(lib)
    
    # Valid pipeline
    valid_calls = [
        {"function": "get_invoices", "inputs": {"month": "March"}},
        {"function": "calculate_total", "inputs": {"items": "$output_0.invoices", "field": "amount"}}
    ]
    
    # Invalid pipeline (missing parameter)
    invalid_calls = [
        {"function": "get_invoices", "inputs": {}},  # Missing required 'month' parameter
        {"function": "unknown_function", "inputs": {"data": "test"}}  # Unknown function
    ]
    
    print("\n✅ Testing Valid Pipeline:")
    valid_result = engine.dry_run(valid_calls)
    print(f"   Valid: {valid_result['valid']}")
    print(f"   Message: {valid_result['message']}")
    
    print("\n❌ Testing Invalid Pipeline:")
    is_valid, error_msg = engine.validate_function_calls(invalid_calls)
    print(f"   Valid: {is_valid}")
    print(f"   Error: {error_msg}")


def show_available_functions():
    """Show all available functions."""
    print("\n\n📚 Available Functions")
    print("=" * 50)
    
    lib = FunctionLibrary()
    functions = lib.get_function_metadata()
    
    categories = {
        "Invoice Management": ["get_invoices", "filter_invoices_by_amount", "summarize_invoices"],
        "Data Processing": ["calculate_total", "group_by_field", "filter_by_date_range"],
        "Communication": ["send_email"],
        "File Operations": ["save_to_file", "read_from_file"],
        "Utilities": ["convert_currency"]
    }
    
    for category, function_names in categories.items():
        print(f"\n🔧 {category}:")
        for func_name in function_names:
            if func_name in functions:
                func_meta = functions[func_name]
                print(f"   • {func_name}")
                print(f"     Description: {func_meta['description']}")
                inputs = ", ".join([f"{k}:{v}" for k, v in func_meta['inputs'].items()])
                print(f"     Inputs: {inputs}")
                outputs = ", ".join([f"{k}:{v}" for k, v in func_meta['outputs'].items()])
                print(f"     Outputs: {outputs}")


def main():
    """Run the demonstration."""
    print("🎯 MCP Smart Function Pipeline - Live Demonstration")
    print("=" * 60)
    print("This demo shows the MCP server capabilities without requiring Ollama")
    print("=" * 60)
    
    try:
        show_available_functions()
        demo_basic_pipeline()
        demo_data_processing()
        demo_function_validation()
        
        print("\n\n🎉 Demonstration completed!")
        print("\n📋 What this demonstrates:")
        print("✅ Function library with 10+ business functions")
        print("✅ Execution engine with data flow management")
        print("✅ Variable resolution ($output_0.field syntax)")
        print("✅ Pipeline validation and error handling")
        print("✅ Structured output management")
        
        print("\n🚀 To use with AI model:")
        print("1. Install and start Ollama: ollama serve")
        print("2. Pull the model: ollama pull mistral:7b")
        print("3. Start the server: python main.py")
        print("4. Send natural language queries to parse into function calls")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
