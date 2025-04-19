import telebot
import json
from PIL import Image
from io import BytesIO
import base64
import time
import requests


BOT_TOKEN = 'YOUR BOT TOKEN'
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
        Сохраняет изображение, закодированное в формате Base64, в объект BytesIO.
        """
        try:
        
            decoded_data = base64.b64decode(base64_string)
         
            image = Image.open(BytesIO(decoded_data))
            return image
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            return None



fusion_brain_api = FusionBrainAPI(
    url='https://api-key.fusionbrain.ai/',
    api_key='18E899E695C9EF3770A16517E41AA7F0',
    secret_key='534EE409B62AA7C82E2A5B9097F8636A'
)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может генерировать изображения по вашему запросу. "
                          "Просто отправьте мне описание желаемого изображения.")



@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_prompt = message.text  # Получаем текст от пользователя
    bot.send_message(message.chat.id, "Генерирую изображение...")

    try:
       
        pipeline_id = fusion_brain_api.get_pipeline()

        uuid = fusion_brain_api.generate(user_prompt, pipeline_id)

        files = fusion_brain_api.check_generation(uuid)[0]

        image = fusion_brain_api.save_image_from_base64(files)

        if image:
            
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)

            
            bot.send_photo(message.chat.id, photo=buffer)
        else:
            bot.send_message(message.chat.id, "Извините, не удалось сгенерировать изображение.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")



if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
