# Technical Decisions & Requirements

**Last Updated**: February 14, 2026  
**Status**: Approved for Implementation

## API & Backend

### Authentication
- **Type**: Public endpoints (no authentication required initially)
- **Base URL**: `https://bff.mangocity.md/events`
- **Rate Limit**: 20 API calls per minute maximum
- **Handling**: Implement rate limiting with queue and retry logic

### TravelPayouts Integration
- **Status**: Credentials available
- **Affiliate Program**: TravelPayouts.com
- **Campaign IDs**: To be configured during n8n setup

### n8n Workflows
- **Development Order**: Home Assistant integration first, n8n workflows handled separately
- **Mock Data**: Use mock API responses for development and testing

## Data & Updates

### Update Frequency
- **Event Lists**: Once per day (86400 seconds)
- **On-Demand**: Manual refresh via service calls
- **Background**: Updates happen automatically in background

### Caching Strategy
- Cache event data for 24 hours
- Cache city list permanently (only refresh on manual trigger)
- Cache location resolution for user's session

## Location & Geography

### City Configuration
- **Primary**: User selects city from predefined list during setup
- **Fallback**: IP-based location detection by country if no city selected
- **Multi-City**: Not supported in v1.0 (single city per integration instance)
- **City Database**: `docs/sities_ids_countries.csv`

### Location Detection
- **Method**: IP-based geolocation for fallback
- **Precision**: Country → City mapping
- **Service**: To be determined (ipapi.co or through n8n)

## User Interface

### Display Strategy
- **Initial Approach**: Standard Home Assistant entities + template examples
- **Future Enhancement**: Custom Lovelace cards if UX is insufficient
- **Target Displays**: Mobile, Browser, TV/Dashboard screens

### Image Handling
- **Source**: API-provided image URLs
- **Storage**: Entity attributes (no camera entities)
- **Format**: Array of image objects with URL and alt text

### QR Code Generation
- **Priority**: Must-have for v1.0
- **Method**: Generated on UI per event item
- **Purpose**: Enable ticket booking from TV displays
- **Contains**: Booking redirect link with all parameters

## Entity Architecture

### Sensor Structure
**Approach**: Option A - One sensor per widget type

**Sensor Types**:
1. **Today Events** (`sensor.tickets_events_today`)
   - Events happening today in configured city
   - Updates: Once per day
   - Max events: 50

2. **Nearby Events** (`sensor.tickets_events_nearby`)
   - Events in configured city/area
   - Updates: Once per day
   - Max events: 50

3. **Calendar Events** (`sensor.tickets_events_calendar`)
   - Date-filtered events
   - Dynamic date range
   - Max events: 50

4. **Search Results** (`sensor.tickets_events_search`)
   - Search query results
   - Updates: On-demand via service
   - Max events: 50

### Entity Attributes
Each sensor contains:
- **State**: Number of events found
- **Attributes**:
  - `events`: Array of event objects (max 50)
  - `destination_title`: City name
  - `destination_url`: Destination page URL
  - `last_updated`: Timestamp
  - `currency`: Active currency
  - `location_type`: city/region

### Event Object Structure
```json
{
  "id": 976227,
  "title": "Event Title",
  "description": "Event description",
  "city": "Bucharest",
  "price": 32.90,
  "price_eur": 32.90,
  "currency": "EUR",
  "rating": 4.3,
  "rating_count": 651,
  "images": [
    {
      "url": "https://...",
      "alt": "Image description"
    }
  ],
  "booking_url": "https://...",
  "booking_url_with_params": "https://...?currency=EUR&partner=...",
  "type": "product",
  "is_checkout_disabled": false,
  "qr_code_data": "base64_encoded_qr_code"
}
```

## Services

### Must-Have Services (v1.0)

#### 1. Search Events
```yaml
service: tickets_events.search_events
data:
  query: "Palace tour"
  currency: "EUR"
```

#### 2. Refresh Events
```yaml
service: tickets_events.refresh_events
data:
  sensor: "today"  # or "nearby", "calendar"
```

#### 3. Get Events by Date
```yaml
service: tickets_events.get_events_by_date
data:
  date_from: "2026-02-14"
  date_to: "2026-02-21"
  currency: "EUR"
```

#### 4. Generate Booking URL
```yaml
service: tickets_events.generate_booking_url
data:
  event_id: 976227
  date: "2026-02-14"
  timeslot: "09:00"
  tickets:
    adult: 2
    child: 1
  language: "eng"
  currency: "EUR"
```

## Booking & Tickets

### URL Generation
- **Method**: Direct link generation with default ticket counts
- **Customization**: Service allows ticket type/count specification
- **Parameters**: All TravelPayouts parameters included

### Default Ticket Configuration
- **Adult**: 1 ticket by default
- **Currency**: User-configured (EUR, USD, GBP, etc.)
- **Date**: Current date or user-specified
- **Language**: User's Home Assistant language setting

## Currency Support

### Supported Currencies
- EUR (Euro) - Default
- USD (US Dollar)
- GBP (British Pound)
- RON (Romanian Leu)
- Additional currencies as needed

### Configuration
- **Setup**: User selects during initial configuration
- **Change**: Reconfigurable via options flow
- **API**: Passed as query parameter to n8n endpoint

## Repository & Domain

### Repository Details
- **Name**: `ha-tickets-event`
- **GitHub Account**: quoda.team@gmail.com
- **Visibility**: Public
- **License**: MIT

### Integration Details
- **Domain**: `tickets_events`
- **Name**: "Tickets & Events"
- **Version**: 0.1.0 (development) → 1.0.0 (release)

### File Paths
- **Custom Component**: `custom_components/tickets_events/`
- **Configuration**: Entry via config flow (UI)
- **Storage**: `.storage/tickets_events/`

## Must-Have Features for v1.0

### Core Features
- ✅ Config flow with city selection
- ✅ IP-based location fallback
- ✅ Currency selection
- ✅ Event sensors (today, nearby, calendar)
- ✅ Once-daily automatic updates
- ✅ Event data with images and pricing

### Services
- ✅ Search events service
- ✅ Refresh events service
- ✅ Get events by date range
- ✅ Generate booking URL with parameters

### Advanced Features
- ✅ QR code generation for each event
- ✅ Multi-language support (i18n)
- ✅ Rate limiting (20 calls/min)
- ✅ Error handling and retry logic

### Documentation
- ✅ README with installation guide
- ✅ Configuration examples
- ✅ Lovelace card templates
- ✅ Service documentation
- ✅ Troubleshooting guide

## Future Enhancements (Post v1.0)

### Low Priority
- Calendar entity integration
- Multi-city support (multiple instances)
- Custom Lovelace cards
- Price alerts and notifications
- Favorite events

### Nice to Have
- Voice assistant booking integration
- Event recommendations
- Historical data tracking
- Mobile app notifications

## Testing Strategy

### Mock Data
- **Location**: `tests/fixtures/`
- **Files**:
  - `events_bucharest.json`
  - `events_search.json`
  - `cities_list.json`
  - `location_response.json`

### Test Coverage
- **Target**: >80%
- **Focus Areas**:
  - Config flow
  - Data coordinator
  - Rate limiting
  - Error handling
  - Service calls

### Test Environments
1. **Local Development**: Mock API responses
2. **Integration Testing**: Real n8n endpoints (when ready)
3. **Production**: Custom HACS repository

## Performance Considerations

### Memory
- **Max Events**: 50 per sensor = reasonable memory footprint
- **Image Storage**: URLs only (no binary data)
- **Cache**: In-memory with 24-hour TTL

### Network
- **Rate Limiting**: 20 calls/min = 1 call per 3 seconds
- **Update Frequency**: Once per day per sensor
- **Optimization**: Batch requests where possible

### Processing
- **Async Operations**: All API calls are async
- **Non-Blocking**: Background updates don't freeze UI
- **Timeout**: 30 seconds per API call

## Security Considerations

### API Keys
- **Current**: No authentication required
- **Future**: Support for API key in config if needed
- **Storage**: Secure storage via HA config entries

### Data Privacy
- **User Location**: Optional, not stored permanently
- **Search Queries**: Not logged or stored
- **Analytics**: None by default

### HTTPS
- **Requirement**: All API calls must use HTTPS
- **Validation**: Verify SSL certificates

## Compliance

### HACS Requirements
- All HACS requirements documented in `HACS_REQUIREMENTS.md`
- Quality scale compliance target: Gold/Silver
- Proper versioning with semantic versioning

### Home Assistant Standards
- Follow HA integration quality scale
- Use async/await patterns
- Implement proper error handling
- Type hints on all functions
- Comprehensive logging

## Development Timeline

### Phase 1: Core (Weeks 1-2)
- Repository structure
- Config flow
- Data coordinator
- Basic sensors

### Phase 2: Features (Weeks 3-4)
- Services implementation
- QR code generation
- Search functionality
- Translations

### Phase 3: Polish (Week 5)
- Testing
- Documentation
- Mock data
- Error handling

### Phase 4: Release (Week 6)
- Custom repository testing
- Bug fixes
- Final documentation
- v1.0.0 release

### Phase 5: Publication (Week 7)
- HACS submission
- Community support setup
- Monitoring and maintenance
