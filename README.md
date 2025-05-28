# Exercise-Tracking-with-Mediapipe-AI
Welcome to our website, the **Exercise Tracker with Mediapipe**
Our website is hosted with Flask server, and uses **mediapipe** to track motions of our body for each different exercises.
Logic of motion tracking varies according to the exercise and updated accordingly
After You click any of the exercise, Click on **Start Tracking**.
Camera will open, Counter and Stage will be shown in the camera.
If you want to Reset the count, click on **Reset Count**
![image](https://github.com/user-attachments/assets/bca45f42-c50e-4ff8-ad81-66db492a45b1)

![image](https://github.com/user-attachments/assets/89b28eae-8a90-4ab1-91a2-190dd7f29aa5)

![image](https://github.com/user-attachments/assets/f4df7ca0-9293-4ec8-b551-8e5bd6bc92ae)

![image](https://github.com/user-attachments/assets/bab1089d-221c-4b57-8ab1-2200b799bc06)

![image](https://github.com/user-attachments/assets/2cbd0966-60e6-4e1a-b665-23fd62ab8bb5)



Below is the mapping functions of each point in our body, assigned by Mediapipe defaultly
![image](https://github.com/user-attachments/assets/f1769703-2937-47fa-823c-ed0e874cc4e7)
# About Mediapipe
![image](https://github.com/user-attachments/assets/2d15be14-be5a-4482-ab41-ace6228b697f)

**MediaPipe** is a cross-platform, open-source framework for building and deploying machine learning (ML) pipelines for real-time applications. It allows developers to process media data like video and audio on various devices, including mobile, web, and desktop, with a focus on on-device inference. MediaPipe offers both pre-built solutions for specific tasks and a framework for building custom pipelines. 

**Key Features of MediaPipe:**

**Cross-Platform:**
MediaPipe supports multiple platforms, including Android, iOS, Web, and C++. 

**Real-time Processing:**
Designed for processing multimedia data in real-time, making it suitable for live streaming and interactive applications. 

**Customizable:**
MediaPipe offers pre-built solutions, but also allows developers to customize and extend them to meet specific needs. 

**On-Device Inference:**
MediaPipe focuses on running ML models directly on the device, reducing latency and data transmission. 

**Open-Source:**
MediaPipe is an open-source project, allowing for community contributions and customization. 

**MediaPipe Solutions:**
Offers pre-built solutions for common tasks like face detection, pose estimation, hand tracking, and gesture recognition. 

**MediaPipe Framework:**
Provides the low-level building blocks for creating custom ML pipelines. 

**MediaPipe Tasks:**
Offers high-level APIs for deploying solutions across different platforms with minimal code. 

**MediaPipe Model Maker:**
Allows developers to customize pre-trained models with their own data. 

**Applications of MediaPipe:**

**Face Detection and Tracking:** Identifying and tracking faces in images and videos. 

**Pose Estimation:** Estimating the pose of a person or object in an image or video. 

**Hand Tracking and Gesture Recognition:** Tracking hands and recognizing gestures in real-time. 

**Virtual Reality and Augmented Reality:** Creating virtual avatars and applying facial filters and effects. 

**Interactive Applications:** Enabling user interaction through hand gestures or voice commands. 

**On-Device Machine Learning:** Running ML models directly on mobile devices and other embedded systems. 

# Firebase - To keep track of Everything
Firebase module is enabled in our website in order to keep track of every exercise you do.
After doing the exercise, there is an option to save the details to Firebase and update the same
After doing the exercise click on the Stop & Log Session, and enter the Reps and Sets Count, and click on save to Firebase
![image](https://github.com/user-attachments/assets/1ff491b1-0a04-4d3f-a646-b15b09d82f1c)

![image](https://github.com/user-attachments/assets/452e40fd-2302-4fc8-993f-671f4f4ab70c)

# Usage
Install **Visual studio Code**

Then in the VS Code terminal:
-pip install requirements.txt

Then,
run -python app.py




