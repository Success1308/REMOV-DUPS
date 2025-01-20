# REMOV DUPS

<p align="center">
  <img src="https://github.com/user-attachments/assets/2bc97d74-859b-4e43-8887-dd92ac1b7518" alt="Image" width="350" />
</p>

## My Journey to Solving a Personal Problem

A while back, I faced a frustrating problem: my devices were cluttered with duplicate images and videos. Every tool I found to clean up this mess either came with a hefty price tag or was riddled with limitations. I needed a solution that was effective and free. Since nothing fit the bill, I decided to take matters into my own hands and create a tool that solves the problem once and for all.

That’s how **REMOV DUPS** was born—a Windows app designed to help not only me but also others like you who are tired of battling duplicate files. And the best part? It’s free and straightforward to use!

---

## What This App Does

**REMOV DUPS** is a Windows desktop application that scans a folder for duplicate images and videos. It identifies duplicates based on perceptual hashing, ensuring that even visually similar files are detected. Once duplicates are identified, the app allows you to:

1. **Delete the duplicates**: Free up space on your device instantly.
2. **Move the duplicates**: Organize them into a separate folder for review later.

With its modern interface and efficient processing, this tool is designed to make cleaning up your files as simple as possible.

---

## How to Use It

1. **Download the App**
   Simply download the executable folder named `OUTPUT`. It contains the app icon (`app_icon.ico`), logo (`app_logo1.png`), and the executable file. All these files must be in the same folder for the app to run. Once ready, just run the executable file—no installation required!

2. **Select a Folder**
   Open the app and select the folder you want to scan for duplicates.

3. **Choose Your Action**
   Decide whether you want to delete duplicates immediately or move them to a dedicated folder.

4. **Start the Process**
   Hit the "Start Removing Duplicates" button, and let the app do the rest! The progress bar will keep you updated as files are scanned and processed.

---

## Why I Made This App

When I couldn’t find a free and reliable solution for removing duplicate images, I decided to build my own. I learned about image processing, perceptual hashing, and UI design along the way. This app is the result of countless hours of coding and testing, driven by the goal of solving my own problem and helping others like me.

![image](https://github.com/user-attachments/assets/35569858-b777-4d3e-b540-40db61f68076)


---

## Features

- **Supports Multiple File Types**: Works with images (e.g., JPG, PNG, HEIC) and videos (e.g., MP4, MOV).
- **User-Friendly Interface**: Intuitive design with clear instructions.
- **Customizable Actions**: Choose between deleting or moving duplicates.
- **Fast and Efficient**: Uses multi-threading to process files quickly.
- **Free to Use**: No hidden costs or premium versions—just download and go!

---

## Technical Tools Used

Creating **REMOV DUPS** involved leveraging a variety of technical tools and libraries:

- **Python**: The core programming language used to develop the application.
- **Pillow (PIL)**: For handling and processing image files.
- **imagehash**: To compute perceptual hashes for identifying duplicate images.
- **OpenCV (cv2)**: For video frame extraction and processing.
- **CustomTkinter**: For building a modern and user-friendly graphical interface.
- **pillow-heif**: To add support for HEIC/HEIF image formats.
- **ThreadPoolExecutor**: For efficient multi-threaded file processing.
- **PyInstaller**: To package the application into a standalone executable for Windows.

This project demonstrates my Python skills, showcasing proficiency in image and video processing, GUI design, multi-threading, and packaging applications for deployment.

---

## Algorithm Used

The application uses a combination of algorithms and techniques to identify duplicate files efficiently:

1. **Perceptual Hashing (pHash)**:

   - Images are processed using the `imagehash` library, which generates a perceptual hash. This allows the app to detect visually similar images, even if they are resized or slightly altered.

2. **Video Frame Hashing**:

   - The first frame of video files is extracted using `OpenCV`, and a perceptual hash is generated. This ensures that visually identical videos are identified as duplicates.

3. **Multi-threading**:

   - File processing is handled using `ThreadPoolExecutor` to enable concurrent execution, speeding up the scanning process.

4. **File Path Sorting**:

   - Duplicate files are sorted based on relative file path and length, ensuring consistency in how duplicates are handled.

5. **Efficient File Handling**:
   - The app only processes supported file types (e.g., images and videos), reducing unnecessary overhead.

---

## Try It Yourself

If you’re tired of paid tools or manual cleanup, give **REMOV DUPS** a try. I built it to solve my problem, and now it’s here to solve yours too. Let’s keep our devices clutter-free together!
