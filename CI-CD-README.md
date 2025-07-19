# MCSL Division H Championship - CI/CD Setup

This repository includes a comprehensive CI/CD pipeline for automated testing and deployment to Netlify.

## 🔧 Setup Instructions

### 1. GitHub Secrets Configuration

To enable automated Netlify deployments, add these secrets to your GitHub repository:

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Add the following repository secrets:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `NETLIFY_AUTH_TOKEN` | Netlify Personal Access Token | 1. Go to [Netlify User Settings](https://app.netlify.com/user/applications) 2. Click "New access token" 3. Copy the generated token |
| `NETLIFY_SITE_ID` | Netlify Site ID | 1. Go to your site dashboard on Netlify 2. Site settings > General 3. Copy the "Site ID" |

### 2. Netlify Configuration

The repository includes a `netlify.toml` file with optimal settings for the swim meet application:

```toml
[build]
  publish = "."
  
[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    
[[headers]]
  for = "*.js"
  [headers.values]
    Cache-Control = "public, max-age=86400"
    
[[headers]]
  for = "*.css"
  [headers.values]
    Cache-Control = "public, max-age=86400"
    
[[headers]]
  for = "*.html"
  [headers.values]
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "/sw.js"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🚀 CI/CD Pipeline

### Pipeline Stages

1. **Lint and Test** (runs on all PRs and pushes)
   - HTML validation with HTMLHint
   - JavaScript linting with ESLint
   - File structure validation
   - JSON validation
   - Basic functionality testing with Puppeteer
   - Accessibility testing with axe-core
   - Performance audit with Lighthouse

2. **Deploy Preview** (runs on PRs only)
   - Deploys to Netlify preview environment
   - Adds deployment URL as PR comment
   - Allows testing changes before merge

3. **Deploy Production** (runs on main branch pushes only)
   - Deploys to production Netlify site
   - Updates <https://finsdivisionals.netlify.app>

### Quality Gates

The pipeline includes several quality checks:

- **HTML Validation**: Ensures proper HTML5 structure
- **JavaScript Linting**: Maintains code quality standards
- **Accessibility**: Scans for WCAG compliance issues
- **Performance**: Lighthouse audit with minimum score thresholds:
  - Performance: 80+
  - Accessibility: 90+
  - Best Practices: 80+

### Test Coverage

Automated tests verify:

- ✅ Page loads on desktop and mobile
- ✅ Critical UI elements are present
- ✅ Search functionality works
- ✅ Navigation elements function
- ✅ Service worker registration
- ✅ PWA manifest validity
- ✅ Team color accessibility
- ✅ Mobile responsiveness

## 📊 Monitoring

### Build Status

Check the Actions tab in GitHub to monitor:

- Build success/failure status
- Test results and coverage
- Performance metrics
- Deployment status

### Netlify Dashboard

Monitor deployment and site analytics at:

- [Netlify Dashboard](https://app.netlify.com)
- Site URL: <https://finsdivisionals.netlify.app>

## 🛠️ Local Development

To run the same tests locally:

```bash
# Install dependencies
npm init -y
npm install --save-dev htmlhint eslint eslint-config-standard lighthouse puppeteer @axe-core/cli

# Run linting
npx htmlhint index.html
npx eslint index.html --ext .html

# Run tests
# (The test files are created dynamically in the CI pipeline)
```

## 🔄 Workflow Triggers

| Event | Trigger | Actions |
|-------|---------|---------|
| Push to `main` | ✅ | Full CI + Production Deploy |
| Pull Request | ✅ | Full CI + Preview Deploy |
| Manual | ✅ | Via GitHub Actions tab |

## 📝 Adding New Tests

To add new tests to the pipeline:

1. Edit `.github/workflows/ci-cd.yml`
2. Add test step under the `lint-and-test` job
3. Use the existing Puppeteer/Node.js setup for consistency

## 🚨 Troubleshooting

### Common Issues

1. **Missing Secrets**: Verify `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` are set
2. **Build Failures**: Check Actions tab for detailed error logs
3. **Deployment Issues**: Verify Netlify site is connected to repository
4. **Performance Issues**: Review Lighthouse recommendations in CI logs

### Support

For CI/CD issues:

1. Check the Actions tab for detailed logs
2. Review this README for configuration steps
3. Verify all secrets are properly configured
