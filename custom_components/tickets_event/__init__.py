"""The Tickets Event integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tickets_event"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Tickets Event component."""
    _LOGGER.info("Setting up Tickets Event integration")

    async def handle_ticket_event(call):
        """Handle the ticket event service call."""
        event_type = call.data.get("type", "new")
        ticket_id = call.data.get("ticket_id")
        description = call.data.get("description", "")
        priority = call.data.get("priority", "normal")

        event_data = {
            "type": event_type,
            "ticket_id": ticket_id,
            "description": description,
            "priority": priority,
        }

        _LOGGER.info("Firing ticket event: %s", event_data)
        hass.bus.async_fire(f"{DOMAIN}_event", event_data)

    # Register the service
    hass.services.async_register(DOMAIN, "fire_event", handle_ticket_event)

    return True
