from ultralytics import YOLO
from multiprocessing import freeze_support

def main():
    model = YOLO("yolov8s.pt")

    model.train(
        data="datasets/data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,
        workers=0,
        name="road_damage_v8s_100ep"
    )

if __name__ == "__main__":
    freeze_support()
    main()