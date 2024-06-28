import telebot
import requests

# thay token Telegram
bot = telebot.TeleBot('7319849696:AAHtI6CGloOVzNZS3S2-P6HX0G3SZRpPh6U')

# gọi API và lấy thông tin từ file json
def get_random_vnc_info():
    response = requests.get('https://computernewb.com/vncresolver/api/scans/vnc/random')
    if response.status_code == 200:
        return response.json()
    else:
        return None

@bot.message_handler(commands=['vnc'])
def handle_start(message):
    vnc_info = get_random_vnc_info()
    if vnc_info:
        reply = (
            f"\n\n Nếu không thể kết nối, vui lòng nhập /vnc để lấy IP mới🥰🥰\n"
            f"\nTelegram: @oatdonemdume\n"
            f"\n"
            f"\nIP: {vnc_info['ip']}:{vnc_info['port']}\n"
            f"Thành phố: {vnc_info['city']}\n"
            f"Tỉnh/Bang: {vnc_info['state']}\n"
            f"Quốc gia: {vnc_info['country']}\n"
            f"Tên máy chủ: {vnc_info['clientname']}\n"
            f"Độ phân giải màn hình: {vnc_info['screenres']}\n"
            f"Tên Host: {vnc_info['hostname']}\n"
            f"Hệ điều hành: {vnc_info['osname']}\n"
            f"Các Port đang mở: {vnc_info['openports']}\n"
            f"Tên người dùng: {vnc_info['username']}\n"
            f"Mật khẩu: {vnc_info['password']}\n"
            f"Đã tạo vào: {vnc_info['createdat']}\n"
        )
    else:
        reply = "\nKhông thể lấy thông tin VNC từ API, có lẽ API đã hết hạn hoặc có một vụ tấn công nào đó đã xảy ra."

    bot.send_message(message.chat.id, reply)

# chạy bot
bot.polling()