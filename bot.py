import telebot
import requests
import socket

bot = telebot.TeleBot('7319849696:AAHtI6CGloOVzNZS3S2-P6HX0G3SZRpPh6U')

def get_random_vnc_info():
    response = requests.get('https://computernewb.com/vncresolver/api/scans/vnc/random')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def send_message_with_retry(chat_id, text):
    while True:
        try:
            bot.send_message(chat_id, text)
            break
        except Exception as e:
            print(f"Error sending message: {e}. Retrying...")

@bot.message_handler(commands=['vnc'])
def handle_vnc(message):
    vnc_info = None
    while True:
        vnc_info = get_random_vnc_info()
        if vnc_info and is_port_open(vnc_info['ip'], vnc_info['port']):
            break

    if vnc_info:
        reply = (
            f"\n\nNếu không thể kết nối, vui lòng nhập /vnc để lấy IP mới🥰🥰\n"
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
        )
    else:
        reply = "\nKhông thể lấy thông tin VNC từ API, có lẽ API đã hết hạn hoặc có một vụ tấn công nào đó đã xảy ra."

    send_message_with_retry(message.chat.id, reply)

bot.polling()