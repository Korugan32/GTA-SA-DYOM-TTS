import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import os
import re

def process_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(f"{output_file}/processed_text.txt", 'w', encoding='utf-8') as out_file:
        for index, line in enumerate(lines):
            line = line.strip()

            if "---------= DYOM Objective texts =-------" in line:
                break

            if line and not line.startswith('*'):  # Ignore empty lines and lines starting with '*'
                # Remove formatting instructions (e.g., ~g~, ~b~, ~y~) and underscores
                line = re.sub(r'~[a-zA-Z]~|_', '', line)

                if line.strip():  # Check if there's any text left after removing formatting and underscores
                    # Text-to-speech conversion with male voice (en-us)
                    tts = gTTS(text=line, lang='en-us')
                    tts.save(f"{output_file}/{index + 1:02d}.mp3")

                    # Save to numbered text file
                    out_file.write(f"{index + 1:02d}. {line}\n")


def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def select_directory(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)


def main():
    # GUI setup
    root = tk.Tk()
    root.title("Korugan Dyom-Text-To-Speech")

    # Configure root window size and make it non-resizable
    root.geometry("600x300")  # Width x Height
    root.resizable(False, False)  # Disable resizing

    # Function to close the window
    def close_window():
        root.destroy()

    # Input file path
    input_label = tk.Label(root, text="Input File Path:")
    input_label.pack()
    input_entry = tk.Entry(root, width=50)
    input_entry.pack()
    input_button = tk.Button(root, text="Select File", command=lambda: select_file(input_entry))
    input_button.pack()

    # Output directory path
    output_label = tk.Label(root, text="Output Directory Path:")
    output_label.pack()
    output_entry = tk.Entry(root, width=50)
    output_entry.pack()
    output_button = tk.Button(root, text="Select Directory", command=lambda: select_directory(output_entry))
    output_button.pack()

    # Button to process the file
    def process_file():
        input_file = input_entry.get()
        output_dir = output_entry.get()
        if input_file and output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            process_text_file(input_file, output_dir)
            messagebox.showinfo("Processing Complete", "Text processing and speech synthesis completed!")
        else:
            messagebox.showerror("Error", "Please provide both input and output paths.")

    process_button = tk.Button(root, text="Process Text", command=process_file)
    process_button.pack()

    # Button to close the window
    close_button = tk.Button(root, text="Close", command=close_window)
    close_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
