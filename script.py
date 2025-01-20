import os
from datetime import datetime
import threading
from tkinter import filedialog, StringVar, END
import customtkinter as ctk
from PIL import Image
import imagehash
from collections import defaultdict
import pillow_heif  
import cv2  
from concurrent.futures import ThreadPoolExecutor




# Register HEIF/HEIC support with Pillow
pillow_heif.register_heif_opener()

def update_progress(progress_bar, status_label, value, message):
    """Update the progress bar and status message."""
    progress_bar.set(value)
    status_label.configure(text=message)

def hash_video(file_path):
    """Generate a hash for a video file by hashing a representative frame."""
    try:
        cap = cv2.VideoCapture(file_path)
        success, frame = cap.read()
        cap.release()
        if success:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            return imagehash.phash(img)
    except Exception:
        return None

def process_file(file_path, folder_path):
    """Process a single file to generate its hash."""
    try:
        if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".heic")):
            with Image.open(file_path) as img:
                return imagehash.phash(img), file_path
        elif file_path.lower().endswith((".mp4", ".mov")):
            video_hash = hash_video(file_path)
            if video_hash:
                return video_hash, file_path
    except Exception:
        return None, file_path
    return None, file_path

def find_and_remove_duplicates(folder_path, action, progress_bar, status_label, ui_update_callback):
    hash_dict = defaultdict(list)
    all_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    total_files = len(all_files)
    if total_files == 0:
        ui_update_callback(progress_bar, status_label, 0, "Selected folder is empty.")
        return

    try:
        ui_update_callback(progress_bar, status_label, 0, "Not started yet")

        with ThreadPoolExecutor() as executor:
            for idx, result in enumerate(executor.map(lambda f: process_file(f, folder_path), all_files)):
                file_hash, file_path = result
                if file_hash:
                    hash_dict[file_hash].append(file_path)

                # Update progress
                progress = (idx + 1) / total_files
                if progress < 0.5:
                    status_message = "Started, hang in there!"
                elif progress < 0.9:
                    status_message = "Halfway there, almost done!"
                else:
                    status_message = "Finishing up, hold tight!"
                ui_update_callback(progress_bar, status_label, progress, f"{int(progress * 100)}% - {status_message}")

        # Handle duplicates
        for img_hash, file_paths in hash_dict.items():
            if len(file_paths) > 1:
                # Sort files by creation time, then by file name for consistency
                file_paths.sort(
                    key=lambda x: (os.path.getctime(x), os.path.basename(x))
                )
                original = file_paths[0]  # Keep the first one
                for duplicate in file_paths[1:]:
                    try:
                        if action == "delete":
                            os.remove(duplicate)  # Delete duplicate
                        elif action == "move":
                            # Create duplicates folder if it doesn't exist
                            duplicate_folder = os.path.join(folder_path, "duplicates")
                            os.makedirs(duplicate_folder, exist_ok=True)
                            
                            # Maintain folder structure in duplicates folder
                            relative_path = os.path.relpath(duplicate, folder_path)
                            duplicate_subfolder = os.path.join(duplicate_folder, os.path.dirname(relative_path))
                            os.makedirs(duplicate_subfolder, exist_ok=True)
                            
                            # Move duplicate
                            new_path = os.path.join(duplicate_subfolder, os.path.basename(duplicate))
                            os.rename(duplicate, new_path)
                    except Exception as e:
                        print(f"Error handling duplicate {duplicate}: {e}")

        ui_update_callback(progress_bar, status_label, 1.0, "Process completed")
    except Exception:
        ui_update_callback(progress_bar, status_label, 1.0, "Critical error occurred")

def browse_folder(folder_path_var, folder_status_label):
    """
    Open a dialog to select a folder and update the path variable.
    """
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)
        folder_status_label.configure(text=f"Selected Folder: {folder_path}")

def start_process(folder_path_var, action_var, progress_bar, status_label):
    """
    Start the duplicate removal process in a separate thread.
    """
    folder_path = folder_path_var.get()
    action = action_var.get()
    if not folder_path:
        update_progress(progress_bar, status_label, 0, "Please select a folder.")
        return

    update_progress(progress_bar, status_label, 0, "Starting process...")

    # Run the process in a separate thread
    threading.Thread(
        target=find_and_remove_duplicates,
        args=(folder_path, action, progress_bar, status_label, update_progress),
        daemon=True
    ).start()

