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

## Common Pitfalls & Best Practices (for VibeBox Users)

This section is based on lessons learned from more complex setups. Following these can save you a lot of time!

### 1. Docker Container Startup Issues: "My app isn't working!"

If a service in your `docker-compose.yml` doesn't seem to start correctly (e.g., the website it serves is down, or `docker-compose ps` shows it as 'Restarting' or 'Exited'):

*   **Check the Logs First:** The very first step is always `docker-compose logs <service_name>`. For example, if your `flask_app` isn't working, run `docker-compose logs flask_app`. This usually tells you *why* it's failing.
*   **Silent Failures (No Logs?):**
    *   Sometimes, an app fails so fast it doesn't produce logs. Try running its command *interactively*.
    *   Look at your `Dockerfile` for the service (e.g., `services/hello_flask_app/Dockerfile`). Find the `CMD` or `ENTRYPOINT` line.
    *   Example: If `flask_app`'s `CMD` is `["python", "app.py"]`, try:
        ```bash
        # First, stop the compose version to free up ports/names
        docker-compose stop flask_app 
        # Then, run it interactively. Adjust image name if needed (usually <project_dir>_<service_name>)
        # Adjust volume mounts and ports to match docker-compose.yml
        docker run --rm -it -p 8002:5000 -v ./services/hello_flask_app:/app vibebox_setup-flask_app python app.py 
        ```
    *   This direct run often shows errors that `docker-compose logs` might miss.
*   **Port Conflicts:**
    *   If a service fails to start and mentions "port already in use" or similar, another process (maybe another Docker container, or a native application on your machine) is using the *host* port.
    *   Check `docker ps` for other containers. Check your system for other services.
    *   Ensure the host ports in `docker-compose.yml` (e.g., ` "8001:80"` - `8001` is the host port) are unique and available.

### 2. Nginx Proxy & SSL (If you add this later)

VibeBox currently doesn't include a central Nginx reverse proxy or SSL by default, but if you add one (like the main VPS setup this is based on):

*   **Service Discovery (Host Not Found):**
    *   If Nginx reports "host not found" for an upstream service (e.g., `proxy_pass http://my_cool_app:5000;` and Nginx can't find `my_cool_app`):
        1.  Make sure `my_cool_app` is defined in `docker-compose.yml` and is **running** (`docker-compose ps my_cool_app`).
        2.  Ensure Nginx and `my_cool_app` are on the same Docker network (Compose usually handles this by default with a `default` network for the project).
        3.  In your Nginx service definition in `docker-compose.yml`, use `depends_on: [my_cool_app]` to help Docker start them in the right order.
*   **SSL Certificate Management (Simplified):**
    *   **Where Certs Live (if using Certbot on the host):** Certbot (a common tool for free Let's Encrypt SSL certificates) stores live certs in `/etc/letsencrypt/live/yourdomain.com/`.
    *   **Making Certs Available to Nginx Container:**
        *   Create a `./certs/yourdomain.com/` directory in your project.
        *   Copy `fullchain.pem` and `privkey.pem` from `/etc/letsencrypt/live/yourdomain.com/` into it.
        *   In `docker-compose.yml`, for your Nginx service, add a volume: `- ./certs:/etc/nginx/certs:ro` (read-only is safer).
    *   **Nginx Config:** In your Nginx site config file (e.g., `my_site.conf`):
        ```nginx
        server {
            listen 443 ssl;
            server_name yourdomain.com;

            ssl_certificate /etc/nginx/certs/yourdomain.com/fullchain.pem;
            ssl_certificate_key /etc/nginx/certs/yourdomain.com/privkey.pem;
            # Consider adding: ssl_dhparam /etc/nginx/certs/ssl-dhparams.pem; (see advanced notes)

            # ... rest of your config ...
        }
        ```
    *   **Wildcard Certificates (`*.yourdomain.com`):** These are powerful but more complex to set up with Certbot (often need DNS changes). For VibeBox, start with specific domain certs (`yourdomain.com`, `app.yourdomain.com`) unless you're comfortable with advanced Certbot. If you *do* use a wildcard, make sure *all* related Nginx configs point to that *same* wildcard certificate.
    *   **SSL Browser Issues (If `curl` works but browser doesn't):** If server-side tests (`curl -IL https://yourdomain.com`) show SSL is fine, but your browser has issues, it's often your browser's cache. Try:
        *   Hard refresh (Ctrl+Shift+R or Cmd+Shift+R).
        *   Clearing cache for that site.
        *   Incognito/Private mode.

### 3. Understanding Docker Compose `command:` vs. Dockerfile `CMD`

*   The `Dockerfile` for a service (e.g., `services/hello_flask_app/Dockerfile`) usually has a `CMD` (or `ENTRYPOINT`) that specifies the default command to run when the container starts.
*   You can *override* this in `docker-compose.yml` using the `command:` directive for that service.
*   If a service is misbehaving, and you ran it interactively with an explicit command (like `docker run ... my_image python app.py`), and that *worked*, consider setting that exact command in `docker-compose.yml`'s `command:` field for that service. This ensures Compose runs it the same way.

    Example for `flask_app` (if its Dockerfile `CMD` was different or problematic):
    ```yaml
    flask_app:
      build: ./services/hello_flask_app
      ports:
        - "8002:5000"
      command: ["python", "app.py"] # Ensures this exact command is run
      # ... rest ...
    ```

### 4. Keep it Simple at First!

*   VibeBox is about getting a vibe quickly. Start with the basics provided.
*   If you expand (e.g., add Nginx proxy, SSL), do it one step at a time and test each step.
*   Refer back to this memory file!
