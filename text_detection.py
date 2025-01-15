import cv2
import pytesseract

class TextDetection:
    # Tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    def text_detect(self):
        _, frame = self.cap.read()
        
        text = pytesseract.image_to_string(frame, lang='eng')
        print("Detected Text:\n")

        d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, d['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Text Detection', frame)
        cv2.waitKey(5000)
        
        self.cap.release()
        cv2.destroyAllWindows()

        print(text)
        
        return text

# See working here
# detector = TextDetection()
# detector.text_detect()