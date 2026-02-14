# HA Tickets & Events Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)](https://www.home-assistant.io/)

A Home Assistant integration that provides event and attraction listings with ticket booking capabilities. Browse events, search attractions, and generate booking links or QR codes for easy ticket purchases.

## Features

- 🎫 **Event Listings**: Display events and attractions from cities worldwide
- 🔍 **Smart Search**: Search for events by name or category
- 📅 **Calendar Views**: Filter events by date ranges (today, this week, this month, etc.)
- 📍 **Location-Based**: Automatic location detection or manual city selection
- 💰 **Multi-Currency**: Support for EUR, USD, GBP, and more
- 📱 **QR Codes**: Generate QR codes for TV/dashboard displays
- 🌍 **Multi-Language**: Support for multiple languages
- ⚡ **Rate Limited**: Respects API limits (20 calls/minute)

## Screenshots

*Coming soon - screenshots of event cards, QR codes, and search interface*

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/mariartcom/ha-tickets-event`
6. Select category: "Integration"
7. Click "Add"
8. Find "Tickets & Events" in the integration list
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/mariartcom/ha-tickets-event/releases)
2. Extract the `tickets_events` folder from the archive
3. Copy the folder to your `custom_components` directory:
   ```
   config/
   └── custom_components/
       └── tickets_events/
           ├── __init__.py
           ├── manifest.json
           ├── config_flow.py
           └── ...
   ```
4. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Tickets & Events**
4. Follow the configuration steps:
   - Select your city or let the integration detect it
   - Choose your preferred currency
   - Set default search radius (optional)

### Options

You can reconfigure the integration at any time:
- Change city
- Update currency preference
- Adjust update frequency

## Entities

### Sensors

The integration creates the following sensors:

| Sensor | Description | Update Frequency |
|--------|-------------|------------------|
| `sensor.tickets_events_today` | Events happening today | Once per day |
| `sensor.tickets_events_nearby` | Events in your city | Once per day |
| `sensor.tickets_events_calendar` | Date-filtered events | On-demand |
| `sensor.tickets_events_search` | Search results | On-demand |

### Sensor Attributes

Each sensor provides rich attributes:

```yaml
state: 15  # Number of events
attributes:
  events:
    - id: 976227
      title: "Palace of the Parliament Tour"
      description: "Guided tour..."
      city: "Bucharest"
      price: 32.90
      currency: "EUR"
      rating: 4.3
      rating_count: 651
      images:
        - url: "https://..."
          alt: "Palace exterior"
      booking_url: "https://..."
      qr_code_data: "base64..."
  destination_title: "Bucharest"
  last_updated: "2026-02-14T10:00:00Z"
  currency: "EUR"
```

## Services

### Search Events

Search for events by query:

```yaml
service: tickets_events.search_events
data:
  query: "museum"
  currency: "EUR"
```

### Get Events by Date

Retrieve events within a date range:

```yaml
service: tickets_events.get_events_by_date
data:
  date_from: "2026-02-14"
  date_to: "2026-02-21"
  currency: "EUR"
```

### Generate Booking URL

Create a customized booking URL:

```yaml
service: tickets_events.generate_booking_url
data:
  event_id: 976227
  date: "2026-02-14"
  timeslot: "09:00"
  tickets:
    adult: 2
    child: 1
  language: "eng"
  currency: "EUR"
```

### Refresh Events

Manually refresh event data:

```yaml
service: tickets_events.refresh_events
data:
  sensor: "today"  # or "nearby", "calendar"
```

## Lovelace Examples

### Basic Event Card

```yaml
type: entities
title: Today's Events
entities:
  - sensor.tickets_events_today
card_mod:
  style: |
    /* Custom styling */
```

### Event List with Images

```yaml
type: custom:auto-entities
card:
  type: grid
  columns: 2
filter:
  template: |
    {% for event in state_attr('sensor.tickets_events_today', 'events') %}
      {{
        {
          'type': 'picture',
          'image': event.images[0].url,
          'title': event.title,
          'tap_action': {
            'action': 'url',
            'url_path': event.booking_url
          }
        }
      }},
    {% endfor %}
```

### QR Code Display (for TV)

```yaml
type: markdown
content: |
  ## {{ state_attr('sensor.tickets_events_today', 'events')[0].title }}
  
  ![QR Code]({{ state_attr('sensor.tickets_events_today', 'events')[0].qr_code_data }})
  
  **Price**: {{ state_attr('sensor.tickets_events_today', 'events')[0].price }} {{ state_attr('sensor.tickets_events_today', 'events')[0].currency }}
```

### Search Interface

```yaml
type: vertical-stack
cards:
  - type: custom:button-card
    name: Search Events
    tap_action:
      action: call-service
      service: tickets_events.search_events
      service_data:
        query: "museum"
  
  - type: entities
    entities:
      - sensor.tickets_events_search
```

## Automations

### Daily Event Notification

```yaml
automation:
  - alias: "Daily Event Digest"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.tickets_events_today
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "Events Today"
          message: >
            {{ state_attr('sensor.tickets_events_today', 'events') | length }} 
            events happening in {{ state_attr('sensor.tickets_events_today', 'destination_title') }} today!
```

### Price Alert

```yaml
automation:
  - alias: "Low Price Event Alert"
    trigger:
      - platform: state
        entity_id: sensor.tickets_events_today
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.tickets_events_today', 'events') 
             | selectattr('price', 'lt', 20) 
             | list | length > 0 }}
    action:
      - service: persistent_notification.create
        data:
          title: "Affordable Events Found!"
          message: "Check out events under €20 today"
```

## Troubleshooting

### Integration Not Loading

1. Check Home Assistant logs: **Settings** → **System** → **Logs**
2. Ensure all files are in `custom_components/tickets_events/`
3. Restart Home Assistant
4. Clear browser cache

### No Events Showing

1. Verify your city is configured correctly
2. Check API rate limits (max 20 calls/minute)
3. Enable debug logging:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.tickets_events: debug
   ```
4. Check if n8n backend is reachable at `https://bff.mangocity.md/events`

### Rate Limit Errors

- The integration respects a 20 calls/minute limit
- Automatic retry after rate limit reset
- Consider increasing update interval if hitting limits frequently

### Location Detection Issues

- Ensure Home Assistant can make external HTTP requests
- Manually select a city in integration options
- Check firewall/network settings

## Debug Logging

Enable detailed logging for troubleshooting:

```yaml
logger:
  default: warning
  logs:
    custom_components.tickets_events: debug
    custom_components.tickets_events.config_flow: debug
    custom_components.tickets_events.coordinator: debug
```

## API Rate Limits

- **Maximum**: 20 API calls per minute
- **Default Update**: Once per day
- **Manual Refresh**: Available via service calls
- **Retry Logic**: Automatic retry with exponential backoff

## Data Privacy

- Location data is only used for event discovery
- No personal data is stored or transmitted
- All API calls use HTTPS
- IP-based location is optional

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/mariartcom/ha-tickets-event/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mariartcom/ha-tickets-event/discussions)
- **Documentation**: [Wiki](https://github.com/mariartcom/ha-tickets-event/wiki)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for Home Assistant
- Uses TravelPayouts affiliate network
- Powered by Tiqets attraction data
- Backend by n8n workflows

## Roadmap

- [ ] v1.0: Core features with QR codes and search
- [ ] v1.1: Custom Lovelace cards
- [ ] v1.2: Calendar entity integration
- [ ] v1.3: Multi-city support
- [ ] v2.0: Voice assistant integration

---

**Made with ❤️ for the Home Assistant community**
