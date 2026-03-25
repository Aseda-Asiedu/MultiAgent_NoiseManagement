def get_policies():
    """
    Returns base policies for different zones. 
    Strict: Library, Hostel (Study)
    Relaxed: Lecture Hall, Co-working
    """
    return {
        "Library": {"acceptable": 35, "caution": 45},
        "Hostel": {"acceptable": 40, "caution": 50},
        "Lecture Hall": {"acceptable": 60, "caution": 70},
        "Co-working": {"acceptable": 65, "caution": 75},
    }