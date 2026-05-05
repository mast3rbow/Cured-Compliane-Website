# Build Configuration Updates

## Changes Made

### 1. Node.js Version Control (`.nvmrc`)
- **File**: `.nvmrc`
- **Purpose**: Pins Node.js to v20.18.1 (LTS) for compatibility with native modules
- **Why**: `better-sqlite3@8.7.0` (TinaCMS dependency) fails to compile with Node.js v22.22.0 due to V8 API changes

### 2. Updated Dependencies (`package.json`)
- **@tinacms/cli**: `^1.5.52` → `^1.6.10` (latest stable)
- **@types/node**: `^22.1.0` → `^20.17.10` (matches Node.js v20 LTS)
- **Added engines field**: Enforces Node.js 18-22 and npm ≥9 for consistency

### 3. npm Configuration (`.npmrc`)
- **engine-strict=false**: Allows npm install even with engine mismatches (with warnings)
- **prefer-offline=true**: Speeds up installs using local cache
- **audit=false**: Reduces noise during CI/CD builds
- **loglevel=warn**: Cleaner output

### 4. GitHub Workflow Updates
- **actions/checkout**: v2 → v3 (current stable)
- **Added Node.js setup step**: Uses `.nvmrc` for consistent builds
- **Added npm caching**: Faster workflow runs

## Deprecated Package Warnings Resolved

The following warnings will be resolved by the TinaCMS update:
- ✅ `@babel/plugin-proposal-*` → Now uses transform versions
- ✅ `uuid@9.0.1` → Updated to v11+ via dependencies
- ✅ `lodash.get` → Modern TinaCMS uses optional chaining
- ✅ `glob@7.2.3` → Updated to secure version
- ✅ `better-sqlite3` → Newer version with Node.js 20 compatibility

## How to Apply These Changes Locally

### Option 1: Clean Install (Recommended)
```powershell
# Remove existing node_modules and lock files
Remove-Item -Path node_modules -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path package-lock.json -Force -ErrorAction SilentlyContinue

# Install NVM for Windows (if not already installed)
# Download from: https://github.com/coreybutler/nvm-windows/releases

# Use the correct Node.js version
nvm install 20.18.1
nvm use 20.18.1

# Verify Node.js version
node --version  # Should show v20.18.1

# Clean install
npm install

# Build the site
npm run css  # If using Gulp for CSS
hugo          # Build Hugo site
```

### Option 2: Quick Update
```powershell
# Use correct Node.js version
nvm use 20.18.1

# Update dependencies
npm update

# Rebuild native modules
npm rebuild

# Test build
hugo
```

## Azure Static Web Apps Build

The GitHub workflow now automatically:
1. Checks out code with submodules
2. Sets up Node.js v20.18.1 from `.nvmrc`
3. Caches npm dependencies for faster builds
4. Runs the Hugo build
5. Deploys to Azure

No manual intervention needed for CI/CD builds.

## Troubleshooting

### Issue: `better-sqlite3` still fails to compile
**Solution**: 
```powershell
# Ensure you're on Node.js 20
node --version

# Clear npm cache
npm cache clean --force

# Reinstall
Remove-Item node_modules -Recurse -Force
npm install
```

### Issue: `npm ERR! engine node`
**Solution**: The `engine-strict=false` in `.npmrc` allows this. If you want strict checking:
```powershell
# Edit .npmrc and set:
# engine-strict=true
```

### Issue: Build works locally but fails in Azure
**Solution**: 
- Check GitHub Actions secrets are set correctly
- Verify `.nvmrc` is committed to git
- Ensure workflow file has the Node.js setup step

## Alternative: Use Docker for Builds

If you want complete build reproducibility, consider adding a `Dockerfile`:

```dockerfile
FROM node:20.18.1-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN hugo --minify

FROM nginx:alpine
COPY --from=build /app/public /usr/share/nginx/html
```

## Verification

After applying changes, verify with:
```powershell
# Check Node version
node --version  # Should be v20.18.1

# Install dependencies
npm install

# Look for these success indicators:
# - No "gyp ERR!" messages
# - No "make: ***" errors
# - "added XXX packages" message

# Test Hugo build
hugo

# Should complete without errors
```

## Next Steps

1. ✅ Commit all new/modified files:
   - `.nvmrc`
   - `.npmrc`
   - `package.json`
   - `.github/workflows/azure-static-web-apps-mango-water-062935500.yml`
   - `BUILD.md` (this file)

2. ✅ Push to `public` branch to trigger Azure deployment

3. ✅ Monitor GitHub Actions for successful build

4. ✅ Consider adding `package-lock.json` to git for dependency locking after successful build
