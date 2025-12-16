# -*- coding: utf-8 -*-
"""
病院受付20セット会話の音声ファイルを自動生成
患者＝女性声（nova）
受付＝男性声（alloy）
出力フォルダ：audio/
"""

import os
from openai import OpenAI

# OpenAIクライアントの初期化
client = OpenAI()

# 保存フォルダ作成
os.makedirs("audio", exist_ok=True)

# === 会話データ（日本語のみ、男女ペア） ===
dialogues = [
    ("こんにちは。保険証またはマイナンバーカードをお持ちですか？", "はい、ここにあります。"),
    ("こちらにお書きください。", "わかりました。"),
    ("初診ですか？再診ですか？", "初診です。"),
    ("お名前と連絡先をお願いします。", "はい、今書きます。"),
    ("今日はどの科を受診されますか？", "内科をお願いします。"),
    ("熱はありますか？", "はい、三十七度くらいあります。"),
    ("喉が痛いですか？", "はい、少し痛いです。"),
    ("お待ち時間は十五分ほどです。", "わかりました。ありがとうございます。"),
    ("風邪の症状ですか？", "はい、咳と鼻が出ます。"),
    ("体温を測ってもらえますか？", "はい、今測ります。"),
    ("結果を教えてください。", "三十八度ありました。"),
    ("診療券を受け取ってください。", "はい、ありがとうございます。"),
    ("このあと、お名前が呼ばれるまでお待ちください。", "はい、わかりました。"),
    ("お待ち席の椅子に座ってお待ちください。", "はい、そこで待ちます。"),
    ("お名前を呼ばれるまで少しお待ちください。", "わかりました。ありがとうございます。"),
    ("診療が終わりましたら、また受付に来てください。", "はい、わかりました。"),
    ("お会計は受付でお願いします。", "はい、医療費はいくらですか？"),
    ("千二百円になります。", "はい、これでお願いします。"),
    ("お釣りは八百円です。", "ありがとうございます。"),
    ("薬局は向こうの角にあります。", "わかりました。ありがとうございました。")
]

# === 音声生成関数 ===
def generate_audio(text, filename, voice):
    """指定テキストを音声合成し、指定ファイルに保存"""
    print(f"▶ 生成中: {filename} ...")
    audio_path = os.path.join("audio", filename)
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    ) as response:
        response.stream_to_file(audio_path)
    print(f"✅ 保存完了: {audio_path}")

# === 音声生成ループ ===
for i, (staff_text, patient_text) in enumerate(dialogues, start=1):
    # 受付（男性声）
    staff_file = f"staff{i:02}.mp3"
    generate_audio(staff_text, staff_file, voice="alloy")

    # 患者（女性声）
    patient_file = f"patient{i:02}.mp3"
    generate_audio(patient_text, patient_file, voice="nova")

print("\n🎉 すべての音声ファイルを 'audio/' フォルダに保存しました。")
