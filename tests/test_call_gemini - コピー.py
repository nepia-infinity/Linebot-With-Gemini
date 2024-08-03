import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# プロンプトを送る
name = "東京タワー"
prompt = f'あなたは週末のお出かけスポット特集の記事原稿を手掛けるライターのプロです。{name}、当該施設の名前に対して以下の情報をjsonで返してください。緯度、経度、当該施設への最寄り駅名、電車やバスを含む公共交通機関、高速道路の出口、徒歩、車などアクセスに関する情報'
response2 = model.generate_content(prompt)
print(response2.text)