# Private Relay API

A privacy-focused API relay service that processes complex queries using OpenAI GPT models and Google Natural Language API for entity recognition, while maintaining user privacy through request obfuscation.

## Features

- Complex query processing using GPT-4o mini
- Entity extraction using Google Natural Language API
- Privacy-preserving request handling
- Future support for vision queries (planned)

## Requirements

- Python 3.11+
- FastAPI
- OpenAI Python Client
- Google Cloud Natural Language API
- python-dotenv
- uvicorn

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd private-relay
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-api-key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
GPT_SYSTEM_PROMPT="You are an AI assistant integrated into a wearable device. Your role is to:\
1. Provide concise, accurate responses that minimize cognitive load\
2. Focus on relevant information based on the user's context\
3. Maintain privacy by not requesting or storing personal information\
4. Process queries efficiently using appropriate models\
5. Provide natural, conversational responses while maintaining accuracy"
```

## Running the API

Start the server:
```bash
python -m external.api
```

The server will run on `http://0.0.0.0:80`

## Example Usage

With the server running in one terminal:

```bash
curl -X POST "http://localhost:80/api/query?type=complex&query=Compare%20the%20weather%20in%20San%20Francisco%20and%20New%20York"
```

Sample Response:
```json
{
    "entities": "New York (LOCATION), San Francisco (LOCATION), weather (OTHER)",
    "result": "San Francisco typically has a mild, Mediterranean climate with cool, foggy summers and wet winters. Average temperatures range from 50°F to 70°F (10°C to 21°C).\n\nNew York experiences a humid continental climate, with hot summers and cold winters. Average temperatures can range from 30°F to 85°F (-1°C to 29°C) depending on the season.\n\nFor current weather conditions, please check a reliable weather service."
}
```

## API Endpoints

### POST /api/query
Processes complex queries with optional entity recognition.

**Parameters:**
- `type` (string): Query type. Currently supports:
  - `complex`: For queries requiring advanced processing
  - `vision`: Planned for future implementation
- `query` (string): The actual query text

## Error Handling

The API returns appropriate HTTP status codes:
- 400: Invalid query type (only 'complex' and 'vision' supported)
- 500: Internal server error
- 501: Vision queries (not yet implemented)

## Development

### Common Issues and Solutions

1. **OpenAI API Key Issues**
   - Ensure your `.env` file contains a valid API key
   - Check that the key begins with "sk-"
   - Verify the key has the necessary permissions

2. **Google Cloud Credentials**
   - Verify the credentials file path in `.env` is correct
   - Ensure the service account has required API permissions
   - Check that Natural Language API is enabled in your Google Cloud project

3. **Import Errors**
   - Always run the application from the project root
   - Use `python -m` syntax to ensure correct module resolution
   - Verify all dependencies are installed in your virtual environment

4. **No Entities Detected**
   - Some queries may naturally return no entities
   - Verify Google Natural Language API is properly configured
   - Try queries with clearly named entities (locations, organizations, etc.)

## Future Enhancements

- Vision query support using Google Cloud Vision
- Additional query types and processing capabilities
- Enhanced privacy features
- Advanced entity recognition and contextual understanding
- Integration with additional AI models for specialized tasks