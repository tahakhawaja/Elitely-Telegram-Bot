import requests

from config import TELEGRAM_SEND_MESSAGE_URL

class TelegramBot:

    def __init__(self):
        """"
        Initializes an instance of the TelegramBot class.

        Attributes:
            chat_id:str: Chat ID of Telegram chat, used to identify which conversation outgoing messages should be send to.
            text:str: Text of Telegram chat
            first_name:str: First name of the user who sent the message
        """

        self.chat_id = None
        self.text = None
        self.first_name = None


    def parse_webhook_data(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions

        Args:
            data:str: JSON string of data
        """

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        return self.chat_id


    def action(self, user_phone_number):
        """
        Conditional actions based on set webhook data.

        Returns:
            bool: True if the action was completed successfully else false
        """

        success = None

        if user_phone_number:
            if self.incoming_message_text == '/start':
                self.outgoing_message_text = "This bot is able to receive notifications from the Elitely platform. Click here to get connected. Get real time updates on meet and chat requests to maximize your experience."
                success = self.send_message()
        else:
            self.outgoing_message_text = "To use the Elitely Bot you must register a phone number to your existing Elitely account. Click here to register a phone number."
            success = self.send_message()
        
        return success

    def sendLurkerRequest(self, chat_id):
        """
        Sends notification to Personality/Influencer when a Lurker requests a meetup or unlocks a chat with him/her
        """

        success = None

        self.outgoing_message_text = "You have received a meet up request. Click here to check the details and accept, reject, or reschedule."
        success = self.send_lurker_message(chat_id)

        return success

    def sendInfluencerPaymentRequest(self, chat_id):
        """
        Sends notification to Lurker when Personality/Influencer accepts a meetup and sends him link to payments page
        """

        success = None

        self.outgoing_message_text = "Your meet up request has been accepted! Click here to make a payment."
        success = self.send_lurker_message(chat_id)

        return success


    def send_message(self):
        """
        Sends message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    
    def send_lurker_message(self, chat_id):
        """
        Sends Lurker request message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    
    def send_influencer_payment_message(self, chat_id):
        """
        Sends Influencer payment request message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    

    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook

        Args:
            url:str: Provides the telegram server with a endpoint for webhook data
        """

        requests.get(url)


