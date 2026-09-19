def calculate_priority(severity_score, damage_type, confidence):
    """
    Calculate repair priority based on:
    - Severity score
    - Damage type
    - Detection confidence
    """

    # Damage importance weights
    damage_weights = {
        "pothole": 100,
        "crack": 70,
        "manhole": 40
    }

    damage_weight = damage_weights.get(damage_type, 50)

    # Convert confidence to percentage
    confidence_percentage = confidence * 100

    # Calculate priority score
    priority_score = (
        0.60 * severity_score
        + 0.25 * damage_weight
        + 0.15 * confidence_percentage
    )

    # Keep score between 0 and 100
    priority_score = min(100, max(0, priority_score))

    # Priority category
    if priority_score < 25:
        priority = "Low"
        recommendation = "Routine inspection"

    elif priority_score < 50:
        priority = "Moderate"
        recommendation = "Schedule maintenance"

    elif priority_score < 75:
        priority = "High"
        recommendation = "Repair should be scheduled soon"

    else:
        priority = "Critical"
        recommendation = "Immediate repair recommended"

    return {
        "priority_score": round(priority_score, 2),
        "priority": priority,
        "recommendation": recommendation
    }