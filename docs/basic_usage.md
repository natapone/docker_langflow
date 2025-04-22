# Langflow Basic Usage Guide

This guide covers the essential tasks for using Langflow, including accessing the application, creating flows, and managing data.

## Accessing Langflow

After starting the Docker containers, access Langflow through your web browser:

```
http://localhost:7860
```

(or the port you specified in your `.env` file)

## Creating Your First Flow

### Step 1: Create a New Flow

1. Click the "**+ New**" button in the top navigation bar
2. A blank canvas will appear where you can build your flow

### Step 2: Add Components

1. On the left sidebar, browse through available components 
2. Drag components onto the canvas
3. Common components to start with:
   - **LLMs**: ChatOpenAI, Anthropic
   - **Prompts**: ChatPromptTemplate
   - **Memory**: ConversationBufferMemory
   - **Chains**: LLMChain, ConversationChain

### Step 3: Connect Components

1. Hover over a component's output handle (right side)
2. Click and drag to another component's input handle (left side)
3. Valid connections will highlight when you hover
4. Release to create the connection

### Step 4: Configure Components

1. Click on a component to view its parameters
2. Fill in required fields (marked with *)
3. For OpenAI components, ensure your API key is set in the `.env` file or enter it in the component settings

### Step 5: Test Your Flow

1. Click the "**Build**" button in the top right corner
2. If your flow is valid, a chat interface will appear
3. Type a message to test your flow
4. Review the response and refine your flow as needed

## Saving and Managing Flows

### Saving Flows

1. Click "**Save**" in the top navigation bar
2. Enter a name for your flow
3. Click "**Save**" to store your flow in the PostgreSQL database

### Loading Saved Flows

1. Click "**Flows**" in the left sidebar
2. Browse your saved flows
3. Click on a flow to open and edit it

### Exporting Flows

1. Open the flow you want to export
2. Click "**Export**" in the top navigation bar
3. Choose "**JSON**" format
4. The flow will download as a JSON file

### Importing Flows

1. Click "**Import**" in the top navigation bar
2. Select a previously exported JSON flow file
3. The flow will load into the canvas

## Using Custom Components

### Adding Custom Components

1. Create Python files in the `custom_components` directory
2. Files should define custom LangChain components
3. Restart the Langflow container:
   ```bash
   docker compose restart
   ```
4. Your custom components will appear in the left sidebar

## Data Management

### Where Data is Stored

All persistent data is stored in the `./data` directory:
- `./data/langflow`: Contains Langflow data (flows, settings, etc.)
- `./data/postgres`: Contains PostgreSQL database files

### Backing Up Data

To backup your flows and settings:
```bash
# Stop containers first
docker compose down

# Backup the data directory
cp -r ./data /path/to/backup/location

# Restart containers
docker compose up -d
```

## Environment Configuration

### Configuring through the .env File

Edit the `.env` file to customize:
- Port settings
- Database credentials
- API keys

Changes require restarting containers:
```bash
docker compose restart
```

### Setting API Keys

For components that require API keys (like OpenAI):
1. Add your key to the `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
2. Uncomment the corresponding line in `docker-compose.yml`
3. Restart containers:
   ```bash
   docker compose restart
   ```

## Troubleshooting

### Common Issues and Solutions

1. **Components not loading**:
   - Check logs: `docker compose logs -f langflow_app`
   - Restart containers: `docker compose restart`

2. **Flow execution errors**:
   - Verify component connections
   - Check API keys are correctly set
   - Confirm component parameters are valid

3. **Database connection issues**:
   - Check database container: `docker compose ps`
   - View database logs: `docker compose logs db`

4. **Custom components not appearing**:
   - Verify file location in `custom_components` directory
   - Check file format and syntax
   - View logs for errors: `docker compose logs langflow_app`

5. **Data persistence issues**:
   - Check permissions: `docker compose run --rm init-volumes`
   - Verify volume mounts: `docker inspect langflow_app | grep Mounts -A 20` 