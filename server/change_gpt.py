from gradio_client import Client
from config import get_gpt_sovits_api_url, get_gpt_weights_path

client = Client(get_gpt_sovits_api_url())
result = client.predict(
		weights_path=get_gpt_weights_path(),
		api_name="/init_t2s_weights"
)
print(result)
