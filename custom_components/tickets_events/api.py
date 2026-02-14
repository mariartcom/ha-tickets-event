"""API client for Tickets & Events."""
from __future__ import annotations

import asyncio
from datetime import datetime
import logging
from typing import Any

import aiohttp
import async_timeout

from .const import (
    API_BASE_URL,
    API_RATE_LIMIT,
    API_RATE_LIMIT_PERIOD,
    CONF_USE_SAMPLE_DATA,
    DEFAULT_TIMEOUT,
    DEFAULT_USE_SAMPLE_DATA,
    ENDPOINT_CALENDAR,
    ENDPOINT_CITIES,
    ENDPOINT_CITY,
    ENDPOINT_LOCATION,
    ENDPOINT_NEARBY,
    ENDPOINT_SEARCH,
    ERROR_CANNOT_CONNECT,
    ERROR_RATE_LIMIT,
    ERROR_UNKNOWN,
)
from .sample_data import (
    SAMPLE_CITIES,
    get_nearby_sample_events,
    get_sample_events_response,
    resolve_sample_location,
    search_sample_events,
)

_LOGGER = logging.getLogger(__name__)


class TicketsEventsApiClientError(Exception):
    """Exception to indicate a general API error."""


class TicketsEventsApiClientCommunicationError(TicketsEventsApiClientError):
    """Exception to indicate a communication error."""


class TicketsEventsApiClientRateLimitError(TicketsEventsApiClientError):
    """Exception to indicate rate limit exceeded."""


