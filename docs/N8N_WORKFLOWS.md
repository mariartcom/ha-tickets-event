# n8n Workflow Specifications

This document provides detailed specifications for the n8n workflows needed for the Tickets & Events integration.

## Base Configuration

- **Base URL**: `https://bff.mangocity.md/events`
- **HTTP Method**: GET for all endpoints
- **Response Format**: JSON
- **CORS**: Enable for Home Assistant requests
- **Rate Limiting**: Implement 20 requests/minute limit

---

## Workflow 1: Get Events by City

### Endpoint
```
GET /events/city/{city_id}
```

### Input Parameters
- `city_id` (path, required): City identifier (e.g., "c76753")
- `currency` (query, optional): Currency code (default: "EUR")
- `limit` (query, optional): Max results (default: 50, max: 50)

### Workflow Steps

1. **Webhook Trigger**
   - Listen on `/events/city/:cityId`
   - Method: GET
   - Extract: `cityId` from path, `currency` and `limit` from query

2. **Validate Input**
   - Check if `cityId` exists
   - Validate `currency` is valid code
   - Validate `limit` is between 1-50

3. **Fetch from Tiqets API**
   - Endpoint: `https://www.tiqets.com/api/v1/destinations/{cityId}/attractions`
   - Headers:
     - `Accept: application/json`
     - `User-Agent: HomeAssistant/1.0`
   - Query params:
     - `currency`: from input
     - `limit`: from input

4. **Transform Response**
   ```javascript
   {
     "destinationTitle": data.destination.name,
     "destinationUrl": `https://www.tiqets.com/en/${cityName}-attractions-${cityId}/?currency=${currency}`,
     "locationType": "city",
     "offeringCards": data.offerings.map(item => ({
       "id": item.id,
       "title": item.title,
       "description": item.description,
       "city": cityName,
       "price": item.price.amount,
       "priceEur": item.price.amountEur,
       "rating": item.rating.average,
       "ratingCount": item.rating.count,
       "images": item.images.map(img => ({
         "url": img.url,
         "alt": img.alt
       })),
       "bookingUrl": item.bookingUrl,
       "type": "product",
       "isCheckoutDisabled": item.disabled || false
     }))
   }
   ```

5. **Return Response**
   - Status: 200
   - Body: Transformed JSON

### Error Handling
- **City Not Found (404)**:
  ```json
  {
    "error": {
      "code": "CITY_NOT_FOUND",
      "message": "The requested city was not found",
      "details": {"cityId": "{cityId}"}
    }
  }
  ```

- **Rate Limit (429)**:
  ```json
  {
    "error": {
      "code": "RATE_LIMIT_EXCEEDED",
      "message": "API rate limit exceeded",
      "retryAfter": 60
    }
  }
  ```

---

## Workflow 2: Search Events

### Endpoint
```
GET /events/search
```

### Input Parameters
- `q` (query, required): Search query
- `currency` (query, optional): Currency code (default: "EUR")
- `limit` (query, optional): Max results (default: 50)

### Workflow Steps

1. **Webhook Trigger**
   - Listen on `/events/search`
   - Extract: `q`, `currency`, `limit` from query

2. **Validate Input**
   - Check `q` is not empty
   - Min length: 2 characters

3. **Search Tiqets API**
   - Endpoint: `https://www.tiqets.com/api/v1/search`
   - Query params:
     - `q`: search query
     - `currency`: from input
     - `type`: "product"
     - `limit`: from input

4. **Transform Response**
   ```javascript
   {
     "query": searchQuery,
     "totalResults": data.total,
     "offeringCards": data.results.map(item => ({
       "id": item.id,
       "title": item.title,
       "description": item.description,
       "city": item.city.name,
       "price": item.price.amount,
       "priceEur": item.price.amountEur,
       "rating": item.rating.average,
       "ratingCount": item.rating.count,
       "images": item.images.map(img => ({
         "url": img.url,
         "alt": img.alt
       })),
       "bookingUrl": item.bookingUrl,
       "type": "product",
       "isCheckoutDisabled": item.disabled || false
     }))
   }
   ```

5. **Return Response**

---

## Workflow 3: Get Nearby Events

### Endpoint
```
GET /events/nearby
```

### Input Parameters
- `lat` (query, required): Latitude
- `lon` (query, required): Longitude
- `radius` (query, optional): Radius in km (default: 50)
- `currency` (query, optional): Currency code (default: "EUR")
- `limit` (query, optional): Max results (default: 50)

### Workflow Steps

1. **Webhook Trigger**

2. **Geocode to City**
   - Use reverse geocoding API (e.g., OpenCage, Nominatim)
   - Get nearest city

3. **Fetch Events for City**
   - Reuse "Get Events by City" logic

4. **Return Response**

---

## Workflow 4: Get Events by Date Range

### Endpoint
```
GET /events/calendar
```

### Input Parameters
- `cityId` (query, required): City identifier
- `date_from` (query, required): Start date (YYYY-MM-DD)
- `date_to` (query, required): End date (YYYY-MM-DD)
- `currency` (query, optional): Currency code (default: "EUR")
- `limit` (query, optional): Max results (default: 50)

### Workflow Steps

1. **Webhook Trigger**

2. **Validate Dates**
   - Parse date_from and date_to
   - Ensure date_from <= date_to
   - Max range: 90 days

3. **Fetch Events**
   - Get events for city
   - Filter by availability dates (if available from API)
   - Or return all events with note about filtering

4. **Return Response**

---

## Workflow 5: Get Cities List

### Endpoint
```
GET /cities
```

