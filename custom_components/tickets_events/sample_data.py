"""Sample data for testing Tickets & Events integration."""
from __future__ import annotations

from typing import Final

SAMPLE_CITIES: Final = [
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
    {
        "id": "c51381",
        "name": "London",
        "country": "United Kingdom",
        "countryCode": "GB",
    },
    {
        "id": "c47717",
        "name": "Rome",
        "country": "Italy",
        "countryCode": "IT",
    },
]

SAMPLE_EVENTS: Final = [
    {
        "id": 976227,
        "title": "Palace of the Parliament Tour",
        "description": "Guided tour of one of the largest buildings in the world. Experience the opulence and grandeur of Romania's most iconic landmark with expert guides.",
        "city": "Bucharest",
        "cityId": "c76753",
        "country": "Romania",
        "price": 32.90,
        "price_eur": 32.90,
        "currency": "EUR",
        "rating": 4.3,
        "rating_count": 651,
        "type": "tour",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2019/03/27093459/Palace-of-the-Parliament-Bucharest.jpg",
                "alt": "Palace of the Parliament exterior",
            },
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2019/03/27093500/Palace-Parliament-Interior.jpg",
                "alt": "Palace interior",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/bucharest-attractions/palace-of-the-parliament/",
        "booking_url_with_params": "https://www.tiqets.com/en/bucharest-attractions/palace-of-the-parliament/?currency=EUR&partner=travelpayouts.com",
    },
    {
        "id": 123456,
        "title": "Eiffel Tower Summit Access",
        "description": "Skip the line and ascend to the summit of Paris's most iconic landmark. Enjoy breathtaking views of the City of Lights from the top.",
        "city": "Paris",
        "cityId": "c67097",
        "country": "France",
        "price": 35.50,
        "price_eur": 35.50,
        "currency": "EUR",
        "rating": 4.7,
        "rating_count": 12543,
        "type": "attraction",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2018/06/19132137/eiffel-tower-paris.jpg",
                "alt": "Eiffel Tower",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/paris-attractions/eiffel-tower/",
        "booking_url_with_params": "https://www.tiqets.com/en/paris-attractions/eiffel-tower/?currency=EUR&partner=travelpayouts.com",
    },
    {
        "id": 234567,
        "title": "Louvre Museum Skip-the-Line",
        "description": "Explore the world's largest art museum with priority access. See the Mona Lisa, Venus de Milo, and thousands of masterpieces.",
        "city": "Paris",
        "cityId": "c67097",
        "country": "France",
        "price": 22.00,
        "price_eur": 22.00,
        "currency": "EUR",
        "rating": 4.6,
        "rating_count": 8932,
        "type": "museum",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2018/08/22095555/louvre-museum-paris.jpg",
                "alt": "Louvre Museum",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/paris-attractions/louvre-museum/",
        "booking_url_with_params": "https://www.tiqets.com/en/paris-attractions/louvre-museum/?currency=EUR&partner=travelpayouts.com",
    },
    {
        "id": 345678,
        "title": "Tower of London Tickets",
        "description": "Discover 1000 years of history at this iconic fortress. See the Crown Jewels and meet the famous ravens.",
        "city": "London",
        "cityId": "c51381",
        "country": "United Kingdom",
        "price": 40.50,
        "price_eur": 47.30,
        "currency": "GBP",
        "rating": 4.5,
        "rating_count": 6754,
        "type": "attraction",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2019/05/14133759/tower-of-london.jpg",
                "alt": "Tower of London",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/london-attractions/tower-of-london/",
        "booking_url_with_params": "https://www.tiqets.com/en/london-attractions/tower-of-london/?currency=GBP&partner=travelpayouts.com",
    },
    {
        "id": 456789,
        "title": "Colosseum & Roman Forum Tour",
        "description": "Walk through ancient Rome with an expert guide. Explore the Colosseum, Roman Forum, and Palatine Hill.",
        "city": "Rome",
        "cityId": "c47717",
        "country": "Italy",
        "price": 54.00,
        "price_eur": 54.00,
        "currency": "EUR",
        "rating": 4.8,
        "rating_count": 15234,
        "type": "tour",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2018/10/02133854/colosseum-rome.jpg",
                "alt": "Colosseum",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/rome-attractions/colosseum/",
        "booking_url_with_params": "https://www.tiqets.com/en/rome-attractions/colosseum/?currency=EUR&partner=travelpayouts.com",
    },
    {
        "id": 567890,
        "title": "Vatican Museums & Sistine Chapel",
        "description": "Skip the line at the Vatican Museums. Marvel at Michelangelo's ceiling in the Sistine Chapel and explore priceless art collections.",
        "city": "Rome",
        "cityId": "c47717",
        "country": "Italy",
        "price": 38.00,
        "price_eur": 38.00,
        "currency": "EUR",
        "rating": 4.7,
        "rating_count": 11456,
        "type": "museum",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2019/01/24111739/sistine-chapel.jpg",
                "alt": "Sistine Chapel",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/rome-attractions/vatican-museums/",
        "booking_url_with_params": "https://www.tiqets.com/en/rome-attractions/vatican-museums/?currency=EUR&partner=travelpayouts.com",
    },
    {
        "id": 678901,
        "title": "British Museum Free Entry",
        "description": "Explore human history from ancient civilizations to modern times. See the Rosetta Stone, Egyptian mummies, and more.",
        "city": "London",
        "cityId": "c51381",
        "country": "United Kingdom",
        "price": 0.00,
        "price_eur": 0.00,
        "currency": "GBP",
        "rating": 4.6,
        "rating_count": 9876,
        "type": "museum",
        "is_checkout_disabled": True,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2019/02/19141823/british-museum.jpg",
                "alt": "British Museum",
            },
        ],
        "booking_url": "https://www.britishmuseum.org/",
        "booking_url_with_params": "https://www.britishmuseum.org/",
    },
    {
        "id": 789012,
        "title": "Arc de Triomphe Rooftop",
        "description": "Climb to the top of this iconic monument for panoramic views of Paris. Learn about French history and Napoleon.",
        "city": "Paris",
        "cityId": "c67097",
        "country": "France",
        "price": 16.00,
        "price_eur": 16.00,
        "currency": "EUR",
        "rating": 4.4,
        "rating_count": 4567,
        "type": "attraction",
        "is_checkout_disabled": False,
        "images": [
            {
                "url": "https://cdn.tiqets.com/wordpress/blog/wp-content/uploads/2019/03/15142234/arc-de-triomphe.jpg",
                "alt": "Arc de Triomphe",
            },
        ],
        "booking_url": "https://www.tiqets.com/en/paris-attractions/arc-de-triomphe/",
        "booking_url_with_params": "https://www.tiqets.com/en/paris-attractions/arc-de-triomphe/?currency=EUR&partner=travelpayouts.com",
    },
]


