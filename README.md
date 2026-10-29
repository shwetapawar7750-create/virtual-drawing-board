# OpenCV Virtual Drawing Board Using Hand Gesture Recognition

## Abstract

A real-time virtual drawing board that lets you draw in the air using your index finger. The application captures your hand via webcam, tracks finger movements using MediaPipe, and reproduces them as strokes on a digital canvas overlaid on the camera feed. Built with Python, OpenCV, MediaPipe, and NumPy.

## Problem Statement

Traditional digital drawing requires a mouse, stylus, or touchscreen. This project enables touchless drawing using only a standard webcam and hand gestures — useful for presentations, education, accessibility, and creative experimentation.

## Objectives

- Detect and track hand landmarks in real-time via webcam.
- Recognize drawing vs. cursor gestures from finger positions.
- Render smooth, persistent strokes on a transparent canvas layer.
- Provide color selection, eraser, undo, clear, and save functionality.
- Display a toolbar and performance metrics on-screen.
- Handle errors (no camera, no hand detected) gracefully.

## Features

| # | Feature |
|---|---------|
| 1 | Real-time webcam feed (mirrored) |
| 2 | Hand landmark detection via MediaPipe |
| 3 | Index-finger tracking |
| 4 | Draw mode (index up, middle down) |
| 5 | Cursor mode (index + middle up — move without drawing) |
| 6 | 6 brush colors: red, green, blue, yellow, white, black |
| 7 | Adjustable brush thickness (+/- keys) |
| 8 | Eraser mode (E key or toolbar) |
| 9 | Clear all (C key or toolbar) |
| 10 | Undo last stroke (Z key or toolbar) |
| 11 | Save drawing as PNG (S key or toolbar) |
| 12 | Reset all settings (R key) |
| 13 | Live FPS counter |
| 14 | Quit with Q key |
| 15 | On-screen toolbar with clickable buttons (via cursor gesture) |
| 16 | Error handling for missing camera / no hand |
| 17 | On-screen instruction text |

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Computer Vision | OpenCV (opencv-python) |
| Hand Tracking | MediaPipe Hands |
| Array Ops | NumPy |
| GUI | OpenCV HighGUI (no extra framework needed) |

## Installation

### 1. Prerequisites

