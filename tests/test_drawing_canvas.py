"""
tests/test_drawing_canvas.py — Unit tests for DrawingCanvas.

Webcam nahi lagat ya tests la — pure logic test hotat:
strokes, undo, clear, rendering.
"""

import sys
import os
import numpy as np

# Ensure project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from drawing_canvas import DrawingCanvas


def test_empty_canvas():
    c = DrawingCanvas(640, 480)
    assert c.stroke_count == 0
    assert not c.is_drawing


def test_stroke_lifecycle():
    c = DrawingCanvas(640, 480)
    c.start_stroke((255, 0, 0), 3)
    assert c.is_drawing

    c.add_point(10, 20)
    c.add_point(30, 40)
    c.end_stroke()

    assert not c.is_drawing
    assert c.stroke_count == 1


def test_single_point_stroke_discarded():
    """A stroke with only one point is not worth keeping."""
    c = DrawingCanvas(640, 480)
    c.start_stroke((0, 255, 0), 5)
    c.add_point(100, 100)
    c.end_stroke()
    assert c.stroke_count == 0  # discarded — needs >=2 points


def test_undo():
    c = DrawingCanvas(640, 480)
    # Two strokes
    for _ in range(2):
        c.start_stroke((0, 0, 255), 2)
        c.add_point(0, 0)
        c.add_point(10, 10)
        c.end_stroke()
    assert c.stroke_count == 2

    c.undo()
    assert c.stroke_count == 1

    c.undo()
    assert c.stroke_count == 0

    # Undo on empty should not crash
    c.undo()
    assert c.stroke_count == 0


def test_clear():
    c = DrawingCanvas(640, 480)
    c.start_stroke((255, 255, 255), 4)
    c.add_point(5, 5)
    c.add_point(50, 50)
    c.end_stroke()
    assert c.stroke_count == 1

    c.clear()
    assert c.stroke_count == 0
    assert not c.is_drawing


def test_render_does_not_crash():
    """Render onto a real numpy frame — should not throw."""
    c = DrawingCanvas(640, 480)
    c.start_stroke((0, 0, 255), 3)
    c.add_point(100, 100)
    c.add_point(200, 200)
    c.end_stroke()

    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    c.render(frame)  # should draw blue line on black frame
    # Verify at least some pixels changed
    assert frame.sum() > 0


def test_render_empty_canvas():
    c = DrawingCanvas(640, 480)
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    c.render(frame)
    assert frame.sum() == 0  # nothing drawn


def test_end_stroke_when_not_drawing():
    """end_stroke with no active stroke should be a no-op."""
    c = DrawingCanvas(640, 480)
    c.end_stroke()  # should not crash
    assert c.stroke_count == 0


# ── Run ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed.")
    sys.exit(0 if passed == len(tests) else 1)
