# Extension Configuration Setup

## Quick Setup

To connect the extension to your Supabase database (same as the web app), you need to copy your Supabase credentials from `web/.env.local` to `config.js`.

### Step 1: Get Your Supabase Credentials

Open `web/.env.local` and copy:
- `NEXT_PUBLIC_SUPABASE_URL` → This is your Supabase URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` → This is your Supabase anon key

### Step 2: Update config.js

Open `frontend-extension/side-bar-and-tabextension/config.js` and replace:

```javascript
const SUPABASE_CONFIG = {
  url: 'YOUR_SUPABASE_URL_HERE', // Replace with your URL from .env.local
  anonKey: 'YOUR_SUPABASE_ANON_KEY_HERE', // Replace with your anon key from .env.local
};
```

**Example:**
```javascript
const SUPABASE_CONFIG = {
  url: 'https://syficrucwcvavdcslntd.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
};
```

### Step 3: Reload Extension

1. Open Chrome Extensions page (`chrome://extensions/`)
2. Find "Clueless-to-Careers-Agent"
3. Click the reload icon
4. Open the extension popup
5. You should now see the sign in/sign up form

## Authentication Required

**Important:** Users must sign in or sign up before using any extension features:
- ✅ Apply for Job button requires authentication
- ✅ Open Sidebar button requires authentication
- ✅ All features are protected behind authentication

## How It Works

1. **Config File**: The extension reads Supabase credentials from `config.js` (similar to how the web app reads from `.env.local`)
2. **Shared Database**: Both extension and web app use the same Supabase database
3. **Session Sync**: If you sign up in the extension, you can sign in on the web (and vice versa)
4. **Auto-save**: Credentials are saved to `chrome.storage.sync` for future use

## Troubleshooting

### "Supabase not configured" error
- Make sure you've updated `config.js` with your actual credentials
- Check that the URL and key are correct (no extra spaces or quotes)
- Reload the extension after updating `config.js`

### Can't sign in
- Make sure you're using the same Supabase project for both extension and web app
- Check that email confirmation is not required (or confirm your email first)
- Verify your credentials are correct

### Session not persisting
- Check browser console for errors
- Make sure `chrome.storage` permission is in `manifest.json`
- Try signing in again

