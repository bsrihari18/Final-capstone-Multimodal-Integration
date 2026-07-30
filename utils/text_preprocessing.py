import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize

# Download resources (runs only once if already present)
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

stemmer = LancasterStemmer()
stop_words = set(stopwords.words("english"))


def preprocess_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"<.*?>", "", text)

    text = re.sub(r"\d+", "", text)

    text = text.translate(str.maketrans("", "", string.punctuation))

    words = word_tokenize(text)

    words = [stemmer.stem(word)
             for word in words
             if word not in stop_words]

    return " ".join(words)