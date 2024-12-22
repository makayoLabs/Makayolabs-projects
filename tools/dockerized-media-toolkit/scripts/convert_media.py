import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import moviepy.editor as mp
from gtts import gTTS
import speech_recognition as sr
import cv2
import unittest

class MediaToolkitApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Media Toolkit")
        self.master.geometry("600x400")

        # Title and Tagline
        self.label_title = tk.Label(master, text="Media Toolkit", font=("Arial", 24))
        self.label_title.pack(pady=10)

        self.label_tagline = tk.Label(master, text="Your all-in-one tool for media processing", font=("Arial", 12))
        self.label_tagline.pack(pady=5)

        # Upload and URL Entry Buttons
        self.upload_button = tk.Button(master, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=20)

        self.url_button = tk.Button(master, text="Enter URL", command=self.enter_url)
        self.url_button.pack(pady=10)

        # Process Options
        self.process_options = ttk.Combobox(master, state="readonly")
        self.process_options.pack(pady=10)
        self.process_options.bind("<<ComboboxSelected>>", self.process_selected)

        self.process_button = tk.Button(master, text="Process", command=self.process_media)
        self.process_button.pack(pady=20)

        # Initialize variables
        self.selected_file = None
        self.media_type = None

    def upload_file(self):
        self.selected_file = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("Audio Files", "*.mp3 *.wav *.aac *.ogg"),
                       ("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                       ("Text Files", "*.txt *.pdf *.docx"),
                       ("Image Files", "*.jpg *.jpeg *.png *.gif"))
        )
        if self.selected_file:
            self.media_type = self.detect_media_type(self.selected_file)
            messagebox.showinfo("Success", f"File successfully uploaded! Detected Media Type: {self.media_type}")
            self.populate_process_options()

    def enter_url(self):
        url = simpledialog.askstring("Input", "Enter media file URL:")
        if url:
            self.selected_file = url  # Assuming the URL is valid
            self.media_type = self.detect_media_type(url)
            messagebox.showinfo("Success", f"File successfully uploaded! Detected Media Type: {self.media_type}")
            self.populate_process_options()

    def detect_media_type(self, file):
        if file.endswith(('.mp3', '.wav', '.aac', '.ogg')):
            return "Audio"
        elif file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            return "Video"
        elif file.endswith(('.txt', '.pdf', '.docx')):
            return "Text"
        elif file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return "Image"
        else:
            return "Unknown"

    def populate_process_options(self):
        options = []
        if self.media_type == "Audio":
            options = [
                "Audio to Text Transcription",
                "Text to Speech",
                "Convert Audio Format"
            ]
        elif self.media_type == "Video":
            options = [
                "Video to Text Transcription",
                "Video to Images Extraction",
                "Video to Audio",
                "Convert Video Format",
                "Trim Video"
            ]
        elif self.media_type == "Text":
            options = [
                "Text to Speech",
                "Text to Video",
                "Convert Text Format"
            ]
        elif self.media_type == "Image":
            options = [
                "Image Resizing",
                "Image Filtering"
            ]  # Placeholder for future features

        self.process_options['values'] = options
        if options:
            self.process_options.current(0)

    def process_selected(self, event):
        selected_process = self.process_options.get()
        if selected_process:
            self.process_button["state"] = "normal"

    def process_media(self):
        selected_process = self.process_options.get()
        if selected_process == "Audio to Text Transcription":
            self.transcribe_audio()
        elif selected_process == "Video to Text Transcription":
            self.transcribe_video()
        elif selected_process == "Video to Images Extraction":
            self.extract_images_from_video()
        elif selected_process == "Text to Speech":
            self.text_to_speech()
        elif selected_process == "Video to Audio":
            self.video_to_audio()
        elif selected_process == "Text to Video":
            self.text_to_video()
        elif selected_process == "Convert Audio Format":
            self.convert_audio_format()
        elif selected_process == "Convert Video Format":
            self.convert_video_format()
        elif selected_process == "Convert Text Format":
            self.convert_text_format()
        elif selected_process == "Image Resizing":
            self.resize_image()
        elif selected_process == "Image Filtering":
            self.filter_image()

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(self.selected_file) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                self.save_transcription(text, "audio_transcription.txt")
                messagebox.showinfo("Transcription Complete", "Audio has been transcribed.")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transcription: {str(e)}")

    def transcribe_video(self):
        try:
            video = mp.VideoFileClip(self.selected_file)
            audio_file = "temp_audio.wav"
            video.audio.write_audiofile(audio_file)

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                self.save_transcription(text, "video_transcription.txt")

            os.remove(audio_file)  # Clean up temporary audio file
            messagebox.showinfo("Transcription Complete", "Video has been transcribed.")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transcription: {str(e)}")

    def extract_images_from_video(self):
        try:
            video_capture = cv2.VideoCapture(self.selected_file)
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            count = 0
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break
                if count % fps == 0:
                    image_name = f"frame_{count // fps}.jpg"
                    cv2.imwrite(image_name, frame)
                count += 1
            video_capture.release()
            messagebox.showinfo("Extraction Complete", "Images have been extracted from the video.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during image extraction: {str(e)}")

    def text_to_speech(self):
        text = simpledialog.askstring("Input", "Enter the text you want to convert to speech:")
        if text:
            try:
                tts = gTTS(text)
                tts.save("output_speech.mp3")
                messagebox.showinfo("Text to Speech Complete", "Speech has been generated.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during text-to-speech conversion: {str(e)}")

    def text_to_video(self):
        text = simpledialog.askstring("Input", "Enter the text to convert to video:")
        if text:
            try:
                audio_file = "text_to_speech.mp3"
                tts = gTTS(text)
                tts.save(audio_file)
                audio = mp.AudioFileClip(audio_file)
                video = mp.ColorClip(size=(640, 480), color=(255, 255, 255), duration=audio.duration)
                video = video.set_audio(audio)
                video.write_videofile("text_to_video.mp4")
                messagebox.showinfo("Video Creation Complete", "Text has been converted to video.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during video creation: {str(e)}")

    def convert_audio_format(self):
        audio_formats = [("MP3", "output.mp3"), ("WAV", "output.wav"), ("AAC", "output.aac"), ("OGG", "output.ogg")]
        selected_format = simpledialog.askstring("Convert Audio", "Select audio format (MP3, WAV, AAC, OGG):")
        for fmt, output_file in audio_formats:
            if selected_format.lower() == fmt.lower():
                try:
                    audio = mp.AudioFileClip(self.selected_file)
                    audio.write_audiofile(output_file)
                    messagebox.showinfo("Conversion Complete", f"Audio converted to {selected_format} format.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during audio conversion: {str(e)}")
                return
        messagebox.showwarning("Invalid Format", "Please select a valid audio format.")

    def convert_video_format(self):
        video_formats = [("MP4", "output.mp4"), ("AVI", "output.avi"), ("MOV", "output.mov"), ("MKV", "output.mkv")]
        selected_format = simpledialog.askstring("Convert Video", "Select video format (MP4, AVI, MOV, MKV):")
        for fmt, output_file in video_formats:
            if selected_format.lower() == fmt.lower():
                try:
                    video = mp.VideoFileClip(self.selected_file)
                    video.write_videofile(output_file)
                    messagebox.showinfo("Conversion Complete", f"Video converted to {selected_format} format.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during video conversion: {str(e)}")
                return
        messagebox.showwarning("Invalid Format", "Please select a valid video format.")

    def convert_text_format(self):
        text_formats = [("TXT", "output.txt"), ("PDF", "output.pdf"), ("DOCX", "output.docx")]
        selected_format = simpledialog.askstring("Convert Text", "Select text format (TXT, PDF, DOCX):")
        
        if not selected_format:
            return  # Exit if no format is selected

        for fmt, output_file in text_formats:
            if selected_format.lower() == fmt.lower():
                try:
                    with open(self.selected_file, 'r') as input_file:
                        text = input_file.read()
                    with open(output_file, 'w') as output_file:
                        output_file.write(text)
                    messagebox.showinfo("Conversion Complete", f"Text converted to {selected_format} format.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during text conversion: {str(e)}")
                return

        messagebox.showwarning("Invalid Format", "Please select a valid text format.")

    def video_to_audio(self):
        try:
            video = mp.VideoFileClip(self.selected_file)

            if video.audio is None:
                messagebox.showwarning("Warning", "The selected video file has no audio track.")
                return  # Exit if no audio track is found

            video.audio.write_audiofile("video_to_audio.mp3")
            messagebox.showinfo("Conversion Complete", "Video has been converted to audio.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during audio extraction: {str(e)}")

    def resize_image(self):
        new_width = simpledialog.askinteger("Resize Image", "Enter new width:")
        new_height = simpledialog.askinteger("Resize Image", "Enter new height:")
        if new_width and new_height:
            try:
                img = cv2.imread(self.selected_file)
                resized_img = cv2.resize(img, (new_width, new_height))
                cv2.imwrite("resized_image.jpg", resized_img)
                messagebox.showinfo("Resizing Complete", "Image has been resized.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during image resizing: {str(e)}")

    def filter_image(self):
        try:
            img = cv2.imread(self.selected_file)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("filtered_image.jpg", gray_img)
            messagebox.showinfo("Filtering Complete", "Image has been filtered to grayscale.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during image filtering: {str(e)}")

    def save_transcription(self, text, filename):
        try:
            with open(filename, 'w') as file:
                file.write(text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the transcription: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaToolkitApp(root)
    root.mainloop()
