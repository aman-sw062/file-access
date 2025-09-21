import base64
import os
import tempfile
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8211056311:AAGN_CYAabMxvXxP36yKg8vWafgXaAQDx4k'
bot = telebot.TeleBot(API_TOKEN)

def anonymous_enc(file_content):
    encoded_content = base64.b64encode(file_content).decode('utf-8')
    
    obfuscated_script = f'''import os,base64,tempfile,sys
anonymous="{encoded_content}"
data=base64.b64decode(anonymous)
tf=tempfile.NamedTemporaryFile(delete=False,suffix=".zip")
try:
 tf.write(data);tf.close()
 os.system(sys.executable+" "+tf.name)
finally:
 try:os.remove(tf.name)
 except:pass
'''
    return obfuscated_script

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🐍 Welcome to Python Script Obfuscator Bot!\n\n"
                 "Send me a Python (.py) file and I'll return the obfuscated version saved as anonymous.py.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ Please send a Python file with .py extension.")
        return
    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    bot.send_message(message.chat.id, f"📥 Received: {message.document.file_name}\n"
                    f"📊 Size: {len(downloaded_file)} bytes\n\n"
                    "Obfuscating your file...")
    
    try:
        obfuscated_content = anonymous_enc(downloaded_file)
        obfuscated_name = "anonymous.py"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(obfuscated_content)
            temp_file.flush()
            
            with open(temp_file.name, 'rb') as file_to_send:
                bot.send_document(
                    message.chat.id,
                    file_to_send,
                    visible_file_name=obfuscated_name, 
                    caption=f"📊 Original size: {len(downloaded_file)} bytes\n"
                           f"📊 Obfuscated size: {len(obfuscated_content)} bytes\n\n"
                           f"✅ File saved as: {obfuscated_name}"
                )
        
        os.unlink(temp_file.name)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error during obfuscation: {str(e)}")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if message.content_type != 'document':
        bot.reply_to(message, "Please send a Python (.py) file to obfuscate.")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    print("Bot username: @" + bot.get_me().username)
    bot.infinity_polling()