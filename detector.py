import threading

import cv2
import torch
from torchvision.models.detection import (
    FasterRCNN_MobileNet_V3_Large_FPN_Weights,
    fasterrcnn_mobilenet_v3_large_fpn,
)
from torchvision.transforms.functional import to_tensor

PHONE_CLASS = 77


class PhoneDetector:
    def __init__(self, config):
        self.confidence_threshold = config["confidence_threshold"]

        weights = FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT
        self.transforms = weights.transforms()
        self.device = torch.device("cpu")
        self.model = fasterrcnn_mobilenet_v3_large_fpn(weights=weights).to(self.device)
        self.model.eval()
        print("Using device:", self.device)

        self.lock = threading.Lock()
        self.latest_boxes = []
        self.latest_scores = []
        self.latest_frame = None
        self.running = False

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._detection_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False

    def update_frame(self, frame):
        with self.lock:
            self.latest_frame = frame.copy()

    def _detection_loop(self):
        while self.running:
            with self.lock:
                frame = self.latest_frame

            if frame is None:
                continue

            boxes, scores = self._detect(frame)

            with self.lock:
                self.latest_boxes = boxes
                self.latest_scores = scores

    def _detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tensor = to_tensor(rgb)
        tensor = self.transforms(tensor).to(self.device)

        with torch.no_grad():
            predictions = self.model([tensor])

        pred = predictions[0]
        mask = (pred["labels"] == PHONE_CLASS) & (pred["scores"] >= self.confidence_threshold)

        boxes = pred["boxes"][mask]
        scores = pred["scores"][mask]

        return boxes, scores

    def get_results(self):
        with self.lock:
            return self.latest_boxes, self.latest_scores
