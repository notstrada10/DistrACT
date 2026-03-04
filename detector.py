import torch
from torchvision.models.detection import (
    FasterRCNN_MobileNet_V3_Large_FPN_Weights,
    fasterrcnn_mobilenet_v3_large_fpn,
)


class PhoneDetector:
    def __init__(self):
        weights = FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT
        self.transforms = weights.transforms()
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.model = fasterrcnn_mobilenet_v3_large_fpn(weights=weights).to(self.device)
        self.model.eval()

    def detect(self, frame):
        pass
