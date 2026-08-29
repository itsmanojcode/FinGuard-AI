def should_stop(already_processed=False, duplicate=False, confidence=1.0):
    if already_processed: return True, "Already processed."
    if duplicate: return True, "Duplicate event."
    if confidence < 0.70: return True, "Confidence below configured threshold."
    return False, "Continue."
