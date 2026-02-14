"""Config flow for Tickets & Events integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_CITY_ID,
    CONF_CITY_NAME,
    CONF_CURRENCY,
    CONF_USE_LOCATION,
    CONF_USE_SAMPLE_DATA,
    DEFAULT_CURRENCY,
    DEFAULT_USE_SAMPLE_DATA,
    DOMAIN,
    SUPPORTED_CURRENCIES,
)
from .api import TicketsEventsApiClient

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.
    
    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Use sample data by default
    use_sample_data = data.get(CONF_USE_SAMPLE_DATA, DEFAULT_USE_SAMPLE_DATA)
    client = TicketsEventsApiClient(use_sample_data=use_sample_data)
    
    # Validate city if provided
    if data.get(CONF_CITY_ID):
        try:
            cities = await client.get_cities()
            city_valid = any(
                city["id"] == data[CONF_CITY_ID] for city in cities
            )
            if not city_valid:
                raise ValueError("Invalid city selected")
        except Exception as err:
            _LOGGER.error("Error validating city: %s", err)
            raise ValueError("Cannot connect to API") from err
    
    # Return info to be stored in the config entry
    return {
        "title": data.get(CONF_CITY_NAME, "Tickets & Events"),
    }


class TicketsEventsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tickets & Events."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._cities: list[dict[str, Any]] = []
        self._location_data: dict[str, Any] | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        # Fetch cities list if not already fetched
        if not self._cities:
            try:
                # Use sample data for config flow
                client = TicketsEventsApiClient(use_sample_data=DEFAULT_USE_SAMPLE_DATA)
                self._cities = await client.get_cities()
            except Exception as err:
                _LOGGER.error("Error fetching cities: %s", err)
                errors["base"] = "cannot_connect"

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except ValueError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Add use_sample_data to the config data
                config_data = dict(user_input)
                # Always use sample data if not explicitly set
                if CONF_USE_SAMPLE_DATA not in config_data:
                    config_data[CONF_USE_SAMPLE_DATA] = DEFAULT_USE_SAMPLE_DATA
                
                # Add city name to config data
                if user_input.get(CONF_CITY_ID) and user_input[CONF_CITY_ID] != "auto":
                    city = next((c for c in self._cities if c["id"] == user_input[CONF_CITY_ID]), None)
                    if city:
                        config_data[CONF_CITY_NAME] = city["name"]
                
                # Create entry
                return self.async_create_entry(
                    title=info["title"],
                    data=config_data,
                )

        # Build city options
        city_options = [
            selector.SelectOptionDict(
                value=city["id"],
                label=f"{city['name']}, {city['country']}"
            )
            for city in self._cities
        ]
        
        # Add "Auto-detect" option
        city_options.insert(
            0,
            selector.SelectOptionDict(
                value="auto",
                label="Auto-detect from IP"
            )
        )

        # Show form
        data_schema = vol.Schema(
            {
                vol.Required(CONF_CITY_ID, default="auto"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=city_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(
                    CONF_CURRENCY, default=DEFAULT_CURRENCY
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=SUPPORTED_CURRENCIES,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return TicketsEventsOptionsFlowHandler(config_entry)


class TicketsEventsOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Tickets & Events."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self._cities: list[dict[str, Any]] = []

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        # Fetch cities list if not already fetched
        if not self._cities:
            try:
                client = TicketsEventsApiClient()
                self._cities = await client.get_cities()
            except Exception as err:
                _LOGGER.error("Error fetching cities: %s", err)
                errors["base"] = "cannot_connect"

        if user_input is not None:
            # Update config entry
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data={**self.config_entry.data, **user_input},
            )
            return self.async_create_entry(title="", data={})

        # Build city options
        city_options = [
            selector.SelectOptionDict(
                value=city["id"],
                label=f"{city['name']}, {city['country']}"
            )
            for city in self._cities
        ]
        
        # Add "Auto-detect" option
        city_options.insert(
            0,
            selector.SelectOptionDict(
                value="auto",
                label="Auto-detect from IP"
            )
        )

        # Get current values
        current_city = self.config_entry.data.get(CONF_CITY_ID, "auto")
        current_currency = self.config_entry.data.get(CONF_CURRENCY, DEFAULT_CURRENCY)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_CITY_ID, default=current_city): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=city_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(
                    CONF_CURRENCY, default=current_currency
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=SUPPORTED_CURRENCIES,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
        )
