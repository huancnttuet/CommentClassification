# from utils.transformer import standardize_data, tokenizer
# a = ['Mình nhận được sp nhưng bị bụi trong màn hình. Tiki và shop đã hỗ trợ đổi sp mới ngay trong tuần, rất hài lòng với cách Tiki care khách hàng!',
#      'sản phẩm được đóng gói kỹ,còn nguyên tem ,cảm thấy hài lòng', 'Tuy hơi lag nhưng vẫn rất tuyệt trong tầm giá, máy đọc Ko mỏi mắt', 'tốt', 'chất lượng', 'Mới mua nhưng sạc không vào, khi đổi sạc khác thì bình thường. Bị hư sạc', 'chữ to, thích hợp cho người lớn tuổi. cảm ơn tiki nhieu', 'mới nhận và xài thấy ổn. tạm thời quánh giá tốt:)', 'mới test thấy ngon', 'wa nhanh tiki',
#      'Bán hàng lừa đảo hả mới sài chưa dc 10 ngày đả bi hư màn hình chưa hề bị rớt bể gì shop bán hang vậy làn sau ai dám mua mất uy tín', 'Sản phẩm đúng mô tả, mình dùng khoảng 4 ngày mới hết pin. Mọi thứ ok, chỉ là chưa tìm thấy chỗ nào giới hạn thời gian cuộc gọi đi', 'Mẫu mã đẹp,nghe gọi ok,giao hàng nhanh', 'Đt giá rẻ nên mua , máy dùng êm Cực kì hài lòng !!!!! Tốt']
# b = []


# print(tokenizer("Bác sĩ bây giờ có thể thản nhiên"))


import torch
from transformers import AutoModel, AutoTokenizer

phobert = AutoModel.from_pretrained("vinai/phobert-base")

# For transformers v4.x+:
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

# For transformers v3.x:
# tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# INPUT TEXT MUST BE ALREADY WORD-SEGMENTED!
line = "Tôi là sinh_viên trường đại_học Công_nghệ ."
print(tokenizer(line))
input_ids = torch.tensor([tokenizer.encode(line)])

with torch.no_grad():
    features = phobert(input_ids)  # Models outputs are now tuples

print(input_ids)
print(features)
