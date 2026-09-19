from flask import Flask, render_template, request
import os
import sys
from PIL import Image


# ============================================================
# PATH SETUP
# ============================================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))

if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from detector import detect_damage
from severity import calculate_severity
from priority import calculate_priority


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder=os.path.join(APP_DIR, "templates"),
    static_folder=os.path.join(APP_DIR, "static")
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        results=None,
        message=None
    )


# ============================================================
# ANALYZE ROAD IMAGE
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # --------------------------------------------------------
    # CHECK UPLOADED FILE
    # --------------------------------------------------------

    if "image" not in request.files:
        return "No image uploaded.", 400

    file = request.files["image"]

    if file.filename == "":
        return "No image selected.", 400


    # --------------------------------------------------------
    # CREATE UPLOAD FOLDER
    # --------------------------------------------------------

    upload_folder = os.path.join(
        APP_DIR,
        "uploads"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    # --------------------------------------------------------
    # SAVE UPLOADED IMAGE
    # --------------------------------------------------------

    image_path = os.path.join(
        upload_folder,
        file.filename
    )

    file.save(image_path)

    print()
    print("=" * 60)
    print("ROADVISION AI - IMAGE ANALYSIS")
    print("=" * 60)

    print(f"Image saved: {image_path}")


    # --------------------------------------------------------
    # GET IMAGE DIMENSIONS
    # --------------------------------------------------------

    try:

        image = Image.open(image_path)

        image_width, image_height = image.size

        print(
            f"Image size: "
            f"{image_width} x {image_height}"
        )

    except Exception as e:

        print(f"Image error: {e}")

        return (
            f"Unable to read image: {e}",
            400
        )


    # --------------------------------------------------------
    # YOLO DETECTION
    # --------------------------------------------------------

    print()
    print("Running YOLO detection...")

    try:

        detections = detect_damage(
            image_path
        )

    except Exception as e:

        print(f"YOLO detection error: {e}")

        return (
            f"Detection failed: {e}",
            500
        )


    print(
        f"Detections found: {len(detections)}"
    )


    # --------------------------------------------------------
    # SEVERITY + PRIORITY ANALYSIS
    # --------------------------------------------------------

    final_results = []


    for detection in detections:

        # ----------------------------------------------------
        # CALCULATE SEVERITY
        # ----------------------------------------------------

        severity_result = calculate_severity(
            detection,
            image_width,
            image_height
        )


        # ----------------------------------------------------
        # CALCULATE REPAIR PRIORITY
        # ----------------------------------------------------

        priority_result = calculate_priority(
            severity_result["severity_score"],
            detection["class"],
            detection["confidence"]
        )


        # ----------------------------------------------------
        # STORE FINAL RESULT
        # ----------------------------------------------------

        final_results.append({

            "damage_type":
                detection["class"],


            "confidence":
                round(
                    detection["confidence"] * 100,
                    2
                ),


            "area_percentage":
                severity_result[
                    "area_percentage"
                ],


            "severity_score":
                severity_result[
                    "severity_score"
                ],


            "severity":
                severity_result[
                    "severity"
                ],


            "priority_score":
                priority_result[
                    "priority_score"
                ],


            "priority":
                priority_result[
                    "priority"
                ],


            "recommendation":
                priority_result[
                    "recommendation"
                ]

        })


    # --------------------------------------------------------
    # PRINT RESULTS IN TERMINAL
    # --------------------------------------------------------

    print()
    print("-" * 60)
    print("ANALYSIS RESULTS")
    print("-" * 60)


    for result in final_results:

        print(
            f"Damage Type       : "
            f"{result['damage_type']}"
        )

        print(
            f"Confidence        : "
            f"{result['confidence']}%"
        )

        print(
            f"Damage Area       : "
            f"{result['area_percentage']}%"
        )

        print(
            f"Severity Score    : "
            f"{result['severity_score']}/100"
        )

        print(
            f"Severity          : "
            f"{result['severity']}"
        )

        print(
            f"Priority Score    : "
            f"{result['priority_score']}/100"
        )

        print(
            f"Repair Priority   : "
            f"{result['priority']}"
        )

        print(
            f"Recommendation    : "
            f"{result['recommendation']}"
        )

        print("-" * 60)


    # --------------------------------------------------------
    # SEND RESULTS TO HTML
    # --------------------------------------------------------

    return render_template(
        "index.html",
        results=final_results,
        image=file.filename,
        message=None
    )


# ============================================================
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )