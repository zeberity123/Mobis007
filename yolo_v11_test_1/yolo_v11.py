from ultralytics import YOLO
import numpy as np


model = YOLO("yolo11x.pt")

p_results = model("089083.png")

# s_result = p_results[0].summary()
# for i in s_result:
#     print(i)
print(p_results[0].show())
# print(jssss[0])
# print(jssss[0]['name'])