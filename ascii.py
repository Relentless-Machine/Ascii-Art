from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog
import random


def get_char(gray_pix):
    char_list = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
    length = len(char_list)
    unit = 256.0 / length
    return char_list[int(((length - 1) * gray_pix) / 256.0)]


class BlessingWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Blessing Window")

        self.blessing_label = tk.Label(self, text="")
        self.blessing_label.pack(padx=20, pady=20)

        self.show_random_blessing()

    def show_random_blessing(self):
        blessings = self.read_blessings_from_file()
        if blessings:
            random_blessing = random.choice(blessings)
            self.blessing_label.config(text=random_blessing)

    def read_blessings_from_file(self):
        try:
            with open("gift.new", "r", encoding="utf-16be") as file:
                blessings = [line.strip() for line in file.readlines()]
            return blessings
        except FileNotFoundError:
            return []


class ImageToASCIIConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Image to ASCII Art Converter")

        self.label = tk.Label(master, text="Select an image:")
        self.label.pack(pady=5)

        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.browse_button = tk.Button(master, text="Browse", command=self.choose_image)
        self.browse_button.pack(pady=10)

        self.convert_button = tk.Button(master, text="Convert to ASCII", command=self.convert_to_ascii)
        self.convert_button.pack(pady=10)

        self.display_button = tk.Button(master, text="Display Image", command=self.display_text_image)
        self.display_button.pack(pady=10)

        self.show_blessing_button = tk.Button(master, text="Show Blessing", command=self.show_blessing)
        self.show_blessing_button.pack(pady=10)

        self.info_label = tk.Label(master, text="")
        self.info_label.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=self.master.destroy, fg="red")
        self.exit_button.pack(pady=10)

        self.blessing_window = None

    def choose_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.img_path = file_path
            self.display_image()

    def display_image(self):
        image = Image.open(self.img_path)

        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        image.thumbnail((window_width, window_height))

        tk_image = ImageTk.PhotoImage(image)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image

    def convert_and_display(self):
        if hasattr(self, 'img_path'):
            img = Image.open(self.img_path)
            img_width = img.size[0]
            img_height = img.size[1]
            img = img.resize((int(img_width * 0.75), int(img_height * 0.5)), Image.NEAREST)
            img_gray = np.array(img.convert('L'), 'f')

            text = []
            char_width = 6
            char_height = 12

            for i in range(int(img_height * 0.5)):
                line = ""
                for j in range(int(img_width * 0.75)):
                    line += get_char(img_gray[i, j]) * char_width
                text.extend([line] * char_height)

            text_name = "ascii_art.txt"
            with open(text_name, "w") as f:
                f.write('\n'.join(text))

            self.info_label.config(text=f"ASCII art saved to {text_name}")
            print(f"ASCII art saved to {text_name}")
            return text_name

    def convert_to_ascii(self):
        if hasattr(self, 'img_path'):
            return self.convert_and_display()

    def display_text_image(self):
        try:
            text_name = self.convert_to_ascii()
            if text_name:
                with open(text_name, "r") as f:
                    ascii_text = f.read().splitlines()

                img = self.ascii_to_image(ascii_text)
                self.display_image_with_ascii(img)

        except FileNotFoundError:
            self.info_label.config(text="ASCII art file not found.")

    def display_image_with_ascii(self, img):
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        img.thumbnail((window_width, window_height))

        tk_image = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image

    def show_blessing(self):
        if self.blessing_window:
            self.blessing_window.destroy()

        self.blessing_window = BlessingWindow(self.master)

    def ascii_to_image(self, ascii_text):
        char_width = 6
        char_height = 12
        font_size = 12

        img_width = len(ascii_text[0]) * char_width
        img_height = len(ascii_text) * char_height

        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        for i, line in enumerate(ascii_text):
            draw.text((0, i * char_height), line, fill='black', font=font)

        return img


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToASCIIConverter(root)
    root.geometry("800x600")
    root.mainloop()