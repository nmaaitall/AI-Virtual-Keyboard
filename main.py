import cv2
import time
from hand_detector import HandDetector
from keyboard_layout import KeyboardLayout
from voice_engine import VoiceEngine
from gesture_manager import GestureManager
from file_manager import FileManager
from settings_panel import SettingsPanel


def main():
    # initialize camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access camera")
        print("Please allow camera permission in System Settings")
        return

    # set camera resolution
    cap.set(3, 1280)
    cap.set(4, 720)

    # initialize all components
    detector = HandDetector(draw_landmarks=True)
    keyboard = KeyboardLayout()
    voice = VoiceEngine()
    gesture_manager = GestureManager()
    file_manager = FileManager()
    settings = SettingsPanel()

    # text variables
    final_text = ""
    text_history = []

    # button click variables
    last_click_time = 0
    click_delay = 0.5
    button_clicked = None

    # UI state
    show_help = False
    show_files = False

    # pinch detection variables
    pinch_start_time = 0
    pinch_count = 0
    is_pinching = False
    pinch_threshold = 35
    double_click_window = 0.5

    print("AI Virtual Keyboard Started!")
    print("Press H for help, ESC to exit")

    # main loop
    while True:
        success, img = cap.read()

        if not success or img is None:
            print("Error: Cannot read from camera")
            break

        # flip image horizontally
        img = cv2.flip(img, 1)

        # detect hands
        img = detector.find_hands(img, draw=True)
        landmark_list = detector.find_position(img)

        # draw keyboard (pass button_clicked for highlight)
        img = keyboard.draw_keyboard(img, button_clicked)

        # process hand gestures
        if landmark_list and len(landmark_list) > 8:
            # detect gesture
            gesture = detector.detect_gesture(landmark_list)
            activated_gesture = gesture_manager.process_gesture(gesture)

            # handle activated gestures
            if activated_gesture == "PEACE":
                # clear all text
                final_text = ""
                voice.speak("cleared all")
                cv2.putText(img, "CLEARED!", (500, 250),
                            cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

            elif activated_gesture == "THUMBS_UP":
                # save to file
                if final_text:
                    if file_manager.save_text(final_text):
                        text_history.append(final_text)
                        voice.speak("saved to file")
                        cv2.putText(img, "SAVED TO FILE!", (400, 250),
                                    cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

            elif activated_gesture == "FIST":
                # undo last save
                if len(text_history) > 0:
                    final_text = text_history[-1]
                    text_history.pop()
                    voice.speak("undo")
                    cv2.putText(img, "UNDO!", (500, 250),
                                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 0), 5)

            # show gesture hold progress
            if gesture:
                progress = gesture_manager.get_hold_progress()
                gesture_text = f"Hold: {gesture}"
                cv2.putText(img, gesture_text, (900, 150),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # progress bar
                bar_width = int(200 * progress)
                cv2.rectangle(img, (900, 170), (1100, 190), (100, 100, 100), -1)
                cv2.rectangle(img, (900, 170), (900 + bar_width, 190), (0, 255, 0), -1)

            # draw finger tips
            img = detector.draw_finger_tips(img, landmark_list)

            # get index finger position
            index_tip = landmark_list[8]
            x, y = index_tip[1], index_tip[2]

            # calculate pinch distance
            distance = detector.get_distance(4, 8, landmark_list)

            # show distance
            cv2.putText(img, f"Distance: {int(distance)}", (50, 650),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            current_time = time.time()

            # check for pinch gesture
            if distance < pinch_threshold:
                # draw line between thumb and index
                thumb_tip = landmark_list[4]
                cv2.line(img, (x, y), (thumb_tip[1], thumb_tip[2]), (0, 255, 0), 5)
                cv2.circle(img, ((x + thumb_tip[1]) // 2, (y + thumb_tip[2]) // 2),
                           10, (0, 0, 255), cv2.FILLED)

                # detect pinch start
                if not is_pinching:
                    is_pinching = True
                    pinch_count += 1

                    # start timer on first pinch
                    if pinch_count == 1:
                        pinch_start_time = current_time

                    # check for double pinch
                    if pinch_count == 2 and (current_time - pinch_start_time) < double_click_window:
                        button_pressed = keyboard.check_button_press((x, y))

                        if button_pressed:
                            # handle button press
                            if button_pressed == "SPACE":
                                final_text += " "
                                voice.speak("space")
                            elif button_pressed == "BACK":
                                final_text = final_text[:-1]
                                voice.speak("backspace")
                            else:
                                final_text += button_pressed
                                voice.speak(button_pressed)

                            button_clicked = button_pressed
                            last_click_time = current_time

                        # reset pinch count
                        pinch_count = 0

            else:
                # pinch released
                is_pinching = False

                # reset pinch count if time window passed
                if current_time - pinch_start_time > double_click_window:
                    pinch_count = 0

            # show pinch count
            if pinch_count > 0:
                cv2.putText(img, f"Pinch: {pinch_count}/2", (50, 680),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

            # remove button highlight after delay
            if button_clicked:
                if time.time() - last_click_time > 0.2:
                    button_clicked = None

        # draw text display box
        cv2.rectangle(img, (50, 500), (1230, 600), (50, 50, 50), cv2.FILLED)

        # show typed text (last 50 chars)
        display_text = final_text[-50:] if len(final_text) > 50 else final_text
        cv2.putText(img, display_text, (60, 570),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        # title
        cv2.putText(img, "AI Virtual Keyboard - Press H for Help", (50, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        # voice status
        voice_status = "Voice: ON" if voice.enabled else "Voice: OFF"
        voice_color = (0, 255, 0) if voice.enabled else (0, 0, 255)
        cv2.putText(img, voice_status, (1050, 650),
                    cv2.FONT_HERSHEY_PLAIN, 2, voice_color, 2)

        # saved count
        cv2.putText(img, f"Saved: {len(text_history)}", (1050, 680),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        # draw overlays
        if settings.show_panel:
            img = settings.draw_panel(img)
        elif show_help:
            img = settings.draw_help(img)
        elif show_files:
            files = file_manager.get_saved_files()
            img = settings.draw_files_list(img, files)

        # show image
        cv2.imshow("AI Virtual Keyboard", img)

        # handle keyboard input
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break
        elif key == ord('v') or key == ord('V'):
            voice.toggle()
        elif key == ord('s') or key == ord('S'):
            settings.toggle_panel()
        elif key == ord('h') or key == ord('H'):
            show_help = not show_help
            show_files = False  # close files if open
        elif key == ord('f') or key == ord('F'):
            show_files = not show_files
            show_help = False  # close help if open

    # cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Program ended")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()