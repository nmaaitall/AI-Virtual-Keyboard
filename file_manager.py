import os
from datetime import datetime


class FileManager:
    def __init__(self):
        self.save_folder = "saved_texts"
        # create folder if not exists
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def save_text(self, text):
        """Save text to a file with timestamp"""
        # check if text is empty
        if not text.strip():
            return False

        # create filename with date and time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"text_{timestamp}.txt"
        filepath = os.path.join(self.save_folder, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def get_saved_files(self):
        """Get last 5 saved text files"""
        try:
            files = os.listdir(self.save_folder)
            # filter only .txt files
            txt_files = [f for f in files if f.endswith('.txt')]
            # sort by newest first
            txt_files.sort(reverse=True)
            # return last 5 files
            return txt_files[:5]
        except Exception as e:
            print(f"Error reading files: {e}")
            return []

    def read_file(self, filename):
        """Read content from a saved file"""
        filepath = os.path.join(self.save_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def delete_file(self, filename):
        """Delete a saved file"""
        filepath = os.path.join(self.save_folder, filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def get_file_count(self):
        """Get total number of saved files"""
        try:
            files = os.listdir(self.save_folder)
            txt_files = [f for f in files if f.endswith('.txt')]
            return len(txt_files)
        except:
            return 0