from flask import Flask, request, abort
import google.generativeai as genai
import os, PIL.Image
from linebot import LineBotApi, WebhookHandler
import linebot.exceptions
from linebot.models import MessageEvent, TextMessage, TextSendMessage

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

LINEBOT_TOKEN  = os.getenv("LINEBOT_CHANNEL_ACCESS_TOKEN")
LINEBOT_SECRET = os.getenv("LINEBOT_CHANNEL_SECRET")

# Flaskのオブジェクトを生成
app = Flask(__name__)

# LINEBOTのAPIのオブジェクトを生成
line_bot_api = LineBotApi(LINEBOT_TOKEN)
handler = WebhookHandler(LINEBOT_SECRET)

@app.route("/Linebot-With-Gemini")
def displayAccessSuccessMessage():
    return "サーバールートのアクセスに成功しました"


# LINEBOTのコールバックを設定する
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
        
    except linebot.exceptions.InvalidSignatureError:
        abort(400)
    return "OK"



# LINEBOTの応答処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # LINE上でユーザーからのメッセージを取得
    prompt = event.message.text
    
    # GeminiのAPIを呼ぶ
    response = model.generate_content(prompt)
    print(response)
    
    # LINEにgeminiの応答を返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(response.text)
    )