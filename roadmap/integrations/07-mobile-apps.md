# Mobile Apps (iOS/Android)

## Implementation Status
**⏳ NOT IMPLEMENTED**

## 1. Feature Description

This feature provides native mobile applications for iOS and Android that allow users to generate and view time-lapses on their mobile devices.

## 2. Intended Functionality

- Browse and select repositories (GitHub, GitLab integration)
- Configure generation options with mobile-friendly UI
- Cloud-based generation (mobile sends request to server)
- Push notifications when generation completes
- Built-in video player with playback controls
- Share to social media directly
- Offline viewing of downloaded time-lapses

## 3. Requirements

- **Dependencies:**
    - React Native or Flutter for cross-platform
    - Backend API for generation requests
    - Cloud storage for generated videos
    - Push notification service
- App Store and Google Play accounts
- OAuth integration for Git providers
- Responsive video player component

## 4. Limitations

- Generation must happen on server (mobile devices lack resources)
- App size constraints
- Platform-specific review processes
- Ongoing app maintenance for OS updates
- Internet connection required for generation
