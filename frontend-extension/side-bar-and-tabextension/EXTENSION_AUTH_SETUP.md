# Extension Authentication Setup

## Overview
The Chrome extension now supports authentication that syncs with the web application's Supabase database. Users can sign up/sign in from either the extension or the web app, and their session will be shared.

## Setup Instructions

### 1. Configure Supabase Credentials

The extension needs your Supabase credentials to connect to the same database as the web app. You have two options:

#### Option A: Manual Configuration (Recommended for first-time setup)

1. Open Chrome DevTools (F12) in any tab
2. Go to the Console tab
3. Run this command (replace with your actual Supabase credentials):

```javascript
chrome.storage.sync.set({
  supabaseUrl: 'https://your-project-id.supabase.co',
  supabaseKey: 'your-anon-key-here'
}, () => {
  console.log('Supabase credentials saved!');
});
```

#### Option B: Auto-sync from Web App (Future Enhancement)

When a user signs in on the web app, the credentials can be automatically synced to the extension. This requires additional implementation.

### 2. Get Your Supabase Credentials

1. Go to: https://supabase.com/dashboard/project/_/settings/api
2. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)

### 3. Test the Setup

1. Reload the extension in Chrome
2. Click the extension icon
3. You should see the sign in/sign up form
4. Sign up or sign in with your credentials
5. The session will be saved and persist across browser restarts

## How It Works

1. **Session Storage**: Authentication sessions are stored in `chrome.storage.local` and persist across browser restarts
2. **Shared Database**: The extension uses the same Supabase database as the web app
3. **Auto-sync**: When you sign in on the web app, you can use the same credentials in the extension (and vice versa)

## Features

- ✅ Sign up with email and password
- ✅ Sign in with email and password
- ✅ Session persistence across browser restarts
- ✅ Shared authentication with web app
- ✅ Automatic session restoration
- ✅ Sign out functionality

## Troubleshooting

### "Supabase library not loaded" error
- Make sure the Supabase CDN script is loaded in `popup.html`
- Check your internet connection
- Reload the extension

### "Supabase credentials not configured" error
- Run the manual configuration script (Option A above)
- Make sure you're using the correct Supabase URL and anon key

### Session not persisting
- Check that `chrome.storage` permission is in `manifest.json`
- Clear extension storage and sign in again

### Can't sign in after signing up
- Check your email for the confirmation link (if email confirmation is enabled in Supabase)
- Make sure you're using the same Supabase project for both extension and web app

