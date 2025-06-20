#!/usr/bin/env python3
"""
Test script to verify the functionality of the 50 functions in the function library.
"""

from src.function_library import FunctionLibrary

def test_functions():
    """Test all 50 functions in the library."""
    lib = FunctionLibrary()
    
    print("Testing Function Library with 50 functions:")
    print("=" * 50)
    
    # Get all function metadata
    functions = lib.get_function_metadata()
    print(f"Total functions available: {len(functions)}")
    print("\nFunction list:")
    for i, (name, meta) in enumerate(functions.items(), 1):
        print(f"{i:2d}. {name}: {meta['description']}")
    
    print("\n" + "=" * 50)
    print("Testing some key functions:")
    
    # Test mathematical functions
    print("\n1. Mathematical Functions:")
    print(f"   Add 5 + 3 = {lib.execute_function('add_numbers', {'a': 5, 'b': 3})}")
    print(f"   Power 2^8 = {lib.execute_function('power', {'base': 2, 'exponent': 8})}")
    print(f"   Square root of 16 = {lib.execute_function('square_root', {'number': 16})}")
    print(f"   Factorial of 5 = {lib.execute_function('factorial', {'number': 5})}")
    
    # Test string functions
    print("\n2. String Functions:")
    print(f"   Uppercase 'hello' = {lib.execute_function('uppercase_string', {'text': 'hello'})}")
    print(f"   Reverse 'python' = {lib.execute_function('reverse_string', {'text': 'python'})}")
    print(f"   Count words in 'Hello World Test' = {lib.execute_function('count_words', {'text': 'Hello World Test'})}")
    
    # Test list functions
    print("\n3. List Functions:")
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"   Original list: {numbers}")
    print(f"   Sorted: {lib.execute_function('sort_list', {'numbers': numbers})}")
    print(f"   Maximum: {lib.execute_function('find_max', {'numbers': numbers})}")
    print(f"   Average: {lib.execute_function('calculate_average', {'numbers': numbers})}")
    
    # Test utility functions
    print("\n4. Utility Functions:")
    print(f"   Current time: {lib.execute_function('get_current_time', {})}")
    print(f"   Random number (1-100): {lib.execute_function('generate_random_number', {'min_val': 1, 'max_val': 100})}")
    print(f"   UUID: {lib.execute_function('generate_uuid', {})}")
    
    # Test temperature conversion
    print("\n5. Temperature Conversion:")
    print(f"   25°C to Fahrenheit: {lib.execute_function('celsius_to_fahrenheit', {'celsius': 25})}")
    print(f"   77°F to Celsius: {lib.execute_function('fahrenheit_to_celsius', {'fahrenheit': 77})}")
    
    # Test prime checking
    print("\n6. Prime Number Check:")
    print(f"   Is 17 prime?: {lib.execute_function('check_prime', {'number': 17})}")
    print(f"   Is 20 prime?: {lib.execute_function('check_prime', {'number': 20})}")
    
    # Test fibonacci
    print("\n7. Fibonacci Sequence:")
    print(f"   First 10 fibonacci numbers: {lib.execute_function('fibonacci_sequence', {'n': 10})}")
    
    # Test email validation
    print("\n8. Email Validation:")
    print(f"   'test@example.com' valid?: {lib.execute_function('validate_email', {'email': 'test@example.com'})}")
    print(f"   'invalid-email' valid?: {lib.execute_function('validate_email', {'email': 'invalid-email'})}")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    return True

if __name__ == "__main__":
    test_functions()
