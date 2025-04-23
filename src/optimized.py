import cv2
import mediapipe as mp
import math
import collections
import time
import serial
import threading

# Constants
ANGLE_HISTORY_SIZE = 5
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
SEND_INTERVAL = 0.5  # seconds

# Globals
angle_history = collections.deque(maxlen=ANGLE_HISTORY_SIZE)
latest_gesture = "r0\n"
latest_speed = "s2\n"
lock = threading.Lock()

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def calculate_angle(x1, y1, x2, y2):
    return math.degrees(math.atan2(x1 - x2, y2 - y1))

def detect_gesture_and_speed(hand_landmarks, handedness, frame_shape):
    global latest_gesture, latest_speed

    h, w, _ = frame_shape
    label = handedness.classification[0].label

    if label == "Right":
        # Get middle finger tip and base
        tip = hand_landmarks.landmark[12]
        base = hand_landmarks.landmark[9]
        x_tip, y_tip = int(tip.x * w), int(tip.y * h)
        x_base, y_base = int(base.x * w), int(base.y * h)

        # Angle
        angle = calculate_angle(x_tip, y_tip, x_base, y_base)
        angle_history.append(angle)
        smoothed_angle = sum(angle_history) / len(angle_history)

        # Position
        if y_base < h // 3:
            pos = "Forward"
        elif y_base > 2 * h // 3:
            pos = "Reverse"
        else:
            pos = "Stop"

        # Direction
        if -110 <= smoothed_angle <= -60:
            dir = "Left"
        elif 60 <= smoothed_angle <= 110:
            dir = "Right"
        elif -20 <= smoothed_angle <= 20:
            dir = pos
        else:
            dir = "None"

        action = f"{pos} {dir}".strip() if dir in ["Left", "Right"] and pos != "Stop" else dir

        gesture_map = {
            "Forward Left": "r7",
            "Forward Right": "r9",
            "Reverse Left": "r1",
            "Reverse Right": "r3",
            "Forward": "r8",
            "Reverse": "r2",
            "Left": "r4",
            "Right": "r6",
        }
        with lock:
            latest_gesture = gesture_map.get(action, "r0") + "\n"

        return smoothed_angle, action

    elif label == "Left":
        index_tip = hand_landmarks.landmark[8]
        y_tip = int(index_tip.y * h)
        speed = "s3" if y_tip < h // 3 else "s1" if y_tip > 2 * h // 3 else "s2"

        with lock:
            latest_speed = speed + "\n"
        return None, None

    return None, None

def serial_communication(serial_connection):
    while True:
        with lock:
            command = latest_speed.strip() + latest_gesture.strip() + "\n"
            if serial_connection:
                serial_connection.write(command.encode('ascii'))
                serial_connection.flush()
                print(f"Sent: {command.strip()}")
        time.sleep(SEND_INTERVAL)

def main():
    # Serial Connection
    try:
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")
        serial_connection.write("done\n".encode('utf-8'))
    except Exception as e:
        print(f"Connection issue: {e}")
        serial_connection = None

    # Start serial thread
    threading.Thread(target=serial_communication, args=(serial_connection,), daemon=True).start()

    # Webcam and Hand Detection
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                        min_detection_confidence=0.5, min_tracking_confidence=0.7) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    angle, action = detect_gesture_and_speed(hand_landmarks, handedness, frame.shape)

                    if angle is not None:
                        cv2.putText(frame, f"Angle: {int(angle)}°", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    if action:
                        cv2.putText(frame, f"Action: {action}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    if handedness.classification[0].label == "Left":
                        cv2.putText(frame, f"Speed: {latest_speed.strip()}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("Hand Gesture Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
