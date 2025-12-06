# Update Database Schema

## Add resume_data column to profiles table

Run this SQL in Supabase SQL Editor to add the `resume_data` column:

```sql
-- Add resume_data column to store extracted resume information
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS resume_data TEXT;

-- Add a comment to document the column
COMMENT ON COLUMN profiles.resume_data IS 'JSON string containing extracted resume data (technical skills, experience, projects)';
```

This will allow the profile to store the extracted resume data (technical skills, experience, projects) so it persists across page refreshes.

