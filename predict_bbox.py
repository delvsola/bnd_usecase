import torch
import cv2
import os
import os.path as op
from tqdm import tqdm
import json

TEST_DIR = "datasets/images/test"
CONF_THRESHOLD = 0.6
model = torch.hub.load('ultralytics/yolov5', 'custom', path="weights/best_yolov5m300.pt")

out = []
for root, folders, files in os.walk(TEST_DIR):
    for file in tqdm(files):
        file_id = file.replace(".tif", "")
        tqdm.write(file_id)
        img = cv2.imread(op.join(root, file))[..., ::-1]
        results = model(img)
        res_json = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
        if res_json:
            for sign in res_json:
                if sign["confidence"] >= CONF_THRESHOLD:
                    out.append("{},{},{},{},{},{}".format(
                        file_id,
                        int(sign["xmin"]),
                        int(sign["ymin"]),
                        int(sign["xmax"]),
                        int(sign["ymax"]),
                        round(sign["confidence"], 2)
                    ))
                elif sign["confidence"] < CONF_THRESHOLD and len(res_json) == 1:
                    out.append(f"{file_id},0,0,0,0,0")
        else:
            out.append(f"{file_id},0,0,0,0,0")

print("Saving submission file...")
with open("bbox_submission.csv", "w") as fp:
    fp.write("id,xmin,ymin,xmax,ymax,confidence\n")
    fp.write("\n".join(out))
