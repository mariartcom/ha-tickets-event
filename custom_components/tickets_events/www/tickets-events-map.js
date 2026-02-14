/**
 * Tickets & Events Map Card
 * Shows all events on an interactive map
 */

class TicketsEventsMapCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._config = {};
    this._hass = null;
    this._map = null;
    this._markers = [];
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
    const title = this._config.title || 'Events Map';
   const height = this._config.height || '400px';
    const defaultZoom = this._config.zoom || 12;

    this.shadowRoot.innerHTML = `
      ${this._getLeafletStyles()}
      ${this._getStyles()}
      <ha-card>
        <div class="card-header">${title}</div>
        <div class="card-content">
          <div id="events-map" class="events-map" style="height: ${height}"></div>
          <div class="map-legend">
            <div class="legend-item">
              <span class="legend-marker tour"></span> Tours
            </div>
            <div class="legend-item">
              <span class="legend-marker museum"></span> Museums
            </div>
            <div class="legend-item">
              <span class="legend-marker concert"></span> Concerts
            </div>
            <div class="legend-item">
              <span class="legend-marker attraction"></span> Attractions
            </div>
            <div class="legend-item">
              <span class="legend-marker food_tour"></span> Food Tours
            </div>
          </div>
          ${events.length === 0 ? '<div class="no-events">No events with location data</div>' : ''}
        </div>
      </ha-card>
    `;

    // Initialize map after render
    setTimeout(() => this._initMap(events, defaultZoom), 100);
  }

  _initMap(events, defaultZoom) {
    if (!window.L) {
      console.error('Leaflet library not loaded');
      return;
    }

    const mapContainer = this.shadowRoot.getElementById('events-map');
    if (!mapContainer) return;

    // Clear existing map
    if (this._map) {
      this._map.remove();
    }
    this._markers = [];

    // Get events with valid coordinates
    const eventsWithLocation = events.filter(e => e.latitude && e.longitude);
    
    if (eventsWithLocation.length === 0) {
      mapContainer.innerHTML = '<div style="padding: 40px; text-align: center; color: var(--secondary-text-color);">No events with location data available</div>';
      return;
    }

    // Calculate center point
    const centerLat = eventsWithLocation.reduce((sum, e) => sum + e.latitude, 0) / eventsWithLocation.length;
    const centerLng = eventsWithLocation.reduce((sum, e) => sum + e.longitude, 0) / eventsWithLocation.length;

    // Create map
    this._map = L.map(mapContainer).setView([centerLat, centerLng], defaultZoom);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(this._map);
    
    // Add markers for each event
    eventsWithLocation.forEach(event => {
      const markerColor = this._getMarkerColor(event.type);
      
      // Create custom icon
      const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div class="marker-pin" style="background-color: ${markerColor};">
                 <span class="marker-icon">${this._getMarkerIcon(event.type)}</span>
              </div>`,
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -40]
      });
      
      const marker = L.marker([event.latitude, event.longitude], { icon })
        .addTo(this._map);
      
      // Create popup content
      const popupContent = this._createPopupContent(event);
      marker.bindPopup(popupContent, {
        maxWidth: 300,
        className: 'event-popup'
      });
      
      this._markers.push(marker);
    });

    // Fit bounds to show all markers
    if (eventsWithLocation.length > 1) {
      const group = L.featureGroup(this._markers);
      this._map.fitBounds(group.getBounds().pad(0.1));
    }

    // Force map to redraw
    setTimeout(() => this._map.invalidateSize(), 100);
  }

  _createPopupContent(event) {
    const imageUrl = event.images && event.images.length > 0 ? event.images[0].url : '';
    const typeBadge = this._getTypeBadge(event.type);
    
    return `
      <div class="popup-content">
        ${imageUrl ? `<img src="${imageUrl}" alt="${event.title}" class="popup-image">` : ''}
        <div class="popup-body">
          ${typeBadge}
          <h3 class="popup-title">${event.title}</h3>
          <div class="popup-meta">
            ${event.rating ? `<span>⭐ ${event.rating.toFixed(1)}</span>` : ''}
            <span>📍 ${event.city || 'Unknown'}</span>
          </div>
          <div class="popup-price">${event.price ? `${event.price.toFixed(2)} ${event.currency || 'EUR'}` : 'Price N/A'}</div>
          <a href="${event.booking_url || event.booking_url_with_params}" target="_blank" class="popup-book-btn">
            🎫 Book Now
          </a>
        </div>
      </div>
    `;
  }

  _getMarkerColor(type) {
    const colorMap = {
      'tour': '#2196F3',
      'museum': '#9C27B0',
      'concert': '#E91E63',
      'attraction': '#FF9800',
      'food_tour': '#4CAF50',
      'show': '#F44336',
      'cruise': '#00BCD4'
    };
    return colorMap[type] || '#757575';
  }

  _getMarkerIcon(type) {
    const iconMap = {
      'tour': '🗺️',
      'museum': '🏛️',
      'concert': '🎵',
      'attraction': '🎡',
      'food_tour': '🍽️',
      'show': '🎭',
      'cruise': '⛴️'
    };
    return iconMap[type] || '📍';
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
        .events-map {
          width: 100%;
          border-radius: 12px;
          overflow: hidden;
          border: 2px solid var(--divider-color, #e0e0e0);
        }
        .map-legend {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-top: 12px;
          padding: 12px;
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 8px;
        }
        .legend-item {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 13px;
          color: var(--primary-text-color);
        }
        .legend-marker {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          border: 2px solid white;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .legend-marker.tour { background: #2196F3; }
        .legend-marker.museum { background: #9C27B0; }
        .legend-marker.concert { background: #E91E63; }
        .legend-marker.attraction { background: #FF9800; }
        .legend-marker.food_tour { background: #4CAF50; }
        .no-events {
          text-align: center;
          padding: 32px;
          color: var(--secondary-text-color);
          font-size: 16px;
        }

        /* Custom Marker Styles */
        .custom-marker {
          background: none;
          border: none;
        }
        .marker-pin {
          width: 30px;
          height: 30px;
          border-radius: 50% 50% 50% 0;
          background: #2196F3;
          position: absolute;
          transform: rotate(-45deg);
          left: 50%;
          top: 50%;
          margin: -20px 0 0 -15px;
          box-shadow: 0 3px 6px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2px solid white;
        }
        .marker-pin::after {
          content: '';
          width: 10px;
          height: 10px;
          background: white;
          border-radius: 50%;
          position: absolute;
        }
        .marker-icon {
          font-size: 16px;
          transform: rotate(45deg);
          position: relative;
          z-index: 1;
        }

        /* Popup Styles */
        :host ::ng-deep .event-popup .leaflet-popup-content-wrapper {
          padding: 0;
          border-radius: 12px;
          overflow: hidden;
        }
        :host ::ng-deep .event-popup .leaflet-popup-content {
          margin: 0;
          width: 280px !important;
        }
        .popup-content {
          display: flex;
          flex-direction: column;
        }
        .popup-image {
          width: 100%;
          height: 150px;
          object-fit: cover;
        }
        .popup-body {
          padding: 12px;
        }
        .type-badge {
          display: inline-block;
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 600;
          color: white;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: 8px;
        }
        .popup-title {
          font-size: 16px;
          font-weight: 600;
          margin: 0 0 8px 0;
          color: var(--primary-text-color);
          line-height: 1.3;
        }
        .popup-meta {
          display: flex;
          gap: 12px;
          font-size: 13px;
          color: var(--secondary-text-color);
          margin-bottom: 8px;
        }
        .popup-price {
          font-size: 18px;
          font-weight: 700;
          color: var(--primary-color);
          margin-bottom: 12px;
        }
        .popup-book-btn {
          display: block;
          text-align: center;
          padding: 10px;
          background: var(--primary-color);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          transition: all 0.2s ease;
        }
        .popup-book-btn:hover {
          background: var(--dark-primary-color);
          transform: scale(1.05);
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
          .map-legend {
            font-size: 12px;
            gap: 8px;
          }
          .events-map {
            min-height: 300px;
          }
        }
      </style>
    `;
  }

  getCardSize() {
    return 5;
  }
}

customElements.define('tickets-events-map', TicketsEventsMapCard);

// Register the card with Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'tickets-events-map',
  name: 'Tickets & Events Map',
  description: 'Display events on an interactive map',
  preview: true,
});
