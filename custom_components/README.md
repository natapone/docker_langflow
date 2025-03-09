# Custom Components for Langflow

This directory is for storing custom Langflow components. Any Python files placed here will be automatically loaded by Langflow at startup.

## How to Create Custom Components

1. Create a Python file with your component implementation
2. Follow the Langflow custom component structure
3. Restart the Langflow container to load your new components

## Example Custom Component

Here's a simple example of a custom component:

```python
from langflow import CustomComponent
from langchain.llms.base import BaseLLM
from typing import Optional

class MyCustomComponent(CustomComponent):
    display_name = "My Custom Component"
    description = "A custom component for demonstration purposes"
    
    def build_config(self):
        return {
            "input_text": {"display_name": "Input Text", "type": "str", "required": True},
            "llm": {"display_name": "Language Model", "type": "BaseLLM", "required": True},
            "temperature": {"display_name": "Temperature", "type": "float", "default": 0.7},
        }
    
    def build(self, input_text: str, llm: BaseLLM, temperature: Optional[float] = 0.7):
        def execute():
            return llm.generate([input_text], temperature=temperature)
        
        return execute
```

## Documentation

For more information on creating custom components, refer to the Langflow documentation:
https://docs.langflow.org/components/custom-components 