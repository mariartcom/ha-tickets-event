"""Sensor platform for Tickets & Events integration."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_DESTINATION_TITLE,
    ATTR_DESTINATION_URL,
    ATTR_EVENTS,
    ATTR_LAST_UPDATED,
    ATTR_LOCATION_TYPE,
    CONF_CURRENCY,
    DEFAULT_MAX_EVENTS,
    DOMAIN,
    SENSOR_NEARBY,
    SENSOR_TODAY,
)
from .coordinator import TicketsEventsDataUpdateCoordinator
from .helpers import process_event_data

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tickets & Events sensors."""
    coordinator: TicketsEventsDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create sensors
    sensors = [
        TicketsEventsTodaySensor(coordinator, entry),
        TicketsEventsNearbySensor(coordinator, entry),
    ]

    async_add_entities(sensors)


class TicketsEventsBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Tickets & Events sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TicketsEventsDataUpdateCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self.sensor_type = sensor_type
        
        # Entity IDs
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_translation_key = sensor_type

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return 0
        
        events = self._get_events()
        return len(events)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        events_data = self.coordinator.data.get("events", {})
        events = self._get_events()
        
        # Process events to add QR codes and full booking URLs
        processed_events = [
            process_event_data(event, self.coordinator.currency)
            for event in events[:DEFAULT_MAX_EVENTS]
        ]

        return {
            ATTR_EVENTS: processed_events,
            ATTR_DESTINATION_TITLE: events_data.get("destinationTitle", ""),
            ATTR_DESTINATION_URL: events_data.get("destinationUrl", ""),
            ATTR_LOCATION_TYPE: events_data.get("locationType", "city"),
            ATTR_LAST_UPDATED: datetime.now().isoformat(),
            CONF_CURRENCY: self.coordinator.currency,
        }

    def _get_events(self) -> list[dict[str, Any]]:
        """Get events list from coordinator data."""
        if not self.coordinator.data:
            return []
        
        events_data = self.coordinator.data.get("events", {})
        return events_data.get("offeringCards", [])


class TicketsEventsTodaySensor(TicketsEventsBaseSensor):
    """Sensor for today's events."""

    _attr_icon = "mdi:calendar-today"

    def __init__(
        self,
        coordinator: TicketsEventsDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the today events sensor."""
        super().__init__(coordinator, entry, SENSOR_TODAY)
        self._attr_name = "Today Events"

    def _get_events(self) -> list[dict[str, Any]]:
        """Get today's events."""
        # For now, return all events
        # In a real implementation, you'd filter by today's date
        return super()._get_events()


class TicketsEventsNearbySensor(TicketsEventsBaseSensor):
    """Sensor for nearby events."""

    _attr_icon = "mdi:map-marker-radius"

    def __init__(
        self,
        coordinator: TicketsEventsDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the nearby events sensor."""
        super().__init__(coordinator, entry, SENSOR_NEARBY)
        self._attr_name = "Nearby Events"

    def _get_events(self) -> list[dict[str, Any]]:
        """Get nearby events."""
        # Return all events from the configured city
        return super()._get_events()
