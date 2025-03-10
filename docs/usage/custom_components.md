# Custom Components in Langflow

This guide explains how to create, add, and use custom components in Langflow.

## Overview

Custom components are created within Langflow and extend the platform's functionality with custom, reusable Python code. Since Langflow operates with Python behind the scenes, you can implement any Python function within a Custom Component, leveraging libraries such as Pandas, Scikit-learn, Numpy, and thousands of other packages.

Custom Components create reusable and configurable components to enhance the capabilities of Langflow, making it a powerful tool for developing complex processing between user and AI messages.

## Directory Structure Requirements

By default, Langflow looks for custom components in specific directories. In our Docker setup, custom components are stored in the `./custom_components` directory:

```
docker_langflow/
├── custom_components/  # Base directory (set by LANGFLOW_COMPONENTS_PATH)
│   ├── category_name/  # Required category subfolder (determines menu name)
│   │   └── my_component.py  # Component file
│   └── another_category/
│       └── another_component.py
└── ...
```

**Important**: Components must be placed inside **category folders**, not directly in the base directory. The category folder name determines where the component appears in the UI menu.

For example, to add a component to the **Helpers** menu, place it in a `helpers` subfolder:

```
docker_langflow/
├── custom_components/  # LANGFLOW_COMPONENTS_PATH
│   └── helpers/  # Shows up as "Helpers" menu
│       └── custom_component.py  # Your component
└── ...
```

You can have **multiple category folders** to organize components into different menus:

```
docker_langflow/
├── custom_components/
│   ├── helpers/
│   │   └── helper_component.py
│   └── tools/
│       └── tool_component.py
└── ...
```

Components placed directly in the base directory will not be loaded:

```
docker_langflow/
├── custom_components/  # LANGFLOW_COMPONENTS_PATH
│   └── custom_component.py  # Won't be loaded - missing category folder!
└── ...
```

## Creating a Custom Component

Creating custom components in Langflow involves creating a Python class that defines the component's functionality, inputs, and outputs.

Here's a basic example:

```python
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data

class CustomComponent(Component):
    display_name = "Custom Component"
    description = "Use as a template to create your own component."
    documentation = "https://docs.langflow.org/components-custom-components"
    icon = "custom_components"
    name = "CustomComponent"

    inputs = [
        MessageTextInput(name="input_value", display_name="Input Value", value="Hello, World!"),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        data = Data(value=self.input_value)
        self.status = data
        return data
```

Save this file as `./custom_components/helpers/custom_component.py`.

### Component Structure

A custom component consists of:

1. **Class Definition**: A class that inherits from `Component`
2. **Metadata**: Display name, description, documentation, and icon
3. **Inputs**: Define the inputs using Langflow's input classes
4. **Outputs**: Define the outputs and their associated methods
5. **Output Methods**: Implement methods for each output, which contains the logic of your component

### Adding Various Input Types

Langflow provides several input types for custom components:

```python
from langflow.custom import Component
from langflow.inputs import StrInput, MultilineInput, SecretStrInput, IntInput, DropdownInput
from langflow.template import Output
from langflow.schema.message import Message

class MyCustomComponent(Component):
    display_name = "My Custom Component"
    description = "An example of a custom component with various input types."

    inputs = [
        StrInput(
            name="username",
            display_name="Username",
            info="Enter your username."
        ),
        SecretStrInput(
            name="password",
            display_name="Password",
            info="Enter your password."
        ),
        MessageTextInput(
            name="special_message",
            display_name="special_message",
            info="Enter a special message.",
        ),
        IntInput(
            name="age",
            display_name="Age",
            info="Enter your age."
        ),
        DropdownInput(
            name="gender",
            display_name="Gender",
            options=["Male", "Female", "Other"],
            info="Select your gender."
        )
    ]

    outputs = [
        Output(display_name="Result", name="result", method="process_inputs"),
    ]

    def process_inputs(self) -> Message:
        """
        Process the user inputs and return a Message object.

        Returns:
            Message: A Message object containing the processed information.
        """
        try:
            processed_text = f"User {self.username} (Age: {self.age}, Gender: {self.gender}) " \
                f"sent the following special message: {self.special_message}"
            return Message(text=processed_text)
        except AttributeError as e:
            return Message(text=f"Error processing inputs: {str(e)}")
```

### Creating a Component with Generic Input

You can also use the generic `Input` class for more flexibility:

