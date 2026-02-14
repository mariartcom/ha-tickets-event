# Development Setup Guide

## Prerequisites

- Python 3.11 or higher
- Home Assistant 2024.1 or higher
- Git
- (Optional) Visual Studio Code with Home Assistant extension

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/quoda-team/ha-tickets-event.git
cd ha-tickets-event
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -r requirements_dev.txt
```

Create `requirements_dev.txt`:
```
homeassistant>=2024.1.0
pytest>=7.0.0
pytest-homeassistant-custom-component
black
pylint
mypy
```

### 4. Link to Home Assistant

Create a symbolic link from your Home Assistant custom_components directory:

```bash
# macOS/Linux
ln -s $(pwd)/custom_components/tickets_events ~/.homeassistant/custom_components/tickets_events

# Windows (run as Administrator)
mklink /D "%APPDATA%\.homeassistant\custom_components\tickets_events" "%CD%\custom_components\tickets_events"
```

### 5. Configure Mock API (Development)

For development without n8n backend, use the mock API responses:

Edit `custom_components/tickets_events/api.py` and add development mode:

```python
DEVELOPMENT_MODE = True  # Set to False for production

if DEVELOPMENT_MODE:
    # Return mock data from tests/fixtures/
    pass
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=custom_components.tickets_events

# Run specific test file
pytest tests/test_config_flow.py

# Run with verbose output
pytest -v
```

## Code Quality

### Format Code

```bash
black custom_components/tickets_events/
```

### Lint Code

```bash
pylint custom_components/tickets_events/
```

### Type Checking

```bash
mypy custom_components/tickets_events/
```

## Debugging

### Enable Debug Logging

Add to your Home Assistant `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.tickets_events: debug
```

### VS Code Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Home Assistant",
      "type": "python",
      "request": "launch",
      "module": "homeassistant",
      "justMyCode": false,
      "args": [
        "-c",
        "config",
        "--debug"
      ]
    }
  ]
}
```

## Testing with Home Assistant

### 1. Start Home Assistant

```bash
hass -c config
```

### 2. Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Tickets & Events**
4. Follow configuration steps

### 3. Check Logs

```bash
tail -f ~/.homeassistant/home-assistant.log | grep tickets_events
```

## Mock API Server (Optional)

For local testing, create a simple Flask server to mock the n8n API:

```python
# mock_server.py
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open('tests/fixtures/mock_api_responses.json') as f:
    mock_data = json.load(f)

@app.route('/events/city/<city_id>')
def get_events(city_id):
    return jsonify(mock_data['events_bucharest'])

@app.route('/cities')
def get_cities():
    return jsonify(mock_data['cities_list'])

if __name__ == '__main__':
    app.run(port=8000)
```

Update `const.py`:
```python
API_BASE_URL = "http://localhost:8000"
```

## Common Issues

### Import Errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Integration Not Loading

1. Check Home Assistant logs
2. Verify all files are present
3. Restart Home Assistant
4. Clear browser cache

### Rate Limiting During Development

Increase the rate limit in `const.py` for development:
```python
API_RATE_LIMIT = 60  # Higher limit for development
```

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes
3. Run tests: `pytest`
4. Format code: `black .`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create pull request

## Release Process

1. Update version in `manifest.json`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release
6. HACS will automatically detect the new version

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [HACS Documentation](https://hacs.xyz/docs/publish/start)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
