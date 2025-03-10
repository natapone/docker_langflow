# Basic Usage Guide

This guide covers the basic usage of Langflow after you've successfully installed it using Docker.

## Accessing Langflow

1. Open your web browser and navigate to:
   ```
   http://localhost:7860
   ```
   (or the port you specified in your `.env` file)

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
   make restart
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

## Data Management

All persistent data is stored in the `./data` directory:

1. **Langflow Data**
   - Located in `./data/langflow`
   - Contains flows, settings, and user data
   - Can be backed up by copying this directory

2. **Database Data**
   - Located in `./data/postgres`
   - Contains the PostgreSQL database files
   - Can be backed up by copying this directory

## Environment Configuration

You can configure Langflow by editing the `.env` file:

1. **Port Configuration**
   - Change `LANGFLOW_PORT` to use a different port
   - Restart the containers with `make restart` for changes to take effect

2. **Database Configuration**
   - Modify `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`
   - Requires a full restart with `make clean` and `make start` to take effect

3. **API Keys**
   - Add your OpenAI API key by uncommenting and setting `OPENAI_API_KEY`
   - Add other API keys as needed for different components

## Advanced Features

1. **API Access**
   - Langflow provides an API for programmatic access
   - Access the API documentation at `http://localhost:7860/docs` (or your custom port)

2. **Cache Configuration**
   - Enable Redis caching by uncommenting and setting the Redis configuration in `.env`
   - Improves performance for repeated operations

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
   - Check Docker logs: `make logs`
   - Restart the container: `make restart`

4. **Data Persistence Issues**
   - Ensure the `./data` directory has proper permissions
   - Run `docker compose run --rm init-volumes` to fix permissions 