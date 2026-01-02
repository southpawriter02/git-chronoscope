# Homebrew Tap for git-chronoscope

This repository contains the Homebrew formula for git-chronoscope.

## Installation

```bash
# Add the tap
brew tap user/git-chronoscope

# Install
brew install git-chronoscope
```

## Usage

After installation, you can use the `git-chronoscope` command:

```bash
git-chronoscope /path/to/repo output.mp4
```

## Updating

```bash
brew update
brew upgrade git-chronoscope
```

## Uninstalling

```bash
brew uninstall git-chronoscope
brew untap user/git-chronoscope
```

## From Source

To install from source without the tap:

```bash
brew install --build-from-source /path/to/Formula/git-chronoscope.rb
```
