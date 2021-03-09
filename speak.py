"""
그냥 kakao.py에서 작동 안해서 분리한 파일
"""
from playsound import playsound  # 파일 재생 라이브러리
import os

path = os.environ["temp"] + "\\sound.mp3"
playsound(path)  # 재셍
