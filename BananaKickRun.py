import re
from gensim.models import FastText
from keras.models import load_model
import numpy as np
import warnings
import random
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

with open('./fword_list.txt', 'r', encoding='UTF8') as f:
    fword_str = ''
    while True:
        line = f.readline()
        if line == '' :
            break
        fword_str += line.strip('\n') + '|'
    fword_str = fword_str[:-2]

def make_trigram(sentence):
    word_position = []
    word_index = 0

    for char in sentence:
        word_position.append(word_index)
        if char == " ":
            word_index += 1

    # 비속어 위치 찾기
    badwords = []
    pattern = re.compile(fword_str)
    matchObjs = re.finditer(pattern, sentence)
    badwords += [word_position[obj.span()[0]] for obj in matchObjs] # 해당 단어가 속한 어절의 위치

    sentence = [" "] + sentence.split(" ") + [" "] # 맨 앞, 맨 뒤 padding
    badwords = list(set(badwords))

    return [(sentence[index], sentence[index+1], sentence[index+2], index) for index in badwords]


# 모델 불러오기
fasttext_model = FastText.load("./Fasttext.model")
cnn_model = load_model("./CNN_model")


# vectorize를 위해 리스트를 청크 단위로 분해
# n = 청크 단위
def chunks(l, n, trigram_list):
        for i in range(0, len(l), n):
            yield (l[i:i + n], trigram_list[i//n][-1])


# 자모분리기
CHOSUNG_LIST = [u'ㄱ',u'ㄲ',u'ㄴ',u'ㄷ',u'ㄸ',u'ㄹ',u'ㅁ',u'ㅂ',u'ㅃ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅉ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']
JOONGSUNG_LISTS = [u'ㅏ',u'ㅐ',u'ㅑ',u'ㅒ',u'ㅓ',u'ㅔ',u'ㅕ',u'ㅖ',u'ㅗ',u'ㅘ',u'ㅙ',u'ㅚ',u'ㅛ',u'ㅜ',u'ㅝ',u'ㅞ',u'ㅟ',u'ㅠ',u'ㅡ',u'ㅢ',u'ㅣ']
JONGSUNG_LIST = [u'_',u'ㄱ',u'ㄲ',u'ㄳ',u'ㄴ',u'ㄵ',u'ㄶ',u'ㄷ',u'ㄹ',u'ㄺ',u'ㄻ',u'ㄼ',u'ㄽ',u'ㄾ',u'ㄿ',u'ㅀ',u'ㅁ',u'ㅂ',u'ㅄ',u'ㅅ',u'ㅆ',u'ㅇ',u'ㅈ',u'ㅊ',u'ㅋ',u'ㅌ',u'ㅍ',u'ㅎ']

def kor_decompose(word, end_char="_"):
    result = []
    
    for char in word:
        char_unicode = ord(char)
        
        if 0xD7A3 < char_unicode or char_unicode < 0xAC00:
            result.append(char)
            continue

        chosung_index = int((((char_unicode - 0xAC00) / 28) / 21) % 19)
        joongsung_index = int(((char_unicode - 0xAC00) / 28) % 21)
        jongsung_index = int((char_unicode - 0xAC00) % 28)
        
        chosung = CHOSUNG_LIST[chosung_index]
        joongsung = JOONGSUNG_LISTS[joongsung_index]
        jongsung = JONGSUNG_LIST[jongsung_index]
        
        # 종성이 없을 경우 end_char
        if jongsung_index == 0:
            jongsung = end_char
        
        result.append(chosung)
        result.append(joongsung)
        result.append(jongsung)

    return "".join(result)


# 실행 함수
def bananaKick(origin_text: str, ref_val=0.65, modes=0):
    global mode
    mode = modes

    text = clear_word(origin_text)
    trigram_list = make_trigram(text)
    
    # vectorize
    trigram_vec = np.array([np.array(fasttext_model.wv[kor_decompose(word)]) for trigram in trigram_list for word in trigram[:-1]])
    trigram_vec = np.array(list(chunks(trigram_vec, 3, trigram_list)))
    trigram_vec = np.array([np.append(_[0].flatten(), _[1]) for _ in trigram_vec]) # 151 dimension

    # 단어 위치만 뽑아내어 분리
    try:
        word_index = np.int8(trigram_vec[:, -1])
    except: 
        return origin_text
    trigram_vec = np.delete(trigram_vec, -1, axis=1)

    # keras input에 맞추기
    trigram_vec = trigram_vec.reshape(trigram_vec.shape[0], trigram_vec.shape[1], 1)
    last_index, result = cnn_predict(trigram_vec, ref_val, word_index)
    
    return cnn_result(last_index, result, origin_text, trigram_list)

def cnn_predict(trigram_vec, ref_val, word_index):
    result = cnn_model.predict(trigram_vec) > ref_val # 기본값 = 0.65보다 높으면 욕설
    result = result.reshape(-1).tolist()
    if mode == 1:
        cnn_describe(trigram_vec, result, word_index)

    all_index = word_index.tolist()
    #print("all_index =", all_index)
    true_index = result
    #print("true_index =", true_index)

    i = 0
    last_index = []
    for num in all_index:
        if true_index[i] == True:
            last_index.append(num)
        i += 1
        
    return last_index, result

def cnn_describe(trigram_vec, result, word_index):
    print("1. 단어 위치\n", word_index)
    print("2. 예측 확률\n", cnn_model.predict(trigram_vec))
    print('3. result =', result)
    print("4. Class, 단어 위치\n", list(zip(result, word_index.tolist())))


def cnn_result(last_index, result, origin_text, trigram_list):
    if mode == 1:
        print("욕설로 분류됨:\n", np.array(trigram_list)[np.array(result)])
        print("욕설이 아닌 것으로 분류됨:\n", np.array(trigram_list)[np.array(result) == False], '\n')

    ujul = []
    index = 0
    tempstr = ''
    for char in origin_text:
        if char == ' ':
            ujul.append(tempstr)
            ujul.append(index)
            index += 1
            tempstr = ''
        else: tempstr += char
    ujul.append(tempstr)
    ujul.append(index)

    index = 0
    result = ''
    for i in ujul:
        if i in last_index:
            ujul[index-1] = happyWord(len(ujul[index-1]))
            ujul.pop(index)
        elif i not in last_index and type(i) == int:
            ujul.pop(index)
        index += 1
    result = ' '.join(s for s in ujul)

    return result

# 순화 단어 리스트
def happyWord(num: int):
    if num == 1:   return random.choice(['꽃', '꿀', '굿'])
    elif num == 2: return random.choice(['아잉', '어머', '좋아', '멋져'])
    elif num == 3: return  random.choice(['사랑해', '나이스', '멋쟁이'])
    elif num >= 4: return random.choice(['아잉', '어머', '좋아', '굿','사랑해', '나이스'])

    else: return "오류: 글자 수가 0임"


pattern = re.compile("[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]") # 특수문자 제거
def clear_word(word):
    word = re.sub(pattern, "", word)
    return word


if __name__ == "__main__":
    while True:
        text = input('입력: ')
        if text == '/종료': break
        
        # modes=0 : 기본값, 결과 문장만 출력
        # modes=1 : 상세 정보 출력
        result = bananaKick(text, modes=1)
        print(result)