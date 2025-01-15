from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator

class ObjectDetection:        
    def object_detect(self):
        model = YOLO('yolov8n.pt')
        
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        _, img = cap.read()

        results = model.predict(img)

        annotator = Annotator(img)
        detected = set()

        o = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = int(box.cls)
                
                label = model.names[c]
                o.append(label)
                annotator.box_label(b, label)
                detected.add(label)
        
        img = annotator.result()
        cv2.imshow('YOLO V8 Detection', img)

        cv2.waitKey(5000)

        cap.release()
        cv2.destroyAllWindows()

        print(o)

        return o

# See working here
# od = ObjectDetection()
# od.object_detect()