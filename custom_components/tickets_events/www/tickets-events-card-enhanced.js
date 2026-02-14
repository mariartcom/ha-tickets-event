/**
 * Tickets & Events Card Enhanced
 * Custom Lovelace card with detail modal, map, QR codes, and booking
 */

class TicketsEventsCardEnhanced extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._config = {};
    this._hass = null;
    this._selectedEvent = null;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this._config = config;
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  render() {
    if (!this._config || !this._hass) return;

    const entity = this._hass.states[this._config.entity];
    
    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div class="card-content">
            <p>Entity ${this._config.entity} not found.</p>
          </div>
        </ha-card>
      `;
      return;
    }

    const events = entity.attributes.events || [];
    const maxEvents = this._config.max_events || 5;
    const title = this._config.title || entity.attributes.destination_title || 'Events';
    const showImages = this._config.show_images !== false;
    const showRating = this._config.show_rating !== false;
    const showPrice = this._config.show_price !== false;

    const limitedEvents = events.slice(0, maxEvents);

    this.shadowRoot.innerHTML = `
      ${this._getStyles()}
      ${this._getLeafletStyles()}
      <ha-card>
        <div class="card-header">${title}</div>
        <div class="card-content">
          <div class="events-list">
            ${limitedEvents.map((event, index) => this._renderEvent(event, index, showImages, showRating, showPrice)).join('')}
          </div>
          ${events.length === 0 ? '<div class="no-events">No events available</div>' : ''}
        </div>
      </ha-card>
      ${this._selectedEvent ? this._renderDetailModal() : ''}
    `;

    // Attach event listeners
    this._attachEventListeners();
  }

  _renderEvent(event, index, showImages, showRating, showPrice) {
    const imageUrl = showImages && event.images && event.images.length > 0 ? event.images[0].url : '';
    const typeBadge = this._getTypeBadge(event.type);
    const dateFormatted = this._formatDate(event.date);

    return `
      <div class="event-card" data-event-index="${index}">
        ${imageUrl ? `<img src="${imageUrl}" alt="${event.title}" class="event-image">` : ''}
        <div class="event-content">
          <div class="event-header">
            ${typeBadge}
            <div class="event-date">${dateFormatted}</div>
          </div>
          <h3 class="event-title">${event.title}</h3>
          <div class="event-meta">
            ${showRating && event.rating ? `
              <div class="event-meta-item">
                <span class="meta-icon">⭐</span>
                <span>${event.rating.toFixed(1)} (${event.rating_count || 0})</span>
              </div>
            ` : ''}
            <div class="event-meta-item">
              <span class="meta-icon">📍</span>
              <span>${event.city || 'Unknown'}</span>
            </div>
          </div>
          <p class="event-description">${event.description || ''}</p>
          <div class="event-footer">
            ${showPrice ? `
              <div class="event-price">
                ${event.price ? `${event.price.toFixed(2)} ${event.currency || 'EUR'}` : 'N/A'}
              </div>
            ` : ''}
            <button class="book-btn view-details-btn" data-event-index="${index}">
              View Details
            </button>
          </div>
        </div>
      </div>
    `;
  }

  _renderDetailModal() {
    if (!this._selectedEvent) return '';

    const event = this._selectedEvent;
    const imageUrl = event.images && event.images.length > 0 ? event.images[0].url : '';
    const typeBadge = this._getTypeBadge(event.type);
    const dateFormatted = this._formatDate(event.date);
    const hasLocation = event.latitude && event.longitude;

    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <button class="modal-close">&times;</button>
          
          <div class="modal-header">
            ${imageUrl ? `<img src="${imageUrl}" alt="${event.title}" class="modal-image">` : ''}
            <div class="modal-header-content">
              ${typeBadge}
              <h2 class="modal-title">${event.title}</h2>
              <div class="modal-meta">
                <span class="meta-icon">📅</span> ${dateFormatted}
                <span style="margin: 0 8px;">•</span>
                <span class="meta-icon">📍</span> ${event.city || 'Unknown'}, ${event.country || ''}
              </div>
              ${event.rating ? `
                <div class="modal-rating">
                  <span class="meta-icon">⭐</span>
                  <span>${event.rating.toFixed(1)} / 5</span>
                  <span class="rating-count">(${event.rating_count || 0} reviews)</span>
                </div>
              ` : ''}
            </div>
          </div>

          <div class="modal-body">
            ${hasLocation ? `
              <div class="map-section">
                <h3>📍 Location</h3>
                <div id="event-map" class="event-map" data-lat="${event.latitude}" data-lng="${event.longitude}"></div>
              </div>
            ` : ''}

            <div class="description-section">
              <h3>📖 Description</h3>
              <p>${event.description || 'No description available.'}</p>
            </div>

            <div class="booking-section">
              <h3>🎫 Booking Information</h3>
              <div class="booking-grid">
                <div class="booking-info">
                  <div class="price-display">
                    <span class="price-label">Price</span>
                    <span class="price-value">${event.price ? `${event.price.toFixed(2)} ${event.currency || 'EUR'}` : 'N/A'}</span>
                  </div>
                  ${event.available_dates && event.available_dates.length > 0 ? `
                    <div class="availability">
                      <span class="availability-label">Available Dates:</span>
                      <div class="dates-list">
                        ${event.available_dates.slice(0, 3).map(date => `<span class="date-chip">${this._formatDate(date)}</span>`).join('')}
                        ${event.available_dates.length > 3 ? `<span class="date-chip">+${event.available_dates.length - 3} more</span>` : ''}
                      </div>
                    </div>
                  ` : ''}
                </div>
                <div class="qr-code-section">
                  <div class="qr-code-placeholder">
                    ${event.qr_code_data ? `<img src="${event.qr_code_data}" alt="QR Code">` : `
                      <svg viewBox="0 0 100 100" width="150" height="150">
                        <rect x="10" y="10" width="15" height="15" fill="#000"/>
                        <rect x="30" y="10" width="5" height="5" fill="#000"/>
                        <rect x="40" y="10" width="10" height="10" fill="#000"/>
                        <rect x="55" y="10" width="5" height="5" fill="#000"/>
                        <rect x="65" y="10" width="10" height="10" fill="#000"/>
                        <rect x="10" y="30" width="5" height="5" fill="#000"/>
                        <rect x="20" y="30" width="5" height="5" fill="#000"/>
                        <rect x="30" y="30" width="15" height="15" fill="#000"/>
                        <rect x="50" y="30" width="10" height="10" fill="#000"/>
                        <rect x="65" y="30" width="5" height="5" fill="#000"/>
                        <rect x="75" y="30" width="15" height="15" fill="#000"/>
                        <rect x="10" y="50" width="10" height="10" fill="#000"/>
                        <rect x="25" y="50" width="15" height="15" fill="#000"/>
                        <rect x="45" y="50" width="5" height="5" fill="#000"/>
                        <rect x="55" y="50" width="10" height="10" fill="#000"/>
                        <rect x="70" y="50" width="5" height="5" fill="#000"/>
                        <rect x="10" y="70" width="15" height="15" fill="#000"/>
                        <rect x="30" y="70" width="10" height="10" fill="#000"/>
                        <rect x="45" y="70" width="15" height="15" fill="#000"/>
                        <rect x="65" y="70" width="5" height="5" fill="#000"/>
                        <rect x="75" y="70" width="10" height="10" fill="#000"/>
                      </svg>
                    `}
                    <p class="qr-label">Scan to Book</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="book-btn book-now-btn" onclick="window.open('${event.booking_url || event.booking_url_with_params}', '_blank')">
              🎫 Book Tickets Now
            </button>
          </div>
        </div>
      </div>
    `;
  }

  _attachEventListeners() {
    // View Details buttons
    this.shadowRoot.querySelectorAll('.view-details-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.target.getAttribute('data-event-index'));
        const entity = this._hass.states[this._config.entity];
        const events = entity.attributes.events || [];
        this._selectedEvent = events[index];
        this.render();
        
        // Initialize map after render if location exists
        if (this._selectedEvent.latitude && this._selectedEvent.longitude) {
          setTimeout(() => this._initMap(), 100);
        }
      });
    });

    // Modal close button
    const closeBtn = this.shadowRoot.querySelector('.modal-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        this._selectedEvent = null;
        this.render();
      });
    }

    // Close modal when clicking overlay
    const overlay = this.shadowRoot.querySelector('.modal-overlay');
    if (overlay) {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          this._selectedEvent = null;
          this.render();
        }
      });
    }
  }

  _initMap() {
    if (!this._selectedEvent || !this._selectedEvent.latitude || !this._selectedEvent.longitude) return;
    
    const mapContainer = this.shadowRoot.getElementById('event-map');
    if (!mapContainer || !window.L) {
      console.warn('Leaflet library not loaded');
      return;
    }

    const lat = this._selectedEvent.latitude;
    const lng = this._selectedEvent.longitude;

    // Clear existing map
    mapContainer.innerHTML = '';
    
    // Create new map
    const map = L.map(mapContainer).setView([lat, lng], 15);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add marker
    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(`<b>${this._selectedEvent.title}</b><br>${this._selectedEvent.city}`).openPopup();
    
    // Force map to redraw
    setTimeout(() => map.invalidateSize(), 100);
  }

  _getTypeBadge(type) {
    const typeMap = {
      'tour': { label: 'Tour', color: '#2196F3' },
      'museum': { label: 'Museum', color: '#9C27B0' },
      'concert': { label: 'Concert', color: '#E91E63' },
      'attraction': { label: 'Attraction', color: '#FF9800' },
      'food_tour': { label: 'Food Tour', color: '#4CAF50' },
      'show': { label: 'Show', color: '#F44336' },
      'cruise': { label: 'Cruise', color: '#00BCD4' }
    };

    const typeInfo = typeMap[type] || { label: type || 'Event', color: '#757575' };
    return `<span class="type-badge" style="background-color: ${typeInfo.color};">${typeInfo.label}</span>`;
  }

  _formatDate(dateString) {
    if (!dateString) return 'Date TBA';
    
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return 'Tomorrow';
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
  }

  _getLeafletStyles() {
    return `
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    `;
  }

  _getStyles() {
    return `
      <style>
        * {
          box-sizing: border-box;
        }
        ha-card {
          padding: 16px;
        }
        .card-header {
          font-size: 24px;
          font-weight: bold;
          margin-bottom: 16px;
          color: var(--primary-text-color);
        }
        .card-content {
          padding: 0;
        }
        .events-list {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .event-card {
          display: flex;
          gap: 16px;
          padding: 16px;
          background: var(--card-background-color, #fff);
          border: 1px solid var(--divider-color, #e0e0e0);
          border-radius: 12px;
          transition: all 0.3s ease;
          cursor: pointer;
          overflow: hidden;
        }
        .event-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          border-color: var(--primary-color);
        }
        .event-image {
          width: 120px;
          height: 120px;
          object-fit: cover;
          border-radius: 8px;
          flex-shrink: 0;
        }
        .event-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          min-width: 0;
        }
        .event-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
          gap: 8px;
        }
        .type-badge {
          display: inline-block;
          padding: 4px 12px;
          border-radius: 16px;
          font-size: 12px;
          font-weight: 600;
          color: white;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .event-date {
          font-size: 13px;
          color: var(--secondary-text-color);
          font-weight: 500;
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
          margin-top: auto;
        }
        .event-price {
          font-size: 20px;
          font-weight: 700;
          color: var(--primary-color);
        }
        .book-btn {
          padding: 10px 20px;
          background: var(--primary-color);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .book-btn:hover {
          background: var(--dark-primary-color);
          transform: scale(1.05);
        }
        .view-details-btn {
          background: var(--primary-color);
        }
        .no-events {
          text-align: center;
          padding: 32px;
          color: var(--secondary-text-color);
          font-size: 16px;
        }

        /* Modal Styles */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9999;
          padding: 20px;
          overflow-y: auto;
        }
        .modal-content {
          background: var(--card-background-color, #fff);
          border-radius: 16px;
          max-width: 800px;
          width: 100%;
          max-height: 90vh;
          overflow-y: auto;
          position: relative;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .modal-close {
          position: absolute;
          top: 16px;
          right: 16px;
          background: rgba(0, 0, 0, 0.5);
          color: white;
          border: none;
          border-radius: 50%;
          width: 36px;
          height: 36px;
          font-size: 24px;
          cursor: pointer;
          z-index: 10;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background 0.2s;
        }
        .modal-close:hover {
          background: rgba(0, 0, 0, 0.8);
        }
        .modal-header {
          position: relative;
        }
        .modal-image {
          width: 100%;
          height: 300px;
          object-fit: cover;
          border-radius: 16px 16px 0 0;
        }
        .modal-header-content {
          padding: 24px;
        }
        .modal-title {
          font-size: 28px;
          font-weight: 700;
          margin: 12px 0;
          color: var(--primary-text-color);
        }
        .modal-meta {
          font-size: 16px;
          color: var(--secondary-text-color);
          margin-bottom: 8px;
        }
        .modal-rating {
          font-size: 18px;
          color: var(--primary-text-color);
        }
        .rating-count {
          color: var(--secondary-text-color);
          font-size: 14px;
          margin-left: 4px;
        }
        .modal-body {
          padding: 0 24px 24px;
        }
        .map-section,
        .description-section,
        .booking-section {
          margin-bottom: 24px;
        }
        .modal-body h3 {
          font-size: 20px;
          font-weight: 600;
          margin: 0 0 12px 0;
          color: var(--primary-text-color);
        }
        .event-map {
          width: 100%;
          height: 300px;
          border-radius: 12px;
          overflow: hidden;
          border: 2px solid var(--divider-color, #e0e0e0);
        }
        .description-section p {
          font-size: 16px;
          line-height: 1.6;
          color: var(--primary-text-color);
          margin: 0;
        }
        .booking-grid {
          display: grid;
          grid-template-columns: 1fr auto;
          gap: 24px;
          align-items: start;
        }
        .booking-info {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .price-display {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }
        .price-label {
          font-size: 14px;
          color: var(--secondary-text-color);
          font-weight: 500;
        }
        .price-value {
          font-size: 32px;
          font-weight: 700;
          color: var(--primary-color);
        }
        .availability {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .availability-label {
          font-size: 14px;
          color: var(--secondary-text-color);
          font-weight: 500;
        }
        .dates-list {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }
        .date-chip {
          padding: 6px 12px;
          background: var(--primary-color);
          color: white;
          border-radius: 16px;
          font-size: 13px;
          font-weight: 500;
        }
        .qr-code-section {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        .qr-code-placeholder {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          padding: 16px;
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 12px;
        }
        .qr-code-placeholder img,
        .qr-code-placeholder svg {
          width: 150px;
          height: 150px;
        }
        .qr-label {
          margin: 0;
          font-size: 14px;
          font-weight: 500;
          color: var(--secondary-text-color);
        }
        .modal-footer {
          padding: 24px;
          border-top: 1px solid var(--divider-color, #e0e0e0);
          display: flex;
          justify-content: center;
        }
        .book-now-btn {
          padding: 16px 48px;
          font-size: 18px;
          font-weight: 700;
          background: var(--primary-color);
          animation: pulse 2s infinite;
        }
        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
          .event-card {
            flex-direction: column;
          }
          .event-image {
            width: 100%;
            height: 200px;
          }
          .modal-content {
            margin: 10px;
          }
          .modal-image {
            height: 200px;
          }
          .booking-grid {
            grid-template-columns: 1fr;
          }
          .qr-code-section {
            order: -1;
          }
        }
      </style>
    `;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('tickets-events-card-enhanced', TicketsEventsCardEnhanced);

// Register the card with Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'tickets-events-card-enhanced',
  name: 'Tickets & Events Card Enhanced',
  description: 'Display events with detail modal, map, and booking features',
  preview: true,
});
