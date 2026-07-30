import nltk

# Download once at import; safe for Streamlit Cloud cold starts.
for resource in ("punkt", "punkt_tab", "stopwords"):
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass
