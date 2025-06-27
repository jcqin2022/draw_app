```mermaid
graph TB
    subgraph Frontend["Frontend (PySide6 GUI)"]
        GUI["Whiteboard GUI"]
        GraphicsSignals["GraphicsSignals"]
    end

    subgraph Backend["Backend (FastAPI + Socket.IO)"]
        Server["FastAPI Server"]
        SocketIO["Socket.IO Server"]
        History["Drawing History"]
    end

    subgraph Components["Drawing Components"]
        Point["Point Module"]
        CurveShape["Curve Shape Module"]
        Menu["Menu Module"]
        Whiteboard["Whiteboard Module"]
    end

    %% Connections
    GUI --> GraphicsSignals
    GraphicsSignals --> Whiteboard
    Whiteboard --> Point
    Whiteboard --> CurveShape
    Whiteboard --> Menu
    
    Server --> History
    SocketIO --> History
    
    %% Communication flows
    Client1["Client 1"] -->|"WebSocket/\nSocket.IO"| SocketIO
    Client2["Client 2"] -->|"WebSocket/\nSocket.IO"| SocketIO
    Client3["Client 3"] -->|"REST API"| Server
    
    SocketIO -->|"Events"| GraphicsSignals
    Server -->|"Updates"| GraphicsSignals
    
    %% Data flow descriptions
    classDef frontend fill:#d4f1f4
    classDef backend fill:#e1f7d5
    classDef components fill:#f7e1d5
    classDef clients fill:#f1d4e5
    
    class Frontend,GUI,GraphicsSignals frontend
    class Backend,Server,SocketIO,History backend
    class Components,Point,CurveShape,Menu,Whiteboard components
    class Client1,Client2,Client3 clients

```

## Architecture Overview

This diagram illustrates the architecture of the draw_app application:

1. **Frontend Layer**
   - PySide6-based GUI for the whiteboard interface
   - GraphicsSignals for event handling between backend and GUI

2. **Backend Layer**
   - FastAPI server handling REST endpoints
   - Socket.IO server for real-time communication
   - Drawing history management

3. **Drawing Components**
   - Point module for coordinate handling
   - CurveShape module for drawing curves
   - Menu module for UI controls
   - Whiteboard module for main drawing functionality

4. **Client Communication**
   - WebSocket/Socket.IO for real-time updates
   - REST API for HTTP-based interactions
   - Multi-client support

5. **Data Flow**
   - Bidirectional communication between clients and server
   - Real-time updates via Socket.IO events
   - State synchronization across all connected clients
