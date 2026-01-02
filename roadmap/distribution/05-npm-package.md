# npm Package (Node.js Wrapper)

## Implementation Status
**✅ IMPLEMENTED** (v0.9.0-beta.2)

## Implementation Details

- **Package Location:** `npm-package/`
- **CLI Wrapper:** `npm-package/bin/cli.js`
- **Programmatic API:** `npm-package/lib/index.js`
- **TypeScript Definitions:** `npm-package/types/index.d.ts`
- **CI/CD Workflow:** `.github/workflows/npm-publish.yml`

## 1. Feature Description

This feature provides an npm package that wraps the git-chronoscope functionality, making it accessible to the JavaScript/Node.js ecosystem.

## 2. Intended Functionality

- Install globally: `npm install -g git-chronoscope`
- Install as project dependency: `npm install git-chronoscope`
- CLI available after installation: `npx git-chronoscope`
- JavaScript API for programmatic use:
  ```javascript
  const chronoscope = require('git-chronoscope');
  await chronoscope.generate('/path/to/repo', 'output.mp4');
  ```
- Works with existing Node.js toolchains

## 3. Requirements

- **Dependencies:**
    - Node.js wrapper around Python CLI
    - package.json with proper metadata
    - Bundled Python interpreter or system dependency
- npm account for publishing
- TypeScript type definitions for IDE support
- CI/CD for automated publishing

## 4. Limitations

- Still requires Python as a dependency (unless bundled)
- Two runtimes (Node.js + Python) may complicate debugging
- Version synchronization between npm and Python packages
- Platform-specific considerations for bundled binaries
