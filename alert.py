import os
import time

import cv2


class AlertManager:
    def __init__(self, config):
        self.cooldown = config["cooldown_seconds"]
        self.last_alert_time = 0
        self.alert_image = cv2.imread(config["image_path"])
        self.sound_path = config["sound_path"]

    def trigger(self):
        now = time.time()
        if now - self.last_alert_time < self.cooldown:
            return

        self.last_alert_time = now
        cv2.imshow("ALERT", self.alert_image)
        os.system(f"afplay {self.sound_path} &")

    def dismiss(self):
        cv2.destroyWindow("ALERT")
