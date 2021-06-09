from vncorenlp import VnCoreNLP
import re
from configs import ROOT_DIR

# See more details at: https://github.com/vncorenlp/VnCoreNLP

# Load rdrsegmenter from VnCoreNLP
rdrsegmenter = VnCoreNLP(ROOT_DIR + "/app/vncorenlp/VnCoreNLP-1.1.1.jar",
                         annotators="wseg", max_heap_size='-Xmx500m')


def standardize_data(row):
    # remove stopword
    # Remove . ? , at index final
    row = re.sub(r"[\.,\?]+$-", "", row)
    # Remove all . , " ... in sentences
    row = row.replace(",", " ").replace(".", " ") \
        .replace(";", " ").replace("“", " ") \
        .replace(":", " ").replace("”", " ") \
        .replace('"', " ").replace("'", " ") \
        .replace("!", " ").replace("?", " ") \
        .replace("-", " ").replace("?", " ")

    row = row.strip()
    return row


# Tokenizer
# def tokenizer(row):
#     return word_tokenize(row, format="text")

def tokenizer(text):
    # To perform word (and sentence) segmentation
    sentences = rdrsegmenter.tokenize(text)
    result = []
    for sentence in sentences:
        result.append(" ".join(sentence))

    return " ".join(result)


def unique_data(data_read):
    uniqueData = []
    for r in data_read:
        if r not in uniqueData:
            uniqueData.append(r)
    return uniqueData
