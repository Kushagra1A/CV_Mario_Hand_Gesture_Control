# 🎮 Hand Gesture Game Controller (Super Mario Edition)

This project uses computer vision and hand tracking to control games using hand gestures. It captures video from a webcam, detects hand movements via **MediaPipe**, and translates them into low-level keyboard inputs. 

This version is specifically optimized for **Super Mario Bros**, featuring independent hand logic and "key holding" for higher jumps.

---

## 🚀 Features

- **Real-time Dual-Hand Tracking:** Independent processing for Left and Right hands.
- **State-Based Key Holding:** Mimics physical key presses, allowing Mario to jump higher by holding a gesture.
- **Visual Debugger:** On-screen UI showing active key states (W, A, D) and movement zones.
- **Low-Level Input Injection:** Uses `ctypes` to bypass Windows security, ensuring compatibility with most game emulators.

---

## 📋 Prerequisites

- **Python 3.12** (Important: Versions higher than 3.12 currently lack stable MediaPipe support)
- **OpenCV** (for image processing)
- **MediaPipe 0.10.21** (for hand landmark detection)
- **Windows OS** (Required for `directkey.py` hardware-level simulation)

---

## ⚙️ Installation

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/Kushagra1A/hand-gesture-game-controller.git](https://github.com/Kushagra1A/hand-gesture-game-controller.git)
   cd hand-gesture-game-controller

   
