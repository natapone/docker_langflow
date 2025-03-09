# Basic Usage Guide

This guide covers the basic usage of Langflow after you've successfully installed it using Docker.

## Accessing Langflow

1. Open your web browser and navigate to:
   ```
   http://localhost:7860
   ```

2. You'll be presented with the Langflow login screen. If this is your first time, you'll need to create an account.

## Creating Your First Flow

1. **Create a New Flow**
   - Click on the "+" button in the top navigation bar
   - Give your flow a name

2. **Add Components**
   - Drag components from the left sidebar onto the canvas
   - Common components include:
     - LLMs (ChatOpenAI, Llama, etc.)
     - Prompts
     - Chains
     - Tools
     - Agents

3. **Connect Components**
   - Click and drag from one component's output node to another component's input node
   - The connections represent the flow of data between components

4. **Configure Components**
   - Click on a component to view and edit its parameters
   - For LLMs, you may need to provide API keys

5. **Test Your Flow**
   - Click the "Build" button to validate your flow
   - Use the chat interface on the right to test your flow

## Saving and Exporting Flows

1. **Save Your Flow**
   - Click the "Save" button in the top navigation bar
   - Your flow will be saved to the PostgreSQL database

2. **Export Your Flow**
   - Click the "Export" button
   - Choose to export as JSON
   - The exported flow can be imported into another Langflow instance

## Using Custom Components

If you've created custom components:

1. Place your Python files in the `custom_components` directory
2. Restart the Langflow container:
   ```bash
   docker compose restart langflow
   ```
3. Your custom components will appear in the components sidebar

## Managing Flows

1. **View All Flows**
   - Click on "Flows" in the sidebar
   - You'll see a list of all your saved flows

2. **Edit a Flow**
   - Click on a flow in the list to open it for editing

3. **Delete a Flow**
   - Hover over a flow in the list
   - Click the delete icon

## Advanced Features

1. **API Access**
   - Langflow provides an API for programmatic access
   - Access the API documentation at `http://localhost:7860/docs`

2. **Environment Variables**
   - Configure environment variables in the `.env` file
   - Restart the container for changes to take effect

## Troubleshooting

If you encounter issues while using Langflow:

1. **Component Errors**
   - Check that all required parameters are filled
   - Verify API keys are correct
   - Look for error messages in the component configuration

2. **Flow Execution Errors**
   - Check the logs in the chat interface
   - Verify connections between components are correct

3. **Container Issues**
   - Check Docker logs: `docker logs langflow_app`
   - Restart the container: `docker compose restart langflow` 