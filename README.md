#  AI Virtual Keyboard

<div align="center">

**Control your keyboard with hand gestures using Computer Vision and AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-red.svg)](https://mediapipe.dev)


</div>

---

##  Features

-  **Hand Gesture Recognition** - Advanced hand tracking using MediaPipe
-  **Virtual Keyboard** - Full QWERTY keyboard layout
-  **Voice Output** - Speaks each letter you type
-  **Gesture Shortcuts** - Quick actions with hand gestures
-  **Auto-Save** - Automatically saves typed text to files
-  **Settings Panel** - Customize your experience
-  **Help Guide** - Built-in tutorial and instructions
-  **Visual Feedback** - Real-time hand tracking visualization

---




##  Requirements

- **Python** 3.8 or higher
- **Webcam** (built-in or external)
- **Operating System**: macOS / Windows / Linux

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/nmaaitall/AI-Virtual-Keyboard.git
cd AI-Virtual-Keyboard
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Usage

### Run the application

```bash
python main.py
```

### First Time Setup

1. **Allow camera access** when prompted
2. Position your hand in front of the camera
3. Wait for hand detection (green lines will appear)
4. Start typing by double-pinching on virtual keys!

---

##  Controls

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **ESC** | Exit application |
| **V** | Toggle voice on/off |
| **S** | Open settings panel |
| **H** | Open help guide |
| **F** | View saved files |

### Hand Gestures

| Gesture | Action | How To |
|---------|--------|--------|
| **Double Pinch** | Type letter | Bring thumb and index finger together twice |
| **✌️ Peace Sign** | Clear all text | Hold index and middle fingers up for 0.7s |
| **👍 Thumbs Up** | Save text to file | Hold thumb up for 0.7s |
| **✊ Fist** | Undo last action | Close all fingers for 0.7s |

---

## 📁 Project Structure

```
AI-Virtual-Keyboard/
├── main.py                 # Main application
├── hand_detector.py        # Hand detection and tracking
├── keyboard_layout.py      # Virtual keyboard layout
├── voice_engine.py         # Text-to-speech engine
├── gesture_manager.py      # Gesture recognition logic
├── file_manager.py         # File saving functionality
├── settings_panel.py       # Settings UI components
├── requirements.txt        # Project dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

---

## 🛠️ Technologies Used

- **[OpenCV](https://opencv.org/)** - Computer vision and image processing
- **[MediaPipe](https://mediapipe.dev/)** - Hand tracking and landmark detection
- **[pyttsx3](https://pyttsx3.readthedocs.io/)** - Text-to-speech conversion
- **[Python](https://www.python.org/)** - Core programming language

---

##  How It Works

1. **Hand Detection**: MediaPipe detects hand landmarks in real-time
2. **Gesture Recognition**: Custom algorithms identify specific hand poses
3. **Pinch Detection**: Measures distance between thumb and index finger
4. **Key Selection**: Maps finger position to virtual keyboard keys
5. **Voice Feedback**: Speaks typed characters using TTS engine
6. **File Management**: Saves text to timestamped files

---

##  Configuration

### Adjusting Sensitivity

In `main.py`, modify these values:

```python
pinch_threshold = 35        # Lower = more sensitive
click_delay = 0.5           # Time between clicks
gesture_hold_time = 0.7     # Hold time for gestures
```

### Changing Voice Settings

In `voice_engine.py`:

```python
self.engine.setProperty('rate', 150)    # Speech speed
self.engine.setProperty('volume', 0.9)  # Volume level
```

---

##  Troubleshooting

### Camera not working
- Check camera permissions in System Settings
- Ensure no other app is using the camera
- Try restarting the application

### Hand not detected
- Ensure good lighting conditions
- Keep hand within camera view
- Try adjusting camera angle

### Voice not working
- Press **V** to toggle voice on
- Check system volume settings
- Verify pyttsx3 installation

---

##  Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

##  Author

**Nour Maaitah**

- GitHub: [@nmaaitall](https://github.com/nmaaitall)
- Project Link: [AI-Virtual-Keyboard](https://github.com/nmaaitall/AI-Virtual-Keyboard)


