# ⚠️ IMPORTANT: Supabase Key Format

## Issue with Current Key

The key in your `config.js` is:
```
anonKey: 'sb_publishable_XBxznv1BKp3aXGkR9sPcTg_d6A8L9j3'
```

This appears to be a **publishable key**, not the **anon/public key** that Supabase uses for authentication.

## Correct Key Format

The **anon/public key** should:
- Start with `eyJ` (it's a JWT token)
- Look like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN5ZmljcnVjd2N2YXZkY3NsbnRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM0NTY3ODAsImV4cCI6MjA0OTAzMjc4MH0...`

## How to Get the Correct Key

1. Go to: https://supabase.com/dashboard/project/_/settings/api
2. Look for **"anon public"** key (NOT "publishable key")
3. Copy the key that starts with `eyJ...`
4. Update `config.js` with the correct key

## Example

```javascript
const SUPABASE_CONFIG = {
  url: 'https://syficrucwcvavdcslntd.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...', // This should start with eyJ
};
```

## Why This Matters

The extension uses the Supabase client library which requires the **anon key** (JWT token) for authentication. The publishable key won't work for auth operations.

