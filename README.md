# Smart Color Sorting Robotic Arm

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry%20Pi-red)
![Status](https://img.shields.io/badge/Status-Finished%20-brightgreen)

> **Inclusive Automation:** An intelligent robotic system designed to autonomously recognize, pick, and organize objects based on their color, demonstrating how computer vision can assist in sorting tasks.

---

## 📋 About the Project

This project consists of a **3D printed robotic gripper** controlled by servomotors, integrated with a computer vision system. The main objective is to create an accessible solution for automated object separation.

Using a **Raspberry Pi** and a **Pi Camera**, the system processes images in real-time using **OpenCV**. Through Color Masking logic, the robot distinguishes between different object categories (e.g., separating blue items from red items) and uses the gripper to sort them into their corresponding places.

### 🎯 Key Features
* **Color-Based Classification:** Uses a color space to filter and identify specific object categories.
* **Smart Tracking:** Calculates the centroid of the detected object for precise gripper positioning.
* **Servomotor Control:** Coordinate movement (Pan/Tilt/Grip) to gently pick up the object.
* **Automated Sorting:** Automatically organizes mixed items into distinct groups based on color.

---

## 🛠️ Hardware and Materials

| Component | Quantity | Description |
| :--- | :---: | :--- |
| **Raspberry Pi 3/4** | 1 | The project brain (image processing and GPIO control). |
| **Pi Camera Module** | 1 | Video capture for OpenCV. |
| **Servomotors** | 4 | SG90 (Micro) models for the joints. |
| **3D Printed Parts** | Kit | Separately printed robotic arm. |
| **Power Supply** | 1 | 9V external battery. |

---

## ⚙️ Software Architecture

The project uses **Python** and the **OpenCV** library. The logic flow works as follows:

1.  **Capture:** The Pi Camera sends the video stream.
2.  **Pre-processing:** The image is converted from BGR to HSV.
3.  **Masking:** A specific color *Range* is defined (e.g., "Target Color"), OpenCV creates a binary mask.
4.  **Contour Detection:** Identifies the object's area and location on the screen.
5.  **Kinematics:** The software converts the coordinates into angles for the servomotors.
6.  **Actuation:** The gripper descends, picks the object, and places it in the correct sorting bin.

---

### Prerequisites
Make sure your Raspberry Pi is up to date.
