import os
import sys
from PIL import Image

# Allow Python to find our app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector import detect_damage
from severity import calculate_severity
from priority import calculate_priority


# --------------------------------------------------
# CHANGE THIS TO ANY ROAD IMAGE YOU WANT TO TEST
# --------------------------------------------------

IMAGE_PATH = "datasets/test/images"


def analyze_image(image_path):

    print("\n" + "=" * 60)
    print("       ROAD DAMAGE DETECTION SYSTEM")
    print("=" * 60)

    # Get image dimensions
    image = Image.open(image_path)

    image_width, image_height = image.size

    print(f"\nImage: {image_path}")
    print(f"Image size: {image_width} x {image_height}")

    # -----------------------------------------------
    # STEP 1: DAMAGE DETECTION
    # -----------------------------------------------

    detections = detect_damage(image_path)

    if not detections:
        print("\nNo road damage detected.")
        return

    print(f"\nDamage objects detected: {len(detections)}")

    # -----------------------------------------------
    # PROCESS EACH DETECTION
    # -----------------------------------------------

    for number, detection in enumerate(detections, start=1):

        damage_type = detection["class"]
        confidence = detection["confidence"]

        # -------------------------------------------
        # STEP 2: SEVERITY
        # -------------------------------------------

        severity_result = calculate_severity(
            detection,
            image_width,
            image_height
        )

        # -------------------------------------------
        # STEP 3: REPAIR PRIORITY
        # -------------------------------------------

        priority_result = calculate_priority(
            severity_result["severity_score"],
            damage_type,
            confidence
        )

        # -------------------------------------------
        # DISPLAY RESULT
        # -------------------------------------------

        print("\n" + "-" * 60)

        print(f"Detection #{number}")

        print(f"Damage Type       : {damage_type}")
        print(f"Confidence        : {confidence * 100:.2f}%")

        print(
            f"Damage Area       : "
            f"{severity_result['area_percentage']:.2f}%"
        )

        print(
            f"Severity Score    : "
            f"{severity_result['severity_score']:.2f}/100"
        )

        print(
            f"Severity Level    : "
            f"{severity_result['severity']}"
        )

        print(
            f"Repair Priority   : "
            f"{priority_result['priority_score']:.2f}/100"
        )

        print(
            f"Priority Level    : "
            f"{priority_result['priority']}"
        )

        print(
            f"Recommendation    : "
            f"{priority_result['recommendation']}"
        )

    print("\n" + "=" * 60)
    print("             ANALYSIS COMPLETE")
    print("=" * 60)


# --------------------------------------------------
# PROGRAM START
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python app\\main.py <image_path>")
        sys.exit()

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        sys.exit()

    analyze_image(image_path)