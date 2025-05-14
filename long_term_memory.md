# Long Term Memory for Vibe Coding

## Purpose

This document serves as the long-term memory for this vibe coding project. It helps maintain context across sessions, track key decisions, document the current state of the project, and outline future goals or ideas.

Think of this as a living journal for your project, co-authored with your AI assistant.

## How to Use

*   **Record Key Decisions:** Why was a particular technology chosen? What alternatives were considered?
*   **Document Current State:** What services are running? What are their URLs/ports? What's the latest major feature implemented?
*   **Track Action Items/Todos:** What needs to be done next?
*   **Store Important Snippets:** Useful commands, configurations, or code snippets.
*   **Log significant changes or events.**
*   **Outline Project Goals:** What is the overall aim of this project?

Regularly update this file as the project evolves.

## Current Project Overview

VibeBox is a lightweight development environment designed to kickstart "vibe coding" projects. It provides a simple Docker Compose setup with example services that demonstrate how to create a containerized development environment.

The goal is to be able to quickly share and bootstrap new projects that follow the vibe coding methodology, emphasizing lightweight, containerized services with clear separation of concerns.

## Services

*   **Service Name:** `static_site`
    *   **Purpose:** Modern welcome page for VibeBox with information about the environment.
    *   **Tech Stack:** Nginx serving static HTML/CSS.
    *   **Access:** `http://localhost:8001` (when running locally via docker-compose)
*   **Service Name:** `flask_app`
    *   **Purpose:** Interactive ChatGPT-like demo with a simple Q&A system.
    *   **Tech Stack:** Python, Flask, Sessions for conversation tracking, OpenAI API integration.
    *   **Access:** `http://localhost:8002` (when running locally via docker-compose)
    *   **Features:** Dark mode interface, conversation history, OpenAI API integration (when API key is configured).
    *   **Configuration:** Requires OpenAI API key to be set in `docker-compose.yml` for full functionality.

## Key Decisions Log

*   **[Initial Setup]**: Created `vibebox_setup` kickstarter with basic services.
    *   **Decision:** Include both a static site and Flask app as examples.
    *   **Reasoning:** To demonstrate both simple static content serving and dynamic application development patterns.

*   **[Update]**: Redesigned the static site with a modern, edgy VibeBox welcome page.
    *   **Decision:** Used clean blues and whites with wave animations and feature boxes.
    *   **Reasoning:** To create a visually appealing landing page that matches the "vibe" in VibeBox and provides information about the environment.

*   **[Update]**: Transformed the Flask app into a ChatGPT-like interface.
    *   **Decision:** Implemented a dark-themed chat UI with a sidebar, message bubbles, and a simple response system.
    *   **Reasoning:** To showcase a more interactive application example and demonstrate session handling in Flask.

*   **[Update]**: Added OpenAI API integration to the Flask app.
    *   **Decision:** Allow the chat app to use OpenAI's API for more intelligent responses while keeping a fallback mode.
    *   **Reasoning:** To demonstrate how to integrate with external APIs while maintaining graceful degradation.

## Setting up the OpenAI API Key

To enable full AI capabilities for the Chat app:

1. Get an API key from OpenAI (https://platform.openai.com/api-keys)
2. Open `docker-compose.yml` and add your API key to the environment section:

```yaml
flask_app:
  # ... other configurations
  environment:
    - FLASK_APP=app.py
    - FLASK_RUN_HOST=0.0.0.0
    # Add your OpenAI API key here
    - OPENAI_API_KEY="sk-yourapikey"
```

3. Restart the container with:

```bash
docker-compose down
docker-compose up -d
```

## Usage Instructions

### Starting the Environment

```bash
cd vibebox_setup
docker-compose up -d
```

### Accessing Services
- Static Site: http://localhost:8001
- Chat Interface: http://localhost:8002

### Interacting with the Chat Demo
1. Visit http://localhost:8002
2. Type a message in the input field at the bottom
3. Try asking about VibeBox, vibe coding, or Docker Compose
4. Reset your chat session by visiting http://localhost:8002/reset

### Stopping the Environment

```bash
docker-compose down
```

## Future Ideas / Todo

*   Add a database service example (e.g., MongoDB or PostgreSQL).
*   Create more interactive examples for the Flask app.
*   Add a React or Vue.js frontend example.
*   Document how to add a new service to `docker-compose.yml`.
