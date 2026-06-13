# InfCanvas

InfCanvas is a local infinite canvas for arranging images, adjusting crop, and saving/loading layouts.

## Requirements

- Windows
- Python 3 installed and available in PATH
- Microsoft Edge (used by the launcher script)

## Quick Start

1. Double-click `run_infcanvas.bat`.
2. When prompted for a layout folder, press Enter to use the default:
   - `C:\Apps\InfCanvas\`
3. The script starts:
   - A static file server on `http://localhost:8000`
   - A save/load server on `http://localhost:9000`
4. Edge opens to `http://localhost:8000/InfCanvas.html`.

## Basic Usage

- Drag and drop an image file onto the canvas to add it.
- Left click an image to select it.
- Drag selected image to move it.
- Drag empty canvas space to pan camera.
- Mouse wheel to zoom camera.
- Shift + mouse wheel to resize selected image.

## On-Screen Overlays (HUD)

- Top-right version badge shows the current app version from `VERSION`.
- Bottom-left tool badge shows key controls, selected layer, and crop values.
- Both overlays are visual-only right now (`pointer-events: none`), so they do not capture mouse hover/click events.

## Keyboard Shortcuts

### Save / Load

- `Ctrl+S`: Save current layout to a timestamped JSON file.
- `Ctrl+L`: Load newest saved layout.
- `Ctrl+Shift+L`: Load the second newest layout.
- `Ctrl+Alt+L`: Load the third newest layout.
- `Ctrl+ArrowDown`: Go back one layout (older) in save history.
- `Ctrl+ArrowUp`: Go forward one layout (newer) in save history.

### Selected Image Export

- `Ctrl+Alt+E`: Export selected image as PNG (with current crop applied).

### Layer Ordering (selected image)

- `Ctrl+]`: Bring selected layer forward by one.
- `Ctrl+[`: Send selected layer backward by one.
- `Ctrl+Shift+]`: Bring selected layer to front.
- `Ctrl+Shift+[`: Send selected layer to back.
- Fallback keys:
  - `Ctrl+Shift+Home`: Bring selected layer to front.
  - `Ctrl+Shift+End`: Send selected layer to back.

### Crop Controls (selected image)

- `Alt+ArrowLeft`: Increase left crop by 10 px.
- `Alt+ArrowRight`: Increase right crop by 10 px.
- `Alt+ArrowUp`: Increase top crop by 10 px.
- `Alt+ArrowDown`: Increase bottom crop by 10 px.
- `Alt+Shift+ArrowLeft`: Reduce left crop by 10 px.
- `Alt+Shift+ArrowRight`: Reduce right crop by 10 px.
- `Alt+Shift+ArrowUp`: Reduce top crop by 10 px.
- `Alt+Shift+ArrowDown`: Reduce bottom crop by 10 px.
- `Alt+0`: Reset crop to full image.

### Z-Scan Mode (layer inspection)

- `Z`: Toggle Z-scan mode.
- `,`: Step to previous layer (while Z-scan is active).
- `.`: Step to next layer (while Z-scan is active).

## Save Files

- Saved layouts are written as:
  - `layout_YYYY-MM-DD_HH-MM-SS.json`
- Save location is the folder you provide at launcher prompt.

## Tips

- If save/load does not work, confirm `save_server.py` is running on port `9000`.
- If the app page does not load, confirm the static server is running on port `8000`.
- The bottom-left tool badge in the app shows key controls and selected layer/crop state.

## HTML, DOM, and Rendering Mental Model

- HTML source: blueprint text
- DOM: live object model built from the blueprint
- Rendered page: pixels painted from DOM + CSS + layout
- Once parsed, the DOM diverges from original HTML source. JavaScript can add/remove/change nodes without changing the original file text.
