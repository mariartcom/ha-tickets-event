"""Services for Tickets & Events integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    ATTR_DATE,
    ATTR_DATE_FROM,
    ATTR_DATE_TO,
    ATTR_EVENT_ID,
    ATTR_LANGUAGE,
    ATTR_QUERY,
    ATTR_SENSOR,
    ATTR_TICKETS,
    ATTR_TIMESLOT,
    CONF_CURRENCY,
    DOMAIN,
    SERVICE_GENERATE_BOOKING_URL,
    SERVICE_GET_EVENTS_BY_DATE,
    SERVICE_REFRESH_EVENTS,
    SERVICE_SEARCH_EVENTS,
    SUPPORTED_CURRENCIES,
    SUPPORTED_LANGUAGES,
)
from .coordinator import TicketsEventsDataUpdateCoordinator
from .helpers import generate_booking_url

_LOGGER = logging.getLogger(__name__)

# Service schemas
SEARCH_EVENTS_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_QUERY): cv.string,
        vol.Optional(CONF_CURRENCY): vol.In(SUPPORTED_CURRENCIES),
    }
)

GET_EVENTS_BY_DATE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DATE_FROM): cv.string,
        vol.Required(ATTR_DATE_TO): cv.string,
        vol.Optional(CONF_CURRENCY): vol.In(SUPPORTED_CURRENCIES),
    }
)

GENERATE_BOOKING_URL_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_EVENT_ID): cv.positive_int,
        vol.Optional(ATTR_DATE): cv.string,
        vol.Optional(ATTR_TIMESLOT): cv.string,
        vol.Optional(ATTR_TICKETS): dict,
        vol.Optional(ATTR_LANGUAGE): vol.In(SUPPORTED_LANGUAGES),
        vol.Optional(CONF_CURRENCY): vol.In(SUPPORTED_CURRENCIES),
    }
)

REFRESH_EVENTS_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_SENSOR): cv.string,
    }
)


async def async_setup_services(
    hass: HomeAssistant,
    coordinator: TicketsEventsDataUpdateCoordinator,
) -> None:
    """Set up services for Tickets & Events."""

    async def handle_search_events(call: ServiceCall) -> None:
        """Handle search events service."""
        query = call.data[ATTR_QUERY]
        currency = call.data.get(CONF_CURRENCY)
        
        _LOGGER.debug("Searching events with query: %s", query)
        
        try:
            results = await coordinator.async_search_events(query, currency)
            _LOGGER.info("Found %d events matching '%s'", len(results.get("offeringCards", [])), query)
            
            # Return results
            return {
                "success": True,
                "results": results,
            }
        except Exception as err:
            _LOGGER.error("Error searching events: %s", err)
            return {
                "success": False,
                "error": str(err),
            }

    async def handle_get_events_by_date(call: ServiceCall) -> None:
        """Handle get events by date service."""
        date_from = call.data[ATTR_DATE_FROM]
        date_to = call.data[ATTR_DATE_TO]
        currency = call.data.get(CONF_CURRENCY)
        
        _LOGGER.debug("Getting events from %s to %s", date_from, date_to)
        
        try:
            results = await coordinator.async_get_events_by_date(date_from, date_to, currency)
            _LOGGER.info("Found %d events in date range", len(results.get("offeringCards", [])))
            
            return {
                "success": True,
                "results": results,
            }
        except Exception as err:
            _LOGGER.error("Error getting events by date: %s", err)
            return {
                "success": False,
                "error": str(err),
            }

    async def handle_generate_booking_url(call: ServiceCall) -> None:
        """Handle generate booking URL service."""
        event_id = call.data[ATTR_EVENT_ID]
        date = call.data.get(ATTR_DATE)
        timeslot = call.data.get(ATTR_TIMESLOT)
        tickets = call.data.get(ATTR_TICKETS)
        language = call.data.get(ATTR_LANGUAGE)
        currency = call.data.get(CONF_CURRENCY, coordinator.currency)
        
        _LOGGER.debug("Generating booking URL for event ID: %s", event_id)
        
        # Find event in coordinator data
        if not coordinator.data:
            _LOGGER.error("No event data available")
            return {
                "success": False,
                "error": "No event data available",
            }
        
        events = coordinator.data.get("events", {}).get("offeringCards", [])
        event = next((e for e in events if e.get("id") == event_id), None)
        
        if not event:
            _LOGGER.error("Event ID %s not found", event_id)
            return {
                "success": False,
                "error": f"Event ID {event_id} not found",
            }
        
        # Generate URL
        try:
            booking_url = generate_booking_url(
                event=event,
                currency=currency,
                date=date,
                timeslot=timeslot,
                tickets=tickets,
                language=language,
            )
            
            _LOGGER.info("Generated booking URL for event: %s", event.get("title"))
            
            return {
                "success": True,
                "booking_url": booking_url,
                "event_title": event.get("title"),
                "event_id": event_id,
            }
        except Exception as err:
            _LOGGER.error("Error generating booking URL: %s", err)
            return {
                "success": False,
                "error": str(err),
            }

    async def handle_refresh_events(call: ServiceCall) -> None:
        """Handle refresh events service."""
        sensor = call.data.get(ATTR_SENSOR)
        
        _LOGGER.debug("Refreshing events (sensor: %s)", sensor or "all")
        
        try:
            await coordinator.async_request_refresh()
            _LOGGER.info("Events refreshed successfully")
            
            return {
                "success": True,
            }
        except Exception as err:
            _LOGGER.error("Error refreshing events: %s", err)
            return {
                "success": False,
                "error": str(err),
            }

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEARCH_EVENTS,
        handle_search_events,
        schema=SEARCH_EVENTS_SCHEMA,
        supports_response="optional",
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_EVENTS_BY_DATE,
        handle_get_events_by_date,
        schema=GET_EVENTS_BY_DATE_SCHEMA,
        supports_response="optional",
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_BOOKING_URL,
        handle_generate_booking_url,
        schema=GENERATE_BOOKING_URL_SCHEMA,
        supports_response="optional",
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH_EVENTS,
        handle_refresh_events,
        schema=REFRESH_EVENTS_SCHEMA,
    )

    _LOGGER.info("Services registered for %s", DOMAIN)
