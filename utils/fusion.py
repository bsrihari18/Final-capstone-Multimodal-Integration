def fuse_emotions(face_emotion, text_emotion):

    # -----------------------------
    # Happy
    # -----------------------------
    if face_emotion == "Happy":

        if text_emotion == "positive":
            return "Happy"

        if text_emotion == "neutral":
            return "Happy"

        return "Neutral"

    # -----------------------------
    # Neutral
    # -----------------------------
    elif face_emotion == "Neutral":

        if text_emotion == "positive":
            return "Happy"

        if text_emotion == "neutral":
            return "Neutral"

        return "Sad"

    # -----------------------------
    # Angry
    # -----------------------------
    elif face_emotion == "Angry":
        return "Angry"

    # -----------------------------
    # Sad
    # -----------------------------
    elif face_emotion == "Sad":

        if text_emotion == "positive":
            return "Neutral"

        return "Sad"

    # -----------------------------
    # Fear
    # -----------------------------
    elif face_emotion == "Fear":
        return "Fear"

    # -----------------------------
    # Surprise
    # -----------------------------
    elif face_emotion == "Surprise":

        if text_emotion == "negative":
            return "Neutral"

        return "Surprise"

    # -----------------------------
    # Disgust
    # -----------------------------
    elif face_emotion == "Disgust":
        return "Disgust"

    return face_emotion