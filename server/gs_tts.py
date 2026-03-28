from gradio_client import Client, file
import os
from config import (
	get_gpt_sovits_api_url,
	get_tts_aux_ref_audio_paths,
	get_tts_prompt_text,
	get_tts_ref_audio_path,
)

def text_to_speech(text, file_name):
	client = Client(get_gpt_sovits_api_url())
	result = client.predict(
			text=text,
			text_lang="中文",
			ref_audio_path=file(get_tts_ref_audio_path()),  
			aux_ref_audio_paths=[file(path) for path in get_tts_aux_ref_audio_paths()], 
			prompt_text=get_tts_prompt_text(),
			prompt_lang="中文",
			top_k=5,
			top_p=1,
			temperature=1,
			text_split_method="不切",
			batch_size=20,
			speed_factor=0.8,
			ref_text_free=False,
			split_bucket=True,
			fragment_interval=0.3,
			seed=-1,
			keep_random=True,
			parallel_infer=True,
			repetition_penalty=1.35,
			api_name="/inference"
	)
	#print(result)
	audio_path = result[0]  

	if os.path.exists(audio_path):
		os.makedirs("Output", exist_ok=True)
		output_wav_path = f"Output/{file_name}"  
		os.rename(audio_path, output_wav_path)
		print(f"音檔已成功儲存為: {output_wav_path}")
	else:
		print(f"文件未找到: {audio_path}")
