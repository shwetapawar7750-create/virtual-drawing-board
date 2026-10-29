"""
ui.py — Toolbar rendering and hit-testing for color/tool buttons.

Toolbar top la render hoto with color swatches, eraser, thickness,
aani status info (current color, mode, FPS).
"""

import cv2
import numpy as np
import config as cfg


class Toolbar:
    """Draws the toolbar and checks if a point clicks a button."""

    def __init__(self, width):
        self.width = width
        self.height = cfg.TOOLBAR_HEIGHT
        self.buttons = []  # list of {"label", "rect":(x1,y1,x2,y2), "color_name" or "action"}
        self._build_buttons()

    def _build_buttons(self):
        """Pre-compute button positions."""
        bw = 80   # button width
        bh = 50   # button height
        gap = 10
        x = gap
        y = (self.height - bh) // 2

        # Color buttons
        for name in cfg.COLOR_ORDER:
            self.buttons.append({
                "label": name,
                "rect": (x, y, x + bw, y + bh),
                "color_name": name,
                "action": "color",
            })
            x += bw + gap

        # Eraser button
        x += gap
        self.buttons.append({
            "label": "ERASER",
            "rect": (x, y, x + bw, y + bh),
            "action": "eraser",
        })
        x += bw + gap

        # Clear button
        self.buttons.append({
            "label": "CLEAR",
            "rect": (x, y, x + bw, y + bh),
            "action": "clear",
        })
        x += bw + gap

        # Undo button
        self.buttons.append({
            "label": "UNDO",
            "rect": (x, y, x + bw, y + bh),
            "action": "undo",
        })
        x += bw + gap

        # Save button
        self.buttons.append({
            "label": "SAVE",
            "rect": (x, y, x + bw, y + bh),
            "action": "save",
        })

    def draw(self, frame, active_color_name, eraser_on, thickness, fps, gesture):
        """Render the toolbar onto the frame."""
        # Dark background bar
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (40, 40, 40), -1)

        for btn in self.buttons:
            x1, y1, x2, y2 = btn["rect"]
            action = btn["action"]

            if action == "color":
                bgr = cfg.COLORS[btn["color_name"]]
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, -1)
                # Highlight active color
                if btn["color_name"] == active_color_name and not eraser_on:
                    cv2.rectangle(frame, (x1 - 3, y1 - 3), (x2 + 3, y2 + 3),
                                  (255, 255, 255), 3)
            else:
                # Tool buttons — grey background, white text
                bg = (80, 80, 80)
                if action == "eraser" and eraser_on:
                    bg = (0, 180, 180)  # highlight if active
                cv2.rectangle(frame, (x1, y1), (x2, y2), bg, -1)
                cv2.putText(frame, btn["label"], (x1 + 5, y2 - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Status text on the right
        status_x = self.width - 350
        cv2.putText(frame, f"Brush: {thickness}px", (status_x, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        cv2.putText(frame, f"FPS: {fps:.0f}", (status_x, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        mode_text = {"draw": "DRAWING", "cursor": "CURSOR", "none": "IDLE"}.get(gesture, "")
        cv2.putText(frame, f"Mode: {mode_text}", (status_x, 72),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0) if gesture == "draw" else (200, 200, 200), 1)

    def hit_test(self, x, y):
        """If (x, y) is inside a button, return its dict; else None."""
        if y > self.height:
            return None
        for btn in self.buttons:
            x1, y1, x2, y2 = btn["rect"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                return btn
        return None


def draw_instructions(frame, y_start):
    """Overlay keyboard/gesture help at bottom of frame."""
    instructions = [
        "Index finger = DRAW | Index+Middle = CURSOR/SELECT | Fist = PAUSE",
        "Keys: Q=Quit  C=Clear  Z=Undo  S=Save  E=Eraser  R=Reset  +/-=Brush size",
    ]
    for i, text in enumerate(instructions):
        cv2.putText(frame, text, (10, y_start + i * 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1, cv2.LINE_AA)
