# 🚗 Gesture-Controlled Car Bot

## 🔍 Project Overview

This project showcases a gesture-controlled robotic car, where hand movements serve as commands to guide a bot wirelessly. It leverages Python for gesture recognition through OpenCV and MediaPipe and bridges the communication to hardware using serial and Bluetooth technologies. The aim is to create a seamless, intuitive interface for controlling robotics systems using natural hand gestures.

---

## ✨ Features

- **Dual-Hand Gesture Interface**:
  - Right hand directs motion (Forward, Reverse, Left, Right).
  - Left hand modulates speed (Slow, Medium, Fast).
- **Real-Time Video Processing**: Utilizes MediaPipe's hand landmark model for precise gesture tracking.
- **Wireless Communication**:
  - Serial communication between Python and Arduino.
  - Bluetooth data transmission between Arduinos.
- **Modular Code Design**:
  - Independent scripts handle gesture detection, signal dispatch, and bot actuation.

---

## 🧰 Tech Stack

- **Software**:
  - Python (OpenCV, MediaPipe, PySerial, Threading)
- **Hardware**:
  - Arduino UNO x2
  - Bluetooth HC-05
  - L298N or RMC2350 Motor Driver
  - USB Webcam
  - 4-Wheel Drive Chassis with DC Motors
- **Protocols**:
  - USB Serial for PC-Arduino communication
  - UART Bluetooth for inter-Arduino communication

---

## 🔁 System Workflow

1. **Gesture Recognition (Python Script)**:
   - Captures webcam feed.
   - Identifies hand posture and finger orientation.
   - Encodes directions and speed into alphanumeric commands.

2. **Serial Data Transmission**:
   - Commands sent from Python to Arduino via USB serial interface.

3. **Bluetooth Relay**:
   - Arduino with `sending_signal.ino` forwards commands wirelessly to the receiver Arduino.

4. **Bot Command Execution**:
   - Arduino with `car_code.ino` interprets the signals and drives motors accordingly.

---

## 🧑‍💻 User Instructions

To use the gesture-controlled bot:

1. **Turn on the bot** (power the Arduino and motor system).
2. **Connect the USB cable** from your PC to the Arduino running the transmitter (`sending_signal.ino`).
3. **Edit the Python code** (`optimized.py`) and set the correct COM port for the USB (e.g., `COM3`, `/dev/ttyUSB0`).
4. **Run the Python script**: python optimized.py

---

## 🛠️ Dev Instructions

To set up the development environment and modify the code:

1. Use Python 3.8 or earlier, as MediaPipe is incompatible with the latest versions.

2. Create a virtual environment (recommended):

3. python3 -m venv venv
- source venv/bin/activate   # On Windows: venv\Scripts\activate

**Install dependencies:**
- pip install mediapipe==0.8.10 opencv-python pyserial

---

## ✅ Conclusion

This car bot project exemplifies an innovative blend of computer vision and embedded systems for real-time robotic control. The gesture interface not only enhances user interaction but also paves the way for developing assistive technologies and educational tools. Future improvements could include sensor-based obstacle avoidance, enhanced gesture models, and integration with mobile platforms.

---

## 📂 File Overview

optimized.py            # Gesture recognition and command generation
sending_signal.ino      # Arduino Transmitter
car_code.ino            # Arduino Receiver
README.md               # Project documentation


