"""
main.py — Entry point. Ties webcam, hand tracking, canvas, and UI together.

He file run kela ki webcam ughdte, hand track hoto,
aani drawing board ready hoto. 'q' press karun exit kara.
"""

import sys
import time
import cv2
import numpy as np

import config as cfg
from hand_tracker import HandTracker
from drawing_canvas import DrawingCanvas
from ui import Toolbar, draw_instructions


def main():
    # ── Camera setup ────────────────────────────────────────────
    # Use DSHOW on Windows for reliable camera access
    cap = cv2.VideoCapture(cfg.CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        # Fallback to default backend if DSHOW fails
        cap = cv2.VideoCapture(cfg.CAMERA_INDEX)

    if not cap.isOpened():
        print("[ERROR] Webcam open nahi zala! Camera connect aahe ka te check kara.")
        print("        Doosra camera try karayche asel tar config.py madhil CAMERA_INDEX badla.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.CAMERA_HEIGHT)

    # Read one frame with retries (camera warm-up)
    ret = False
    test_frame = None
    for attempt in range(5):
        ret, test_frame = cap.read()
        if ret and test_frame is not None:
            break
        time.sleep(0.5)

    if not ret or test_frame is None:
        print("[ERROR] Camera varun frame read nahi hota. Camera busy/problem aahe ka check kara.")
        print("        Krupaye other apps (Zoom, Teams, Camera app) band kara.")
        cap.release()
        sys.exit(1)
    h, w = test_frame.shape[:2]
    print(f"[INFO] Camera ready: {w}x{h}")

    # ── Modules ─────────────────────────────────────────────────
    tracker = HandTracker()
    canvas = DrawingCanvas(w, h)
    toolbar = Toolbar(w)

    # ── State ───────────────────────────────────────────────────
    current_color_name = cfg.DEFAULT_COLOR
    current_color = cfg.COLORS[current_color_name]
    thickness = cfg.BRUSH_THICKNESS_DEFAULT
    eraser_on = False
    prev_gesture = "none"
    fps = 0.0
    prev_time = time.time()
    save_msg = ""          # transient "Saved!" message
    save_msg_until = 0.0   # timestamp until which to show it

    # ── Main loop ───────────────────────────────────────────────
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame read fail — retrying…")
            continue

        # Mirror so it feels natural (like a mirror)
        frame = cv2.flip(frame, 1)

        # ── FPS ─────────────────────────────────────────────────
        now = time.time()
        dt = now - prev_time
        if dt > 0:
            fps = cfg.FPS_SMOOTHING * fps + (1 - cfg.FPS_SMOOTHING) * (1.0 / dt)
        prev_time = now

        # ── Hand tracking ───────────────────────────────────────
        landmarks = tracker.process(frame)
        gesture = "none"

        if landmarks:
            tracker.draw_landmarks(frame, landmarks)
            gesture = tracker.get_gesture(landmarks)
            ix, iy = tracker.get_index_pos(landmarks, frame.shape)

            # ── Toolbar interaction (cursor mode) ───────────────
            if gesture == "cursor" and iy < toolbar.height:
                btn = toolbar.hit_test(ix, iy)
                if btn:
                    action = btn["action"]
                    if action == "color":
                        current_color_name = btn["color_name"]
                        current_color = cfg.COLORS[current_color_name]
                        eraser_on = False
                    elif action == "eraser":
                        eraser_on = not eraser_on
                    elif action == "clear":
                        canvas.clear()
                    elif action == "undo":
                        canvas.undo()
                    elif action == "save":
                        # Render clean frame for saving
                        _, save_frame = cap.read()
                        if save_frame is not None:
                            save_frame = cv2.flip(save_frame, 1)
                            canvas.render(save_frame)
                            path = canvas.save(save_frame)
                            save_msg = f"Saved: {path}"
                            save_msg_until = time.time() + 2.0
                            print(f"[INFO] {save_msg}")

            # ── Drawing ─────────────────────────────────────────
            if gesture == "draw" and iy > toolbar.height:
                draw_color = (0, 0, 0) if eraser_on else current_color
                draw_thick = cfg.ERASER_THICKNESS if eraser_on else thickness

                if not canvas.is_drawing:
                    canvas.start_stroke(draw_color, draw_thick)
                canvas.add_point(ix, iy)

                # Visual cursor
                cv2.circle(frame, (ix, iy), draw_thick // 2 + 2, draw_color, 2)
            else:
                # Not drawing → finish current stroke
                if canvas.is_drawing:
                    canvas.end_stroke()

            # Cursor indicator
            if gesture == "cursor":
                cv2.circle(frame, (ix, iy), 10, (255, 255, 0), 2)

        else:
            # No hand detected → end any active stroke
            if canvas.is_drawing:
                canvas.end_stroke()

        # ── Transition: end stroke when gesture changes ─────────
        if gesture != "draw" and prev_gesture == "draw":
            if canvas.is_drawing:
                canvas.end_stroke()
        prev_gesture = gesture

        # ── Render canvas strokes onto frame ────────────────────
        canvas.render(frame)

        # ── Toolbar overlay ─────────────────────────────────────
        toolbar.draw(frame, current_color_name, eraser_on, thickness, fps, gesture)

        # ── Instructions ────────────────────────────────────────
        draw_instructions(frame, h - 50)

        # ── Save notification ───────────────────────────────────
        if time.time() < save_msg_until:
            cv2.putText(frame, save_msg, (w // 2 - 150, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # ── Show ────────────────────────────────────────────────
        cv2.imshow(cfg.WINDOW_NAME, frame)

        # ── Keyboard input ──────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF

        if key == cfg.KEY_QUIT:
            break
        elif key == cfg.KEY_CLEAR:
            canvas.clear()
        elif key == cfg.KEY_UNDO:
            canvas.undo()
        elif key == cfg.KEY_ERASER:
            eraser_on = not eraser_on
        elif key == cfg.KEY_RESET:
            canvas.clear()
            current_color_name = cfg.DEFAULT_COLOR
            current_color = cfg.COLORS[current_color_name]
            thickness = cfg.BRUSH_THICKNESS_DEFAULT
            eraser_on = False
        elif key in (cfg.KEY_THICKNESS_UP, cfg.KEY_THICKNESS_UP_ALT):
            thickness = min(thickness + cfg.BRUSH_THICKNESS_STEP, cfg.BRUSH_THICKNESS_MAX)
        elif key == cfg.KEY_THICKNESS_DOWN:
            thickness = max(thickness - cfg.BRUSH_THICKNESS_STEP, cfg.BRUSH_THICKNESS_MIN)
        elif key == cfg.KEY_SAVE:
            save_frame = frame.copy()
            path = canvas.save(save_frame)
            save_msg = f"Saved: {path}"
            save_msg_until = time.time() + 2.0
            print(f"[INFO] {save_msg}")

    # ── Cleanup ─────────────────────────────────────────────────
    tracker.close()
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Application band zale. Bye!")


if __name__ == "__main__":
    main()
