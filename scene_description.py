import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class SceneDescription:        
    def scene_detect(self):
        # BLIP model and processor
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        blip_model.load_state_dict(torch.load("fine-tuned_BLIP.pt"))

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        
        _, img = cap.read()
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        inputs = processor(images=img_rgb, return_tensors="pt")
        
        with torch.no_grad():
            caption = blip_model.generate(**inputs)
            scene_description = processor.decode(caption[0], skip_special_tokens=True)
        
        cv2.putText(img, scene_description, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('BLIP Scene Description', img)

        cv2.waitKey(7000)

        cap.release()
        cv2.destroyAllWindows()

        print(scene_description)

        return scene_description
    
# See working here
# sd = SceneDescription()
# sd.scene_detect()