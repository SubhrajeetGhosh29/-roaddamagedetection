from ultralytics import YOLO


# Load our trained YOLOv8s model
MODEL_PATH = "runs/detect/road_damage_v8s_100ep/weights/best.pt"

model = YOLO(MODEL_PATH)


def detect_damage(image_path):
    """
    Detect potholes, cracks and manholes
    from a road image.
    """

    results = model.predict(
        source=image_path,
        conf=0.25,
        save=False
    )

    detections = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class": class_name,
                "confidence": confidence,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })

    return detections