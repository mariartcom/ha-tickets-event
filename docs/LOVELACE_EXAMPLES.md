# Lovelace Card Examples

## Basic Event List

### Simple Entity Card

```yaml
type: entities
title: Today's Events in Bucharest
entities:
  - entity: sensor.tickets_events_today
    type: attribute
    attribute: destination_title
    name: Location
  - entity: sensor.tickets_events_today
    name: Total Events
```

### Event Details Card

```yaml
type: markdown
content: |
  ## Events in {{ state_attr('sensor.tickets_events_today', 'destination_title') }}
  
  **Total Events**: {{ states('sensor.tickets_events_today') }}
  
  **Currency**: {{ state_attr('sensor.tickets_events_today', 'currency') }}
  
  {% for event in state_attr('sensor.tickets_events_today', 'events')[:5] %}
  ### {{ event.title }}
  
  **Price**: {{ event.price }} {{ event.currency }} | **Rating**: ⭐ {{ event.rating }} ({{ event.rating_count }} reviews)
  
  {{ event.description }}
  
  [Book Now]({{ event.booking_url_with_params }})
  
  ---
  {% endfor %}
```

## Event Grid with Images

```yaml
type: grid
columns: 2
square: false
cards:
  - type: custom:button-card
    entity: sensor.tickets_events_today
    template: |
      [[[
        const events = entity.attributes.events || [];
        const event = events[0];
        if (!event) return 'No events';
        return `
          <div>
            <img src="${event.images[0].url}" style="width:100%">
            <h3>${event.title}</h3>
            <p>${event.price} ${event.currency}</p>
          </div>
        `;
      ]]]
```

## QR Code Display for TV

### Single Event QR Code

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # {{ state_attr('sensor.tickets_events_today', 'events')[0].title }}
      
      ![Event]({{ state_attr('sensor.tickets_events_today', 'events')[0].images[0].url }})
  
  - type: markdown
    content: |
      ## Scan to Book
      
      ![QR Code]({{ state_attr('sensor.tickets_events_today', 'events')[0].qr_code_data }})
  
  - type: markdown
    content: |
      **Price**: {{ state_attr('sensor.tickets_events_today', 'events')[0].price }} {{ state_attr('sensor.tickets_events_today', 'events')[0].currency }}
      
      **Rating**: {{ state_attr('sensor.tickets_events_today', 'events')[0].rating }} ⭐
```

### Rotating QR Codes

```yaml
type: custom:auto-entities
card:
  type: carousel
  cards_per_view: 1
  autoplay:
    delay: 10000
filter:
  template: |
    {% set events = state_attr('sensor.tickets_events_today', 'events') %}
    {% for event in events[:5] %}
      {
        "type": "markdown",
        "content": "# {{ event.title }}\n\n![QR]({{ event.qr_code_data }})\n\n**{{ event.price }} {{ event.currency }}**"
      },
    {% endfor %}
```

## Search Interface

### Input Text + Button

```yaml
type: vertical-stack
cards:
  - type: entities
    entities:
      - input_text.event_search_query
  
  - type: button
    name: Search Events
    tap_action:
      action: call-service
      service: tickets_events.search_events
      service_data:
        query: "{{ states('input_text.event_search_query') }}"
        currency: EUR
  
  - type: markdown
    content: |
      ## Search Results
      <!-- Results would be displayed here -->
```

### Search with Results

Add to `configuration.yaml`:
```yaml
input_text:
  event_search_query:
    name: Search Events
    icon: mdi:magnify
```

Lovelace card:
```yaml
type: vertical-stack
cards:
  - type: entities
    entities:
      - entity: input_text.event_search_query
        name: Search Query
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Museum
        tap_action:
          action: call-service
          service: tickets_events.search_events
          service_data:
            query: "museum"
      
      - type: button
        name: Castle
        tap_action:
          action: call-service
          service: tickets_events.search_events
          service_data:
            query: "castle"
      
      - type: button
        name: Tour
        tap_action:
          action: call-service
          service: tickets_events.search_events
          service_data:
            query: "tour"
```

## Date Filter

### Calendar View

```yaml
type: entities
title: Events Calendar
entities:
  - type: buttons
    entities:
      - entity: input_button.events_today
        name: Today
        tap_action:
          action: call-service
          service: tickets_events.get_events_by_date
          service_data:
            date_from: "{{ now().strftime('%Y-%m-%d') }}"
            date_to: "{{ now().strftime('%Y-%m-%d') }}"
      
      - entity: input_button.events_this_week
        name: This Week
        tap_action:
          action: call-service
          service: tickets_events.get_events_by_date
          service_data:
            date_from: "{{ now().strftime('%Y-%m-%d') }}"
            date_to: "{{ (now() + timedelta(days=7)).strftime('%Y-%m-%d') }}"
