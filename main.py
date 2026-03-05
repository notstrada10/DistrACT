import cv2

from alert import AlertManager
from detector import PhoneDetector
from tracker import DistractionTracker


def main():
    detector = PhoneDetector()
    tracker = DistractionTracker(threshold_seconds=3)
    alert = AlertManager(cooldown_seconds=5)
    cap = cv2.VideoCapture(0)

    frame_count = 0
    last_boxes = []
    phone_detected = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            if frame_count % 30 == 0:
                boxes, scores = detector.detect(frame)
                last_boxes = boxes
                phone_detected = len(boxes) > 0

            distracted = tracker.update(phone_detected)

            if distracted:
                alert.trigger()
            else:
                alert.dismiss()

            for box in last_boxes:
                x1, y1, x2, y2 = box.int().tolist()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            cv2.imshow("DistrACT", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
