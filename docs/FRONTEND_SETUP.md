# Frontend Resources Setup

## Automatic Setup via HACS

When you install this integration via HACS, the JavaScript files are automatically made available at:
- `/hacsfiles/tickets_events/tickets-events-card.js`
- `/hacsfiles/tickets_events/tickets-events-card-enhanced.js`
- `/hacsfiles/tickets_events/tickets-events-map.js`

**However, you need to register them once as Lovelace resources.**

## How to Add Resources (One-Time Setup)

### Method 1: Via UI (Recommended)

1. Go to **Settings** → **Dashboards** → **⋮** (three dots menu) → **Resources**
2. Click **"+ Add Resource"**
3. Add each card:

   **Basic Card:**
   - URL: `/hacsfiles/tickets_events/tickets-events-card.js`
   - Resource type: **JavaScript Module**

   **Enhanced Card (with Modal):**
   - URL: `/hacsfiles/tickets_events/tickets-events-card-enhanced.js`
   - Resource type: **JavaScript Module**

   **Map Card:**
   - URL: `/hacsfiles/tickets_events/tickets-events-map.js`
   - Resource type: **JavaScript Module**

4. Click **"Create"**

### Method 2: Via configuration.yaml

Add to your `configuration.yaml`:

```yaml
lovelace:
  mode: yaml
  resources:
    - url: /hacsfiles/tickets_events/tickets-events-card.js
      type: module
    - url: /hacsfiles/tickets_events/tickets-events-card-enhanced.js
      type: module
    - url: /hacsfiles/tickets_events/tickets-events-map.js
      type: module
```

**Note:** This method requires Lovelace to be in YAML mode.

### Method 3: Quick Add via Browser Console

For advanced users, paste this in your browser console on the Lovelace page:

```javascript
// Add all three cards at once
const cards = [
  'tickets-events-card.js',
  'tickets-events-card-enhanced.js',
  'tickets-events-map.js'
];

cards.forEach(async (card) => {
  await window.hassConnection.sendMessagePromise({
    type: 'lovelace/resources/create',
    res_type: 'module',
    res_url: `/hacsfiles/tickets_events/${card}`
  });
});

console.log('Cards registered! Refresh the page.');
```

Then refresh your browser.

## Why Manual Registration?

- **Integrations vs Plugins**: This is a full Home Assistant integration (with sensors, calendar, etc.) that also provides Lovelace cards
- **HACS Behavior**: HACS automatically serves the files but doesn't auto-register resources for integrations
- **Standalone plugin cards** (like button-card) auto-register, but **integration cards** require one-time manual setup
- **Updates**: Once registered, HACS updates the files automatically with the `?hacstag=` parameter for cache busting

## Verify Installation

After adding resources:
1. Go to **Settings** → **Dashboards** → **Resources**
2. You should see entries like:
   ```
   /hacsfiles/tickets_events/tickets-events-card.js?hacstag=XXXXXXXXX
   JavaScript Module
   ```
3. Clear browser cache (Ctrl+F5 / Cmd+Shift+R)
4. Edit a dashboard and click **"+ Add Card"**
5. Search for "Tickets Events" - the cards should appear!

## Troubleshooting

### Cards don't appear in card picker
1. Verify resources are added in **Settings** → **Dashboards** → **Resources**
2. Clear browser cache completely
3. Check browser console (F12) for JavaScript errors
4. Ensure file paths use `/hacsfiles/tickets_events/` (no `www`)

### Files not found (404 error)
1. Verify integration is installed via HACS
2. Restart Home Assistant
3. Check files exist in: `config/custom_components/tickets_events/www/`

### Cards show as "Custom element doesn't exist"
1. Ensure resource type is **JavaScript Module** (not "JavaScript")
2. Check for typos in URLs
3. Hard refresh browser (Ctrl+Shift+R)

## After Setup

Once resources are registered, you can:
- ✅ Add cards from the visual card picker
- ✅ Use card types in YAML dashboards
- ✅ Get automatic updates via HACS
- ✅ Cards will have cache-busting `?hacstag=` automatically

The one-time setup is complete, and everything works automatically afterward!
