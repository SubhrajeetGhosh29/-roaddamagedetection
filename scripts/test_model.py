from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model.predict(
    source="datasets/test/images",
    save=True,
    conf=0.25
)

print("Prediction completed")