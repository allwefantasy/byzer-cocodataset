import json
import os
import itertools


def create_coco_format_json(rows, target_dir: str):
    import cv2
    image_path = os.path.join(target_dir, "images")
    annotation_path = os.path.join(target_dir, "annotations")

    if not os.path.exists(annotation_path):
        os.makedirs(annotation_path)

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    coco_format = {
        "info": {"datasetName": "dataset", "url": "", "version": "", "year": 2017, "contributor": "",
                 "date_created": ""},
        "licenses": [],
        "images": [],
        "categories": [],
        "annotations": []
    }

    catagories = []

    row_index = 0
    for row in rows:
        row_index += 1
        name: str = row["name"]
        img_path = os.path.join(image_path, name)
        with open(img_path, "wb") as f:
            f.write(row["data"])

        meta_str: str = row["meta"]
        meta = json.loads(meta_str)

        img = cv2.imread(img_path)
        img_height = img.shape[0]
        img_width = img.shape[1]
        img_channels = img.shape[2]

        coco_format["images"].append({
            "license": 0, "file_name": name, "coco_url": "",
            "height": img_height, "width": img_width, "date_captured": "", "flickr_url": "",
            "id": row_index
        })

        for obj in meta["data"]["result"]["objects"]:

            if obj["classType"] not in catagories:
                catagories.append(obj["classType"])

            category_id = catagories.index(obj["classType"])

            segmentation = [list(itertools.chain(*[[item["x"], item["y"]] for item in obj["coordinate"]]))]
            coco_format["annotations"].append({
                "segmentation": segmentation,
                "area": 0.0,
                "iscrowd": 0, "image_id": row_index,
                "bbox": [], "category_id": category_id,
                "id": row_index, "caption": ""
            })
        coco_meta_json = json.dumps(coco_format)
        coco_meta_path = os.path.join(annotation_path, "coco.json")
        with open(coco_meta_path, "w", encoding='utf-8') as f:
            f.write(coco_meta_json)

        return coco_meta_path
