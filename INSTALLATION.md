# Installation Guide

This guide provides detailed instructions for adding this local project to your Home Assistant installation.

## Prerequisites

- Home Assistant installed and running (version 2023.1.0 or later recommended)
- Access to your Home Assistant configuration directory
- Basic knowledge of YAML and Home Assistant configuration

## Step-by-Step Installation

### Step 1: Locate Your Home Assistant Configuration Directory

Your Home Assistant configuration directory is typically located at:

- **Home Assistant OS / Supervised**: `/config`
- **Docker**: Usually mounted at `/config` inside the container
- **Core (venv)**: `~/.homeassistant/` or where you installed it
- **Windows**: `%APPDATA%\.homeassistant\`

You can verify the location by checking **Settings > System > Repairs** in the Home Assistant UI, or by looking at the logs.

### Step 2: Download or Clone This Repository

**Option A: Using Git**
```bash
git clone https://github.com/mariartcom/ha-tickets-event.git
cd ha-tickets-event
```

**Option B: Download ZIP**
1. Go to https://github.com/mariartcom/ha-tickets-event
2. Click "Code" > "Download ZIP"
3. Extract the ZIP file to a temporary location

### Step 3: Copy the Custom Component

1. Navigate to your Home Assistant configuration directory
2. Create a `custom_components` directory if it doesn't exist:
   ```bash
   mkdir -p custom_components
   ```
3. Copy the `tickets_event` folder:
   ```bash
   cp -r /path/to/ha-tickets-event/custom_components/tickets_event custom_components/
   ```

Your directory structure should look like:
```
/config/
├── custom_components/
│   └── tickets_event/
│       ├── __init__.py
│       ├── manifest.json
│       └── services.yaml
├── configuration.yaml
└── ... (other Home Assistant files)
```

### Step 4: Restart Home Assistant

Restart Home Assistant to load the new integration:

- **UI Method**: Go to **Settings > System > Restart**
- **CLI Method**: Run `ha core restart` (if using Home Assistant CLI)
- **Docker**: Restart the container

### Step 5: Verify Installation

1. Go to **Developer Tools > Services**
2. Look for `tickets_event.fire_event` in the service list
3. If you see it, the installation was successful!

## Testing the Integration

### Test 1: Fire a Test Event

1. Go to **Developer Tools > Services**
2. Select `tickets_event.fire_event`
3. Enter the following YAML:
   ```yaml
   service: tickets_event.fire_event
   data:
     type: "new"
     ticket_id: "TEST-001"
     description: "This is a test ticket"
     priority: "normal"
   ```
4. Click "Call Service"

### Test 2: Listen for the Event

1. Go to **Developer Tools > Events**
2. In the "Listen to events" section, enter: `tickets_event_event`
3. Click "Start Listening"
4. Fire a test event using the steps above
5. You should see the event data appear in the events panel

## Troubleshooting

### Integration Not Showing Up

1. **Check the logs**: Go to **Settings > System > Logs** and look for errors related to `tickets_event`
2. **Verify file permissions**: Ensure the files are readable by the Home Assistant user
3. **Check directory structure**: Make sure the files are in `custom_components/tickets_event/`

### Common Errors

**"Integration 'tickets_event' not found"**
- The custom component folder is not in the correct location
- Try restarting Home Assistant again

**"Failed to import component"**
- Check for syntax errors in the Python files
- Ensure all required files are present (`__init__.py`, `manifest.json`, `services.yaml`)

**"Version not specified in manifest"**
- This shouldn't happen with the provided files, but ensure `manifest.json` contains a `version` field

## Updating the Integration

To update to a newer version:

1. Download or pull the latest version from the repository
2. Replace the files in `custom_components/tickets_event/`
3. Restart Home Assistant

## Uninstalling

To remove the integration:

1. Delete the `custom_components/tickets_event/` directory
2. Restart Home Assistant
3. Remove any automations or scripts that use the integration

## Next Steps

- Read the [README.md](README.md) for usage examples
- Check [example_configuration.yaml](example_configuration.yaml) for automation ideas
- Create your own automations using the `tickets_event.fire_event` service

## Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/mariartcom/ha-tickets-event/issues)
2. Review the Home Assistant logs
3. Ask for help in the Home Assistant community forums