```

## Mobile-Optimized Card

### Compact List View

```yaml
type: custom:layout-card
layout_type: masonry
cards:
  {% for event in state_attr('sensor.tickets_events_today', 'events')[:10] %}
  - type: custom:button-card
    entity: sensor.tickets_events_today
    name: {{ event.title }}
    show_state: false
    styles:
      card:
        - background-image: url("{{ event.images[0].url }}")
        - background-size: cover
        - height: 120px
      name:
        - color: white
        - text-shadow: 0 0 10px black
        - font-weight: bold
    tap_action:
      action: url
      url_path: {{ event.booking_url_with_params }}
    custom_fields:
      price:
        card:
          type: custom:button-card
          name: {{ event.price }} {{ event.currency }}
          styles:
            card:
              - background: rgba(0,0,0,0.7)
              - padding: 5px
  {% endfor %}
```

## Dashboard for Tablets

### Full Event Dashboard

```yaml
type: custom:grid-layout
title: Events & Attractions
layout:
  grid-template-columns: 1fr 1fr 1fr
  grid-template-rows: auto
  grid-gap: 10px
cards:
  # Featured Event (Large)
  - type: picture
    image: {{ state_attr('sensor.tickets_events_today', 'events')[0].images[0].url }}
    title: {{ state_attr('sensor.tickets_events_today', 'events')[0].title }}
    grid-column: 1 / 3
    grid-row: 1 / 3
    tap_action:
      action: url
      url_path: {{ state_attr('sensor.tickets_events_today', 'events')[0].booking_url_with_params }}
  
  # Stats
  - type: glance
    entities:
      - entity: sensor.tickets_events_today
        name: Today
      - entity: sensor.tickets_events_nearby
        name: Nearby
    grid-column: 3
    grid-row: 1
  
  # Other events (Small cards)
  {% for event in state_attr('sensor.tickets_events_today', 'events')[1:7] %}
  - type: picture
    image: {{ event.images[0].url }}
    title: {{ event.title }}
    tap_action:
      action: url
      url_path: {{ event.booking_url_with_params }}
  {% endfor %}
```

## TV Display (Kiosk Mode)

### Full-Screen Event Showcase

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 3em; margin: 0;">{{ state_attr('sensor.tickets_events_today', 'events')[0].title }}</h1>
      </div>
  
  - type: markdown
    content: |
      <div style="text-align: center;">
        <img src="{{ state_attr('sensor.tickets_events_today', 'events')[0].images[0].url }}" style="max-width: 80%; height: auto;">
      </div>
  
  - type: markdown
    content: |
      <div style="display: flex; justify-content: space-around; padding: 40px;">
        <div style="text-align: center;">
          <h2>Scan to Book</h2>
          <img src="{{ state_attr('sensor.tickets_events_today', 'events')[0].qr_code_data }}" style="width: 400px;">
        </div>
        <div style="text-align: left; font-size: 1.5em;">
          <p><strong>Price:</strong> {{ state_attr('sensor.tickets_events_today', 'events')[0].price }} {{ state_attr('sensor.tickets_events_today', 'events')[0].currency }}</p>
          <p><strong>Rating:</strong> {{ state_attr('sensor.tickets_events_today', 'events')[0].rating }} ⭐ ({{ state_attr('sensor.tickets_events_today', 'events')[0].rating_count }} reviews)</p>
          <p>{{ state_attr('sensor.tickets_events_today', 'events')[0].description }}</p>
        </div>
      </div>
```

## Conditional Cards

### Show Events Only When Available

```yaml
type: conditional
conditions:
  - entity: sensor.tickets_events_today
    state_not: "0"
card:
  type: markdown
  content: |
    ## {{ states('sensor.tickets_events_today') }} Events Today!
    
    {% for event in state_attr('sensor.tickets_events_today', 'events')[:3] %}
    - **{{ event.title }}** - {{ event.price }} {{ event.currency }}
    {% endfor %}
```

## Custom Button with Service Call

### Quick Booking Button

```yaml
type: button
name: Book Top Event
icon: mdi:ticket
tap_action:
  action: call-service
  service: tickets_events.generate_booking_url
  service_data:
    event_id: {{ state_attr('sensor.tickets_events_today', 'events')[0].id }}
    date: "{{ now().strftime('%Y-%m-%d') }}"
    tickets:
      adult: 2
    currency: EUR
```

## Notes

- Some examples use custom cards (button-card, auto-entities, layout-card)
- Install these via HACS if needed
- Template syntax may need adjustment based on your Home Assistant version
- Test templates in Developer Tools → Template before using in cards
- For TV displays, use Kiosk mode browser extension
