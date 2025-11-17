# Deployment Guide - Advanced Phishing Detector

## Deploying to Render.com

Your current deployment: https://phishing-detector-98j4.onrender.com/

### Step 1: Update Your Repository

1. **Commit all changes to your Git repository:**
```bash
git add .
git commit -m "Add advanced phishing detection features"
git push origin main
```

### Step 2: Update Render Service

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Select your service**: `phishing-detector-98j4`
3. **Click "Manual Deploy"** → **"Deploy latest commit"**
4. **Wait for deployment** (5-10 minutes)

### Step 3: Verify Deployment

Test the API endpoint:
```bash
curl -X POST https://phishing-detector-98j4.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com", "advanced": true}'
```

### Step 4: Update Frontend

If you have a separate frontend deployment:
1. Update the API_URL in `frontend/script.js` (already done)
2. Deploy frontend to your hosting service (Netlify, Vercel, etc.)

## Environment Variables (Optional)

Add these to Render dashboard for enhanced features:

```
PHISHTANK_API_KEY=your_key_here
GOOGLE_SAFEBROWSING_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here
```

## Performance Optimization for Render

### 1. Increase Instance Resources
- Go to Settings → Instance Type
- Upgrade to "Standard" or "Pro" for better performance
- Free tier may timeout on complex analysis

### 2. Add Redis Cache (Optional)
```bash
# In Render dashboard, add Redis service
# Update app.py to use Redis for caching
```

### 3. Set Environment Variables
```
FLASK_ENV=production
WORKERS=2
TIMEOUT=120
```

## Monitoring & Logs

### View Logs
1. Go to your Render service
2. Click "Logs" tab
3. Monitor for errors or warnings

### Health Check
```bash
curl https://phishing-detector-98j4.onrender.com/health
```

## Troubleshooting

### Issue: Deployment Fails
**Solution**: Check build logs for missing dependencies
```bash
# Ensure requirements.txt is up to date
pip freeze > requirements.txt
```

### Issue: Timeout Errors
**Solution**: Increase timeout in render.yaml
```yaml
services:
  - type: web
    name: phishing-detector
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --timeout 120 --workers 2
```

### Issue: SSL Certificate Errors
**Solution**: Already handled with `verify=False` in requests

### Issue: Memory Errors
**Solution**: Upgrade Render instance or optimize code
- Reduce concurrent requests
- Clear objects after use
- Implement request queuing

## Cost Optimization

### Free Tier Limitations
- 750 hours/month
- Spins down after 15 minutes of inactivity
- Limited CPU and memory

### Recommendations
1. **Keep on Free Tier**: For testing and low traffic
2. **Upgrade to Starter ($7/mo)**: For production use
3. **Add Caching**: Reduce API calls and processing time

## Alternative Deployment Options

### 1. Heroku
```bash
# Create Procfile
web: gunicorn app:app --timeout 120

# Deploy
heroku create phishing-detector
git push heroku main
```

### 2. AWS Lambda (Serverless)
- Use Zappa or Serverless Framework
- Cost-effective for sporadic usage
- May have cold start delays

### 3. DigitalOcean App Platform
- Similar to Render
- $5/month starter tier
- Good performance

### 4. Google Cloud Run
- Pay per request
- Auto-scaling
- Good for variable traffic

## Security Considerations

### 1. Rate Limiting
Add to app.py:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # ... existing code
```

### 2. API Key Authentication
```python
@app.before_request
def check_api_key():
    if request.endpoint == 'predict':
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            return jsonify({'error': 'Unauthorized'}), 401
```

### 3. CORS Configuration
Already configured in app.py:
```python
CORS(app)  # Allow all origins
# Or restrict to specific domains:
# CORS(app, origins=['https://your-frontend.com'])
```

## Maintenance

### Regular Updates
1. **Update Dependencies**: Monthly
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

2. **Monitor Logs**: Weekly
- Check for errors
- Monitor response times
- Track usage patterns

3. **Security Patches**: As needed
- Update Python version
- Update vulnerable packages

### Backup Strategy
1. **Code**: Git repository (already done)
2. **Model Files**: Store in cloud storage
3. **Configuration**: Document all settings

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **Issue Tracker**: Create issues in your Git repo

## Next Steps

1. ✅ Deploy updated code to Render
2. ✅ Test all new features
3. ⏳ Obtain API keys for threat feeds (optional)
4. ⏳ Set up monitoring and alerts
5. ⏳ Implement caching for better performance
6. ⏳ Add rate limiting for production use

## Quick Deploy Checklist

- [ ] All code committed to Git
- [ ] requirements.txt updated
- [ ] Render service redeployed
- [ ] Health check passes
- [ ] Test basic prediction
- [ ] Test advanced features
- [ ] Frontend updated (if separate)
- [ ] Monitor logs for errors
- [ ] Document any issues
- [ ] Share with users!

---

**Current Status**: Ready to deploy! 🚀

Just push your code and trigger a manual deploy in Render dashboard.