- Python 3.10 or 3.11 installed ([python.org](https://www.python.org/downloads/))
- A working webcam (built-in or USB)
- Windows 10/11, macOS, or Linux

### 2. Clone or download

```bash
cd your-workspace
# If cloned from git:
git clone <repo-url>
cd opencv_virtual_drawing_board

# Or just navigate to the project folder
cd opencv_virtual_drawing_board
```

### 3. Create virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify installation

```bash
python -c "import cv2; print('OpenCV', cv2.__version__)"
python -c "import mediapipe; print('MediaPipe', mediapipe.__version__)"
python -c "import numpy; print('NumPy', numpy.__version__)"
```

All three should print version numbers without errors.

## Project Structure

```
opencv_virtual_drawing_board/
├── main.py                # Entry point — main loop
├── hand_tracker.py        # Hand detection & gesture recognition
├── drawing_canvas.py      # Stroke storage, undo, render, save
├── ui.py                  # Toolbar rendering & button hit-testing
├── config.py              # All constants & settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── tests/
│   └── test_drawing_canvas.py   # Unit tests (no webcam needed)
└── output/                # Saved drawings (auto-created)
```

### File Purposes

| File | Role |
|------|------|
| `config.py` | Central place for colors, sizes, keys, thresholds. Change settings here only. |
| `hand_tracker.py` | Wraps MediaPipe Hands — detects landmarks, determines gesture (draw/cursor/none). |
| `drawing_canvas.py` | Manages stroke list, current stroke, undo/clear/save. Pure data — no webcam dependency. |
| `ui.py` | Draws the toolbar, handles button hit-testing, renders on-screen instructions. |
| `main.py` | Connects everything: reads webcam → tracks hand → updates canvas → renders UI → handles keys. |

## How to Run

```bash
cd opencv_virtual_drawing_board
python main.py
```

A window titled "Virtual Drawing Board" will open showing your webcam feed with a toolbar at the top.

## Controls & Gestures

### Hand Gestures

| Gesture | Fingers | Action |
|---------|---------|--------|
| ☝️ Draw | Index UP, middle DOWN | Draw on canvas |
| ✌️ Cursor | Index UP, middle UP | Move cursor / select toolbar buttons |
| ✊ Idle | All down (fist) or other | Pause — nothing drawn |

### Toolbar Buttons (use Cursor gesture to select)

Move your index+middle fingers over a toolbar button to activate it:
- **Color swatches** — switch brush color
- **ERASER** — toggle eraser mode
- **CLEAR** — remove all strokes
- **UNDO** — remove last stroke
- **SAVE** — save current drawing as PNG

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Q` | Quit |
| `C` | Clear canvas |
| `Z` | Undo last stroke |
| `S` | Save as PNG |
| `E` | Toggle eraser |
| `R` | Reset (clear + default settings) |
| `+` / `=` | Increase brush size |
| `-` | Decrease brush size |

## How It Works (Architecture)

```
Webcam Frame
    │
    ▼
┌──────────────┐
│ HandTracker  │──→ landmarks, gesture ("draw"/"cursor"/"none")
└──────────────┘
    │
    ▼
┌──────────────┐
│DrawingCanvas │──→ stores strokes, renders onto frame
└──────────────┘
    │
    ▼
┌──────────────┐
│   Toolbar    │──→ color/tool buttons, status display
└──────────────┘
    │
    ▼
  cv2.imshow() → displayed to user
```

1. **Frame capture**: Webcam frame is read and flipped (mirror effect).
2. **Hand detection**: MediaPipe finds 21 hand landmarks.
3. **Gesture recognition**: Finger-up flags determine draw/cursor/none mode.
4. **Drawing**: In draw mode, index-fingertip coordinates are added to the current stroke.
5. **Toolbar interaction**: In cursor mode, if fingertip is in the toolbar area, buttons are hit-tested.
6. **Rendering**: All completed + in-progress strokes are drawn onto the frame. Toolbar is overlaid.
7. **Display**: Final composited frame is shown. Keyboard input is checked.

### Stroke Management & Undo

Each stroke is a dict: `{"points": [(x,y),...], "color": (B,G,R), "thickness": int}`.
- Drawing → points are appended to the current stroke.
- Gesture changes from "draw" to anything else → stroke is finalized and added to the list.
- Undo → last stroke is popped from the list.
- This means strokes are separated naturally when you lift your hand or switch gesture.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Webcam open nahi zala" error | Check camera is connected. Try changing `CAMERA_INDEX` in `config.py` to 1 or 2. |
| Black/frozen window | Another app may be using the camera. Close it and retry. |
| Hand not detected | Ensure good lighting. Keep hand ~30–60 cm from camera. Move slowly. |
| Drawing has gaps | Move finger more slowly. Increase `TRACKING_CONFIDENCE` in `config.py`. |
| Strokes are too thin/thick | Use `+`/`-` keys or edit `BRUSH_THICKNESS_DEFAULT` in `config.py`. |
| Colors look wrong | OpenCV uses BGR, not RGB. Colors in `config.py` are already in BGR format. |
| MediaPipe import error | `pip install mediapipe>=0.10.9`. On older Python, try `pip install mediapipe==0.10.9`. |
| `cv2.imshow` doesn't work (WSL/SSH) | You need a display. Run on a machine with a monitor, not a headless server. |
| Saved image is black | The save captures the composited frame — make sure you have drawn something first. |

## Limitations

- Single-hand tracking only (configurable in `config.py`).
- Eraser draws black — works on dark backgrounds; on a saved image the erased area is black, not transparent.
- Toolbar buttons are selected by hovering (cursor gesture), not by clicking — accidental selection can happen.
- Works best with a plain, non-cluttered background and good lighting.
- No multi-touch or two-handed gestures.

## Future Enhancements

- **Shape recognition**: Auto-detect and snap circles, rectangles, lines.
- **Multi-hand support**: Draw with both hands simultaneously.
- **Layer system**: Multiple canvas layers with transparency.
- **Text tool**: Type text onto the canvas.
- **Canvas zoom/pan**: Navigate a larger canvas.
- **Network sharing**: Stream drawings over a network for collaborative whiteboarding.
- **Voice commands**: "Clear", "Undo", "Save" via speech recognition.
- **Custom backgrounds**: Load an image as the canvas background.
- **Pressure simulation**: Map finger speed to brush thickness for calligraphy effects.

---

## Project Report Outline (College Submission)

Use this structure for a formal report:

1. **Title Page** — Project name, student name, guide name, college, date.
2. **Certificate / Declaration**
3. **Acknowledgement**
4. **Abstract** — (use the abstract above)
5. **Table of Contents**
6. **Chapter 1: Introduction**
   - 1.1 Background & Motivation
   - 1.2 Problem Statement
   - 1.3 Objectives
   - 1.4 Scope
7. **Chapter 2: Literature Review**
   - 2.1 Hand Gesture Recognition Techniques
   - 2.2 MediaPipe Hands Architecture
   - 2.3 OpenCV in Real-Time Applications
   - 2.4 Comparison with Existing Systems
8. **Chapter 3: System Design & Methodology**
   - 3.1 System Architecture Diagram
   - 3.2 Data Flow Diagram
   - 3.3 Module Design (HandTracker, DrawingCanvas, Toolbar)
   - 3.4 Gesture Recognition Algorithm
9. **Chapter 4: Implementation**
   - 4.1 Environment Setup
   - 4.2 Module-wise Code Walkthrough
   - 4.3 Integration
   - 4.4 Screenshots
10. **Chapter 5: Testing**
    - 5.1 Unit Testing Results
    - 5.2 Manual Testing Checklist
    - 5.3 Performance Analysis (FPS, latency)
11. **Chapter 6: Results & Discussion**
    - Screenshots of the working application
    - Performance metrics
    - Observations
12. **Chapter 7: Conclusion & Future Work**
13. **References**
    - MediaPipe documentation
    - OpenCV documentation
    - Python official docs
    - Research papers on hand gesture recognition
14. **Appendix** — Full source code

---

## References

- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Python Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)

---

*Built as a capstone project demonstrating real-time computer vision and gesture-based interaction.*
