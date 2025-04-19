import telebot
import json
from PIL import Image
from io import BytesIO
import base64
import time
import requests
import os


BOT_TOKEN = 'BOT TOKEN'
bot = telebot.TeleBot(BOT_TOKEN)


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

        raise TimeoutError("Generation timed out. Please try again.")

    def save_image_from_base64(self, base64_string):
        """
        Saves an image encoded in Base64 format into a BytesIO object.
        """
        try:
            decoded_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(decoded_data))
            return image
        except Exception as e:
            print(f"Error processing image: {e}")
            return None


fusion_brain_api = FusionBrainAPI(
    url='https://api-key.fusionbrain.ai/',
    api_key='API KEY',
    secret_key='SECRET KEY'
)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot that can generate images based on your requests. "
                          "Just send me a text description of the desired image, and I'll create it for you!")


@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_prompt = message.text
    generating_message = bot.send_message(message.chat.id, "Generating image...")
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        pipeline_id = fusion_brain_api.get_pipeline()
        uuid = fusion_brain_api.generate(user_prompt, pipeline_id)
        files = fusion_brain_api.check_generation(uuid)[0]
        image = fusion_brain_api.save_image_from_base64(files)

        if image:
            temp_file_path = "temp_image.jpg"
            image.save(temp_file_path, format="JPEG")
            with open(temp_file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo)
            bot.delete_message(message.chat.id, generating_message.message_id)
            os.remove(temp_file_path)
        else:
            bot.send_message(message.chat.id, "Sorry, I couldn't generate the image.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
