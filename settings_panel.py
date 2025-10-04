import cv2


class SettingsPanel:
    def __init__(self):
        self.show_panel = False
        self.voice_enabled = True
        self.sensitivity = 35
        self.panel_position = (50, 100)
        self.panel_size = (400, 300)

    def toggle_panel(self):
        """Show or hide settings panel"""
        self.show_panel = not self.show_panel

    def draw_panel(self, img):
        """Draw settings panel"""
        if not self.show_panel:
            return img

        x, y = self.panel_position
        w, h = self.panel_size

        # semi transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (40, 40, 40), -1)
        img = cv2.addWeighted(overlay, 0.8, img, 0.2, 0)  # fixed

        # border
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # title
        cv2.putText(img, "SETTINGS", (x + 120, y + 40),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        # settings options
        cv2.putText(img, "Press S to close", (x + 20, y + 80),
                    cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 200), 2)

        cv2.putText(img, "Press V - Toggle Voice", (x + 20, y + 120),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv2.putText(img, "Press H - View Help", (x + 20, y + 160),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv2.putText(img, "Press F - View Files", (x + 20, y + 200),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv2.putText(img, f"Sensitivity: {self.sensitivity}", (x + 20, y + 240),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

        return img

    def draw_help(self, img):
        """Draw help screen"""
        # semi transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (200, 100), (1080, 600), (40, 40, 40), -1)
        img = cv2.addWeighted(overlay, 0.9, img, 0.1, 0)  # fixed

        # border
        cv2.rectangle(img, (200, 100), (1080, 600), (0, 255, 0), 3)

        # title
        cv2.putText(img, "HELP GUIDE", (480, 150),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # help text
        help_text = [
            "Double Pinch - Type letters",
            "Peace Sign (hold) - Clear all text",
            "Thumbs Up (hold) - Save text to file",
            "Fist (hold) - Undo last save",
            "Press V - Toggle voice",
            "Press S - Settings menu",
            "Press F - View saved files",
            "Press ESC - Exit program"
        ]

        y_pos = 220
        for i, text in enumerate(help_text):
            # alternate colors for readability
            color = (255, 255, 255) if i % 2 == 0 else (200, 200, 200)
            cv2.putText(img, text, (250, y_pos),
                        cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
            y_pos += 40

        cv2.putText(img, "Press H to close", (450, 570),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

        return img

    def draw_files_list(self, img, files):
        """Draw saved files list"""
        # semi transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (200, 100), (1080, 600), (40, 40, 40), -1)
        img = cv2.addWeighted(overlay, 0.9, img, 0.1, 0)  # fixed

        # border
        cv2.rectangle(img, (200, 100), (1080, 600), (0, 255, 255), 3)

        # title
        cv2.putText(img, "SAVED FILES", (450, 150),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)

        if files:
            y_pos = 220
            for i, file in enumerate(files[:5]):
                cv2.putText(img, f"{i + 1}. {file}", (250, y_pos),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                y_pos += 50
        else:
            cv2.putText(img, "No saved files yet", (400, 350),
                        cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 200), 2)

        cv2.putText(img, "Press F to close", (450, 570),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

        return img