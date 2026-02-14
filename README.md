# Home Assistant Tickets Event Integration

A custom integration for Home Assistant that allows you to fire and handle ticket events in your automations. This integration provides a service to trigger custom events that can be used to integrate with ticketing systems, notifications, and automations.

## Features

- Fire custom ticket events from automations or scripts
- Support for different event types (new, updated, closed, etc.)
- Configurable priority levels
- Easy integration with Home Assistant's automation system

## Installation

### Method 1: Manual Installation (Recommended for Local Development)

1. **Clone or download this repository** to your local machine:
   ```bash
   git clone https://github.com/mariartcom/ha-tickets-event.git
   ```

2. **Copy the custom component to your Home Assistant configuration directory:**
   ```bash
   # Navigate to your Home Assistant config directory
   cd /path/to/your/homeassistant/config
   
   # Create the custom_components directory if it doesn't exist
   mkdir -p custom_components
   
   # Copy the tickets_event integration
   cp -r /path/to/ha-tickets-event/custom_components/tickets_event custom_components/
   ```

3. **Restart Home Assistant** to load the new integration.

### Method 2: Using HACS (Home Assistant Community Store)

> **Note:** This integration is not yet available in HACS. Use Manual Installation for now.

### Method 3: Direct Copy

If you're developing locally, you can directly create a symbolic link:

```bash
# From your Home Assistant config directory
ln -s /path/to/ha-tickets-event/custom_components/tickets_event custom_components/tickets_event
```

## Configuration

This integration does not require any configuration in `configuration.yaml`. Once installed, the `tickets_event.fire_event` service will be automatically available.

## Usage

### Firing a Ticket Event

You can use the `tickets_event.fire_event` service in your automations or scripts:

```yaml
service: tickets_event.fire_event
data:
  type: "new"
  ticket_id: "TICKET-123"
  description: "New support request received"
  priority: "high"
```

### Example Automation

Here's an example automation that fires a ticket event and then sends a notification:

```yaml
automation:
  - alias: "Create Ticket on Button Press"
    trigger:
      - platform: state
        entity_id: input_button.create_ticket
    action:
      - service: tickets_event.fire_event
        data:
          type: "new"
          ticket_id: "{{ now().strftime('%Y%m%d%H%M%S') }}"
          description: "Manual ticket created via button"
          priority: "normal"
      - service: notify.mobile_app
        data:
          message: "Ticket created!"

  - alias: "Handle Ticket Event"
    trigger:
      - platform: event
        event_type: tickets_event_event
        event_data:
          priority: "high"
    action:
      - service: notify.mobile_app
        data:
          message: "High priority ticket: {{ trigger.event.data.ticket_id }}"
          title: "Urgent Ticket Alert"
```

## Service Parameters

### `tickets_event.fire_event`

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `type` | No | `"new"` | The type of ticket event (e.g., new, updated, closed) |
| `ticket_id` | Yes | - | The unique identifier for the ticket |
| `description` | No | `""` | A description of the ticket or event |
| `priority` | No | `"normal"` | Priority level: low, normal, high, or critical |

## Event Data

When a ticket event is fired, it triggers a `tickets_event_event` event with the following data:

```json
{
  "type": "new",
  "ticket_id": "TICKET-123",
  "description": "New support request received",
  "priority": "high"
}
```

You can listen to this event in your automations using the `event` platform.

## Development

### Project Structure

```
ha-tickets-event/
├── custom_components/
│   └── tickets_event/
│       ├── __init__.py       # Main integration code
│       ├── manifest.json     # Integration metadata
│       └── services.yaml     # Service definitions
└── README.md                 # This file
```

### Testing Locally

1. Set up a Home Assistant development environment
2. Copy or link this integration to your `custom_components` directory
3. Restart Home Assistant
4. Use Developer Tools > Services to test the `tickets_event.fire_event` service
5. Use Developer Tools > Events to listen for `tickets_event_event` events

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source. Please check the repository for license details.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/mariartcom/ha-tickets-event).