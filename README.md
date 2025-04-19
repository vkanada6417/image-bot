# image-bot

# **Image Generation Bot**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)  
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)](https://core.telegram.org/bots)  

This Telegram bot generates images based on user-provided text descriptions using the **FusionBrain API**. Simply send a description of the desired image, and the bot will create and send it to you!

---

## **Features**

- **Text-to-Image Generation**: Generate images from textual descriptions.
- **Temporary File Management**: Images are stored temporarily in memory and deleted after being sent.
- **Error Handling**: The bot provides feedback if something goes wrong during image generation.
- **Typing Simulation**: Simulates typing while generating images for a better user experience.

---

## **How It Works**

1. The user sends a text description of the desired image.
2. The bot sends the request to the **FusionBrain API**.
3. The API generates the image and returns it in Base64 format.
4. The bot decodes the Base64 string into an image, saves it temporarily, and sends it to the user.
5. Temporary files are deleted after sending to save disk space.

---

## **Installation and Setup**

### **Prerequisites**
- Python 3.7 or higher
- A Telegram bot token (create one using [BotFather](https://core.telegram.org/bots#botfather))
- FusionBrain API credentials (`API_KEY` and `SECRET_KEY`)

### **Dependencies**
Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

### **Environment Variables**
Create a `.env` file in the root directory of the project and add the following variables:
```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
API_KEY=YOUR_FUSIONBRAIN_API_KEY
SECRET_KEY=YOUR_FUSIONBRAIN_SECRET_KEY
```

### **Run the Bot**
1. Ensure all dependencies are installed and environment variables are set.
2. Run the bot

## **Usage**

1. Start a chat with your bot on Telegram.
2. Use the `/start` or `/help` command to see the bot's description.
3. Send a text description of the image you want (e.g., "a spaceship flying over a mountain").
4. The bot will respond with "Generating image..." and send the generated image once it's ready.

---

## **Example**

**User Input:**
```
A futuristic city at sunset
```

**Bot Response:**
```
Generating image...
```
(After image generation completes)
![](![photo_2025-04-19_20-47-29](https://github.com/user-attachments/assets/87558543-81a7-4f6f-bc7a-48083683e47b))

---

## **API Details**

The bot uses the **FusionBrain API** to generate images. You need the following credentials:
- `API_KEY`: Your FusionBrain API key.
- `SECRET_KEY`: Your FusionBrain secret key.

For more information about the API, refer to the official documentation: [FusionBrain API](https://api-key.fusionbrain.ai/).

---

## **Author**

- **Name**: vkanada6417

---
