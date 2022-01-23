from django.forms import inlineformset_factory
import matplotlib
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2

## Download Model

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


## Make Detections From Image

# img = 'https://ultralytics.com/images/zidane.jpg'
# results = model(img)
# results.print()

# plt.imshow(np.squeeze(results.render()))
# results.show()

## Realtime Detections

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    
    # Make detections
    results = model(frame)
    
    np.squeeze(results.render())
    
    print(results.pandas().xyxy[0].name)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()