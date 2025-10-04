import pyttsx3
import threading
import queue


class VoiceEngine:
    def __init__(self):
        self.enabled = True
        self.engine = None
        self.speech_queue = queue.Queue()
        self.is_speaking = False

        try:
            # initialize voice engine
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)

            # start worker thread
            self.worker_thread = threading.Thread(target=self._speech_worker)
            self.worker_thread.daemon = True
            self.worker_thread.start()

        except Exception as e:
            print(f"Voice engine error: {e}")
            self.enabled = False

    def speak(self, text):
        """Add text to speech queue"""
        if self.enabled and text:
            self.speech_queue.put(str(text))

    def _speech_worker(self):
        """Worker thread to handle speech queue"""
        while True:
            try:
                # get text from queue
                text = self.speech_queue.get()

                if text and self.enabled:
                    self.is_speaking = True
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.is_speaking = False

                # mark task as done
                self.speech_queue.task_done()

            except Exception as e:
                print(f"Speech error: {e}")
                self.is_speaking = False

    def toggle(self):
        """Toggle voice on/off"""
        self.enabled = not self.enabled

        # clear queue if disabled
        if not self.enabled:
            self.clear_queue()

        return self.enabled

    def set_enabled(self, enabled):
        """Set voice enabled state"""
        self.enabled = enabled

        if not self.enabled:
            self.clear_queue()

    def clear_queue(self):
        """Clear all pending speech"""
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except:
                break

    def is_busy(self):
        """Check if currently speaking"""
        return self.is_speaking

    def set_rate(self, rate):
        """Set speech speed (words per minute)"""
        if self.engine:
            try:
                self.engine.setProperty('rate', rate)
            except:
                pass

    def set_volume(self, volume):
        """Set voice volume (0.0 to 1.0)"""
        if self.engine:
            try:
                volume = max(0.0, min(1.0, volume))
                self.engine.setProperty('volume', volume)
            except:
                pass