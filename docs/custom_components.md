# Custom Components Guide for Langflow

This guide explains how to create and use custom components with Langflow in the Docker setup.

## Understanding Custom Components

Custom components allow you to extend Langflow with your own LangChain components, including:
- Custom LLM wrappers
- Custom chains
- Custom tools
- Custom agents
- Custom document loaders
- Custom embeddings

## Basic Setup

### Location for Custom Components

All custom components should be placed in the `custom_components` directory at the root of your project:

```
docker_langflow/
├── custom_components/  <-- Place your components here
│   ├── your_component1.py
│   ├── your_component2.py
│   └── ...
```

### Component Discovery

When Langflow starts, it automatically scans the `/app/custom_components` directory (which is mapped to your local `./custom_components` directory) for Python files containing component definitions.

## Creating a Simple Custom Component

### Step 1: Create a Python File

Create a new file in the `custom_components` directory:

```bash
touch custom_components/my_custom_tool.py
```

### Step 2: Define Your Component

Here's an example of a simple custom tool:

```python
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, Type

class CalculatorInput(BaseModel):
    """Input for the calculator tool."""
    operation: str = Field(description="Mathematical operation to perform (add, subtract, multiply, divide)")
    a: float = Field(description="First number")
    b: float = Field(description="Second number")

class CustomCalculatorTool(BaseTool):
    name = "custom_calculator"
    description = "A simple calculator for basic math operations"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, operation: str, a: float, b: float) -> str:
        """Run the calculator."""
        if operation == "add":
            return f"{a} + {b} = {a + b}"
        elif operation == "subtract":
            return f"{a} - {b} = {a - b}"
        elif operation == "multiply":
            return f"{a} * {b} = {a * b}"
        elif operation == "divide":
            if b == 0:
                return "Error: Division by zero"
            return f"{a} / {b} = {a / b}"
        else:
            return f"Error: Unknown operation '{operation}'"
    
    def _arun(self, operation: str, a: float, b: float):
        """Run the calculator asynchronously."""
        # This tool doesn't need async, so we just call the sync version
        return self._run(operation, a, b)
```

## More Complex Component Examples

### Custom LLM Wrapper

```python
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
import requests

class CustomAPILLM(LLM):
    """Custom LLM wrapper for an external API."""
    
    api_url: str
    api_key: str
    
    @property
    def _llm_type(self) -> str:
        return "custom_api_llm"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the external API."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"prompt": prompt, "max_tokens": 500}
        
        if stop:
            data["stop"] = stop
            
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise ValueError(f"API call failed: {response.text}")
            
        return response.json().get("output", "")
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Return identifying parameters."""
        return {"api_url": self.api_url}
```

### Custom Document Loader

```python
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
import csv
from typing import List

class CustomCSVLoader(BaseLoader):
    """Load CSV files with custom processing."""
    
    file_path: str
    content_column: str
    metadata_columns: List[str]
    
    def __init__(self, file_path: str, content_column: str, metadata_columns: List[str] = None):
        self.file_path = file_path
        self.content_column = content_column
        self.metadata_columns = metadata_columns or []
    
    def load(self) -> List[Document]:
        """Load and parse documents."""
        docs = []
        
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                # Extract content
                if self.content_column not in row:
                    raise ValueError(f"Column '{self.content_column}' not found in CSV")
                content = row[self.content_column]
                
                # Extract metadata
                metadata = {"source": self.file_path, "row": i}
                for col in self.metadata_columns:
                    if col in row:
                        metadata[col] = row[col]
                
                docs.append(Document(page_content=content, metadata=metadata))
                
        return docs
```

## Loading Python Packages in Custom Components

If your custom component requires additional Python packages that aren't included in the base Langflow image, you have two options:

### Option 1: Update the docker-compose.yml Command

Add the required packages to the pip install command in docker-compose.yml:

```yaml
command: >
  /bin/bash -c "
  pip install gspread oauth2client google-api-python-client google-auth google-auth-httplib2 your-new-package &&
  python -m langflow"
```

### Option 2: Install Packages in Your Component Code

You can handle missing packages within your component code:

```python
try:
    import some_package
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "some_package"])
    import some_package
```

## Applying and Testing Your Components

### Step 1: Restart Langflow

After adding or modifying custom components, restart Langflow:

```bash
docker compose restart
```

### Step 2: Verify Component Loading

Check the logs to ensure your components loaded successfully:

```bash
docker compose logs -f langflow_app
```

Look for messages indicating component discovery.

### Step 3: Use Your Component in Langflow

1. Open Langflow in your browser
2. Look for your custom component in the appropriate category in the left sidebar
3. Drag it onto the canvas
4. Configure its parameters
5. Connect it to other components
6. Test the flow with the "Build" button

## Troubleshooting Custom Components

### Component Not Appearing

1. Check file location: Ensure your Python file is in the `custom_components` directory
2. Check syntax: Verify your Python code is valid
3. Check logs: Look for errors in `docker compose logs -f langflow_app`
4. Restart: Try running `docker compose restart` again

### Component Appears But Causes Errors

1. Check implementation: Debug your component code
2. Check dependencies: Ensure all required packages are installed
3. Try a minimal test case: Create a simpler version of your component to isolate the issue

### Missing Dependencies

If your component requires packages not available in the base image:
1. Add them to the `command` section in docker-compose.yml
2. Restart with `docker compose restart`

## Best Practices

1. **Keep it simple**: Start with simple components before creating complex ones
2. **Handle errors gracefully**: Include proper error handling in your components
3. **Add clear descriptions**: Make your components user-friendly with good descriptions
4. **Version control**: Keep track of component changes in your version control system
5. **Test thoroughly**: Verify your components work as expected in various scenarios
6. **Documentation**: Document your custom components, including their purpose and parameters 