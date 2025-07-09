#!/usr/bin/env python3
"""
Test runner for cube.py unit tests using pytest
"""

import sys
import os
import subprocess

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all tests using pytest"""
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'test_cube.py', 
            '-v',
            '--tb=short'
        ], capture_output=True, text=True)
        
        # Print output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Return exit code based on test results
        return result.returncode
        
    except FileNotFoundError:
        print("Error: pytest not found. Please install it with: pip install pytest")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code) 