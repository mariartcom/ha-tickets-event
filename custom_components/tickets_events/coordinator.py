"""DataUpdateCoordinator for Tickets & Events."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import (
    TicketsEventsApiClient,
    TicketsEventsApiClientCommunicationError,
    TicketsEventsApiClientError,
)
from .const import (
    CONF_CITY_ID,
    CONF_CITY_NAME,
    CONF_CURRENCY,
    CONF_USE_SAMPLE_DATA,
    DEFAULT_CURRENCY,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_USE_SAMPLE_DATA,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class TicketsEventsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Tickets & Events data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        self.config_entry = entry
        
        # Get use_sample_data from entry data, default to True
        use_sample_data = entry.data.get(CONF_USE_SAMPLE_DATA, DEFAULT_USE_SAMPLE_DATA)
        
        self.api = TicketsEventsApiClient(
            session=hass.helpers.aiohttp_client.async_get_clientsession(),
            use_sample_data=use_sample_data,
        )
        
        # Get configuration
        self.city_id = entry.data.get(CONF_CITY_ID, "auto")
        self.city_name = entry.data.get(CONF_CITY_NAME, "Unknown")
        self.currency = entry.data.get(CONF_CURRENCY, DEFAULT_CURRENCY)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            # If city_id is "auto", resolve location first
            city_id = self.city_id
            if city_id == "auto":
                try:
                    location = await self.api.resolve_location()
                    city_id = location.get("cityId")
                    self.city_name = location.get("city", "Unknown")
                    _LOGGER.debug("Resolved location to city: %s (%s)", self.city_name, city_id)
                except Exception as err:
                    _LOGGER.warning("Could not resolve location: %s. Using fallback.", err)
                    # Fallback to a default city (e.g., first from list)
                    cities = await self.api.get_cities()
                    if cities:
                        city_id = cities[0]["id"]
                        self.city_name = cities[0]["name"]
                    else:
                        raise UpdateFailed("No city available and location resolution failed")

            # Fetch events for the city
            events_data = await self.api.get_events_by_city(
                city_id=city_id,
                currency=self.currency,
            )
            
            # Store city information
            if city_id and city_id != self.city_id:
                # Update stored city_id if it was auto-detected
                self.city_id = city_id

            return {
                "city_id": city_id,
                "city_name": self.city_name,
                "currency": self.currency,
                "events": events_data,
            }

        except TicketsEventsApiClientCommunicationError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except TicketsEventsApiClientError as err:
            raise UpdateFailed(f"API error: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_search_events(
        self,
        query: str,
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Search for events."""
        if currency is None:
            currency = self.currency
        
        try:
            return await self.api.search_events(query=query, currency=currency)
        except Exception as err:
            _LOGGER.error("Error searching events: %s", err)
            raise

    async def async_get_events_by_date(
        self,
        date_from: str,
        date_to: str,
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Get events by date range."""
        if currency is None:
            currency = self.currency
        
        city_id = self.city_id
        if city_id == "auto":
            # Use the resolved city_id from last update
            city_id = self.data.get("city_id") if self.data else None
            if not city_id:
                raise ValueError("City not resolved yet. Please wait for initial data update.")
        
        try:
            return await self.api.get_events_by_date(
                city_id=city_id,
                date_from=date_from,
                date_to=date_to,
                currency=currency,
            )
        except Exception as err:
            _LOGGER.error("Error fetching events by date: %s", err)
            raise
