import time


class GestureManager:
    def __init__(self):
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.5  # wait time between gestures
        self.gesture_hold_time = 0.7  # how long to hold gesture
        self.gesture_start_time = 0
        self.current_gesture = None

    def process_gesture(self, gesture):
        """Check if gesture is held long enough and ready to activate"""
        current_time = time.time()

        # no gesture detected - reset
        if gesture is None:
            self.current_gesture = None
            self.gesture_start_time = 0
            return None

        # same gesture continues
        if gesture == self.current_gesture:
            # check if held long enough
            held_time = current_time - self.gesture_start_time

            if held_time >= self.gesture_hold_time:
                # check cooldown period passed
                time_since_last = current_time - self.last_gesture_time

                if time_since_last >= self.gesture_cooldown:
                    # activate gesture
                    self.last_gesture = gesture
                    self.last_gesture_time = current_time
                    self.current_gesture = None
                    self.gesture_start_time = 0
                    return gesture
        else:
            # new gesture started
            self.current_gesture = gesture
            self.gesture_start_time = current_time

        return None

    def get_hold_progress(self):
        """Get progress bar value (0 to 1)"""
        if self.current_gesture and self.gesture_start_time > 0:
            elapsed = time.time() - self.gesture_start_time
            progress = min(elapsed / self.gesture_hold_time, 1.0)
            return progress
        return 0

    def reset(self):
        """Reset all gesture tracking"""
        self.current_gesture = None
        self.gesture_start_time = 0
        self.last_gesture = None
        self.last_gesture_time = 0