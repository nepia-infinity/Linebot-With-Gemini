import google.generativeai as genai
import PIL.Image
import os

# 画像をgeminiに送り、何の画像かを判別してもらう
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
file_path = r'C:\Users\nepia\OneDrive\デスクトップ\linebot_with_gemini\img\sakura.jpg'
img = PIL.Image.open(file_path)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content(["これは何ですか？日本語で説明してください", img])
print(response.text)


# プロンプトを送る
prompt = "400年後の現代社会に生きる魔女狩りの末裔の少女についての小説を書いてください"
response2 = model.generate_content(prompt)
print(response2.text)