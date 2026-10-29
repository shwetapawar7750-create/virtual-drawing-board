"""
hand_tracker.py — Hand detection and gesture recognition using MediaPipe.

Ha module webcam frame gheun tyatun hand landmarks detect karto,
aani gesture (drawing / cursor / eraser) return karto.
"""

import mediapipe as mp
import cv2
import config as cfg


class HandTracker:
    """Detects one hand and reports finger states + index-finger position."""

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=cfg.MAX_HANDS,
            min_detection_confidence=cfg.DETECTION_CONFIDENCE,
            min_tracking_confidence=cfg.TRACKING_CONFIDENCE,
        )
        self.mp_draw = mp.solutions.drawing_utils

    # ── public API ──────────────────────────────────────────────

    def process(self, frame):
        """Run detection on a BGR frame.

        Returns:
            landmarks list (or None), the raw mediapipe results
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        if self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks[0]  # first hand
        return None

    def get_index_pos(self, landmarks, frame_shape):
        """Return (x, y) pixel position of index fingertip."""
        h, w, _ = frame_shape
        lm = landmarks.landmark[cfg.INDEX_TIP]
        return int(lm.x * w), int(lm.y * h)

    def fingers_up(self, landmarks):
        """Return list of booleans for [thumb, index, middle, ring, pinky].

        True = finger is up (tip above pip joint in y-axis).
        MediaPipe coordinates: y increases downward, so tip.y < pip.y ⇒ up.
        """
        lm = landmarks.landmark
        fingers = []

        # Thumb: compare x (works for right hand facing camera = mirrored).
        # Tip is more to the LEFT of IP joint in mirrored view ⇒ up.
        fingers.append(lm[cfg.THUMB_TIP].x < lm[cfg.THUMB_IP].x)

        # Index
        fingers.append(lm[cfg.INDEX_TIP].y < lm[cfg.INDEX_PIP].y)
        # Middle
        fingers.append(lm[cfg.MIDDLE_TIP].y < lm[cfg.MIDDLE_PIP].y)
        # Ring
        fingers.append(lm[cfg.RING_TIP].y < lm[cfg.RING_PIP].y)
        # Pinky
        fingers.append(lm[cfg.PINKY_TIP].y < lm[cfg.PINKY_PIP].y)

        return fingers

    def get_gesture(self, landmarks):
        """Determine gesture from finger states.

        Returns one of:
            "draw"   — index up, middle down  → draw on canvas
            "cursor" — index AND middle up     → move without drawing
            "none"   — anything else (fist, open palm, etc.)
        """
        up = self.fingers_up(landmarks)
        index_up = up[1]
        middle_up = up[2]

        if index_up and not middle_up:
            return "draw"
        if index_up and middle_up:
            return "cursor"
        return "none"

    def draw_landmarks(self, frame, landmarks):
        """Draw hand skeleton on frame (optional visual feedback)."""
        self.mp_draw.draw_landmarks(
            frame, landmarks, self.mp_hands.HAND_CONNECTIONS
        )

    def close(self):
        self.hands.close()
