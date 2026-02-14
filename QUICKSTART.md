# Quick Start Guide

Welcome! This guide will help you quickly add this local project to your Home Assistant installation.

## TL;DR

```bash
# 1. Clone the repository
git clone https://github.com/mariartcom/ha-tickets-event.git

# 2. Copy to Home Assistant
cp -r ha-tickets-event/custom_components/tickets_event /config/custom_components/

# 3. Restart Home Assistant

# 4. Use in automations
service: tickets_event.fire_event
data:
  ticket_id: "MY-TICKET-001"
  type: "new"
  description: "Something happened"
  priority: "high"
```

## What Does This Integration Do?

This integration adds a **service** to Home Assistant that lets you fire custom ticket events. These events can trigger automations, send notifications, or integrate with external ticketing systems.

## 5-Minute Setup

### Step 1: Get the Files

**Option A - Using Git:**
```bash
cd ~
git clone https://github.com/mariartcom/ha-tickets-event.git
```

**Option B - Download:**
Download the ZIP from GitHub and extract it.

### Step 2: Install to Home Assistant

Copy the integration to your Home Assistant:

```bash
# Find your Home Assistant config directory (usually /config or ~/.homeassistant)
cd /config  # or wherever your HA config is

# Create custom_components if it doesn't exist
mkdir -p custom_components

# Copy the integration
cp -r ~/ha-tickets-event/custom_components/tickets_event custom_components/
```

Your structure should look like:
```
/config/
├── custom_components/
│   └── tickets_event/    ← This folder
│       ├── __init__.py
│       ├── manifest.json
│       └── services.yaml
└── configuration.yaml
```

### Step 3: Restart

Restart Home Assistant:
- UI: Settings → System → Restart
- CLI: `ha core restart`

### Step 4: Test It!

1. Go to **Developer Tools → Services**
2. Find `tickets_event.fire_event`
3. Try this:

```yaml
service: tickets_event.fire_event
data:
  ticket_id: "TEST-001"
  type: "new"
  description: "My first ticket"
  priority: "normal"
```

4. Click "Call Service" ✓

## First Automation

Create your first ticket automation:

```yaml
# In configuration.yaml or automations.yaml
automation:
  - alias: "Button Creates Ticket"
    trigger:
      - platform: state
        entity_id: input_button.help_button
    action:
      - service: tickets_event.fire_event
        data:
          ticket_id: "{{ now().strftime('%Y%m%d-%H%M%S') }}"
          type: "new"
          description: "Help button pressed"
          priority: "high"
      - service: notify.mobile_app
        data:
          message: "Ticket created!"

  - alias: "React to High Priority Tickets"
    trigger:
      - platform: event
        event_type: tickets_event_event
        event_data:
          priority: "high"
    action:
      - service: notify.mobile_app
        data:
          title: "Urgent Ticket!"
          message: "Ticket {{ trigger.event.data.ticket_id }}: {{ trigger.event.data.description }}"
```

## Troubleshooting

**Service doesn't appear:**
- Check logs: Settings → System → Logs
- Verify files are in the right place
- Restart again

**Import errors:**
- Make sure all three files are present
- Check file permissions

## Next Steps

- 📖 Read [README.md](README.md) for detailed documentation
- 📝 Check [INSTALLATION.md](INSTALLATION.md) for troubleshooting
- 💡 See [example_configuration.yaml](example_configuration.yaml) for more ideas

## Get Help

- Issues: https://github.com/mariartcom/ha-tickets-event/issues
- Discussions: Home Assistant Community Forums

---

**That's it!** You now have a working ticket event system in Home Assistant. 🎉
