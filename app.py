import threading
import time

import cv2
import rumps
import yaml

from detector import PhoneDetector
from tracker import DistractionTracker


class DistrACTApp(rumps.App):
    def __init__(self):
        super().__init__("DistrACT", title="📵", quit_button=None)

        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        self.detector = PhoneDetector(config["detection"])
        self.tracker = DistractionTracker(config["tracker"])
        self.alert_config = config["alert"]

        self.cap = None
        self.running = False

    def _monitor_loop(self):
        self.cap = cv2.VideoCapture(0)
        self.detector.start()
        last_alert_time = 0

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.detector.update_frame(frame)
            boxes, scores = self.detector.get_results()
            phone_detected = len(boxes) > 0

            distracted = self.tracker.update(phone_detected)

            if distracted:
                now = time.time()
                if now - last_alert_time >= self.alert_config["cooldown_seconds"]:
                    last_alert_time = now
                    rumps.notification(
                        "DistrACT",
                        "Put your phone down!",
                        "Get back to studying!",
                    )

        self.detector.stop()
        self.cap.release()

    @rumps.clicked("Start Monitoring")
    def toggle_monitoring(self, sender):
        if self.running:
            self.running = False
            sender.title = "Start Monitoring"
        else:
            self.running = True
            sender.title = "Stop Monitoring"
            thread = threading.Thread(target=self._monitor_loop, daemon=True)
            thread.start()

    @rumps.clicked("Quit")
    def quit_app(self, _):
        self.running = False
        rumps.quit_application()


if __name__ == "__main__":
    DistrACTApp().run()
