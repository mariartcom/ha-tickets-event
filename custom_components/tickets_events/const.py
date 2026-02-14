"""Constants for the Tickets & Events integration."""
from datetime import timedelta
from typing import Final

# Domain
DOMAIN: Final = "tickets_events"

# Configuration
CONF_CITY_ID: Final = "city_id"
CONF_CITY_NAME: Final = "city_name"
CONF_CURRENCY: Final = "currency"
CONF_USE_LOCATION: Final = "use_location"
CONF_UPDATE_INTERVAL: Final = "update_interval"

# Defaults
DEFAULT_CURRENCY: Final = "EUR"
DEFAULT_UPDATE_INTERVAL: Final = timedelta(hours=24)  # Once per day
DEFAULT_MAX_EVENTS: Final = 50
DEFAULT_TIMEOUT: Final = 30

# API
API_BASE_URL: Final = "https://bff.mangocity.md/events"
API_RATE_LIMIT: Final = 20  # calls per minute
API_RATE_LIMIT_PERIOD: Final = 60  # seconds

# Endpoints
ENDPOINT_CITY: Final = "/events/city/{city_id}"
ENDPOINT_SEARCH: Final = "/events/search"
ENDPOINT_NEARBY: Final = "/events/nearby"
ENDPOINT_CALENDAR: Final = "/events/calendar"
ENDPOINT_CITIES: Final = "/cities"
ENDPOINT_LOCATION: Final = "/location/resolve"

# Sensors
SENSOR_TODAY: Final = "today"
SENSOR_NEARBY: Final = "nearby"
SENSOR_CALENDAR: Final = "calendar"
SENSOR_SEARCH: Final = "search"

SENSOR_TYPES: Final = [
    SENSOR_TODAY,
    SENSOR_NEARBY,
    SENSOR_CALENDAR,
    SENSOR_SEARCH,
]

# Services
SERVICE_SEARCH_EVENTS: Final = "search_events"
SERVICE_GET_EVENTS_BY_DATE: Final = "get_events_by_date"
SERVICE_GENERATE_BOOKING_URL: Final = "generate_booking_url"
SERVICE_REFRESH_EVENTS: Final = "refresh_events"

# Service Parameters
ATTR_QUERY: Final = "query"
ATTR_DATE_FROM: Final = "date_from"
ATTR_DATE_TO: Final = "date_to"
ATTR_EVENT_ID: Final = "event_id"
ATTR_DATE: Final = "date"
ATTR_TIMESLOT: Final = "timeslot"
ATTR_TICKETS: Final = "tickets"
ATTR_LANGUAGE: Final = "language"
ATTR_SENSOR: Final = "sensor"

# Event attributes
ATTR_EVENTS: Final = "events"
ATTR_DESTINATION_TITLE: Final = "destination_title"
ATTR_DESTINATION_URL: Final = "destination_url"
ATTR_LOCATION_TYPE: Final = "location_type"
ATTR_LAST_UPDATED: Final = "last_updated"

# Event fields
EVENT_ID: Final = "id"
EVENT_TITLE: Final = "title"
EVENT_DESCRIPTION: Final = "description"
EVENT_CITY: Final = "city"
EVENT_PRICE: Final = "price"
EVENT_PRICE_EUR: Final = "price_eur"
EVENT_CURRENCY: Final = "currency"
EVENT_RATING: Final = "rating"
EVENT_RATING_COUNT: Final = "rating_count"
EVENT_IMAGES: Final = "images"
EVENT_BOOKING_URL: Final = "booking_url"
EVENT_BOOKING_URL_FULL: Final = "booking_url_with_params"
EVENT_TYPE: Final = "type"
EVENT_IS_CHECKOUT_DISABLED: Final = "is_checkout_disabled"
EVENT_QR_CODE: Final = "qr_code_data"

# Currencies
SUPPORTED_CURRENCIES: Final = [
    "EUR",  # Euro
    "USD",  # US Dollar
    "GBP",  # British Pound
    "RON",  # Romanian Leu
    "CHF",  # Swiss Franc
    "AUD",  # Australian Dollar
    "CAD",  # Canadian Dollar
    "JPY",  # Japanese Yen
    "CNY",  # Chinese Yuan
]

# Languages
SUPPORTED_LANGUAGES: Final = [
    "eng",  # English
    "fra",  # French
    "deu",  # German
    "spa",  # Spanish
    "ita",  # Italian
    "por",  # Portuguese
    "nld",  # Dutch
    "ron",  # Romanian
]

# TravelPayouts
TRAVELPAYOUTS_PARTNER: Final = "travelpayouts.com"
TRAVELPAYOUTS_UTM_MEDIUM: Final = "affiliate"
TRAVELPAYOUTS_UTM_CONTENT: Final = "availability_widget"

# Booking URL parameters
BOOKING_PARAM_CURRENCY: Final = "currency"
BOOKING_PARAM_PARTNER: Final = "partner"
BOOKING_PARAM_CAMPAIGN: Final = "tq_campaign"
BOOKING_PARAM_UTM_CAMPAIGN: Final = "utm_campaign"
BOOKING_PARAM_UTM_SOURCE: Final = "utm_source"
BOOKING_PARAM_UTM_CONTENT: Final = "utm_content"
BOOKING_PARAM_UTM_MEDIUM: Final = "utm_medium"
BOOKING_PARAM_DATE: Final = "selected_date"
BOOKING_PARAM_TIMESLOT: Final = "selected_timeslot_id"
BOOKING_PARAM_VARIANTS: Final = "selected_variants"
BOOKING_PARAM_LANGUAGE: Final = "selected_variant_language"

# QR Code
QR_CODE_VERSION: Final = 1
QR_CODE_ERROR_CORRECTION: Final = "L"  # ~7% error correction
QR_CODE_BOX_SIZE: Final = 10
QR_CODE_BORDER: Final = 4

# Error messages
ERROR_CANNOT_CONNECT: Final = "cannot_connect"
ERROR_INVALID_AUTH: Final = "invalid_auth"
ERROR_RATE_LIMIT: Final = "rate_limit_exceeded"
ERROR_UNKNOWN: Final = "unknown"
ERROR_CITY_NOT_FOUND: Final = "city_not_found"
ERROR_NO_EVENTS: Final = "no_events_found"

# State
STATE_UNAVAILABLE: Final = "unavailable"
