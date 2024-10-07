import ast
import astunparse
from openai import OpenAI


client = OpenAI(api_key="")

def generate_unit_test_cases(python_code):
    """Generates unit test cases from Python code using an LLM and AST parser.

    Args:
        python_code (str): The Python code to generate test cases for.

    Returns:
        list: A list of generated unit test cases as strings.
    """

    # Parse the Python code using the AST parser
    tree = ast.parse(python_code)

    # Extract relevant information from the AST, such as functions and classes
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    # Generate unit test cases for each function and class
    test_cases = []
    for node in functions + classes:
        # Construct a prompt for the LLM, providing the node information
        prompt = f"""
Generate unit test cases for the Python {node.__class__.__name__}:

```python
{astunparse.unparse(node)}
Consider the node's parameters, return type, and potential edge cases.
"""
        print(prompt)
        
        # Use the LLM to generate test cases
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Adjust model as needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        print(response.choices[0].message.content)
        # Extract the generated test cases from the LLM response
        test_cases.append(response.choices[0].message.content)

    return test_cases


def generate_test_cases_for_chunk(python_code):
    """Generates unit test cases from Python code using an LLM, AST parser, and LangChain.

    Args:
        python_code (str): The Python code to generate test cases for.

    Returns:
        list: A list of generated unit test cases as strings.
    """

    # Parse the Python code using the AST parser
    tree = ast.parse(python_code)

    # Extract relevant information from the AST, such as functions and classes
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    # Generate unit test cases for each function
    test_cases = []
    for function in functions:
        # Handle large functions by breaking them down into smaller chunks
        if len(astunparse.unparse(function)) > 1024:
            # Divide the function into smaller chunks
            chunks = []
            current_chunk = ""
            for line in astunparse.unparse(function).splitlines():
                if len(current_chunk) + len(line) + 1 > 1024:
                    chunks.append(current_chunk)
                    current_chunk = ""
                current_chunk += line + "\n"
            if current_chunk:
                chunks.append(current_chunk)

            # Generate test cases for each chunk
            for chunk in chunks:
                prompt = f"""
                    Generate unit test cases for the Python function:

                    ```python
                    {chunk}

                    Consider the function's parameters, return type, and potential edge cases.
                    """
                # test_cases.append(llm_generate(prompt))
            else:
                prompt = f"""
                Generate unit test cases for the Python function:

                ```python
                {astunparse.unparse(function)}
                """
                # test_cases.append(llm_generate(prompt))

    return test_cases

python_code = """
    
class Calculator:

    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y
"""

test_cases = generate_unit_test_cases(python_code)
print(test_cases)

