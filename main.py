"""
트핀봇!
"""
import random
import time

import irc.bot  # 트위치 채팅
import requests  # 웹훅
import auth  # 개인정보들
import kakao  # 카카오 API

speaking = False  # 지금 말하고 있는지


class TwitchBot(irc.bot.SingleServerIRCBot):
    """
    트위치 봇
    """
    def __init__(self, username, client_id, token, channel, delay_time):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.delay_time = delay_time

        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # irc 접속
        server = 'irc.chat.twitch.tv'
        port = 6667

        print('Connecting to ' + server + ' on port ' + str(port) + '...')

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    # noinspection PyUnusedLocal
    def on_welcome(self, c, e):
        """
        :param c:저도 잘 모르니까 무시하세요
        :param e:저도 잘 모르니까 무시하세요
        """
        # 트위치 IRC 접속 준비
        print('Joining ' + self.channel)

        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    # noinspection PyUnusedLocal
    def on_pubmsg(self, c, e):
        """
        :param c: 저도 잘 모르니까 무시하세요
        :param e: 저도 잘 모르니까 무시하세요
        :return: 저도 잘 모르니까 무시하세요
        """
        global speaking
        time.sleep(1)
        if speaking:  # 말하고 있으면 정지
            return
        if e.arguments[0][:1] == "#" or e.arguments[0][:1] == "@":  # 주석 또는 멘션이면 정지
            return
        speaking = True
        print("->" + e.arguments[0])  # 채팅 받음

        def recieve(query):  # 핑퐁빌더
            """
            :param query: 핑퐁빌더에게 요청할 것
            :return: 요청한 결과
            """
            # 웹훅 준비
            url = auth.pingpong_url.format(auth.channel+str(random.randint(0,25566)))
            head = {"Authorization": auth.pingpong_token, "Content-Type": "application/json"}
            data = '{"request": {"query":"' + query + '"}}'
            data = data.encode("utf-8")
            res = requests.post(url, headers=head, data=data)

            # 텍스트 추출
            tmp = res.json()["response"]["replies"]

            # noinspection PyStatementEffect
            [
                {
                    'text': '아무말에도 곧잘 대답하는 이 봇은 핑퐁 빌더로 만든 봇이에요 😚\n👉 https://pingpong.us'
                },
                {
                    'from':
                        {
                            'score': 0.9958863854408264, 'name': 'conversation', 'link': '/bot/6041a285e4b078d873a1a4b0/conversation?scriptId=6041a285e4b078d873a1a519', 'from': '대화 시나리오 / 안녕'
                        },
                    'type': 'text',
                    'text': '아아아아안녕하신지요!'
                 }
            ]
            ret=[]
            for i in tmp:
                if(i.get("text") is None):
                    #사진 등
                    continue
                if(i["text"].find("https://pingpong.us") == -1):
                    #브랜드 메세지 아님
                    ret.append(i["text"])
            """
            try:
                tmp = tmp[len(tmp) - 1]["text"]
            except KeyError:
                tmp = tmp[len(tmp) - 2]["text"]"""
            for i in ret:
                print("<-" + i)  # 추출 완료
            return ret

        txt = recieve(e.arguments[0])
        for j in txt:
            c.privmsg(self.channel, j)  # 채팅 보냄
            kakao.gettts(j)  # 재생
        speaking = False
        return e.arguments[0]


def main():
    """
    초기 시작 프로세스
    """
    username = auth.UserName
    client_id = auth.twitch_ClientID
    token = auth.twitch_token
    channel = auth.channel
    delay_time = 20

    bot = TwitchBot(username, client_id, token, channel, delay_time)
    bot.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
