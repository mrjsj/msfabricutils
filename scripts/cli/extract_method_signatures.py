import yaml
import inspect
from typing import Any, Dict, List, Optional
import re
from msfabricpysdkcore import FabricClientAdmin, FabricClientCore

def parse_google_docstring(docstring: Optional[str]) -> Dict[str, Dict[str, str]]:
    """
    Parse a Google-style docstring to extract parameter types and descriptions.
    
    Example Google format:
    Args:
        param1 (type): description
        param2 (type, optional): description
    """
    if not docstring:
        return {}

    params = {}
    
    # Find the Args section
    args_match = re.search(r'Args:(.*?)(?:\n\n|$)', docstring, re.DOTALL)
    if not args_match:
        return params

    args_section = args_match.group(1)
    
    # Parse each parameter line
    # Matches lines like: "    param_name (param_type): param_description"
    # or "    param_name (param_type, optional): param_description"
    param_pattern = r'\s*(\w+)\s*\(([^)]+)\):\s*(.+?)(?:\n|$)'
    
    for match in re.finditer(param_pattern, args_section):
        name, type_info, description = match.groups()
        
        # Clean up the type information
        type_info = type_info.strip()
        # Remove 'optional' from type but note if it was present
        is_optional = 'optional' in type_info.lower()
        type_info = re.sub(r',?\s*optional', '', type_info, flags=re.IGNORECASE)
        
        params[name] = {
            'type': type_info.strip(),
            'description': description.strip(),
            'optional': is_optional
        }
    
    return params

def get_parameter_info(func: Any) -> List[Dict[str, Any]]:
    """Extract parameter information from a function, including signature and docstring details."""
    signature = inspect.signature(func)
    docstring_info = parse_google_docstring(inspect.getdoc(func))
    
    parameters = []
    for name, param in signature.parameters.items():
        # Skip 'self' parameter
        if name == 'self':
            continue
            
        param_info = {
            'name': name,
            'required': param.default == inspect.Parameter.empty,
            'default': None if param.default == inspect.Parameter.empty else param.default
        }
        
        # Add docstring information if available
        if name in docstring_info:
            param_info.update({
                'type': docstring_info[name]['type'],
                'description': docstring_info[name]['description']
            })
            # Override required based on docstring if marked as optional
            if docstring_info[name].get('optional'):
                param_info['required'] = False
        else:
            param_info.update({
                'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Unknown',
                'description': ''
            })
        # if param_info['type'] == 'Unknown':
        #     continue
        parameters.append(param_info)
    
    return parameters

def update_yaml_with_args(data: Dict, client_class: Any) -> None:
    """Recursively update the YAML structure with argument information."""
    if isinstance(data, dict):
        if 'function' in data and 'args' in data:
            func_name = data['function']
            if hasattr(client_class, func_name):
                func = getattr(client_class, func_name)
                data['args'] = get_parameter_info(func)
        
        # Handle custom_function cases (like partial functions)
        elif 'custom_function' in data and 'args' in data:
            # Skip these as they're special cases
            pass
        
        # Recurse through all dictionary items
        for value in data.values():
            update_yaml_with_args(value, client_class)
    elif isinstance(data, list):
        for item in data:
            update_yaml_with_args(item, client_class)

def main():
    # Read the YAML file
    with open('src/msfabricutils/cli/sdk-funcs.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    # Process each area
    for area in data.get('areas', []):
        # Determine which client class to use
        client_name = area.get('client')
        if client_name == 'FabricClientAdmin':
            client_class = FabricClientAdmin
        elif client_name == 'FabricClientCore':
            client_class = FabricClientCore
        else:
            print(f"Unknown client class: {client_name}")
            continue
        
        # Update args for this area
        update_yaml_with_args(area.get('commands', {}), client_class)
    
    # Write the updated YAML back to file
    with open('src/msfabricutils/cli/sdk-funcs1.yaml', 'w') as file:
        yaml.dump(data, file, sort_keys=False, indent=2)

if __name__ == "__main__":
    main()