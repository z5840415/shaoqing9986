import os
import time
import cv2
import mediapipe as mp
import pyautogui
from dotenv import load_dotenv


def main() -> None:
    """Run the air gesture control application."""
    load_dotenv()
    cam_index = int(os.getenv("CAM_INDEX", 0))
    alpha = float(os.getenv("SMOOTHING_ALPHA", 0.35))
    pinch_px = float(os.getenv("PINCH_PX", 40))
    long_pinch_sec = float(os.getenv("LONG_PINCH_SEC", 0.6))

    pyautogui.FAILSAFE = False
    try:
        screen_w, screen_h = pyautogui.size()
    except Exception as exc:  # permission issues on macOS
        print(f"PyAutoGUI is not permitted to control the mouse: {exc}")
        print("Grant accessibility permissions and restart the program.")
        return

    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"Unable to open camera index {cam_index}.")
        return

    hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
    drawing = mp.solutions.drawing_utils

    smoothed_x, smoothed_y = 0.0, 0.0
    pinching = False
    dragging = False
    pinch_start = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from camera.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                lm = hand.landmark
                ix, iy = lm[8].x, lm[8].y  # index fingertip
                tx, ty = lm[4].x, lm[4].y  # thumb tip

                # map to screen coordinates
                x = ix * screen_w
                y = iy * screen_h
                if smoothed_x == 0 and smoothed_y == 0:
                    smoothed_x, smoothed_y = x, y
                else:
                    smoothed_x = alpha * x + (1 - alpha) * smoothed_x
                    smoothed_y = alpha * y + (1 - alpha) * smoothed_y
                try:
                    pyautogui.moveTo(smoothed_x, smoothed_y)
                except Exception as exc:  # permissions
                    print(f"PyAutoGUI error: {exc}")
                    print("Ensure the application has screen control permissions.")
                    break

                dx = (ix - tx) * frame.shape[1]
                dy = (iy - ty) * frame.shape[0]
                dist = (dx**2 + dy**2) ** 0.5

                if dist < pinch_px:
                    if not pinching:
                        pinching = True
                        pinch_start = time.time()
                        dragging = False
                    else:
                        if not dragging and time.time() - pinch_start > long_pinch_sec:
                            try:
                                pyautogui.mouseDown()
                                dragging = True
                            except Exception as exc:
                                print(f"PyAutoGUI error: {exc}")
                                break
                else:
                    if pinching:
                        if dragging:
                            pyautogui.mouseUp()
                        else:
                            pyautogui.click()
                    pinching = False
                    dragging = False

                drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

            cv2.imshow("Air Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()


if __name__ == "__main__":
    main()
