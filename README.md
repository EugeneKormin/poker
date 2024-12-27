Certainly! Here is the complete documentation with the client-side setup and usage details added:

---

# Poker Assistant System

The **Poker Assistant System** is an advanced solution designed to process poker game screen captures, analyze game states using machine learning models, and provide actionable advice via a locally hosted API. This project enables real-time gameplay monitoring, state management, and AI-driven decision-making, optimized for use in both 6-player and 8-player poker tables.

---

## Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Modules](#modules)
  - [Screen Capture](#screen-capture)
  - [Data Parsing](#data-parsing)
  - [AI Integration](#ai-integration)
  - [Utilities](#utilities)
- [Server-Side Setup](#server-side-setup)
- [Client-Side Setup](#client-side-setup)
- [Configuration](#configuration)
- [Considerations](#considerations)
- [License](#license)

---

## Features
- **Real-Time Screen Capture**: Captures poker game screens for data extraction.
- **State Management**: Tracks game elements such as player bets, pots, cards, and dealer positions.
- **Machine Learning Integration**: Leverages YOLO models for object detection on the game screen.
- **AI-Driven Advice**: Integrates with a local LLM API to provide poker advice based on the game state.
- **Flexible Table Layouts**: Supports both 6- and 8-player table configurations.
- **Redis Integration**: Stores and retrieves game state information for continuity and analysis.

---

## Architecture Overview
The system comprises several core components that work in unison to provide seamless poker game monitoring and analysis:
1. **ScreenCapture**: Captures game screen data via the Windows interface.
2. **PokerDataParser**: Extracts game-related data (e.g., bets, cards, pots, dealer position) from screen captures.
3. **Predictor**: Manages and executes YOLO models for object detection, specifically tailored to poker gameplay elements.
4. **PokerTableDistributor**: Maps detected objects (cards, bets, pots) to logical entities in the poker game (players, board, dealer).
5. **SLM**: Interacts with a local API to generate poker advice based on the game state.
6. **Utilities**: Includes helper functions for data processing, card sorting, and window management.

---

## Requirements
- **Python**: >= 3.8
- **Dependencies**:
  - `opencv-python`
  - `numpy`
  - `pywin32`
  - `ultralytics`
  - `redis`
  - `pyyaml`
- **Redis**: A running Redis server for storing and retrieving game data.
- **GPU**: CUDA-compatible GPU for optimal YOLO model performance (optional, see [Considerations](#considerations)).
- **Operating System**: Primarily tested on Windows. Linux version may be available upon request.

---

## Setup

### Clone the repository:
```bash
git clone https://github.com/EugeneKormin/poker.git
cd poker
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Configure Redis:
A Redis server has already been initialized on the developer's server. You do **not need to start Redis manually**. Ensure the system can access the Redis server running at `103.90.73.217` on port `6379`.

### Add YOLO models:
Place your YOLO model files (board, bet, pot, card detectors) in the `./client/models/` directory as specified in the `config.yaml`.

### Configure the system:
Edit `config.yaml` to match your environment configuration. The file contains paths to the model weights, server settings, and logging configurations.

---

## Usage

### 1. **Client-Side System**

The client-side application is responsible for real-time game monitoring and providing poker advice based on detected game elements. 

1. **Run the Poker Assistant System (Client-Side)**:
   Launch the client-side application to begin real-time game monitoring and advice:
   ```bash
   python -m client.Main
   ```

   The client will:
   - Continuously capture screenshots of the poker table.
   - Detect game elements (cards, bets, pots, etc.) and parse the game state.
   - Provide AI-driven advice based on the detected game state.

2. **Client-Side Modules**:
   - **ScreenCapture**: Captures the screen and processes game elements.
   - **PokerDataParser**: Parses the screen capture data for poker-related information.
   - **Predictor**: Uses YOLO-based models to detect cards, bets, and pots.
   - **SLM (State Management)**: Interacts with the backend API to get advice based on the current game state.

The client will continuously send the game state to the backend, where it will be processed and analyzed. It will then display the results as recommendations to the user.

### 2. **Server-Side System**

The backend server has already been set up and is running on the developer's remote server. This server:
   - Listens for updates via Redis.
   - Streams the detected game data to connected clients via the `/stream` endpoint.

---

## Server-Side Setup

### Dockerfile for Backend

The backend server has already been deployed on the developer's server. However, for reference, here is the **Dockerfile** used to set up the backend:

```dockerfile
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Flask server
CMD ["python", "Backend.py"]
```

This Dockerfile builds a containerized Flask backend server that listens on port 8001. However, as mentioned, **there is no need to run this manually**, as the backend is already operational on the developer's server.

### Backend (Flask Server)

The backend server is implemented in Flask and is responsible for receiving game state updates and streaming this data to the client via Server-Sent Events (SSE). 

The backend script (`Backend.py`) subscribes to a Redis channel for receiving game data updates and streams.

---

## Client-Side Setup

The **client-side** of the system is responsible for interacting with the user's poker table, capturing game data, and displaying advice based on the game state.

1. **Install Dependencies**:
   - The client requires all Python dependencies listed in the `requirements.txt` to function properly.

2. **Run the Client Application**:
   After the setup, you can launch the client application to start capturing and processing game data. The client will:
   - Continuously capture screenshots of the poker game window.
   - Use YOLO models to detect cards, bets, and pots.
   - Parse this data and send it to the backend server for analysis.

3. **Configuration**:
   You may need to adjust settings in the `config.yaml` to match your specific environment, such as:
   - Paths to the YOLO models.
   - Server address for the backend API.
   - Log file paths.

The **client-side** also includes utilities for managing screen capture regions, sorting cards, and organizing game state data. 

---

## Configuration

The `config.yaml` file is used to configure the system. Key parameters include model paths, server settings, and logging options.

```yaml
models:
  board_detector:
    path: './client/models/board_detector.pt'
  bet_detector:
    path: './client/models/bet_detector.pt'
  player-pot_detector:
    path: './client/models/pot_detector.pt'
  accepted_pot_detector:
    path: './client/models/accepted_pot_detector.pt'
  non_accepted_pot_detector:
    path: './client/models/non_accepted_pot_detector.pt'
  card_detector:
    path: './client/models/card_detector.pt'

server:
  url: '103.90.73.217'
  redis_port: '6379'

logging:
  level: 'INFO'
  path: '/var/log/poker_analyzer'
```

---

## Considerations

- **GPU Usage**: The YOLO models can be significantly accelerated using a CUDA-compatible GPU. Ensure that the system has access to a compatible GPU if optimal performance is required.
- **Cross-Platform**: The client-side has primarily been tested on Windows. If you're using a different operating system (e.g., Linux), additional adjustments may be required.
- **Redis Server**: The Redis server is already running on a remote server. Ensure that the client has access to this server to stream game data in real-time.

### Issues Identified
While the system is functional and operational, the following issues have been identified and require attention for a more polished production experience:

1. **Card Detection**:
   - The detection of Jacks, Queens, and Aces is occasionally inaccurate due to inconsistencies in the training data. This needs improvement, especially for better reliability in competitive settings.

2. **Bet Detection**:
   - The detection of 3 and 5 bets on the board is sometimes confused, leading to incorrect identification of bet amounts. This issue stems from a limited number of training images for certain bet types, which requires additional data to resolve.

3. **Player Pot Detection**:
   - In some cases, the player's pots for tables with 6 or 8 players are duplicated. This issue also arises from limited training data, causing the system to misinterpret certain areas of the screen.

### Solution Paths

