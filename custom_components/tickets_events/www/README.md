# Tickets & Events Custom Card

A beautiful custom Lovelace card for displaying events with booking buttons.

## Installation

### Automatic (via Integration)

The card is automatically installed when you install the Tickets & Events integration via HACS.

### Manual Installation

1. Copy `tickets-events-card.js` to your `www` folder:
   ```
   /config/www/tickets-events-card.js
   ```

2. Add to your Lovelace resources:
   - Go to **Settings** → **Dashboards** → **⋮** (top right) → **Resources**
   - Click **+ Add Resource**
   - URL: `/local/tickets-events-card.js`
   - Resource type: **JavaScript Module**

## Usage

### Basic Configuration

```yaml
type: custom:tickets-events-card
entity: sensor.tickets_events_today
```

### Full Configuration

```yaml
type: custom:tickets-events-card
entity: sensor.tickets_events_today
title: "Today's Events"
max_events: 5
show_images: true
show_rating: true
show_price: true
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | **Required** | Entity ID (e.g., `sensor.tickets_events_today`) |
| `title` | string | Auto | Card title (uses destination name if not set) |
| `max_events` | number | `5` | Maximum number of events to display |
| `show_images` | boolean | `true` | Show event images |
| `show_rating` | boolean | `true` | Show event ratings |
| `show_price` | boolean | `true` | Show event prices |

## Features

### 🎨 Beautiful Design
- Modern card layout with hover effects
- Responsive design (mobile-friendly)
- Event images with rounded corners
- Type badges with color coding

### 📊 Rich Information
- Event title and description
- Event images
- Price and currency
- Rating and review count
- Event type badges (Tour, Museum, Concert, etc.)
- Location (City, Country)
- Date (Today, Tomorrow, or formatted date)

### 🔘 Interactive Elements
- **Book Now** button for each event
- Opens booking URL in new tab
- Click event card to see more details
- Hover effects for better UX

### 📱 Responsive
- Adapts to screen size
- Mobile-optimized layout
- Touch-friendly buttons

## Examples

### Today's Events
```yaml
type: custom:tickets-events-card
entity: sensor.tickets_events_today
title: "Happening Today"
max_events: 3
```

### Nearby Events (No Images)
```yaml
type: custom:tickets-events-card
entity: sensor.tickets_events_nearby
title: "Events Near You"
show_images: false
max_events: 10
```

### Price Comparison View
```yaml
type: custom:tickets-events-card
entity: sensor.tickets_events_today
title: "Compare Prices"
show_images: false
show_rating: false
show_price: true
```

### Multiple Cards Layout
```yaml
type: vertical-stack
cards:
  - type: custom:tickets-events-card
    entity: sensor.tickets_events_today
    title: "Today"
    max_events: 2
  
  - type: custom:tickets-events-card
    entity: sensor.tickets_events_nearby
    title: "This Week"
    max_events: 3
```

## Event Type Badges

The card automatically shows colored badges for different event types:

- 🔵 **Tour** - Blue
- 🟣 **Museum** - Purple
- 🟠 **Attraction** - Orange
- 🔴 **Concert** - Red
- 🟢 **Food Tour** - Green
- ⚫ **Other** - Grey

## Styling

The card uses Home Assistant theme variables and adapts to your theme automatically:
- `--primary-color` for accents
- `--card-background-color` for backgrounds
- `--primary-text-color` for main text
- `--secondary-text-color` for metadata

## Troubleshooting

### Card Not Loading

1. Clear browser cache (Ctrl+F5)
2. Verify resource is added in Lovelace
3. Check browser console for errors

### Events Not Showing

1. Verify entity has events data: Developer Tools → States → Check your entity
2. Ensure coordinator is fetching data successfully
3. Check Home Assistant logs for errors

### Images Not Loading

- Check if event has images in attributes
- Verify image URLs are accessible
- Try `show_images: false` to test without images

## Calendar Integration

Use alongside the calendar entity for date filtering:

```yaml
type: vertical-stack
cards:
  - type: calendar
    entities:
      - calendar.tickets_events_events_calendar
    initial_view: dayGridMonth
  
  - type: custom:tickets-events-card
    entity: sensor.tickets_events_today
    title: "Today's Events"
```

## Screenshots

### Desktop View
Events displayed with images, ratings, and booking buttons.

### Mobile View
Responsive layout stacks elements vertically for better mobile experience.

### Dark Theme
Card adapts to dark themes automatically.

## Support

For issues or feature requests, visit:
https://github.com/mariartcom/ha-tickets-event/issues
