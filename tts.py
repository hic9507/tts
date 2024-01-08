# -*- coding: utf-8 -*-
"""TTS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DUaAIxQEK46oM11zar2hDg1xnWYFlv_0

## 1. 구글 드라이브 마운트

---



음성합성을 위해 학습한 모델이 있는 구글 드라이브를 마운트한다.  
마운트할 구글 드라이브 내에 다음 파일들이 존재하는지 확인한다.

- `/Colab Notebooks/data/glowtts-v2/model_file.pth.tar`
- `/Colab Notebooks/data/glowtts-v2/config.json`
- `/Colab Notebooks/data/hifigan-v2/model_file.pth.tar`
- `/Colab Notebooks/data/hifigan-v2/config.json`
"""

from google.colab import drive
drive.mount('/content/drive')

!nvidia-smi

"""## 2. 필수 라이브러리 및 함수 불러오기

실행에 필요한 라이브러리 및 함수를 불러온다.

"""

import os
import sys
from pathlib import Path

# Commented out IPython magic to ensure Python compatibility.
# %cd /content
!git clone --depth 1 https://github.com/sce-tts/TTS.git -b sce-tts
!git clone --depth 1 https://github.com/sce-tts/g2pK.git
# %cd /content/TTS
!pip install -q --no-cache-dir -e .
# %cd /content/g2pK
!pip install -q --no-cache-dir "konlpy" "jamo" "nltk" "python-mecab-ko"
!pip install -q --no-cache-dir -e .

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/g2pK
import g2pk
g2p = g2pk.G2p()

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/TTS
import re
import sys
from unicodedata import normalize
import IPython

from TTS.utils.synthesizer import Synthesizer

def normalize_text(text):
    text = text.strip()

    for c in ",;:":
        text = text.replace(c, ".")
    text = remove_duplicated_punctuations(text)

    text = jamo_text(text)

    text = g2p.idioms(text)
    text = g2pk.english.convert_eng(text, g2p.cmu)
    text = g2pk.utils.annotate(text, g2p.mecab)
    text = g2pk.numerals.convert_num(text)
    text = re.sub("/[PJEB]", "", text)

    text = alphabet_text(text)

    # remove unreadable characters
    text = normalize("NFD", text)
    text = "".join(c for c in text if c in symbols)
    text = normalize("NFC", text)

    text = text.strip()
    if len(text) == 0:
        return ""

    # only single punctuation
    if text in '.!?':
        return punctuation_text(text)

    # append punctuation if there is no punctuation at the end of the text
    if text[-1] not in '.!?':
        text += '.'

    return text


def remove_duplicated_punctuations(text):
    text = re.sub(r"[.?!]+\?", "?", text)
    text = re.sub(r"[.?!]+!", "!", text)
    text = re.sub(r"[.?!]+\.", ".", text)
    return text


def split_text(text):
    text = remove_duplicated_punctuations(text)

    texts = []
    for subtext in re.findall(r'[^.!?\n]*[.!?\n]', text):
        texts.append(subtext.strip())

    return texts


def alphabet_text(text):
    text = re.sub(r"(a|A)", "에이", text)
    text = re.sub(r"(b|B)", "비", text)
    text = re.sub(r"(c|C)", "씨", text)
    text = re.sub(r"(d|D)", "디", text)
    text = re.sub(r"(e|E)", "이", text)
    text = re.sub(r"(f|F)", "에프", text)
    text = re.sub(r"(g|G)", "쥐", text)
    text = re.sub(r"(h|H)", "에이치", text)
    text = re.sub(r"(i|I)", "아이", text)
    text = re.sub(r"(j|J)", "제이", text)
    text = re.sub(r"(k|K)", "케이", text)
    text = re.sub(r"(l|L)", "엘", text)
    text = re.sub(r"(m|M)", "엠", text)
    text = re.sub(r"(n|N)", "엔", text)
    text = re.sub(r"(o|O)", "오", text)
    text = re.sub(r"(p|P)", "피", text)
    text = re.sub(r"(q|Q)", "큐", text)
    text = re.sub(r"(r|R)", "알", text)
    text = re.sub(r"(s|S)", "에스", text)
    text = re.sub(r"(t|T)", "티", text)
    text = re.sub(r"(u|U)", "유", text)
    text = re.sub(r"(v|V)", "브이", text)
    text = re.sub(r"(w|W)", "더블유", text)
    text = re.sub(r"(x|X)", "엑스", text)
    text = re.sub(r"(y|Y)", "와이", text)
    text = re.sub(r"(z|Z)", "지", text)

    return text


def punctuation_text(text):
    # 문장부호
    text = re.sub(r"!", "느낌표", text)
    text = re.sub(r"\?", "물음표", text)
    text = re.sub(r"\.", "마침표", text)

    return text