### Workflow Steps

1. **Webhook Trigger**

2. **Read CSV File**
   - Read from `docs/sities_ids_countries.csv`
   - Parse CSV

3. **Transform to JSON**
   ```javascript
   cities.map(row => ({
     "id": row.city_id,
     "name": row.city_name,
     "country": row.country_name,
     "countryCode": row.country_code
   }))
   ```

4. **Cache Response**
   - Cache for 24 hours
   - Return cached data on subsequent requests

5. **Return Response**
   - Status: 200
   - Body: Array of cities

---

## Workflow 6: Resolve Location by IP

### Endpoint
```
GET /location/resolve
```

### Input Parameters
- `ip` (query, optional): IP address (auto-detect if not provided)

### Workflow Steps

1. **Webhook Trigger**

2. **Get IP Address**
   - If not provided, extract from request headers

3. **IP Geolocation**
   - Use service like ipapi.co or ip-api.com
   - Endpoint: `https://ipapi.co/{ip}/json/`

4. **Map to Nearest City**
   - Read cities list
   - Find city in same country
   - Or find closest city by coordinates

5. **Return Response**
   ```json
   {
     "ip": "185.120.32.45",
     "city": "Bucharest",
     "cityId": "c76753",
     "country": "Romania",
     "countryCode": "RO",
     "latitude": 44.4268,
     "longitude": 26.1025,
     "timezone": "Europe/Bucharest",
     "currency": "RON"
   }
   ```

---

## Global Error Handling

All workflows should catch and return consistent errors:

### 400 Bad Request
```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid request parameters",
    "details": {"field": "value"}
  }
}
```

### 404 Not Found
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

### 429 Rate Limit
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
```

### 500 Internal Error
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred"
  }
}
```

---

## Rate Limiting Implementation

### n8n Rate Limiter Node

1. **Use Redis** (recommended)
   - Store: `{ip}:{endpoint}:count`
   - TTL: 60 seconds
   - Increment on each request
   - If count > 20, return 429

2. **Alternative: In-Memory**
   - Use n8n Function node
   - Store counts in global variable
   - Reset every 60 seconds

### Example Function Node
```javascript
const now = Date.now();
const minute = Math.floor(now / 60000);
const key = `${$node.context.ip}:${minute}`;

let count = $node.context.counts?.[key] || 0;
count++;

if (count > 20) {
  return {
    statusCode: 429,
    body: {
      error: {
        code: "RATE_LIMIT_EXCEEDED",
        message: "Rate limit exceeded",
        retryAfter: 60
      }
    }
  };
}

// Store count
$node.context.counts = $node.context.counts || {};
$node.context.counts[key] = count;

// Cleanup old keys
Object.keys($node.context.counts).forEach(k => {
  if (k < minute - 2) delete $node.context.counts[k];
});

return items;
```

---

## TravelPayouts Integration

### Affiliate Parameters

When constructing booking URLs, include:

```javascript
const bookingUrl = new URL(originalUrl);
bookingUrl.searchParams.append('partner', 'travelpayouts.com');
bookingUrl.searchParams.append('tq_campaign', 'YOUR_CAMPAIGN_ID');
bookingUrl.searchParams.append('utm_campaign', 'travelpayouts.com');
bookingUrl.searchParams.append('utm_source', 'YOUR_AFFILIATE_ID');
bookingUrl.searchParams.append('utm_medium', 'affiliate');
bookingUrl.searchParams.append('utm_content', 'availability_widget');
```

### Required Credentials
- Campaign ID: `YOUR_CAMPAIGN_ID`
- Affiliate Source ID: `YOUR_AFFILIATE_ID`

---

## Testing

### Test Each Endpoint

```bash
# Get events by city
curl "https://bff.mangocity.md/events/city/c76753?currency=EUR"

# Search events
curl "https://bff.mangocity.md/events/search?q=museum&currency=EUR"

# Get cities
curl "https://bff.mangocity.md/events/cities"

# Resolve location
curl "https://bff.mangocity.md/events/location/resolve"

# Nearby events
curl "https://bff.mangocity.md/events/nearby?lat=44.4268&lon=26.1025"

# Events by date
curl "https://bff.mangocity.md/events/calendar?cityId=c76753&date_from=2026-02-14&date_to=2026-02-21"
```

### Response Time Targets
- Cities list: < 100ms (cached)
- Events by city: < 2s
- Search: < 3s
- Location resolve: < 1s

---

## Deployment Checklist

- [ ] All 6 workflows created
- [ ] Error handling implemented
- [ ] Rate limiting active
- [ ] TravelPayouts credentials configured
- [ ] CORS enabled for Home Assistant
- [ ] HTTPS certificate valid
- [ ] Monitoring/logging enabled
- [ ] Test all endpoints
- [ ] Document any API changes

---

## Monitoring

### Key Metrics to Track
- Request count per endpoint
- Response times
- Error rates
- Rate limit hits
- Tiqets API errors

### Logging
Log each request with:
- Timestamp
- Endpoint
- IP address
- Response time
- Status code
- Error (if any)

---

## Notes

1. **Tiqets API**: You may need to register for Tiqets API access or use web scraping if no official API
2. **Cities CSV**: Located at `docs/sities_ids_countries.csv`
3. **Caching**: Implement caching for cities list and popular queries
4. **Mock Mode**: During development, return mock data from `tests/fixtures/mock_api_responses.json`

---

**Ready to implement? Start with Workflow 5 (Cities List) as it's the simplest, then move to Workflow 1 (Events by City).**
