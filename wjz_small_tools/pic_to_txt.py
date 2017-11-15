from PIL import Image
import os
import platform
from werkzeug.utils import secure_filename

ascii_char = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

if 'Linux' in platform.system():
	base_path = '/home/wjzDemo_config/pictotxt/'
else:
	base_path = 'C:\\Wangjz\\wjzDemo_config\\pictotxt\\'

if not os.path.exists(base_path):
	os.makedirs(base_path)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def get_char(r, g, b, alpha=256):
	if alpha == 0:
		return ''
	length = len(ascii_char)
	if r > 235 and g > 235 and b > 235:
		r, g, b = 255, 255, 255
	gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
	return ascii_char[int(gray / 257 * length)]


def picToTxt(f, size):
	filename = secure_filename(f.filename)
	pic_path = os.path.join(base_path, filename)
	if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
		return False
	f.save(pic_path)
	im = Image.open(pic_path)
	old_x, old_y = im.size
	new_x = 2 * size * old_x // old_y
	im = im.resize((new_x, size))
	txt = ""
	for y in range(size):
		for x in range(new_x):
			rgb = im.getpixel((x, y))
			txt += get_char(*rgb)
		txt += '\n'
	txt_path = os.path.splitext(pic_path)[0] + r'.txt'
	with open(txt_path, 'wt') as f:
		f.write(txt)
	return os.path.basename(txt_path)