def get_sample_events_response(
    city_id: str | None = None,
    currency: str = "EUR",
    limit: int = 50,
) -> dict:
    """Get sample events response."""
    events = SAMPLE_EVENTS
    
    if city_id:
        events = [e for e in events if e.get("cityId") == city_id]
    
    # Convert prices if currency is different
    # For sample data, we'll keep the original currency
    
    events = events[:limit]
    
    city_name = "Multiple Cities"
    if city_id:
        city_data = next((c for c in SAMPLE_CITIES if c["id"] == city_id), None)
        if city_data:
            city_name = city_data["name"]
    
    return {
        "events": events,
        "destination_title": city_name,
        "destination_url": "https://www.tiqets.com",
        "location_type": "city",
        "total_count": len(events),
        "currency": currency,
    }


def search_sample_events(query: str, currency: str = "EUR", limit: int = 50) -> dict:
    """Search sample events by query."""
    query_lower = query.lower()
    
    filtered_events = [
        e for e in SAMPLE_EVENTS
        if query_lower in e["title"].lower()
        or query_lower in e["description"].lower()
        or query_lower in e.get("type", "").lower()
    ]
    
    filtered_events = filtered_events[:limit]
    
    return {
        "events": filtered_events,
        "destination_title": f"Search: {query}",
        "destination_url": "https://www.tiqets.com",
        "location_type": "search",
        "total_count": len(filtered_events),
        "query": query,
        "currency": currency,
    }


def get_nearby_sample_events(
    latitude: float,
    longitude: float,
    currency: str = "EUR",
    radius: int = 50,
    limit: int = 50,
) -> dict:
    """Get sample nearby events."""
    # For sample data, return events from Bucharest (approx coordinates)
    return get_sample_events_response("c76753", currency, limit)


def resolve_sample_location(ip_address: str | None = None) -> dict:
    """Resolve sample location."""
    return {
        "city_id": "c76753",
        "city_name": "Bucharest",
        "country": "Romania",
        "country_code": "RO",
        "latitude": 44.4268,
        "longitude": 26.1025,
        "detected_from": "ip" if ip_address else "default",
    }
