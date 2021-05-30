"""
카카오 API
"""
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

    # 다운
    req = urllib.request.Request(url, data=body, headers=head, method="POST")
    data = urllib.request.urlopen(req).read()

    # 파일 작성
    if os.path.isfile(path):  # 파일 존재하면
        os.remove(path)  # 삭제
    f = open(path, "wb")
    f.write(data)
    f.close()

    # 재생
    os.system("C:\\Users\\_endorphin\\Documents\\vs\\venv\\pythonProject\\Scripts\\python.exe ./speak.py")
