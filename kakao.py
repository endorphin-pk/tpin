"""
카카오 API
"""
import time

import auth
import os
# noinspection PyCompatibility
import urllib.request


def gettts(text):  # TTS 제작
    """
    :param text: TTS 생성할 텍스트
    """
    # TTS 다운 준비
    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    head = {"Content-Type": "application/xml", "Authorization": auth.kakao_restkey}
    body = "<speak><voice name=\"WOMAN_READ_CALM\">{}</voice></speak>".format(text)
    body = body.encode("utf-8")

    path = os.environ["temp"] + "\\sound.mp3"
    path.replace("\\","/")

    # 다운
    req = urllib.request.Request(url, data=body, headers=head, method="POST")
    data = urllib.request.urlopen(req).read()

    # 파일 작성
    if os.path.isfile(path):  # 파일 존재하면
        os.remove(path)  # 삭제
    f = open(path, "wb")
    f.write(data)
    f.close()

    #재생
    import pygame

    freq = 16000  # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
    bitsize = -16  # signed 16 bit. support 8,-8,16,-16
    channels = 1  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get right sound)

    # default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(30)
    time.sleep(0.5)
    pygame.mixer.quit()