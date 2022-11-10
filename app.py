# importing libraries
from flask import Flask, request, jsonify
from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL
from elitely_number_verification import USER_PHONE_NUMBER

app = Flask(__name__)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)

# Endpoint that's used to activate bot using "/start" and return greeting message or redirect to register phone number
@app.route('/webhook', methods=['POST'])
def index():
    req = request.get_json()
    bot = TelegramBot()
    global chat_id
    chat_id = bot.parse_webhook_data(req)
    success = bot.action(USER_PHONE_NUMBER)
    return jsonify(success=success) # TODO: Success should reflect the success of the reply

# Endpoint is used to send a lurker request using chat_id
@app.route('/LurkerRequest/<string:chat_id>', methods=['GET'])
def LurkerFunction(chat_id):
    bot = TelegramBot()
    success = bot.sendLurkerRequest(chat_id)
    return jsonify(success=success) # TODO: Success should reflect the success of the reply

# Endpoint is used to send an influencer payment request to lurker using chat_id
@app.route('/InfluencerPayment/<string:chat_id>', methods=['GET'])
def InfluencerPaymentRequest(chat_id):
    bot = TelegramBot()
    success = bot.sendInfluencerPaymentRequest(chat_id)
    return jsonify(success=success) # TODO: Success should reflect the success of the reply

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)