# -----------------------------
# Text Model Integration
# -----------------------------

def integrate_text_predictions(svc, rf, xgb):

    # All models agree
    if svc == rf == xgb:
        return svc

    # Majority Vote
    if svc == rf:
        return svc

    if svc == xgb:
        return svc

    if rf == xgb:
        return rf

    # No agreement
    # Priority:
    # SVC > RF > XGB

    return svc