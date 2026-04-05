# Civil Server - Node.js + Slint Rebuild

Pixel-perfect rebuild of the Civil Server application using Node.js and Slint.dev as a native Linux desktop replacement for the Python/Qt version.

## Features

- ✅ Pixel-perfect UI matching Python/Qt version
- ✅ Server process management (start/stop/sync)
- ✅ Configuration management
- ✅ Status updates with real-time feedback
- ✅ Cross-platform native desktop application

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

## Configuration

Configure server settings through the Configuration dialog:
- Port (default: 4567)
- Start command (default: node src/test-server.js)
- Project directory

## Development

- UI: Slint (.slint files)
- Backend: Node.js
- Build: Native compilation via Slint compiler

## Files

- `src/ui.slint` - Main window UI
- `src/config-dialog.slint` - Configuration dialog
- `src/about-dialog.slint` - About dialog
- `src/main.js` - Application entry point
- `src/server-manager.js` - Server process management
- `src/test-server.js` - Simple test server
