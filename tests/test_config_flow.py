"""Test the config flow for Tickets & Events."""
from unittest.mock import patch

import pytest

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.tickets_events.const import DOMAIN


@pytest.fixture(autouse=True)
def mock_api_client():
    """Mock the API client."""
    with patch(
        "custom_components.tickets_events.config_flow.TicketsEventsApiClient"
    ) as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get_cities.return_value = [
            {
                "id": "c76753",
                "name": "Bucharest",
                "country": "Romania",
                "countryCode": "RO",
            },
            {
                "id": "c67097",
                "name": "Paris",
                "country": "France",
                "countryCode": "FR",
            },
        ]
        yield mock_client


async def test_form_user(hass: HomeAssistant) -> None:
    """Test we get the user form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}


async def test_form_user_create_entry(hass: HomeAssistant) -> None:
    """Test we can create an entry from user input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "city_id": "c76753",
            "currency": "EUR",
        },
    )
    
    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Tickets & Events"
    assert result2["data"] == {
        "city_id": "c76753",
        "currency": "EUR",
    }


async def test_form_cannot_connect(hass: HomeAssistant, mock_api_client) -> None:
    """Test we handle cannot connect error."""
    mock_api_client.return_value.get_cities.side_effect = Exception("Cannot connect")
    
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}
