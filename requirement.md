# Functional Requirements for draw_app

## Overview
This document describes the main functionalities implemented in the current version of the `draw_app` project, based on the code in `main.py` and related modules.

## 1. Whiteboard GUI
- Launches a graphical whiteboard window using PySide6.
- Allows drawing of lines, rectangles, ellipses, and curves.
- Supports remote drawing via signals and Socket.IO events.

## 2. Real-time Collaboration
- Integrates a FastAPI backend with Socket.IO for real-time communication.
- Multiple clients can connect and interact with the whiteboard simultaneously.
- All drawing actions are broadcast to connected clients.

## 3. REST API Endpoints
- **GET `/history`**: Returns the current drawing history of the whiteboard.
- **POST `/clear`**: Clears the whiteboard and its history, and notifies all clients.
- **POST `/draw_line`**: Draws a line on the whiteboard with specified start, width, height, and color.
- **POST `/draw_dotted_line`**: Draws a dotted line with specified start, width, height, color, and optional dot interval.
- **POST `/draw_ellipse`**: Draws an ellipse (circle) with specified center, radii, and color.
- **POST `/draw_circle`**: Draws a perfect circle with specified center position and radius.
- **POST `/draw_rect`**: Draws a rectangle with specified position, width, height, and color.
- **POST `/draw_curve`**: Draws a curve based on a list of points and a color.

## 4. Socket.IO Events
- **connect**: Sends the current drawing history to the newly connected client.
- **draw_shape**: Receives drawing data from a client and updates the whiteboard.
- **clear**: Clears the whiteboard for all clients.
- **disconnect**: Handles client disconnection events.

## 5. CORS and WebSocket Support
- CORS is enabled for all origins to allow cross-origin requests.
- WebSocket transport is used for efficient real-time updates.

## 6. Threaded Server Startup
- The FastAPI/Socket.IO server runs in a background thread, allowing the GUI to remain responsive.

## 7. Signal Handling
- Uses custom signals (`GraphicsSignals`) to connect backend events to GUI updates.

---
This document reflects the current implementation and may need updates as new features are added or existing ones are changed.
