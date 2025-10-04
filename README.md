# AI Virtual Keyboard

A virtual keyboard controlled by hand gestures using computer vision.

## Features

- Type using hand gestures detected by webcam
- Double pinch to select keys
- Peace sign (hold 0.7s) - Clear text
- Thumbs up (hold 0.7s) - Save to file
- Fist (hold 0.7s) - Undo
- Voice feedback for typed characters
- Save typed text to files

## Tech Stack

- OpenCV - Video processing
- MediaPipe - Hand detection
- pyttsx3 - Text-to-speech

## Installation
```bash
pip install -r requirements.txt
python main.py
