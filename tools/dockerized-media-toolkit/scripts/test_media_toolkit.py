import unittest
from your_media_toolkit_module import MediaToolkitApp  # Adjust the import based on your module name

class TestMediaToolkitApp(unittest.TestCase):
    def setUp(self):
        self.app = MediaToolkitApp()  # Initialize your app instance

    def test_detect_media_type(self):
        self.assertEqual(self.app.detect_media_type("test.mp3"), "Audio")
        self.assertEqual(self.app.detect_media_type("test.mp4"), "Video")
        self.assertEqual(self.app.detect_media_type("test.txt"), "Text")
        self.assertEqual(self.app.detect_media_type("test.jpg"), "Image")
        self.assertEqual(self.app.detect_media_type("unknown.xyz"), "Unknown")

    def test_save_transcription(self):
        try:
            self.app.save_transcription("Sample transcription text", "test_transcription.txt")
            with open("test_transcription.txt", 'r') as file:
                content = file.read()
            self.assertEqual(content, "Sample transcription text")
        except Exception as e:
            self.fail(f"Save transcription raised an exception: {str(e)}")

    # Add more tests for other functions

if __name__ == "__main__":
    unittest.main()
