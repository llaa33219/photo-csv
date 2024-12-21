import random
import csv
from PIL import Image
import os

def load_eligible_words(word_file):
    # words.txt에서 단어 로드: 6글자 이하인 단어만 필터
    with open(word_file, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip() and len(line.strip()) <= 6]
    return words

def word_to_numbers(word):
    # 단어를 숫자로 변환: a=1, ..., z=26
    nums = [ord(c) - ord('a') + 1 for c in word]
    # 6글자 미만이면 0으로 패딩
    while len(nums) < 6:
        nums.append(0)
    return nums[:6]

def image_to_data(img_path):
    # 이미지 파일 로드 -> 흑백 변환 -> 20x20 리사이즈 -> 픽셀(0~255) -> 0~9 스케일링
    with Image.open(img_path).convert("L") as img:
        img = img.resize((20,20))
        pixels = list(img.getdata())  # 400개 값 (0~255)
        scaled_pixels = [int((p * 10) / 256) for p in pixels]  # 0~9로 축소
        return "1" + "".join(str(p) for p in scaled_pixels)  # '1' + 400자리 숫자

# 1. 실제로 있는 단어 중 6글자 이하인 것을 선정
word_file = "words.txt"
words = load_eligible_words(word_file)
if not words:
    raise ValueError("6글자 이하의 단어가 없습니다.")

# 여기서는 임의로 하나를 선택
selected_word = random.choice(words)

# 2. 그 단어에 맞는 이미지가 준비되어 있다고 가정 (images/<단어>.jpg)
img_path = f"images/{selected_word}.jpg"
if not os.path.exists(img_path):
    raise FileNotFoundError(f"단어 '{selected_word}'에 맞는 이미지 '{img_path}'가 존재하지 않습니다. 이미지 준비가 필요합니다.")

# 3. 단어를 숫자로 변환
word_nums = word_to_numbers(selected_word)

# 4. 이미지를 숫자로 변환
image_str = image_to_data(img_path)

# 예: CSV로 한 행 저장
output_file = "output.csv"
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    # CSV 한 행: (단어숫자6개, 이미지숫자401자리 문자열)
    row = word_nums + [image_str]
    writer.writerow(row)

print(f"단어: {selected_word}")
print("단어 숫자 변환:", word_nums)
print("이미지 숫자 변환(길이):", len(image_str), "첫 50글자:", image_str[:50])
print(f"CSV파일 '{output_file}'에 저장 완료.")
