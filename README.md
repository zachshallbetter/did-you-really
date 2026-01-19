# One-By-One - Lightweight Pixel & Request Tracking Hub

One-By-One is a minimalist, high-performance Flask tracking server designed for orchestrating and logging request telemetry. It provides a specialized `/track` endpoint for capturing granular details (IP, User-Agent, Referer, and custom query arguments) from web interactions or tracking pixels.

## Core Features

- **Granular Request Logging**: Captures full request context including headers, base URLs, and custom parameters to a centralized `access.log`.
- **Pixel Tracking Bridge**: Integrated `add_tracking.py` utility for dynamically injecting tracking markers into documents (like resumes or PDFs).
- **Silent Operation**: Configured for minimal process overhead with buffered output management for long-running deployments.
- **Health Orchestration**: Built-in `/health` endpoint for monitoring server status in automated environments.
- **Secure Persistence**: Logs are structured and timestamped (ISO format) for easy secondary analysis or ingestion into data pipelines.

## Technical Implementation

- **Flask Engine**: Lightweight, efficient request handling on port `5001`.
- **Modular Data Capture**: Systematic logging of `request_data` using a rotating file handler strategy.
- **Document Tracking**: Research into "tracked" document versions (e.g., `Zachary-Shallbetter-Resume_tracked.pdf`) to monitor engagement.

## Future Research & Ideas

- **Real-Time Webhook Relay**: Automatically forward tracking events to a Discord or Slack channel for instant engagement alerts.
- **Browser Fingerprinting**: Incorporate lightweight client-side fingerprinting into the tracking pipeline for more accurate session correlation.
- **PDF Interaction Analytics**: Research embedding more complex tracking logic into PDF interactive elements (buttons, links) beyond simple pixel loads.
- **Visual Analytics Dashboard**: A simple companion dashboard to visualize "Hits over Time" and geographic distribution of tracking events.
