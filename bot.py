import os
from decouple import config
import telebot

# Load environment variables from the .env file
BOT_TOKEN = config('BOT_TOKEN')
YOUR_CHAT_ID = config('YOUR_CHAT_ID')  # Your personal Telegram chat ID

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}  # Dictionary to store user responses

# Define a list of questions
questions = [
    "1. What is your company's name?",
    "2. What industry is your company in?",
    "3. What is your company's tagline?",
    "4. What do you want your company's image to be? (e.g., reliable, modern, friendly, luxury)",
    "5. Customer age range?",
    "6. Primary goal for this service? (Choose from options: building customer loyalty, brand awareness, etc.)"
]

# Define a function to start the conversation
@bot.message_handler(commands=['start'])
def start(message):
    user_data.clear()  # Clear previous user data
    send_question(message, questions[0])

# Define a function to send a question and store the response
def send_question(message, question):
    chat_id = message.chat.id
    bot.send_message(chat_id, question)
    bot.register_next_step_handler(message, process_response)

# Define a function to process the user's response
def process_response(message):
    chat_id = message.chat.id
    user_response = message.text
    user_data[questions[len(user_data)]] = user_response  # Store the answer with the question as the key

    # Check if all questions are asked
    if len(user_data) < len(questions):
        send_question(message, questions[len(user_data)])
    else:
        send_summary_and_thank_you(message)

# Define a function to send a summary of user responses to your personal account
def send_summary_and_thank_you(message):
    chat_id = message.chat.id
    user_info = "\n".join([f"{key}:\n{value}" for key, value in user_data.items()])
    
    # Get the user's @username if available
    user_username = message.from_user.username
    if user_username:
        summary_message = f"@{user_username}'s responses:\n{user_info}"
    else:
        summary_message = f"User's responses:\n{user_info}"
    
    # Send the summary to your personal Telegram account
    bot.send_message(YOUR_CHAT_ID, summary_message, parse_mode='Markdown')

    # Send a thank-you message to the user
    bot.send_message(chat_id, "Thank you for your time. We will contact you back.")

# Start the bot's polling process
bot.polling()
