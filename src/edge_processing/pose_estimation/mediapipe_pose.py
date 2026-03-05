import mediapipe as mp
import cv2

class MediaPipePose:

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False)

    def estimate(self, image):

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        result = self.pose.process(image_rgb)

        keypoints = []

        if result.pose_landmarks:
            for lm in result.pose_landmarks.landmark:
                keypoints.append((lm.x, lm.y))

        return keypoints
    