```python
from langflow.template import Input, Output
from langflow.custom import Component
from langflow.field_typing import Text
from langflow.schema.message import Message
from typing import Dict, Any

class TextAnalyzerComponent(Component):
    display_name = "Text Analyzer"
    description = "Analyzes input text and provides basic statistics."

    inputs = [
        Input(
            name="input_text",
            display_name="Input Text",
            field_type="Message",
            required=True,
            placeholder="Enter text to analyze",
            multiline=True,
            info="The text you want to analyze.",
            input_types=["Text"]
        ),
        Input(
            name="include_word_count",
            display_name="Include Word Count",
            field_type="bool",
            required=False,
            info="Whether to include word count in the analysis.",
        ),
        Input(
            name="perform_sentiment_analysis",
            display_name="Perform Sentiment Analysis",
            field_type="bool",
            required=False,
            info="Whether to perform basic sentiment analysis.",
        ),
    ]

    outputs = [
        Output(display_name="Analysis Results", name="results", method="analyze_text"),
    ]

    def analyze_text(self) -> Message:
        # Extract text from the Message object
        if isinstance(self.input_text, Message):
            text = self.input_text.text
        else:
            text = str(self.input_text)

        results = {
            "character_count": len(text),
            "sentence_count": text.count('.') + text.count('!') + text.count('?')
        }

        if self.include_word_count:
            results["word_count"] = len(text.split())

        if self.perform_sentiment_analysis:
            # Basic sentiment analysis
            text_lower = text.lower()
            if "happy" in text_lower or "good" in text_lower:
                sentiment = "positive"
            elif "sad" in text_lower or "bad" in text_lower:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            results["sentiment"] = sentiment

        # Convert the results dictionary to a formatted string
        formatted_results = "\n".join([f"{key}: {value}" for key, value in results.items()])

        # Return a Message object
        return Message(text=formatted_results)
```

### Creating a Component with Multiple Outputs

Custom components can have multiple outputs, each associated with a specific method:

```python
from typing import Callable
from langflow.custom import Component
from langflow.inputs import StrInput
from langflow.template import Output
from langflow.field_typing import Text

class DualOutputComponent(Component):
    display_name = "Dual Output"
    description = "Processes input text and returns both the result and the processing function."
    icon = "double-arrow"

    inputs = [
        StrInput(
            name="input_text",
            display_name="Input Text",
            info="The text input to be processed.",
        ),
    ]

    outputs = [
        Output(display_name="Processed Data", name="processed_data", method="process_data"),
        Output(display_name="Processing Function", name="processing_function", method="get_processing_function"),
    ]

    def process_data(self) -> Text:
        # Process the input text (e.g., convert to uppercase)
        processed = self.input_text.upper()
        self.status = processed
        return processed

    def get_processing_function(self) -> Callable[[], Text]:
        # Return the processing function itself
        return self.process_data
```

## Special Operations

Advanced methods and attributes offer additional control and functionality:

* `self.inputs`: Access all defined inputs
* `self.outputs`: Access all defined outputs
* `self.status`: Update the component's status or intermediate results
* `self.graph.flow_id`: Retrieve the flow ID for context or debugging
* `self.stop("output_name")`: Stop data from being sent through other components

## Adding Custom Components to Your Setup

To add a custom component to your Langflow Docker setup:

1. Create the appropriate category directory in `./custom_components/` if it doesn't exist
2. Create your Python file with the component class in that directory
3. Restart the Langflow container:
   ```bash
   make restart
   ```

## Testing Custom Components

To test your custom component:

1. After adding your component and restarting Langflow, open the Langflow UI
2. Look for your component in the components panel under the appropriate category
3. Drag it onto the canvas and connect it to other components
4. Configure the component parameters
5. Test the flow to see if your component works as expected

## Debugging Custom Components

If your component doesn't appear or doesn't work as expected:

1. Check the Langflow logs:
   ```bash
   make logs
   ```

2. Verify that your component file has the correct structure and is in the right directory
3. Check for Python syntax errors
4. Ensure that all required dependencies are available in the container

## Best Practices

1. **Organize by Category**: Place components in appropriate category folders
2. **Descriptive Names**: Use clear, descriptive names for your components
3. **Documentation**: Include detailed descriptions and documentation links
4. **Error Handling**: Implement proper error handling in your components
5. **Type Annotations**: Use proper type annotations for inputs and outputs
6. **Status Updates**: Use `self.status` to provide feedback on component state
7. **Testing**: Test your components thoroughly before using them in production

## Resources

- [Official Langflow Documentation](https://docs.langflow.org/components-custom-components)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Custom Components Examples](https://github.com/langflow-ai/langflow/tree/dev/src/backend/langflow/components/customs) 