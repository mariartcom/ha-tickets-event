/**
 * Tickets & Events Card
 * Custom Lovelace card for displaying event information
 */

class TicketsEventsCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  set hass(hass) {
    this._hass = hass;
    
    if (!this.config) return;

    const entity = hass.states[this.config.entity];
    
    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div class="card-content">
            <p>Entity ${this.config.entity} not found.</p>
          </div>
        </ha-card>
      `;
      return;
    }

    const events = entity.attributes.events || [];
    const maxEvents = this.config.max_events || 5;
    const title = this.config.title || entity.attributes.destination_title || 'Events';
    const showImages = this.config.show_images !== false;
    const showRating = this.config.show_rating !== false;
    const showPrice = this.config.show_price !== false;

    this.shadowRoot.innerHTML = `
      <style>
        ha-card {
          padding: 16px;
        }
        .card-header {
          font-size: 24px;
          font-weight: 500;
          padding-bottom: 12px;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .header-icon {
          color: var(--primary-color);
        }
        .event-count {
          font-size: 14px;
          color: var(--secondary-text-color);
          margin-left: auto;
        }
        .events-container {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .event-card {
          border: 1px solid var(--divider-color);
          border-radius: 12px;
          padding: 16px;
          transition: all 0.3s ease;
          cursor: pointer;
          background: var(--card-background-color);
        }
        .event-card:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          transform: translateY(-2px);
        }
        .event-header {
          display: flex;
          gap: 16px;
          margin-bottom: 12px;
        }
        .event-image {
          width: 120px;
          height: 120px;
          border-radius: 8px;
          object-fit: cover;
          flex-shrink: 0;
        }
        .event-info {
          flex: 1;
          min-width: 0;
        }
        .event-title {
          font-size: 18px;
          font-weight: 600;
          margin: 0 0 8px 0;
          color: var(--primary-text-color);
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
        .event-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-bottom: 8px;
          font-size: 14px;
        }
        .event-meta-item {
          display: flex;
          align-items: center;
          gap: 4px;
          color: var(--secondary-text-color);
        }
        .meta-icon {
          font-size: 16px;
        }
        .event-description {
          font-size: 14px;
          color: var(--secondary-text-color);
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          margin-bottom: 12px;
          line-height: 1.4;
        }
        .event-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
        }
        .event-price {
          font-size: 20px;
          font-weight: 700;
          color: var(--primary-color);
        }
        .price-label {
          font-size: 12px;
          font-weight: 400;
          color: var(--secondary-text-color);
        }
        .event-rating {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 14px;
        }
        .stars {
          color: #ffa500;
          font-weight: 600;
        }
        .rating-count {
          color: var(--secondary-text-color);
          font-size: 12px;
        }
        .book-button {
          background: var(--primary-color);
          color: white;
          border: none;
          padding: 10px 24px;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          gap: 6px;
          text-decoration: none;
        }
        .book-button:hover {
          background: var(--primary-color);
          opacity: 0.9;
          transform: scale(1.05);
        }
        .book-button:active {
          transform: scale(0.98);
        }
        .event-type-badge {
          display: inline-block;
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .badge-tour { background: #e3f2fd; color: #1976d2; }
        .badge-museum { background: #f3e5f5; color: #7b1fa2; }
        .badge-attraction { background: #fff3e0; color: #f57c00; }
        .badge-concert { background: #fce4ec; color: #c2185b; }
        .badge-food_tour { background: #e8f5e9; color: #388e3c; }
        .badge-default { background: #f5f5f5; color: #616161; }
        .no-events {
          text-align: center;
          padding: 32px;
          color: var(--secondary-text-color);
        }
        .event-date {
          display: flex;
          align-items: center;
          gap: 4px;
          color: var(--primary-color);
          font-weight: 600;
        }
        @media (max-width: 600px) {
          .event-header {
            flex-direction: column;
          }
          .event-image {
            width: 100%;
            height: 180px;
          }
          .event-footer {
            flex-direction: column;
            align-items: flex-start;
          }
          .book-button {
            width: 100%;
            justify-content: center;
          }
        }
      </style>
      
      <ha-card>
        <div class="card-header">
          <span class="header-icon">🎫</span>
          ${title}
          <span class="event-count">${events.length} events</span>
        </div>
        <div class="events-container">
          ${events.length === 0 ? `
            <div class="no-events">
              <p>No events available</p>
            </div>
          ` : events.slice(0, maxEvents).map(event => this._renderEvent(event, showImages, showRating, showPrice)).join('')}
        </div>
      </ha-card>
    `;

    // Add click handlers for booking buttons
    this.shadowRoot.querySelectorAll('.book-button').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const url = btn.getAttribute('data-url');
        if (url) {
          window.open(url, '_blank');
        }
      });
    });

    // Add click handlers for event cards (show more info)
    this.shadowRoot.querySelectorAll('.event-card').forEach((card, index) => {
      card.addEventListener('click', () => {
        this._showEventDetails(events[index]);
      });
    });
  }

  _renderEvent(event, showImages, showRating, showPrice) {
    const image = event.images && event.images[0] ? event.images[0].url : '';
    const price = event.price || 0;
    const currency = event.currency || 'EUR';
    const rating = event.rating || 0;
    const ratingCount = event.rating_count || 0;
    const type = event.type || 'event';
    const date = event.date || '';
    const bookingUrl = event.booking_url_with_params || event.booking_url || '#';
    
    const badgeClass = `badge-${type.replace('_', '-')}`;
    
    return `
      <div class="event-card" data-event-id="${event.id}">
        <div class="event-header">
          ${showImages && image ? `
            <img class="event-image" src="${image}" alt="${event.title}" loading="lazy" />
          ` : ''}
          <div class="event-info">
            <h3 class="event-title">${event.title}</h3>
            <div class="event-meta">
              <span class="event-type-badge ${badgeClass}">${type.replace('_', ' ')}</span>
              ${date ? `
                <span class="event-date">
                  <span class="meta-icon">📅</span>
                  ${this._formatDate(date)}
                </span>
              ` : ''}
              ${showRating && rating > 0 ? `
                <div class="event-rating">
                  <span class="stars">⭐ ${rating}</span>
                  <span class="rating-count">(${ratingCount})</span>
                </div>
              ` : ''}
            </div>
            <div class="event-meta">
              <span class="event-meta-item">
                <span class="meta-icon">📍</span>
                ${event.city}, ${event.country}
              </span>
            </div>
          </div>
        </div>
        <p class="event-description">${event.description || ''}</p>
        <div class="event-footer">
          ${showPrice ? `
            <div class="event-price">
              ${price > 0 ? `${price.toFixed(2)} ${currency}` : 'Free'}
              ${price > 0 ? `<span class="price-label">per person</span>` : ''}
            </div>
          ` : ''}
          <button class="book-button" data-url="${bookingUrl}">
            🎫 Book Now
          </button>
        </div>
      </div>
    `;
  }

  _formatDate(dateStr) {
    try {
      const date = new Date(dateStr);
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      // Reset times to compare dates only
      today.setHours(0, 0, 0, 0);
      tomorrow.setHours(0, 0, 0, 0);
      const eventDate = new Date(date);
      eventDate.setHours(0, 0, 0, 0);
      
      if (eventDate.getTime() === today.getTime()) {
        return 'Today';
      } else if (eventDate.getTime() === tomorrow.getTime()) {
        return 'Tomorrow';
      } else {
        return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      }
    } catch (e) {
      return dateStr;
    }
  }

  _showEventDetails(event) {
    // Dispatch custom event for showing details
    const moreInfoEvent = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: {
        entityId: this.config.entity,
      },
    });
    this.dispatchEvent(moreInfoEvent);
  }

  getCardSize() {
    const entity = this._hass?.states[this.config.entity];
    const events = entity?.attributes?.events || [];
    const maxEvents = this.config.max_events || 5;
    return Math.min(events.length, maxEvents) * 3 + 1;
  }
}

customElements.define('tickets-events-card', TicketsEventsCard);

// Register the card with Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'tickets-events-card',
  name: 'Tickets & Events Card',
  description: 'Display events with beautiful cards and booking buttons',
  preview: true,
});

console.info(
  '%c TICKETS-EVENTS-CARD %c v1.0.0 ',
  'color: white; background: #039be5; font-weight: 700;',
  'color: #039be5; background: white; font-weight: 700;',
);
