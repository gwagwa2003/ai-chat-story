from gradio_client import Client
from config import get_gpt_sovits_api_url, get_sovits_weights_path

client = Client(get_gpt_sovits_api_url())
result = client.predict(
		sovits_path=get_sovits_weights_path(),
		prompt_language="中文",
		text_language="中文",
		api_name="/change_sovits_weights"
)
print(result)
