"""
drawing_canvas.py — Canvas state: strokes, undo, clear, save.

Canvas ek transparent layer aahe je webcam frame var overlay hoto.
Strokes as list-of-points store hotat for undo support.
"""

import os
import time
import numpy as np
import cv2
import config as cfg


class DrawingCanvas:
    """Manages the drawing surface, stroke history, and persistence."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Each stroke: {"points": [(x,y), ...], "color": (B,G,R), "thickness": int}
        self.strokes = []
        self._current_stroke = None

    # ── stroke lifecycle ────────────────────────────────────────

    def start_stroke(self, color, thickness):
        """Begin a new stroke with given color and thickness."""
        self._current_stroke = {
            "points": [],
            "color": color,
            "thickness": thickness,
        }

    def add_point(self, x, y):
        """Append a point to the current stroke."""
        if self._current_stroke is not None:
            self._current_stroke["points"].append((x, y))

    def end_stroke(self):
        """Finish the current stroke and store it."""
        if self._current_stroke and len(self._current_stroke["points"]) > 1:
            self.strokes.append(self._current_stroke)
        self._current_stroke = None

    # ── canvas operations ───────────────────────────────────────

    def undo(self):
        """Remove the last completed stroke."""
        if self.strokes:
            self.strokes.pop()

    def clear(self):
        """Remove all strokes."""
        self.strokes.clear()
        self._current_stroke = None

    # ── rendering ───────────────────────────────────────────────

    def render(self, frame):
        """Draw all strokes (and current in-progress stroke) onto frame.

        Directly modifies the frame in-place for speed.
        """
        for stroke in self.strokes:
            self._draw_stroke(frame, stroke)
        if self._current_stroke:
            self._draw_stroke(frame, self._current_stroke)

    @staticmethod
    def _draw_stroke(frame, stroke):
        """Draw a single stroke as connected line segments."""
        pts = stroke["points"]
        color = stroke["color"]
        thick = stroke["thickness"]
        for i in range(1, len(pts)):
            cv2.line(frame, pts[i - 1], pts[i], color, thick, cv2.LINE_AA)

    # ── save ────────────────────────────────────────────────────

    def save(self, frame):
        """Save current frame (with drawings) to output/ as PNG.

        Returns the saved file path.
        """
        os.makedirs(cfg.SAVE_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(cfg.SAVE_DIR, f"drawing_{timestamp}.png")
        cv2.imwrite(path, frame)
        return path

    # ── state queries ───────────────────────────────────────────

    @property
    def is_drawing(self):
        return self._current_stroke is not None

    @property
    def stroke_count(self):
        return len(self.strokes)