def jamo_text(text):
    # 기본 자모음
    text = re.sub(r"ㄱ", "기역", text)
    text = re.sub(r"ㄴ", "니은", text)
    text = re.sub(r"ㄷ", "디귿", text)
    text = re.sub(r"ㄹ", "리을", text)
    text = re.sub(r"ㅁ", "미음", text)
    text = re.sub(r"ㅂ", "비읍", text)
    text = re.sub(r"ㅅ", "시옷", text)
    text = re.sub(r"ㅇ", "이응", text)
    text = re.sub(r"ㅈ", "지읒", text)
    text = re.sub(r"ㅊ", "치읓", text)
    text = re.sub(r"ㅋ", "키읔", text)
    text = re.sub(r"ㅌ", "티읕", text)
    text = re.sub(r"ㅍ", "피읖", text)
    text = re.sub(r"ㅎ", "히읗", text)
    text = re.sub(r"ㄲ", "쌍기역", text)
    text = re.sub(r"ㄸ", "쌍디귿", text)
    text = re.sub(r"ㅃ", "쌍비읍", text)
    text = re.sub(r"ㅆ", "쌍시옷", text)
    text = re.sub(r"ㅉ", "쌍지읒", text)
    text = re.sub(r"ㄳ", "기역시옷", text)
    text = re.sub(r"ㄵ", "니은지읒", text)
    text = re.sub(r"ㄶ", "니은히읗", text)
    text = re.sub(r"ㄺ", "리을기역", text)
    text = re.sub(r"ㄻ", "리을미음", text)
    text = re.sub(r"ㄼ", "리을비읍", text)
    text = re.sub(r"ㄽ", "리을시옷", text)
    text = re.sub(r"ㄾ", "리을티읕", text)
    text = re.sub(r"ㄿ", "리을피읍", text)
    text = re.sub(r"ㅀ", "리을히읗", text)
    text = re.sub(r"ㅄ", "비읍시옷", text)
    text = re.sub(r"ㅏ", "아", text)
    text = re.sub(r"ㅑ", "야", text)
    text = re.sub(r"ㅓ", "어", text)
    text = re.sub(r"ㅕ", "여", text)
    text = re.sub(r"ㅗ", "오", text)
    text = re.sub(r"ㅛ", "요", text)
    text = re.sub(r"ㅜ", "우", text)
    text = re.sub(r"ㅠ", "유", text)
    text = re.sub(r"ㅡ", "으", text)
    text = re.sub(r"ㅣ", "이", text)
    text = re.sub(r"ㅐ", "애", text)
    text = re.sub(r"ㅒ", "얘", text)
    text = re.sub(r"ㅔ", "에", text)
    text = re.sub(r"ㅖ", "예", text)
    text = re.sub(r"ㅘ", "와", text)
    text = re.sub(r"ㅙ", "왜", text)
    text = re.sub(r"ㅚ", "외", text)
    text = re.sub(r"ㅝ", "워", text)
    text = re.sub(r"ㅞ", "웨", text)
    text = re.sub(r"ㅟ", "위", text)
    text = re.sub(r"ㅢ", "의", text)

    return text


def normalize_multiline_text(long_text):
    texts = split_text(long_text)
    normalized_texts = [normalize_text(text).strip() for text in texts]
    return [text for text in normalized_texts if len(text) > 0]

def synthesize(text):
    wavs = synthesizer.tts(text, None, None)
    return wavs

"""## 3. 학습한 모델 불러오기

학습한 Glow-TTS와 HiFi-GAN 모델을 불러옵니다.

다른 체크포인트에서 불러오시려면 아래 코드에서 경로를 아래와 같이 적절하게 수정한다.

```python
synthesizer = Synthesizer(
    "/content/drive/My Drive/Colab Notebooks/data/glowtts-v2/glowtts-v2-May-31-2021_08+17AM-d897f2e/best_model.pth.tar",
    "/content/drive/My Drive/Colab Notebooks/data/glowtts-v2/glowtts-v2-May-31-2021_08+17AM-d897f2e/config.json",
    None,
    "/content/drive/My Drive/Colab Notebooks/data/hifigan-v2/hifigan-v2-May-31-2021_08+26AM-d897f2e/checkpoint_300000.pth.tar",
    "/content/drive/My Drive/Colab Notebooks/data/hifigan-v2/hifigan-v2-May-31-2021_08+26AM-d897f2e/config.json",
    None,
    None,
    False,
)
```
"""

synthesizer = Synthesizer(
    "/content/drive/My Drive/Colab Notebooks/data/glowtts-v2/model_file.pth.tar",
    "/content/drive/My Drive/Colab Notebooks/data/glowtts-v2/config.json",
    None,
    "/content/drive/My Drive/Colab Notebooks/data/hifigan-v2/model_file.pth.tar",
    "/content/drive/My Drive/Colab Notebooks/data/hifigan-v2/config.json",
    None,
    None,
    False,
)
symbols = synthesizer.tts_config.characters.characters

"""## 4. 음성 합성

실제 음성 합성을 수행하고 텍스트를 음성으로 변경해준다.
"""

texts = """
안녕하세요 저는 황인창입니다, 오늘은 날씨가 많이 춥네요, 추울 땐 따뜻한 차 한 잔 어때요?
나 졸업한다!
나 졸업한다.
나 졸업하니?
내가 그린 기린 그림은 긴 기린 그림이고 니가 그린 기린 그림은 안 긴 기린 그림이다.
"""
for text in normalize_multiline_text(texts):
    wav = synthesizer.tts(text, None, None)
    IPython.display.display(IPython.display.Audio(wav, rate=22050))