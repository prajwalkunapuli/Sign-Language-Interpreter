**Sign Language Interpreter**

This project is a real-time sign language interpreter using computer vision and text-to-speech. It detects hand gestures via webcam, interprets them as words, and speaks them aloud. Emojis and the interpreted sentence are displayed on the screen.

**Features**

- Detects basic sign language gestures: Hello, Bye, Yes, No, Thanks, Wait, OK
- Shows corresponding emoji and word on the video feed
- Speaks detected words using text-to-speech
- Displays the interpreted sentence

**Requirements**

- Python 3.7+
- Webcam

**Python Libraries**

- opencv-python
- mediapipe
- pyttsx3

**Installation**

1. Clone or download this repository.
2. Install dependencies:
    ```
    pip install opencv-python mediapipe pyttsx3
    ```

**Usage**

1. Run the interpreter:
    ```
    python main.py
    ```
2. The webcam window will open. Show hand gestures to the camera.
3. Detected words and emojis will appear on the screen and be spoken aloud.
4. Press `q` to quit.
5. Press `c` to clear the sentence.

**Files**

- `main.py` - Main application for gesture detection and interpretation.
- `test_speech.py` - (Optional) For testing text-to-speech functionality.

**Notes**

- Make sure your webcam is connected and accessible.
- The interpreter works best in good lighting and with clear hand gestures.
