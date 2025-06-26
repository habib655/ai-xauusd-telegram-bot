
import requests
import joblib
import numpy as np
from telegram import Bot

TELEGRAM_TOKEN = '8131550793:AAEMAAwKk5oUWu_uG_eJl9p0oGt_-G0yAVU'
CHAT_ID = '6751832888'
API_KEY = 'd1dumk1r01qpp0b47e1gd1dumk1r01qpp0b47e20'

def fetch_price():
    url = f"https://finnhub.io/api/v1/quote?symbol=XAUUSD&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("c", 0), data

def predict_signal(price):
    model = joblib.load("model.pkl")
    features = np.array([price, price - 0.5, price + 0.5, price * 1.01, price * 0.99]).reshape(1, -1)
    pred = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][int(pred)]
    return ("BUY" if pred == 1 else "SELL"), confidence * 100

def send_signal():
    price, _ = fetch_price()
    signal, confidence = predict_signal(price)
    message = f"🤖 AI XAU/USD Bot\n💰 Price: ${price}\n📊 Sinyal: {signal}\n🎯 Confidence: {confidence:.2f}%"
    Bot(token=TELEGRAM_TOKEN).send_message(chat_id=CHAT_ID, text=message)

send_signal()
