"""Helper utilities for Tickets & Events."""
from __future__ import annotations

import base64
from io import BytesIO
import logging
from typing import Any
from urllib.parse import urlencode

import qrcode

from .const import (
    BOOKING_PARAM_CAMPAIGN,
    BOOKING_PARAM_CURRENCY,
    BOOKING_PARAM_DATE,
    BOOKING_PARAM_LANGUAGE,
    BOOKING_PARAM_PARTNER,
    BOOKING_PARAM_TIMESLOT,
    BOOKING_PARAM_UTM_CAMPAIGN,
    BOOKING_PARAM_UTM_CONTENT,
    BOOKING_PARAM_UTM_MEDIUM,
    BOOKING_PARAM_UTM_SOURCE,
    BOOKING_PARAM_VARIANTS,
    EVENT_BOOKING_URL,
    EVENT_ID,
    EVENT_QR_CODE,
    QR_CODE_BORDER,
    QR_CODE_BOX_SIZE,
    QR_CODE_ERROR_CORRECTION,
    QR_CODE_VERSION,
    TRAVELPAYOUTS_PARTNER,
    TRAVELPAYOUTS_UTM_CONTENT,
    TRAVELPAYOUTS_UTM_MEDIUM,
)

_LOGGER = logging.getLogger(__name__)


def generate_booking_url(
    event: dict[str, Any],
    currency: str = "EUR",
    date: str | None = None,
    timeslot: str | None = None,
    tickets: dict[str, int] | None = None,
    language: str | None = None,
    campaign_id: str | None = None,
    affiliate_source: str | None = None,
) -> str:
    """Generate a complete booking URL with all parameters."""
    base_url = event.get(EVENT_BOOKING_URL, "")
    if not base_url:
        _LOGGER.warning("No booking URL found for event %s", event.get(EVENT_ID))
        return ""

    # Build parameters
    params = {
        BOOKING_PARAM_CURRENCY: currency,
        BOOKING_PARAM_PARTNER: TRAVELPAYOUTS_PARTNER,
        BOOKING_PARAM_UTM_CAMPAIGN: TRAVELPAYOUTS_PARTNER,
        BOOKING_PARAM_UTM_MEDIUM: TRAVELPAYOUTS_UTM_MEDIUM,
        BOOKING_PARAM_UTM_CONTENT: TRAVELPAYOUTS_UTM_CONTENT,
    }

    # Add campaign ID if provided
    if campaign_id:
        params[BOOKING_PARAM_CAMPAIGN] = campaign_id

    # Add affiliate source if provided
    if affiliate_source:
        params[BOOKING_PARAM_UTM_SOURCE] = affiliate_source

    # Add date if provided
    if date:
        params[BOOKING_PARAM_DATE] = date

    # Add timeslot if provided
    if timeslot:
        params[BOOKING_PARAM_TIMESLOT] = timeslot

    # Add language if provided
    if language:
        params[BOOKING_PARAM_LANGUAGE] = language

    # Add ticket variants if provided
    if tickets:
        # Format: 47923=1&47929=1 (variant_id=quantity)
        # For now, we'll just pass the dict as-is and let the API handle it
        # In a real implementation, you'd need to map ticket types to variant IDs
        variant_str = "&".join(f"{k}={v}" for k, v in tickets.items())
        params[BOOKING_PARAM_VARIANTS] = variant_str

    # Build query string
    query_string = urlencode(params)
    
    # Combine URL
    separator = "&" if "?" in base_url else "?"
    return f"{base_url}{separator}{query_string}"


def generate_qr_code(url: str) -> str:
    """Generate a QR code as base64 encoded image."""
    try:
        # Create QR code
        qr = qrcode.QRCode(
            version=QR_CODE_VERSION,
            error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{QR_CODE_ERROR_CORRECTION}"),
            box_size=QR_CODE_BOX_SIZE,
            border=QR_CODE_BORDER,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"

    except Exception as err:
        _LOGGER.error("Error generating QR code: %s", err)
        return ""


def process_event_data(
    event: dict[str, Any],
    currency: str = "EUR",
) -> dict[str, Any]:
    """Process raw event data and add generated fields."""
    # Generate booking URL with parameters
    booking_url_full = generate_booking_url(event, currency=currency)
    
    # Generate QR code
    qr_code_data = generate_qr_code(booking_url_full) if booking_url_full else ""
    
    # Add generated fields to event
    processed_event = {
        **event,
        "booking_url_with_params": booking_url_full,
        EVENT_QR_CODE: qr_code_data,
    }
    
    return processed_event


def format_price(price: float, currency: str) -> str:
    """Format price with currency symbol."""
    currency_symbols = {
        "EUR": "€",
        "USD": "$",
        "GBP": "£",
        "RON": "lei",
        "CHF": "Fr",
        "AUD": "A$",
        "CAD": "C$",
        "JPY": "¥",
        "CNY": "¥",
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    # Format based on currency
    if currency in ["JPY", "CNY"]:
        # No decimals for these currencies
        return f"{symbol}{int(price)}"
    else:
        return f"{symbol}{price:.2f}"
