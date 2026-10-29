"""
config.py — All constants and settings in one place.

Yethil sagle settings ahet: colors, brush size, window size, gestures.
Kuthlehi change karayche asel tar phakt hya file madhe kara.
"""

import numpy as np

# ─── Window & Camera ────────────────────────────────────────────
CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
WINDOW_NAME = "Virtual Drawing Board"

# ─── Toolbar ────────────────────────────────────────────────────
TOOLBAR_HEIGHT = 80  # pixels at top of frame

# Color palette: (B, G, R) format for OpenCV
COLORS = {
    "red":    (0, 0, 255),
    "green":  (0, 255, 0),
    "blue":   (255, 0, 0),
    "yellow": (0, 255, 255),
    "white":  (255, 255, 255),
    "black":  (0, 0, 0),
}
COLOR_ORDER = ["red", "green", "blue", "yellow", "white", "black"]
DEFAULT_COLOR = "blue"

# ─── Brush ──────────────────────────────────────────────────────
BRUSH_THICKNESS_MIN = 2
BRUSH_THICKNESS_MAX = 30
BRUSH_THICKNESS_DEFAULT = 5
BRUSH_THICKNESS_STEP = 2

ERASER_THICKNESS = 40  # eraser is thicker for convenience

# ─── Hand Tracking ──────────────────────────────────────────────
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7
MAX_HANDS = 1

# Landmark indices (MediaPipe hand model)
INDEX_TIP = 8
INDEX_PIP = 6
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
RING_PIP = 14
PINKY_TIP = 20
PINKY_PIP = 18
THUMB_TIP = 4
THUMB_IP = 3

# ─── Keyboard shortcuts ────────────────────────────────────────
KEY_QUIT = ord('q')
KEY_CLEAR = ord('c')
KEY_SAVE = ord('s')
KEY_UNDO = ord('z')
KEY_ERASER = ord('e')
KEY_RESET = ord('r')
KEY_THICKNESS_UP = ord('+')      # or '='
KEY_THICKNESS_UP_ALT = ord('=')
KEY_THICKNESS_DOWN = ord('-')

# ─── Gesture thresholds ────────────────────────────────────────
# "Drawing mode" = index finger up, middle finger down.
# "Cursor mode"  = index AND middle fingers up.
# This keeps it simple and reliable.

# ─── Misc ───────────────────────────────────────────────────────
SAVE_DIR = "output"
FPS_SMOOTHING = 0.9  # exponential moving average factor
