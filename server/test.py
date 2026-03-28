SYSMSG={"role": "system", "content": "你是一個溫柔活潑的女朋友"}
MESSAGE=[{"role": "user", "content": "現在跟你說話的人是你的男朋友"},{"role": "assistant", "content": "知道拉！"}]
MESSAGE.insert(0, SYSMSG)
print(MESSAGE)
del MESSAGE[0]
print(MESSAGE)