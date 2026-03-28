# 戀AI物語

這個專案目前保留可公開的程式碼，模型權重、訓練素材、參考音檔、輸出音檔與 API 金鑰都不會提交到 GitHub。

## 本機準備

1. 複製 `.env.example` 成 `.env`
2. 在 `.env` 填入 `OPENAI_API_KEY` 與 `ANTHROPIC_API_KEY`
3. 把本機模型與參考音檔放回下列資料夾
   - `server/GPT_weights/`
   - `server/SoVITS_weights/`
   - `server/Voice/`
4. 確認 GPT-SoVITS API 有啟動，預設是 `http://localhost:9872/`

## 執行順序

1. 啟動 GPT-SoVITS WebUI 並載入模型
2. 視需要執行 `server/change_gpt.py` 或 `server/change_sovits.py`
3. 執行 `server/server.py`
4. 開啟 `web/index.html`

## GitHub 上傳前注意

- `.env` 不會上傳
- `流螢-training/`、`server/GPT_weights/`、`server/SoVITS_weights/`、`server/Voice/` 不會上傳
- `Output/` 和 `output.wav` 不會上傳
