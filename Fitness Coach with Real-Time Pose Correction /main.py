# Fitness Coach with Real-Time Pose Correction — main.py

import cv2
import mediapipe as mp
import numpy as np

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def detect_pose_and_feedback(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        feedback = []

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

            if angle < 160:
                feedback.append(f'Bend your right elbow more; current angle: {int(angle)}')
            else:
                feedback.append(f'Good right elbow form; angle: {int(angle)}')

            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return image, feedback

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    pose_estimator = PoseEstimator()
    print('Starting pose estimation. Press q to quit.')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image, feedback = pose_estimator.detect_pose_and_feedback(frame)

        for i, text in enumerate(feedback):
            cv2.putText(image, text, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Fitness Coach - Pose Correction', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Requirements:
# pip install opencv-python mediapipe numpy

# Extension Ideas:
# - Add left-side joint checking
# - Implement squats, planks, and other exercise modules
# - Count exercise reps automatically
# - Store session history and plot form progress
# - Add voice feedback with a TTS module
