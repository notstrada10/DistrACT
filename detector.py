import cv2
import torch
from torchvision.models.detection import (
    FasterRCNN_MobileNet_V3_Large_FPN_Weights,
    fasterrcnn_mobilenet_v3_large_fpn,
)
from torchvision.transforms.functional import to_tensor

PHONE_CLASS = 77
CONFIDENCE_THRESHOLD = 0.7


class PhoneDetector:
    def __init__(self):
        weights = FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT
        self.transforms = weights.transforms()
        self.device = torch.device("cpu")
        self.model = fasterrcnn_mobilenet_v3_large_fpn(weights=weights).to(self.device)
        self.model.eval()

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tensor = to_tensor(rgb)
        tensor = self.transforms(tensor).to(self.device)

        with torch.no_grad():
            predictions = self.model([tensor])

        pred = predictions[0]
        mask = (pred["labels"] == PHONE_CLASS) & (pred["scores"] >= CONFIDENCE_THRESHOLD)

        boxes = pred["boxes"][mask]
        scores = pred["scores"][mask]

        print("Using device:", self.device)

        return boxes, scores
