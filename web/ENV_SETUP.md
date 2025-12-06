# Environment Variables Setup

## Quick Setup

1. **Copy the example file:**
   ```bash
   cd web
   cp .env.local.example .env.local
   ```

2. **Get your Supabase credentials:**
   - Go to: https://supabase.com/dashboard/project/_/settings/api
   - Copy your **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - Copy your **anon/public key** (starts with `eyJ...`)

3. **Edit `.env.local` and add your credentials:**
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   NEXT_PUBLIC_API_URL=http://localhost:5001
   ```
   
   **Note:** `NEXT_PUBLIC_API_URL` is optional. If not set, it defaults to `http://localhost:5001` (port 5001 is used to avoid conflict with macOS AirPlay Receiver on port 5000). Update this if your backend API is running on a different URL.

4. **Restart your Next.js dev server:**
   ```bash
   # Stop the server (Ctrl+C) and restart
   npm run dev
   ```

## Important Notes

- `.env.local` is already in `.gitignore` - your credentials won't be committed
- Never commit your Supabase keys to version control
- The `NEXT_PUBLIC_` prefix makes these variables available in the browser
- After changing `.env.local`, you must restart the dev server

## Troubleshooting

If you still see the error after setting up `.env.local`:

1. Make sure the file is named exactly `.env.local` (not `.env` or `.env.local.txt`)
2. Make sure the file is in the `web/` directory (same level as `package.json`)
3. Restart your dev server completely
4. Check that there are no typos in the variable names
5. Make sure there are no quotes around the values (unless they're part of the actual value)

