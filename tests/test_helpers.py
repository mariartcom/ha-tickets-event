"""Test helpers for Tickets & Events."""
from custom_components.tickets_events.helpers import (
    format_price,
    generate_booking_url,
    generate_qr_code,
)


def test_format_price_eur():
    """Test EUR price formatting."""
    assert format_price(32.90, "EUR") == "€32.90"


def test_format_price_usd():
    """Test USD price formatting."""
    assert format_price(45.50, "USD") == "$45.50"


def test_format_price_jpy():
    """Test JPY price formatting (no decimals)."""
    assert format_price(1500.00, "JPY") == "¥1500"


def test_generate_booking_url():
    """Test booking URL generation."""
    event = {
        "id": 976227,
        "bookingUrl": "https://www.tiqets.com/en/bucharest-attractions-c76753/tickets-for-palace-p976227/",
    }
    
    url = generate_booking_url(event, currency="EUR", date="2026-02-14")
    
    assert "currency=EUR" in url
    assert "partner=travelpayouts.com" in url
    assert "selected_date=2026-02-14" in url


def test_generate_qr_code():
    """Test QR code generation."""
    url = "https://example.com/booking"
    qr_code = generate_qr_code(url)
    
    assert qr_code.startswith("data:image/png;base64,")
    assert len(qr_code) > 100  # QR code should have substantial data
