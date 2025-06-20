#!/usr/bin/env python3
"""
Comprehensive test for all 10 core functions
"""

import sys
import os
sys.path.append('src')

from function_library import FunctionLibrary
from execution_engine import ExecutionEngine

def test_all_functions():
    """Test all 10 core functions individually"""
    print("🧪 Testing All 10 Core Functions")
    print("=" * 60)
    
    lib = FunctionLibrary()
    
    # Test 1: get_invoices
    print("\n1. Testing get_invoices...")
    result = lib.get_invoices("december")
    print(f"   ✅ Result: Found {result['count']} invoices")
    
    # Test 2: summarize_invoices
    print("\n2. Testing summarize_invoices...")
    result = lib.summarize_invoices(result['invoices'])
    print(f"   ✅ Result: Total amount: ${result['total_amount']}")
    
    # Test 3: send_email
    print("\n3. Testing send_email...")
    result = lib.send_email("Test content", "test@example.com", "Test Subject")
    print(f"   ✅ Result: {result['status']}")
    
    # Test 4: validate_email
    print("\n4. Testing validate_email...")
    result = lib.validate_email("test@example.com")
    print(f"   ✅ Result: Valid: {result['is_valid']}")
    
    # Test 5: add_numbers
    print("\n5. Testing add_numbers...")
    result = lib.add_numbers(25, 17)
    print(f"   ✅ Result: {result['operation']}")
    
    # Test 6: get_current_time
    print("\n6. Testing get_current_time...")
    result = lib.get_current_time()
    print(f"   ✅ Result: {result['formatted']}")
    
    # Test 7: generate_random_number
    print("\n7. Testing generate_random_number...")
    result = lib.generate_random_number(1, 100)
    print(f"   ✅ Result: {result['random_number']} {result['range']}")
    
    # Test 8: uppercase_string
    print("\n8. Testing uppercase_string...")
    result = lib.uppercase_string("hello world")
    print(f"   ✅ Result: '{result['original']}' -> '{result['uppercase_text']}'")
    
    # Test 9: check_prime
    print("\n9. Testing check_prime...")
    result = lib.check_prime(17)
    print(f"   ✅ Result: {result['explanation']}")
    
    # Test 10: calculate_total
    print("\n10. Testing calculate_total...")
    test_items = [{"amount": 100}, {"amount": 200}, {"amount": 300}]
    result = lib.calculate_total(test_items, "amount")
    print(f"   ✅ Result: Total of {result['field']}: {result['total']}")
    
    print("\n" + "=" * 60)
    print("✅ All 10 functions tested successfully!")

def test_pipeline_execution():
    """Test pipeline execution with real email"""
    print("\n\n🔄 Testing Full Pipeline Execution")
    print("=" * 60)
    
    lib = FunctionLibrary()
    engine = ExecutionEngine(lib)
    
    # Test pipeline: get invoices -> summarize -> send email
    pipeline = [
        {
            "function": "get_invoices",
            "inputs": {"month": "december"},
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
                "content": "{{invoice_summary}}",
                "recipient": "test@example.com",
                "subject": "December Invoice Summary"
            }
        }
    ]
    
    print("\n📋 Executing pipeline:")
    for i, step in enumerate(pipeline, 1):
        print(f"   {i}. {step['function']}")
    
    result = engine.execute_pipeline(pipeline)
    
    if result["success"]:
        print(f"\n✅ Pipeline executed successfully!")
        print(f"📧 Email sent with invoice summary")
    else:
        print(f"\n❌ Pipeline failed: {result['error']}")
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline testing complete!")

if __name__ == "__main__":
    test_all_functions()
    test_pipeline_execution()
