# Debugging Guide

## Common Issues and Solutions

### 1. Recommendations Not Showing

**Symptoms:**
- "No recommendations available at the moment" message
- Empty recommendations list

**Debugging Steps:**

1. **Check Backend Logs:**
   - Look for "DEBUG: Loaded X job templates" message
   - Check for "DEBUG: Returning X recommendations" message
   - Look for any error messages

2. **Check Browser Console:**
   - Open Developer Tools (F12)
   - Go to Console tab
   - Look for "Recommendations API result:" log
   - Check for any error messages

3. **Check Network Tab:**
   - Open Developer Tools (F12)
   - Go to Network tab
   - Click "Get Recommendations"
   - Check the `/api/recommendations` request
   - Verify response status (should be 200)
   - Check response body for recommendations array

4. **Verify Backend is Running:**
   ```bash
   # Check if Flask server is running
   # Should see: "Running on http://localhost:5000"
   ```

5. **Test API Directly:**
   ```bash
   curl -X POST http://localhost:5000/api/recommendations \
     -H "Content-Type: application/json" \
     -d '{"resume_skills": [], "limit": 10}'
   ```

**Common Fixes:**
- Ensure Flask server is running
- Check that `data/job_templates.json` exists and has valid JSON
- Verify CORS is enabled (should be automatic)
- Check browser console for CORS errors

### 2. Dashboard Stuck Loading

**Symptoms:**
- Dashboard shows "..." or loading spinner
- Never displays data
- Page seems frozen

**Debugging Steps:**

1. **Check Loading Overlay:**
   - The loading overlay should hide after API call completes
   - If stuck, check browser console for errors

2. **Check Browser Console:**
   - Look for "Dashboard API result:" log
   - Check for JavaScript errors
   - Look for Chart.js errors

3. **Check Network Tab:**
   - Verify `/api/analytics` request completes
   - Check response status and body

4. **Verify Chart.js is Loaded:**
   - Check if Chart.js CDN is accessible
   - Look for Chart.js errors in console

**Common Fixes:**
- Refresh the page
- Check if Chart.js CDN is blocked
- Verify canvas element exists in HTML
- Check for JavaScript errors preventing execution

### 3. API Connection Issues

**Symptoms:**
- "Failed to fetch" errors
- Network errors in console
- CORS errors

**Solutions:**

1. **Verify Backend is Running:**
   ```bash
   python run.py
   # Should see: "Starting server on http://localhost:5000"
   ```

2. **Check API Base URL:**
   - In `frontend/js/api.js`, verify `API_BASE_URL` is correct
   - Should be: `http://localhost:5000/api`

3. **Check CORS:**
   - Backend should have CORS enabled (already configured)
   - If CORS errors, check Flask-CORS is installed

4. **Firewall/Antivirus:**
   - Some security software blocks localhost connections
   - Try disabling temporarily to test

### 4. Quick Test Commands

**Test Backend:**
```bash
# Start server
python run.py

# In another terminal, test API
curl http://localhost:5000/api/recommendations -X POST \
  -H "Content-Type: application/json" \
  -d '{"resume_skills": []}'
```

**Test Frontend:**
1. Open browser to `http://localhost:5000`
2. Open Developer Tools (F12)
3. Go to Console tab
4. Try clicking "Get Recommendations"
5. Check console logs and network requests

### 5. Reset Everything

If nothing works:

1. **Restart Backend:**
   ```bash
   # Stop server (Ctrl+C)
   # Start again
   python run.py
   ```

2. **Clear Browser Cache:**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Or clear browser cache

3. **Check File Permissions:**
   - Ensure `data/job_templates.json` is readable
   - Check file paths are correct

## Expected Behavior

### Recommendations:
- Should always return at least some jobs (even with 0% match)
- Without resume: Shows 10 jobs with base scores (5-15%)
- With resume: Shows jobs sorted by match percentage

### Dashboard:
- Should always display (never stuck loading)
- Without resume: Shows 0s and placeholder chart
- With resume: Shows actual analytics and chart

## Still Having Issues?

1. Check all console logs (browser and terminal)
2. Verify all files are saved
3. Restart both frontend and backend
4. Check for typos in console errors
5. Verify Python version is 3.12

