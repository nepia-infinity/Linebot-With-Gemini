from flask import Flask, request, abort
import google.generativeai as genai
import os, PIL.Image
from linebot import LineBotApi, WebhookHandler
import linebot.exceptions
from linebot.models import MessageEvent, TextMessage, TextSendMessage

LINEBOT_TOKEN  = os.getenv("LINEBOT_CHANNEL_ACCESS_TOKEN")
LINEBOT_SECRET = os.getenv("LINEBOT_CHANNEL_SECRET")

# Flaskのオブジェクトを生成
app = Flask(__name__)

# LINEBOTのAPIのオブジェクトを生成
line_bot_api = LineBotApi(LINEBOT_TOKEN)
handler = WebhookHandler(LINEBOT_SECRET)

@app.route("/linebot-with-gemini")
def displayRootAccessConfirmation():
    return "サーバールートのアクセスに成功しました"


# LINEBOTのコールバックを設定する
@app.route("/linebot-with-gemini/callback", methods=['POST'])
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
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    print(response)
    
    # LINEにgeminiの応答を返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(response.text)
    )
    

if __name__ == "__main__":
    # SSL証明書が保存されたディレクトリを指定
    cert_dir = '/etc/letsencrypt/live/bot.digitalcreation.tokyo/'
    
    # FlaskでSSLを使用してWebサーバーを起動
    import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(
        f'{cert_dir}fullchain.pem',
        f'{cert_dir}privkey.pem'
    )
    
    # 5000番ポートを使用するように変更
    app.run(debug=True, port=5000, host='0.0.0.0', ssl_context=ssl_context)
