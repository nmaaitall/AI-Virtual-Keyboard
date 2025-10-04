import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, draw_landmarks=True):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_landmarks = draw_landmarks

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw and self.draw_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    self.mp_draw.DrawingSpec(color=(255, 0, 255), thickness=2)
                )

        return img

    def find_position(self, img):
        landmark_list = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([id, cx, cy])

        return landmark_list

    def get_distance(self, p1, p2, landmark_list):
        if len(landmark_list) >= max(p1, p2):
            x1, y1 = landmark_list[p1][1], landmark_list[p1][2]
            x2, y2 = landmark_list[p2][1], landmark_list[p2][2]

            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return distance
        return 0

    def draw_finger_tips(self, img, landmark_list):
        finger_tips = [4, 8, 12, 16, 20]

        for tip_id in finger_tips:
            if len(landmark_list) > tip_id:
                x, y = landmark_list[tip_id][1], landmark_list[tip_id][2]

                if tip_id == 8:
                    cv2.circle(img, (x, y), 15, (0, 255, 255), cv2.FILLED)
                elif tip_id == 4:
                    cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)
                else:
                    cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)

        return img

    def count_fingers(self, landmark_list):
        if len(landmark_list) == 0:
            return 0

        fingers = []

        # Detect hand orientation (left or right hand)
        # Compare wrist (0) with pinky base (17)
        is_right_hand = landmark_list[0][1] < landmark_list[17][1]

        # Thumb - check based on hand orientation
        if is_right_hand:
            # Right hand - thumb is up if tip is to the right of the base
            if landmark_list[4][1] > landmark_list[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Left hand - thumb is up if tip is to the left of the base
            if landmark_list[4][1] < landmark_list[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Other fingers - check if tip is above the middle joint
        finger_tips = [8, 12, 16, 20]
        for tip in finger_tips:
            if landmark_list[tip][2] < landmark_list[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)

    def detect_gesture(self, landmark_list):
        if len(landmark_list) == 0:
            return None

        fingers = self.count_fingers(landmark_list)

        # Peace sign - index and middle fingers up, others down
        if fingers == 2:
            index_up = landmark_list[8][2] < landmark_list[6][2]
            middle_up = landmark_list[12][2] < landmark_list[10][2]
            ring_down = landmark_list[16][2] > landmark_list[14][2]
            pinky_down = landmark_list[20][2] > landmark_list[18][2]

            if index_up and middle_up and ring_down and pinky_down:
                return "PEACE"

        # Thumbs up - only thumb up, all other fingers down
        elif fingers == 1:
            # Check if thumb tip is higher than thumb base (Y coordinate)
            thumb_up = landmark_list[4][2] < landmark_list[2][2]

            # Check that all other fingers are down
            index_down = landmark_list[8][2] > landmark_list[6][2]
            middle_down = landmark_list[12][2] > landmark_list[10][2]
            ring_down = landmark_list[16][2] > landmark_list[14][2]
            pinky_down = landmark_list[20][2] > landmark_list[18][2]

            if thumb_up and index_down and middle_down and ring_down and pinky_down:
                return "THUMBS_UP"

        # Fist - all fingers down
        elif fingers == 0:
            return "FIST"

        return None