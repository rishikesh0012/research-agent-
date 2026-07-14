"""
Docstring conventions and standards for the project.
"""

"""
All docstrings should follow Google style guide:

    Example:
        def function_name(param1: str, param2: int) -> bool:
            \"\"\"
            Brief description of what the function does.
            
            Longer explanation if needed. Can span multiple lines.
            
            Args:
                param1: Description of param1
                param2: Description of param2
            
            Returns:
                Description of return value
            
            Raises:
                ValueError: Description of when this is raised
                TypeError: Description of when this is raised
            
            Example:
                >>> function_name("test", 42)
                True
            \"\"\"
            pass

Class docstrings:
    
    class ClassName:
        \"\"\"
        Brief description of the class.
        
        Longer description if needed.
        
        Attributes:
            attr1: Description of attr1
            attr2: Description of attr2
        \"\"\"
        
        def __init__(self, attr1: str, attr2: int):
            \"\"\"
            Initialize the class.
            
            Args:
                attr1: First attribute
                attr2: Second attribute
            \"\"\"
            pass
"""
