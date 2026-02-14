"""Calendar platform for Tickets & Events integration."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_EVENTS,
    DOMAIN,
)
from .coordinator import TicketsEventsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tickets & Events calendar."""
    coordinator: TicketsEventsDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create calendar entity
    async_add_entities([TicketsEventsCalendar(coordinator, entry)])


class TicketsEventsCalendar(CoordinatorEntity, CalendarEntity):
    """Calendar entity for Tickets & Events."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TicketsEventsDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the calendar."""
        super().__init__(coordinator)
        self.entry = entry
        
        # Entity IDs
        self._attr_unique_id = f"{entry.entry_id}_calendar"
        self._attr_name = "Events Calendar"
        self._attr_icon = "mdi:calendar-star"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        events = self._get_calendar_events()
        
        if not events:
            return None
        
        # Return the first upcoming event
        now = dt_util.now()
        upcoming = [e for e in events if e.start >= now]
        
        if upcoming:
            return upcoming[0]
        
        # If no upcoming events, return the first event
        return events[0] if events else None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Get events in a specific date range."""
        _LOGGER.debug(
            "Getting calendar events from %s to %s",
            start_date.isoformat(),
            end_date.isoformat()
        )
        
        events = self._get_calendar_events()
        
        # Filter events within the requested date range
        filtered_events = [
            event for event in events
            if event.start < end_date and event.end > start_date
        ]
        
        _LOGGER.debug("Returning %d calendar events", len(filtered_events))
        return filtered_events

    def _get_calendar_events(self) -> list[CalendarEvent]:
        """Convert events to calendar events."""
        if not self.coordinator.data:
            return []

        events_data = self.coordinator.data.get("events", {})
        events = events_data.get("events", [])
        
        calendar_events = []
        now = dt_util.now()
        
        for event in events:
            # Get event date or use available dates
            event_date = event.get("date")
            available_dates = event.get("available_dates", [])
            
            # If no specific date, use available dates or default to today
            dates_to_process = []
            if event_date:
                dates_to_process = [event_date]
            elif available_dates:
                dates_to_process = available_dates
            else:
                # Default to today
                dates_to_process = [now.date().isoformat()]
            
            # Create a calendar event for each available date
            for date_str in dates_to_process:
                try:
                    # Parse the date
                    event_date_obj = datetime.fromisoformat(date_str)
                    
                    # Set event time (default to 10:00 AM - 6:00 PM for all-day events)
                    start_time = event_date_obj.replace(hour=10, minute=0, second=0, microsecond=0)
                    # Make timezone aware
                    start_time = dt_util.as_local(start_time)
                    
                    # End time (8 hours later for tours/activities)
                    end_time = start_time + timedelta(hours=8)
                    
                    # Create calendar event
                    calendar_event = CalendarEvent(
                        start=start_time,
                        end=end_time,
                        summary=event.get("title", "Event"),
                        description=self._format_description(event),
                        location=f"{event.get('city', '')}, {event.get('country', '')}".strip(", "),
                        uid=f"{event.get('id')}_{date_str}",
                    )
                    
                    calendar_events.append(calendar_event)
                    
                except (ValueError, TypeError) as err:
                    _LOGGER.warning("Error parsing date %s for event %s: %s", date_str, event.get("id"), err)
                    continue
        
        # Sort by start date
        calendar_events.sort(key=lambda x: x.start)
        
        return calendar_events

    def _format_description(self, event: dict[str, Any]) -> str:
        """Format event description for calendar."""
        description_parts = []
        
        # Add main description
        if desc := event.get("description"):
            description_parts.append(desc)
        
        # Add price
        price = event.get("price", 0)
        currency = event.get("currency", "EUR")
        if price > 0:
            description_parts.append(f"\n💰 Price: {price:.2f} {currency}")
        else:
            description_parts.append("\n💰 Free Entry")
        
        # Add rating
        if rating := event.get("rating"):
            rating_count = event.get("rating_count", 0)
            description_parts.append(f"⭐ Rating: {rating}/5 ({rating_count} reviews)")
        
        # Add type
        if event_type := event.get("type"):
            description_parts.append(f"📍 Type: {event_type.replace('_', ' ').title()}")
        
        # Add booking URL
        if booking_url := event.get("booking_url"):
            description_parts.append(f"\n🎫 Book now: {booking_url}")
        
        return "\n".join(description_parts)
