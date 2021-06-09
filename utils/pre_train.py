import torch
from transformers import AutoModel, AutoTokenizer
import numpy
from vncorenlp import VnCoreNLP
from configs import ROOT_DIR
phobert = AutoModel.from_pretrained("vinai/phobert-base")

# For transformers v4.x+:
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

# For transformers v3.x:
# tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# See more details at: https://github.com/vncorenlp/VnCoreNLP

# Load rdrsegmenter from VnCoreNLP
rdrsegmenter = VnCoreNLP(ROOT_DIR + "/app/vncorenlp/VnCoreNLP-1.1.1.jar",
                         annotators="wseg", max_heap_size='-Xmx500m')


def pre_train(text):
    # INPUT TEXT MUST BE ALREADY WORD-SEGMENTED!
    # line = "Tôi là sinh_viên trường đại_học Công_nghệ . Tôi đến từ Hải Phòng."

    sentences = rdrsegmenter.tokenize(text)
    v_tokenized = []
    for sentence in sentences:
        v_tokenized.append(tokenizer.encode(" ".join(sentence)))
    max_len = 100
    # Chèn thêm số 1 vào cuối câu nếu như không đủ 100 từ
    padded = numpy.array([i + [1] * (max_len - len(i)) for i in v_tokenized])
    # Đánh dấu các từ thêm vào = 0 để không tính vào quá trình lấy features
    attention_mask = numpy.where(padded == 1, 0, 1)

    # Chuyển thành tensor
    padded = torch.tensor(padded).to(torch.long)
    attention_mask = torch.tensor(attention_mask)
    # Lấy features dầu ra từ BERT
    with torch.no_grad():
        last_hidden_states = phobert(
            input_ids=padded, attention_mask=attention_mask)

    v_features = last_hidden_states[0][:, 0, :].numpy()

    return v_features
# With TensorFlow 2.0+:
# from transformers import TFAutoModel
# phobert = TFAutoModel.from_pretrained("vinai/phobert-base")
