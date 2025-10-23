import yaml
from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

with open("./client/configs/config.yaml", "r") as f:
    client_config = yaml.safe_load(f)

HTTP_API: Final = client_config["telegram"]["HTTP_API"]
BOTNAME: Final = client_config["telegram"]["botname"]

start_command_str = "Xin chào! Đây là dịch vụ chăm sóc khách hàng của công ty NATMIN.\nQuý khách có thể đặt bất kỳ cầu hỏi nào quý khách muốn.\nRất vui được giải đáp các thắc mắc của quý khách!"
develop_information_str = "Dịch vụ đang trong giai đoạn thử nghiệm và phát triển.\nBản quyền thuộc về Nguyễn Nhật Minh.\nMail address: minh.nn0402@gmail.com"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_command_str)

async def dev_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(develop_information_str)

def process_text(input: str) -> str:
    return f"Nguyễn Nhật Minh đang test với input {input}"

async def handler_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    input: str = update.message.text.lower()

    print(f"User ({update.message.chat.id}) in {message_type}: {input}")

    if message_type == 'group':
        if BOTNAME in input:
            removed_botname_input = input.replace(BOTNAME,"")
            output = process_text(input=removed_botname_input)
        else:
            return
    else:
        output = process_text(input=input)
    
    ##joke
    if "đức" in input:
        output = "Đỗ Thành Đức là người yêu của Nguyễn Văn Thọ"
    ##end_joke

    print(f"Bot: {output}")

    await update.message.reply_text(output)

async def handler_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}! ")


if __name__ == "__main__":
    print("Starting Bot...")
    app = Application.builder().token(HTTP_API).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('dev_info', dev_info_command))
    app.add_handler(MessageHandler(filters.TEXT, handler_message))
    app.add_error_handler(handler_error)

    print("Polling...")
    app.run_polling(poll_interval=3)


    