import cv2
import yaml

from alert import AlertManager
from detector import PhoneDetector
from tracker import DistractionTracker


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    detector = PhoneDetector(config["detection"])
    tracker = DistractionTracker(config["tracker"])
    alert = AlertManager(config["alert"])
    cap = cv2.VideoCapture(0)

    detector.start()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detector.update_frame(frame)
            boxes, scores = detector.get_results()
            phone_detected = len(boxes) > 0

            distracted = tracker.update(phone_detected)

            if distracted:
                alert.trigger()
            else:
                alert.dismiss()

            for box in boxes:
                x1, y1, x2, y2 = box.int().tolist()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            cv2.imshow("DistrACT", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        detector.stop()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
