def calculate_severity(detection, image_width, image_height):
    """
    Calculate a severity score for a detected road-damage object.

    The score is based on:
    1. Damage type
    2. Relative bounding-box area
    """

    damage_type = detection["class"]

    x1 = detection["x1"]
    y1 = detection["y1"]
    x2 = detection["x2"]
    y2 = detection["y2"]

    # Bounding-box dimensions
    box_width = max(0, x2 - x1)
    box_height = max(0, y2 - y1)

    # Bounding-box area
    box_area = box_width * box_height

    # Total image area
    image_area = image_width * image_height

    # Relative area percentage
    area_percentage = (box_area / image_area) * 100

    # Damage-type weights
    damage_weights = {
        "pothole": 1.0,
        "crack": 0.7,
        "manhole": 0.4
    }

    weight = damage_weights.get(damage_type, 0.5)

    # Calculate preliminary severity score
    raw_score = area_percentage * weight * 10

    # Keep score between 0 and 100
    severity_score = min(100, max(0, raw_score))

    # Severity category
    if severity_score < 25:
        severity = "Low"

    elif severity_score < 50:
        severity = "Moderate"

    elif severity_score < 75:
        severity = "High"

    else:
        severity = "Critical"

    return {
        "damage_type": damage_type,
        "area_percentage": round(area_percentage, 2),
        "severity_score": round(severity_score, 2),
        "severity": severity
    }