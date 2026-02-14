# Events Integration for Home Assistant

## Project Overview
A Home Assistant HACS integration that provides event listing widgets and search functionality for attractions, tours, and activities worldwide.

## Features

### 1. Event Widgets
- **Today Events**: Display events happening today nearby
- **Search Events**: Search by event name or city
- **Event Calendar**: Filter by date ranges
  - Today
  - Tomorrow
  - This Week
  - Next Week
  - Next 2 Weeks
  - This Month
  - Next Month

### 2. Event Data Structure
Each event includes:
- **Name**: Event title
- **Description**: Event details
- **Dates**: Event date/time
- **Location**: City, State, Country
- **Image**: Event thumbnail/hero image
- **Price**: Ticket price (with currency)
- **Offer Tag**: Special offers/badges
- **Ticket Counts**: Available ticket types and counts
- **Geo Coordinates**: Latitude/longitude
- **Booking URL**: Link to purchase tickets

### 3. User Configuration
- Predefined city selection in settings
- IP-based location resolution (fallback)
- Currency selection
- Default date range preferences

### 4. Ticket Purchase Flow
- **Mobile/Browser**: Redirect to booking URL
- **TV/Dashboard**: Display QR code for scanning

## Technical Architecture

### Backend
- **Platform**: n8n workflows
- **Base URL**: `bff.mangocity.md/events`
- **Data Source**: Tiqets API via TravelPayouts affiliate

### Frontend
- **Platform**: Home Assistant Custom Component
- **UI Framework**: Home Assistant Lovelace Cards
- **Display**: Cards, Entities, Custom Frontend

### API Endpoints (Estimated)
1. `GET /events/city/{cityId}` - Get events by city
2. `GET /events/search?q={query}` - Search events
3. `GET /events/nearby?lat={lat}&lon={lon}` - Get nearby events
4. `GET /events/calendar?date_from={date}&date_to={date}` - Get events by date range
5. `GET /cities` - Get list of available cities

### URL Parameters for Booking
```
?currency=EUR
&partner=travelpayouts.com
&tq_campaign={campaign_id}
&selected_date={YYYY-MM-DD}
&selected_timeslot_id={HH:MM}
&selected_variants={ticket_types}
&selected_variant_language={language}
```

## Data Sources

### Cities Database
Location: `docs/sities_ids_countries.csv`
- City names
- City IDs (for API calls)
- Country information

### Sample Event Data
```json
{
  "id": 976227,
  "title": "Palace of the Parliament: Entry Ticket + Guided Tour",
  "description": "Communist megalomania meets Neoclassical architecture",
  "city": "Bucharest",
  "price": 32.90,
  "priceEur": 32.90,
  "rating": 4.3,
  "ratingCount": 651,
  "images": [...],
  "bookingUrl": "https://www.tiqets.com/...",
  "type": "product",
  "isCheckoutDisabled": false
}
```

## Development Workflow

### Phase 1: Custom Repository
1. Create HACS-compliant repository structure
2. Develop integration locally
3. Test with custom repository installation
4. Iterate and refine

### Phase 2: Publication
1. Complete HACS requirements checklist
2. Submit to HACS default directory
3. Await review and approval

## References
- [HACS Documentation](https://www.hacs.xyz/docs/contribute/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- Home Assistant Templates & Frontend Ecosystem

## Repository
- **GitHub Account**: quoda.team@gmail.com
- **Repository Name**: TBD (e.g., `ha-events-integration`)

## Compliance
- Must follow HACS quality scale requirements
- Must include proper documentation
- Must follow Home Assistant integration guidelines
- Must handle errors gracefully
- Must respect rate limits
