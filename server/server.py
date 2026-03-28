import openai
from websockets.server import serve
import json
import asyncio
import anthropic
import base64
import stt
from gs_tts import text_to_speech
from config import (
    get_anthropic_api_key,
    get_default_chat_model,
    get_openai_api_key,
    get_server_host,
    get_server_port,
)

gpt_key = get_openai_api_key()
claude_key = get_anthropic_api_key()
client = anthropic.Anthropic(api_key = claude_key)


IPADDR=get_server_host()
PORT=get_server_port()
MODEL=get_default_chat_model()
#SYSMSG={"role": "system", "content": "你是一個溫柔活潑的女朋友"}
#MESSAGE=[SYSMSG,{"role": "user", "content": "現在跟你說話的人是你的男朋友"},{"role": "assistant", "content": "知道拉！"}]
GPT_History=[{"role": "system", "content": "你是一個溫柔活潑的女朋友"}, {"role": "user", "content": "用繁體中文跟我聊天"},{"role": "assistant", "content": "我知道拉！"}]
Claude_History=[{"role": "user", "content": "我是你的男朋友"},{"role": "assistant", "content": "我知道拉！"}]

socketList={}

class GPT:
    def __init__(self, gpt_key):
        openai.api_key=gpt_key
        self.model=MODEL
        self.picflag = False
    def Prediction(self,socket,inputMessage):
        print(MODEL)

        if socket not in socketList.keys():
            socketList[socket]=GPT_History.copy()    
        if MODEL == "ft:gpt-4o-mini-2024-07-18:personal:chatv1:AESsNK7j":
            socketList[socket][0] = {"role": "system", "content": "你是一個溫柔活潑的女朋友"}
        if MODEL == "ft:gpt-4o-mini-2024-07-18:personal:shy:AFA0sorC":
            socketList[socket][0] = {"role": "system", "content": "你是一個性格文靜且靦腆的女朋友"}
        if len(inputMessage)<100:
            socketList[socket].append({"role":"user","content":inputMessage})
        else:
            self.picflag = True
            socketList[socket].append({"role": "user","content": [
                    {
                        "type": "text",
                        "text": "圖片是我想對你說的話"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{inputMessage}"
                        }
                    }
                ]
            })
        print("gpt start")
        completion=openai.chat.completions.create(
            model=self.model,
            messages=socketList[socket]
            )
        print(completion.choices[0].message.content)
        socketList[socket].append({"role":"assistant","content":completion.choices[0].message.content})
        if self.picflag:
            socketList[socket][-2] = {"role":"user","content":"我上傳了一張圖片，請描述一下你看到了什麼"}
            self.picflag = False
        print(socketList[socket])
        return completion.choices[0].message.content
    

class Claude:   
    def __init__(self, claude_key):
        anthropic.Anthropic(api_key = claude_key)
        self.model="claude-3-opus-20240229"
        self.picflag = False
    def Prediction(self,socket,inputMessage):
        if socket not in socketList.keys():
            socketList[socket]=Claude_History.copy() 
        if len(inputMessage)<100:
            socketList[socket].append({"role":"user","content":inputMessage})
        else:
            self.picflag = True
            socketList[socket].append({"role": "user","content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": inputMessage,
                    },
                },
                {
                    "type": "text", 
                    "text": "圖片是我想對你說的話"
                }
            ],})
        print("claude")
        response = anthropic.Anthropic(api_key = claude_key).messages.create(
            model=self.model,
            max_tokens = 128,
            temperature = 0,
            system = "你叫依琪，是雍心的的女朋友，說話自然，俏皮可愛，不囉唆，你的任務是回答男朋友的問題，回答的內容不要超過十個字，像是：{問題：“去吃火鍋不” 回答：“好呀好呀，想去耶！”}。此外，你在對話中偶爾要使用表情！",
            messages = socketList[socket]
        )
        print((response.content)[0].text)
        socketList[socket].append({"role":"assistant","content":(response.content)[0].text})
        if self.picflag:
            socketList[socket][-2] = {"role":"user","content":"我上傳了一張圖片，請描述一下你看到了什麼"}
            self.picflag = False
        print(socketList[socket])
        return (response.content)[0].text


class WebSocket:
    def __init__(self, content):
        self.content = content
        self.current_model = "ft:gpt-4o-mini-2024-07-18:personal:chatv1:AESsNK7j"  # 預設使用 GPT 模型

    async def flow(self, socket):
        type = self.message["type"]
        msg = self.message["msg"]

        if type == "content":
            print(self.current_model)
            if self.current_model != "claude-3-opus-20240229":    
                response = self.content.gpt.Prediction(socket, msg)
            else:
                response = self.content.claude.Prediction(socket, msg)
            TextToSpeech(response, socket)
            await self.SendStatus(socket, response)
        elif type == "mode":
            #if self.current_model == "ft:gpt-4o-mini-2024-07-18:personal:chatv1:AESsNK7j":
             #   print(1)
              #  socketList[socket][0] = {"role": "system", "content": "你是一個溫柔活潑的女朋友"}
            #elif self.current_model == "ft:gpt-4o-mini-2024-07-18:personal:shy:AFA0sorC":
             #   print(2)
              #  socketList[socket][0] = {"role": "system", "content": "你是一個性格文靜且靦腆的女朋友"}
            if msg in ["ft:gpt-4o-mini-2024-07-18:personal:chatv1:AESsNK7j", "ft:gpt-4o-mini-2024-07-18:personal:shy:AFA0sorC", "claude-3-opus-20240229"]:
                self.current_model = msg 
                global MODEL
                MODEL = self.current_model
                print(f"切換到模型: {self.current_model}")
            #print(socketList[socket])
        elif type == "pic":
            print(self.current_model)
            msg = msg[22:]
            if self.current_model != "claude-3-opus-20240229":    
                response = self.content.gpt.Prediction(socket, msg)
            else:
                response = self.content.claude.Prediction(socket, msg)
            TextToSpeech(response, socket)
            await self.SendStatus(socket, response)
        elif type == "audio":
            print(self.current_model)
            print("audio")
            print(msg)
            base64_str = msg.split(',')[1]
            audio_data = base64.b64decode(base64_str)
            with open('./output.wav', 'wb') as f:
                f.write(audio_data)

            msg = stt.stt('./output.wav')
            response = self.content.claude.Prediction(socket, msg)
            TextToSpeech(response, socket)
            await self.SendStatus(socket, response)

    async def AcceptConnection(self, socket):
        async for message in socket:
            items = json.loads(message)
            self.message = items
            await self.flow(socket)
          
    async def SendStatus(self, socket, status):
        await socket.send(status)

    async def SocketInit(self):
        async with serve(self.AcceptConnection, IPADDR, PORT):
            await asyncio.Future() 


class Content:
    def __init__(self):
        self.gpt=GPT(gpt_key)
        self.claude=Claude(claude_key)
        self.webSocket=WebSocket(self)
    
    def Flow(self):
        asyncio.run(self.webSocket.SocketInit())
    

def TextToSpeech(text,socket):
    FILE_NAME = f"{int((len(socketList[socket])-2)/2)}.wav"
    try:
        text_to_speech(text, FILE_NAME)
        print(f"生成音頻文件: {FILE_NAME}")
    except Exception as err:
        print("發生異常:", err)

def main():
    content=Content()
    print(f"server start.Listening on {IPADDR}:{PORT}")
    content.Flow()

if __name__=="__main__":
    main()
