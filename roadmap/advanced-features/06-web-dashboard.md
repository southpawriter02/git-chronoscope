# Web Dashboard (SaaS)

## Implementation Status
**⏳ NOT IMPLEMENTED**

## 1. Feature Description

This feature provides a hosted web application where users can generate time-lapses without installing any software. A freemium SaaS model for easy access.

## 2. Intended Functionality

- Web interface at chronoscope.io (example)
- GitHub/GitLab OAuth for private repository access
- Drag-and-drop or paste repository URL
- Interactive configuration UI:
    - Date range picker
    - Branch/tag selection
    - Output format and quality
    - Theme customization
- Generation queue with progress tracking
- Video preview and download
- Share links for generated videos

## 3. Requirements

- **Dependencies:**
    - Frontend framework (React, Vue, or Next.js)
    - Backend API (Python/FastAPI or Node.js)
    - Cloud storage for generated videos (S3, GCS)
    - Task queue (Celery, Bull)
- User authentication and authorization
- Subscription/billing system for paid tiers
- CDN for video delivery
- Horizontal scaling for generation workers

## 4. Limitations

- Infrastructure costs for compute and storage
- Generation time limited by server resources
- Free tier may have restrictions (public repos only, video length limits)
- Requires ongoing maintenance and monitoring
