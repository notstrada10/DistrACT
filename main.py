import cv2

from detector import PhoneDetector

detector = PhoneDetector()
cap = cv2.VideoCapture(0)

frame_count = 0

while True:
    ret, frame = cap.read()
    frame_count += 1

    if frame_count % 30 == 0:  # detect every 5th frame
        boxes, scores = detector.detect(frame)
        for box in boxes:
            x1, y1, x2, y2 = box.int().tolist()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)



        print(boxes, scores)

    cv2.imshow("DistrACT", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
