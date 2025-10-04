import cv2


class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


class KeyboardLayout:
    def __init__(self):
        self.buttons = []
        self.create_keyboard()

    def create_keyboard(self):
        """Create all keyboard buttons"""
        # first row
        keys_row1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        for i, key in enumerate(keys_row1):
            self.buttons.append(Button([100 + i * 100, 100], key))

        # second row
        keys_row2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
        for i, key in enumerate(keys_row2):
            self.buttons.append(Button([150 + i * 100, 200], key))

        # third row
        keys_row3 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        for i, key in enumerate(keys_row3):
            self.buttons.append(Button([200 + i * 100, 300], key))

        # space bar
        self.buttons.append(Button([300, 400], 'SPACE', [400, 85]))

        # backspace
        self.buttons.append(Button([750, 400], 'BACK', [150, 85]))

    def _draw_single_button(self, img, button, highlight=False):
        """Draw a single button with optional highlight"""
        x, y = button.pos
        w, h = button.size

        # choose color
        bg_color = (0, 255, 0) if highlight else (50, 50, 50)

        # draw button background
        cv2.rectangle(img, button.pos, (x + w, y + h), bg_color, cv2.FILLED)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 255), 2)

        # draw text centered
        text_size = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, button.text, (text_x, text_y),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    def draw_keyboard(self, img, highlighted_button=None):
        """Draw all keyboard buttons"""
        for button in self.buttons:
            # check if this button should be highlighted
            is_highlighted = (highlighted_button == button.text)
            self._draw_single_button(img, button, is_highlighted)
        return img

    def check_button_press(self, pos):
        """Check if position is inside any button"""
        for button in self.buttons:
            x, y = button.pos
            w, h = button.size

            # check if pos is inside button
            if x < pos[0] < x + w and y < pos[1] < y + h:
                return button.text

        return None

    def highlight_button(self, img, button_text):
        """Highlight a specific button (deprecated - use draw_keyboard)"""
        # keep for backward compatibility
        return self.draw_keyboard(img, button_text)