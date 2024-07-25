import time
import random
import requests
import json
from datetime import datetime, timedelta

# Fungsi untuk membaca data dari data.txt
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    accounts = [(lines[i].strip(), lines[i+1].strip()) for i in range(0, len(lines), 2)]
    return accounts

# Fungsi untuk mendapatkan User-Agent acak
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        # Tambahkan User-Agent lain jika diperlukan
    ]
    return random.choice(user_agents)

# Fungsi untuk melakukan permintaan POST
def make_post_request(url, payload, headers):
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"Status code error: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

# Fungsi untuk menampilkan hitung mundur dengan waktu yang bergerak
def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"\rWaktu tersisa: {remaining_time}", end="")
        time.sleep(1)
    print("\nWaktu habis! Melanjutkan proses...")

# Fungsi untuk mendapatkan nama akun dari teleId
def get_account_name(tele_id):
    return f"Akun {tele_id}"

# Fungsi untuk login ke akun
def login_to_account(headers):
    login_url = "https://api.taman.fun/users"
    success = make_post_request(login_url, {}, headers)
    if success:
        print(f"Berhasil login.")
    else:
        print(f"Gagal login.")
    return success

# Fungsi utama untuk memproses semua akun
def process_accounts(accounts, initial_run=True, invite_option_1="", invite_option_10=""):
    num_accounts = len(accounts)

    if initial_run:
        complete_task_x = input("Apakah ingin menyelesaikan tugas X? (y/n): ").strip().lower() == 'y'
        invite_option_1 = input("Pilih opsi undangan teman 1: (1) Tanyakan satu per satu (2) Anggap sudah semua (3) Anggap belum semua: ").strip()
        invite_option_10 = input("Pilih opsi undangan teman 10: (1) Tanyakan satu per satu (2) Anggap sudah semua (3) Anggap belum semua: ").strip()
    else:
        complete_task_x = False

    for index, (tele_id, wallet) in enumerate(accounts):
        user_agent = get_random_user_agent()
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": user_agent,
            "Wallet": wallet
        }

        account_name = get_account_name(tele_id)
        print(f"\nMemproses akun {index + 1}/{num_accounts}: TeleID={tele_id}")

        # Login ke akun
        if not login_to_account(headers):
            print(f"Melanjutkan ke akun berikutnya karena login gagal untuk {tele_id}.")
            continue

        if initial_run and complete_task_x:
            tasks = [
                {"taskId": 11, "teleId": tele_id},
                {"taskId": 6, "teleId": tele_id},
                {"taskId": 7, "teleId": tele_id},
                {"taskId": 8, "teleId": tele_id},
                {"taskId": 12, "teleId": tele_id},
                {"taskId": 2, "teleId": tele_id}
            ]
            
            for task in tasks:
                success = make_post_request("https://api.taman.fun/take-task", task, headers)
                if success:
                    print(f"Tugas {task['taskId']} selesai.")
                else:
                    print(f"Gagal menyelesaikan tugas {task['taskId']}.")
                time.sleep(3)  # Jeda 3 detik antara tugas

            quest_rewards = [1, 2, 4, 3, 13, 14]
            for quest_id in quest_rewards:
                success = make_post_request("https://api.taman.fun/return-quest", {"questId": quest_id}, headers)
                if success:
                    print(f"Berhasil mengambil hadiah quest {quest_id}.")
                else:
                    print(f"Gagal mengambil hadiah quest {quest_id}.")
                time.sleep(3)  # Jeda 3 detik antara pengambilan hadiah

        if initial_run and not complete_task_x:
            if invite_option_1 == "1":
                invite_friend_1 = input(f"Apakah akun {account_name} sudah mengundang 1 teman? (y/n): ").strip().lower() == 'y'
                if invite_friend_1:
                    success = make_post_request("https://api.taman.fun/return-quest", {"questId": 10}, headers)
                    if success:
                        print(f"Berhasil mengambil hadiah undangan teman untuk akun {account_name}.")
                    else:
                        print(f"Gagal mengambil hadiah undangan teman untuk akun {account_name}. Kemungkinan belum mengundang teman.")
            elif invite_option_1 == "2":
                success = make_post_request("https://api.taman.fun/return-quest", {"questId": 10}, headers)
                if success:
                    print(f"Berhasil mengambil hadiah undangan teman untuk akun {account_name}.")
                else:
                    print(f"Gagal mengambil hadiah undangan teman untuk akun {account_name}. Kemungkinan belum mengundang teman.")
            elif invite_option_1 == "3":
                print(f"Melewati pengambilan hadiah undangan teman untuk akun {account_name}.")

            if invite_option_10 == "1":
                invite_friend_10 = input(f"Apakah akun {account_name} sudah mengundang 10 teman? (y/n): ").strip().lower() == 'y'
                if invite_friend_10:
                    success = make_post_request("https://api.taman.fun/return-quest", {"questId": 12}, headers)
                    if success:
                        print(f"Berhasil mengambil hadiah undangan 10 teman untuk akun {account_name}.")
                    else:
                        print(f"Gagal mengambil hadiah undangan 10 teman untuk akun {account_name}. Kemungkinan belum mengundang 10 teman.")
            elif invite_option_10 == "2":
                success = make_post_request("https://api.taman.fun/return-quest", {"questId": 12}, headers)
                if success:
                    print(f"Berhasil mengambil hadiah undangan 10 teman untuk akun {account_name}.")
                else:
                    print(f"Gagal mengambil hadiah undangan 10 teman untuk akun {account_name}. Kemungkinan belum mengundang 10 teman.")
            elif invite_option_10 == "3":
                print(f"Melewati pengambilan hadiah undangan 10 teman untuk akun {account_name}.")
        
        success = make_post_request("https://api.taman.fun/mining", {}, headers)
        if success:
            print("Tugas claim 1 jam selesai.")
        else:
            print("Gagal menjalankan tugas claim 1 jam.")

        if index < num_accounts - 1:
            print("Menunggu 5 detik sebelum berpindah ke akun berikutnya...")
            time.sleep(5)

    print("Semua akun telah diproses. Menunggu 1 jam sebelum memulai ulang...")
    countdown_timer(3600)

# Membaca data dari data.txt
accounts = read_data('data.txt')

# Memulai proses akun
while True:
    process_accounts(accounts)
