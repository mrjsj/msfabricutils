from functools import wraps
from inspect import signature
import ast
from typing import Callable

class FabricClientCallValidator(ast.NodeVisitor):
    """AST Visitor that validates FabricClient method calls"""
    def __init__(self, client_class):
        self.client_class = client_class
        self.errors = []

    def visit_Call(self, node):
        # Check if this is a client method call
        if (isinstance(node.func, ast.Attribute) and 
            isinstance(node.func.value, ast.Name) and 
            node.func.value.id == 'client'):
            
            method_name = node.func.attr
            if hasattr(self.client_class, method_name):
                # Get expected signature
                expected_sig = signature(getattr(self.client_class, method_name))
                expected_params = set(expected_sig.parameters.keys())
                expected_params.remove('self')
                
                # Get actual parameters
                actual_params = set()
                for kw in node.keywords:
                    actual_params.add(kw.arg)
                
                # Check for mismatches
                missing = expected_params - actual_params
                unexpected = actual_params - expected_params
                
                if missing:
                    self.errors.append(f"Missing parameters in {method_name} call: {', '.join(missing)}")
                if unexpected:
                    self.errors.append(f"Unexpected parameters in {method_name} call: {', '.join(unexpected)}")
        
        self.generic_visit(node)

def validate_fabric_client_calls(source_code: str, client_class) -> list[str]:
    """
    Validate all FabricClient method calls in the given source code.
    
    Args:
        source_code: The source code to check
        client_class: The client class to validate against (e.g., FabricClientAdmin)
    
    Returns:
        List of validation error messages
    """
    tree = ast.parse(source_code)
    validator = FabricClientCallValidator(client_class)
    validator.visit(tree)
    return validator.errors


import os
from msfabricpysdkcore import FabricClientAdmin, FabricClientCore
from msfabricpysdkcore.client import FabricClient
from typing import Type
# from msfabricutils.decorators import validate_fabric_client_calls

def validate_commands_directory(base_path: str, client_class: Type[FabricClient]) -> None:
    """Validate all command files in the given directory"""
    errors = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    source = f.read()
                error = validate_fabric_client_calls(source, client_class)
                if error:
                    error_file = {"file": file_path, "errors": error}
                    errors.append(error_file)
    return errors

if __name__ == "__main__":
    commands_path = "cli/commands"  # Adjust this path as needed
    errors = validate_commands_directory(commands_path + "/admin", FabricClientAdmin)
    errors.extend(validate_commands_directory(commands_path + "/core", FabricClientCore))
    if errors:
        print("\nValidation errors found:")
        for error in errors:
            for error_item in error['errors']:

                print(f" {error['file']} - {error_item}")
        #raise Exception("Validation errors found")
