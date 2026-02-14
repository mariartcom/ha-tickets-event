"""Tests for Tickets & Events integration."""
import pytest
from homeassistant.core import HomeAssistant

from custom_components.tickets_events.const import DOMAIN


@pytest.fixture
def mock_config_entry():
    """Return a mock config entry."""
    return {
        "entry_id": "test",
        "domain": DOMAIN,
        "data": {
            "city_id": "c76753",
            "city_name": "Bucharest",
            "currency": "EUR",
        },
        "options": {},
        "title": "Tickets & Events",
    }


@pytest.fixture
async def setup_integration(hass: HomeAssistant, mock_config_entry):
    """Set up the integration for testing."""
    # This would normally set up the integration with mock data
    # For now, it's a placeholder
    pass