def show_ui():
    """
    Create the main UI window with all elements on the same page, organized in sections.
    """
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("REMOV DUPS")
    app.geometry("900x700")
    app.iconbitmap("app_icon.ico")

    # Main Container
    container = ctk.CTkFrame(app, fg_color="#000000", corner_radius=5)
    container.pack(pady=0, padx=0, fill="both", expand=True)

    # Logo Section
    logo_frame = ctk.CTkFrame(container, fg_color="transparent")
    logo_frame.pack(pady=0)

    logo_image = ctk.CTkImage(Image.open("app_logo1.png"), size=(180, 175))
    logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
    logo_label.pack()

    # Folder Selection Section
    folder_frame = ctk.CTkFrame(container, fg_color="#161B22", corner_radius=15)
    folder_frame.pack(pady=10, padx=20, fill="x")

    folder_path_var = StringVar()
    folder_status_label = ctk.CTkLabel(
        folder_frame, text="No Folder Selected", font=("Trebuchet MS", 16), text_color="#FFFFFF"
    )
    folder_status_label.pack(pady=5)

    folder_button = ctk.CTkButton(
        folder_frame,
        text="Select Folder",
        command=lambda: browse_folder(folder_path_var, folder_status_label),
        fg_color="#E0E0E0",
        hover_color="#D6D6D6",
        font=("Trebuchet MS", 16, "bold"),
        text_color="#000000",
        corner_radius=25,
        height=50,
        width=200
    )
    folder_button.pack(pady=10)

    # Action Section
    action_frame = ctk.CTkFrame(container, fg_color="#1E242C", corner_radius=15, height=100 )
    action_frame.pack(pady=5, padx=20, fill="x")  

    action_var = StringVar(value="delete")

    # Container for buttons
    button_container = ctk.CTkFrame(action_frame, fg_color="transparent")  
    button_container.pack(expand=True, pady=10) 

    delete_button = ctk.CTkRadioButton(
        button_container,
        text="Delete Duplicates",
        variable=action_var,
        value="delete",
        font=("Trebuchet MS", 14),
        text_color="#FFFFFF",
        hover_color="#645bff",
        fg_color="#7B61FF",
        border_color="#9fa8da",
        corner_radius=10
    )
    delete_button.pack(side="left", padx=50, pady=10)

    move_button = ctk.CTkRadioButton(
        button_container,
        text="Move Duplicates",
        variable=action_var,
        value="move",
        font=("Trebuchet MS", 14),
        text_color="#FFFFFF",
        hover_color="#645bff",
        fg_color="#7B61FF",
        border_color="#9fa8da",
        corner_radius=10        
    )
    move_button.pack(side="left", padx=50, pady=10)


    # Progress Section
    progress_frame = ctk.CTkFrame(container, fg_color="#161B22", corner_radius=15)
    progress_frame.pack(pady=20, padx=20, fill="x")

    progress_bar = ctk.CTkProgressBar(progress_frame, width=600, corner_radius=10, fg_color="#3D3D5C")
    progress_bar.set(0)  # Ensure progress bar starts at 0
    progress_bar.pack(pady=20)

    status_label = ctk.CTkLabel(
        progress_frame, text="Not started yet", font=("Trebuchet MS", 20), text_color="#FFFFFF"
    )
    status_label.pack(pady=10)

    # Start Button
    start_button_frame = ctk.CTkFrame(container, fg_color="#000000", corner_radius=15)
    start_button_frame.pack(pady=20)

    start_button = ctk.CTkButton(
        start_button_frame,
        text="Start Removing Duplicates",
        command=lambda: start_process(folder_path_var, action_var, progress_bar, status_label),
        fg_color="#FFFFFF",
        hover_color="#D6D6D6",
        font=("Trebuchet MS", 18, "bold"),
        text_color="#000000",
        corner_radius=25,
        height=60,
        width=280
    )
    start_button.pack()

    # Background Pattern
    app.configure(bg="#000000")

    app.mainloop()

# Run the UI
if __name__ == "__main__":
    show_ui()
