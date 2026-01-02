#!/usr/bin/env node

/**
 * git-chronoscope CLI wrapper
 *
 * This is a Node.js wrapper around the Python git-chronoscope CLI.
 * It requires Python 3.7+ and the git-chronoscope Python package to be installed.
 */

const { spawn } = require('child_process');
const { checkDependencies, getPythonCommand } = require('../lib/utils');

const args = process.argv.slice(2);

// Handle --version flag specially to show npm package version too
if (args.includes('--version') || args.includes('-v')) {
  const pkg = require('../package.json');
  console.log(`git-chronoscope npm wrapper v${pkg.version}`);
  // Continue to show Python version as well
}

// Handle --help with additional npm-specific info
if (args.includes('--help') || args.includes('-h')) {
  console.log('git-chronoscope - Generate time-lapse visualizations of Git repositories\n');
  console.log('This is a Node.js wrapper. Python git-chronoscope must be installed.');
  console.log('Install: pip install git-chronoscope\n');
}

// Check dependencies before running
async function main() {
  try {
    const { pythonCmd, errors } = await checkDependencies();

    if (errors.length > 0) {
      console.error('\x1b[31mError: Missing dependencies\x1b[0m\n');
      errors.forEach(err => console.error(`  - ${err}`));
      console.error('\nPlease install the required dependencies:');
      console.error('  1. Python 3.7+: https://www.python.org/downloads/');
      console.error('  2. git-chronoscope: pip install git-chronoscope');
      console.error('  3. FFmpeg: https://ffmpeg.org/download.html');
      process.exit(1);
    }

    // Spawn the Python CLI
    const proc = spawn(pythonCmd, ['-m', 'src.main', ...args], {
      stdio: 'inherit',
      shell: process.platform === 'win32'
    });

    proc.on('error', (err) => {
      if (err.code === 'ENOENT') {
        console.error('\x1b[31mError: Could not find git-chronoscope.\x1b[0m');
        console.error('Please install: pip install git-chronoscope');
        process.exit(1);
      }
      console.error(`\x1b[31mError: ${err.message}\x1b[0m`);
      process.exit(1);
    });

    proc.on('close', (code) => {
      process.exit(code || 0);
    });

  } catch (err) {
    console.error(`\x1b[31mError: ${err.message}\x1b[0m`);
    process.exit(1);
  }
}

main();
