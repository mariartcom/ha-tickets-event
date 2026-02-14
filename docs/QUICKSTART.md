# Quick Start Guide

## Installation

### Method 1: HACS (Recommended)

1. **Open HACS**
   - In Home Assistant, navigate to **HACS** in the sidebar
   - If you don't have HACS, install it from [hacs.xyz](https://hacs.xyz)

2. **Add Custom Repository**
   - Click the three dots (⋮) in the top right
   - Select **Custom repositories**
   - Enter URL: `https://github.com/quoda-team/ha-tickets-event`
   - Category: **Integration**
   - Click **Add**

3. **Install Integration**
   - Search for "Tickets & Events"
   - Click **Download**
   - Restart Home Assistant

### Method 2: Manual Installation

1. **Download**
   ```bash
   cd /config/custom_components
   git clone https://github.com/quoda-team/ha-tickets-event.git tickets_events
   ```

2. **Restart Home Assistant**

## Configuration

### Initial Setup

1. **Add Integration**
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for "Tickets & Events"

2. **Choose City**
   - Select "Auto-detect from IP" or choose a specific city
   - The integration will detect your location if you choose auto-detect

3. **Select Currency**
   - Choose your preferred currency (EUR, USD, GBP, etc.)

4. **Complete Setup**
   - Click **Submit**
   - Your integration is now configured!

## Basic Usage

### View Events

After setup, you'll have two sensors:
- `sensor.tickets_events_today` - Events happening today
- `sensor.tickets_events_nearby` - All events in your city

### Check Events in UI

1. **Developer Tools**
   - Go to **Developer Tools** → **States**
   - Find `sensor.tickets_events_today`
   - Click to view all event attributes

2. **Entity Card**
   ```yaml
   type: entities
   entities:
     - sensor.tickets_events_today
     - sensor.tickets_events_nearby
   ```

### Search for Events

1. **Developer Tools** → **Services**
2. Select `tickets_events.search_events`
3. Enter service data:
   ```yaml
   query: "museum"
   currency: "EUR"
   ```
4. Click **Call Service**

## First Dashboard

### Simple Event List

1. **Edit Dashboard**
2. **Add Card** → **Markdown**
3. Paste this code:

```yaml
type: markdown
content: |
  # Events in {{ state_attr('sensor.tickets_events_today', 'destination_title') }}
  
  Found **{{ states('sensor.tickets_events_today') }} events**
  
  {% for event in state_attr('sensor.tickets_events_today', 'events')[:3] %}
  ## {{ event.title }}
  
  **{{ event.price }} {{ event.currency }}** | ⭐ {{ event.rating }}
  
  {{ event.description }}
  
  [Book Now]({{ event.booking_url_with_params }})
  
  ---
  {% endfor %}
```

### Event with QR Code (for TV)

```yaml
type: markdown
content: |
  # {{ state_attr('sensor.tickets_events_today', 'events')[0].title }}
  
  ![QR Code]({{ state_attr('sensor.tickets_events_today', 'events')[0].qr_code_data }})
  
  **Price**: {{ state_attr('sensor.tickets_events_today', 'events')[0].price }} {{ state_attr('sensor.tickets_events_today', 'events')[0].currency }}
  
  **Scan the QR code with your phone to book tickets**
```

## Common Tasks

### Change City

1. **Settings** → **Devices & Services**
2. Find "Tickets & Events"
3. Click **Configure**
4. Select new city
5. Click **Submit**

### Manual Refresh

**Via Developer Tools:**
```yaml
service: tickets_events.refresh_events
data: {}
```

**Via Automation:**
```yaml
service: tickets_events.refresh_events
```

### Get Events by Date Range

```yaml
service: tickets_events.get_events_by_date
data:
  date_from: "2026-02-14"
  date_to: "2026-02-21"
  currency: "EUR"
```

## Automation Examples

### Morning Event Notification

```yaml
automation:
  - alias: "Morning Event Digest"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.tickets_events_today
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "Good Morning!"
          message: >
            {{ states('sensor.tickets_events_today') }} events 
            happening in {{ state_attr('sensor.tickets_events_today', 'destination_title') }} today
```

### Weekend Event Alert

```yaml
automation:
  - alias: "Weekend Events"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: time
        weekday:
          - fri
    action:
      - service: persistent_notification.create
        data:
          title: "Weekend Events"
          message: "Check out events for the weekend!"
```

## Troubleshooting

### No Events Showing

1. **Check sensor state**:
   - Go to **Developer Tools** → **States**
   - Look for `sensor.tickets_events_today`
   - If state is 0, no events are available

2. **Check city configuration**:
   - Make sure city is correctly selected
   - Try changing to a different city

3. **Enable debug logging**:
   ```yaml
   logger:
     logs:
       custom_components.tickets_events: debug
   ```

### Integration Not Loading

1. **Check logs**:
   - **Settings** → **System** → **Logs**
   - Look for errors mentioning `tickets_events`

2. **Verify files**:
   ```bash
   ls -la config/custom_components/tickets_events/
   ```
   
3. **Restart Home Assistant**:
   - **Settings** → **System** → **Restart**

### API Errors

1. **Rate limit**: Wait a few minutes and try again
2. **Connection error**: Check your internet connection
3. **City not found**: Select a different city from the list

## Next Steps

1. **Explore Services**: Try different services in Developer Tools
2. **Create Dashboard**: Use the Lovelace examples in `docs/LOVELACE_EXAMPLES.md`
3. **Build Automations**: Set up notifications and alerts
4. **Customize**: Adjust update frequency and preferences

## Get Help

- **Issues**: [GitHub Issues](https://github.com/quoda-team/ha-tickets-event/issues)
- **Discussions**: [GitHub Discussions](https://github.com/quoda-team/ha-tickets-event/discussions)
- **Documentation**: [Full Documentation](https://github.com/quoda-team/ha-tickets-event/wiki)

## Tips

- Events update once per day automatically
- Use manual refresh for immediate updates
- QR codes are generated automatically for each event
- Search works across all cities, not just your configured one
- Currency can be changed without reconfiguring the integration

---

**Enjoy discovering events and attractions with Home Assistant! 🎫✨**
