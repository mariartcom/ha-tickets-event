# API Specification

## Base URL
```
https://bff.mangocity.md/events
```

## Authentication
TBD - Need to confirm:
- API key header?
- OAuth?
- Public endpoints?

## Endpoints (Estimated)

### 1. Get Events by City
```http
GET /events/city/{cityId}
```

**Parameters:**
- `cityId` (path, required): City identifier from cities database
- `currency` (query, optional): Currency code (default: EUR)
- `limit` (query, optional): Number of results (default: 20)

**Response:**
```json
{
  "destinationTitle": "Bucharest",
  "destinationUrl": "...",
  "locationType": "city",
  "offeringCards": [
    {
      "id": 976227,
      "title": "...",
      "description": "...",
      "city": "Bucharest",
      "price": 32.90,
      "priceEur": 32.90,
      "rating": 4.3,
      "ratingCount": 651,
      "images": [...],
      "bookingUrl": "...",
      "type": "product",
      "isCheckoutDisabled": false
    }
  ]
}
```

### 2. Search Events
```http
GET /events/search
```

**Parameters:**
- `q` (query, required): Search query (event name or city)
- `currency` (query, optional): Currency code
- `limit` (query, optional): Number of results

### 3. Get Nearby Events
```http
GET /events/nearby
```

**Parameters:**
- `lat` (query, required): Latitude
- `lon` (query, required): Longitude
- `radius` (query, optional): Search radius in km (default: 50)
- `currency` (query, optional): Currency code

### 4. Get Events by Date Range
```http
GET /events/calendar
```

**Parameters:**
- `cityId` (query, required): City identifier
- `date_from` (query, required): Start date (YYYY-MM-DD)
- `date_to` (query, required): End date (YYYY-MM-DD)
- `currency` (query, optional): Currency code

### 5. Get Cities List
```http
GET /cities
```

**Response:**
```json
[
  {
    "id": "c76753",
    "name": "Bucharest",
    "country": "Romania",
    "countryCode": "RO"
  }
]
```

### 6. Resolve Location by IP
```http
GET /location/resolve
```

**Parameters:**
- `ip` (query, optional): IP address (auto-detected if not provided)

**Response:**
```json
{
  "city": "Bucharest",
  "cityId": "c76753",
  "country": "Romania",
  "countryCode": "RO",
  "lat": 44.4268,
  "lon": 26.1025
}
```

## Booking URL Generation

### Base Booking URL
```
https://www.tiqets.com/en/checkout/tickets-for-{event-slug}-p{eventId}/booking_details/
```

### Required Parameters
- `currency`: Currency code (EUR, USD, etc.)
- `partner`: travelpayouts.com
- `tq_campaign`: Campaign ID
- `utm_campaign`: travelpayouts.com
- `utm_source`: Affiliate source ID
- `utm_content`: availability_widget
- `utm_medium`: affiliate

### Optional Parameters
- `selected_date`: Date in YYYY-MM-DD format
- `selected_timeslot_id`: Time slot (HH:MM format)
- `selected_variants`: Ticket types (e.g., `47923=1&47929=1`)
- `selected_variant_language`: Language code (eng, ita, fra, etc.)

### Example
```
https://www.tiqets.com/en/checkout/tickets-for-mont-saint-michel-abbey-entry-p974575/booking_details/?currency=EUR&partner=travelpayouts.com&selected_date=2026-02-14&selected_timeslot_id=09:00
```

## Rate Limiting
TBD - Need to confirm:
- Requests per minute/hour?
- Rate limit headers?
- Handling strategies?

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

### Common Error Codes
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## n8n Workflow Structure

### Workflow 1: Events by City
- Trigger: Webhook
- Parse city ID
- Fetch data from Tiqets API
- Transform data
- Return response

### Workflow 2: Search Events
- Trigger: Webhook
- Parse search query
- Search across cities
- Return aggregated results

### Workflow 3: Nearby Events
- Trigger: Webhook
- Resolve coordinates to cities
- Fetch events for nearby cities
- Return sorted results

### Workflow 4: Calendar Events
- Trigger: Webhook
- Parse date range
- Fetch events with date filtering
- Return filtered results

### Workflow 5: Location Resolution
- Trigger: Webhook
- IP geolocation lookup
- Map to nearest city
- Return city information
