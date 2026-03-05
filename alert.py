import os
import time

import cv2
import numpy as np


class AlertManager:
    def __init__(self, cooldown_seconds=5):
        self.cooldown = cooldown_seconds
        self.last_alert_time = 0
        self.alert_image = cv2.imread("img/putdown.jpg")


    def _create_alert_image(self):
        img = np.zeros((300, 600, 3), dtype=np.uint8)
        img[:] = (0, 0, 200)  # red background
        cv2.putText(img, "PUT YOUR PHONE DOWN!", (30, 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        return img

    def trigger(self):
        now = time.time()
        if now - self.last_alert_time < self.cooldown:
            return

        self.last_alert_time = now
        cv2.imshow("ALERT", self.alert_image)
        # macOS built-in alert sound
        os.system("afplay /System/Library/Sounds/Sosumi.aiff &")

    def dismiss(self):
        cv2.destroyWindow("ALERT")