class RateLimiter:
    """Simple rate limiter."""

    def __init__(self, max_calls: int, period: int) -> None:
        """Initialize rate limiter."""
        self.max_calls = max_calls
        self.period = period
        self.calls: list[float] = []
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire rate limit slot."""
        async with self._lock:
            now = datetime.now().timestamp()
            # Remove calls outside the time window
            self.calls = [call for call in self.calls if now - call < self.period]
            
            if len(self.calls) >= self.max_calls:
                # Calculate wait time
                oldest_call = min(self.calls)
                wait_time = self.period - (now - oldest_call)
                if wait_time > 0:
                    _LOGGER.warning(
                        "Rate limit reached. Waiting %.2f seconds", wait_time
                    )
                    await asyncio.sleep(wait_time)
                    # Recursive call after waiting
                    await self.acquire()
                    return
            
            # Add current call
            self.calls.append(now)


class TicketsEventsApiClient:
    """API client for Tickets & Events."""

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        use_sample_data: bool = DEFAULT_USE_SAMPLE_DATA,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._close_session = False
        self._rate_limiter = RateLimiter(API_RATE_LIMIT, API_RATE_LIMIT_PERIOD)
        self._use_sample_data = use_sample_data

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True
        
        if self._use_sample_data:
            _LOGGER.info("API client initialized with SAMPLE DATA mode enabled")

    async def close(self) -> None:
        """Close the session."""
        if self._close_session and self._session:
            await self._session.close()

    async def _api_request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make API request with rate limiting."""
        # Acquire rate limit slot
        await self._rate_limiter.acquire()

        url = f"{API_BASE_URL}{endpoint}"
        
        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._session.request(
                    method="GET",
                    url=url,
                    params=params,
                    headers={"Content-Type": "application/json"},
                )
                
                if response.status == 429:
                    # Rate limit exceeded
                    retry_after = response.headers.get("Retry-After", 60)
                    _LOGGER.error("Rate limit exceeded. Retry after %s seconds", retry_after)
                    raise TicketsEventsApiClientRateLimitError(
                        f"Rate limit exceeded. Retry after {retry_after}s"
                    )
                
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error("Timeout error fetching data from %s: %s", url, exception)
            raise TicketsEventsApiClientCommunicationError(
                "Timeout communicating with API"
            ) from exception
        except aiohttp.ClientError as exception:
            _LOGGER.error("Error fetching data from %s: %s", url, exception)
            raise TicketsEventsApiClientCommunicationError(
                "Error communicating with API"
            ) from exception
        except Exception as exception:
            _LOGGER.error("Unexpected error: %s", exception)
            raise TicketsEventsApiClientError(
                "Unexpected error communicating with API"
            ) from exception

    async def get_cities(self) -> list[dict[str, Any]]:
        """Get list of available cities."""
        if self._use_sample_data:
            _LOGGER.debug("Returning sample cities data")
            return SAMPLE_CITIES
        
        try:
            data = await self._api_request(ENDPOINT_CITIES)
            return data if isinstance(data, list) else []
        except Exception as err:
            _LOGGER.error("Error fetching cities: %s", err)
            # Return mock data for development
            return [
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

    async def get_events_by_city(
        self,
        city_id: str,
        currency: str = "EUR",
        limit: int = 50,
    ) -> dict[str, Any]:
        """Get events for a specific city."""
        if self._use_sample_data:
            _LOGGER.debug("Returning sample events for city %s", city_id)
            return get_sample_events_response(city_id, currency, limit)
        
        endpoint = ENDPOINT_CITY.format(city_id=city_id)
        params = {
            "currency": currency,
            "limit": limit,
        }
        
        try:
            return await self._api_request(endpoint, params)
        except Exception as err:
            _LOGGER.error("Error fetching events for city %s: %s", city_id, err)
            raise

    async def search_events(
        self,
        query: str,
        currency: str = "EUR",
        limit: int = 50,
    ) -> dict[str, Any]:
        """Search for events."""
        if self._use_sample_data:
            _LOGGER.debug("Returning sample search results for query: %s", query)
            return search_sample_events(query, currency, limit)
        
        params = {
            "q": query,
            "currency": currency,
            "limit": limit,
        }
        
        try:
            return await self._api_request(ENDPOINT_SEARCH, params)
        except Exception as err:
            _LOGGER.error("Error searching events with query '%s': %s", query, err)
            raise

    async def get_nearby_events(
        self,
        latitude: float,
        longitude: float,
        currency: str = "EUR",
        radius: int = 50,
        limit: int = 50,
    ) -> dict[str, Any]:
        """Get events near a location."""
        if self._use_sample_data:
            _LOGGER.debug("Returning sample nearby events")
            return get_nearby_sample_events(latitude, longitude, currency, radius, limit)
        
        params = {
            "lat": latitude,
            "lon": longitude,
            "radius": radius,
            "currency": currency,
            "limit": limit,
        }
        
        try:
            return await self._api_request(ENDPOINT_NEARBY, params)
        except Exception as err:
            _LOGGER.error(
                "Error fetching nearby events at (%s, %s): %s",
                latitude,
                longitude,
                err,
            )
            raise

    async def get_events_by_date(
        self,
        city_id: str,
        date_from: str,
        date_to: str,
        currency: str = "EUR",
        limit: int = 50,
    ) -> dict[str, Any]:
        """Get events within a date range."""
        if self._use_sample_data:
            _LOGGER.debug("Returning sample events for date range %s to %s", date_from, date_to)
            return get_sample_events_response(city_id, currency, limit)
        
        params = {
            "cityId": city_id,
            "date_from": date_from,
            "date_to": date_to,
            "currency": currency,
            "limit": limit,
        }
        
        try:
            return await self._api_request(ENDPOINT_CALENDAR, params)
        except Exception as err:
            _LOGGER.error(
                "Error fetching events for date range %s to %s: %s",
                date_from,
                date_to,
                err,
            )
            raise

    async def resolve_location(self, ip_address: str | None = None) -> dict[str, Any]:
        """Resolve location from IP address."""
        if self._use_sample_data:
            _LOGGER.debug("Returning sample location data")
            return resolve_sample_location(ip_address)
        
        params = {}
        if ip_address:
            params["ip"] = ip_address
        
        try:
            return await self._api_request(ENDPOINT_LOCATION, params)
        except Exception as err:
            _LOGGER.error("Error resolving location: %s", err)
            raise
