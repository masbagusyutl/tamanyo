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
        return response.status_code == 200
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

# Fungsi utama untuk memproses semua akun
def process_accounts(accounts, initial_run=True):
    num_accounts = len(accounts)

    if initial_run:
        # Menanyakan apakah ingin menyelesaikan tugas X
        complete_task_x = input("Apakah ingin menyelesaikan tugas X? (y/n): ").strip().lower() == 'y'
        invite_friend = False
    else:
        complete_task_x = False
        invite_friend = False

    # Memproses setiap akun
    for index, (tele_id, wallet) in enumerate(accounts):
        user_agent = get_random_user_agent()
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
            "Cache-Control": "no-cache",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "Origin": "https://taman.fun",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://taman.fun/",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": user_agent,
            "Wallet": wallet
        }

        account_name = get_account_name(tele_id)
        print(f"\nMemproses akun {index + 1}/{num_accounts}: Nama={account_name}, TeleID={tele_id}, Wallet={wallet}")
        
        # Menyelesaikan tugas X jika diminta (hanya pada awal eksekusi)
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

            # Mengambil hadiah tugas X
            quest_rewards = [1, 2, 4, 3, 13, 14]
            for quest_id in quest_rewards:
                success = make_post_request("https://api.taman.fun/return-quest", {"questId": quest_id}, headers)
                if success:
                    print(f"Berhasil mengambil hadiah quest {quest_id}.")
                else:
                    print(f"Gagal mengambil hadiah quest {quest_id}.")
                time.sleep(3)  # Jeda 3 detik antara pengambilan hadiah

        # Menanyakan apakah sudah mengundang teman (hanya pada awal eksekusi)
        if initial_run and not complete_task_x:
            invite_friend = input("Apakah sudah mengundang 1 teman? (y/n): ").strip().lower() == 'y'
            if invite_friend:
                success = make_post_request("https://api.taman.fun/return-quest", {"questId": 10}, headers)
                if success:
                    print("Berhasil mengambil hadiah undangan teman.")
                else:
                    print("Gagal mengambil hadiah undangan teman. Kemungkinan belum mengundang teman.")
        
        # Menjalankan tugas claim 1 jam sekali
        success = make_post_request("https://api.taman.fun/mining", {}, headers)
        if success:
            print("Tugas claim 1 jam selesai.")
        else:
            print("Gagal menjalankan tugas claim 1 jam.")

        # Jeda 5 detik sebelum berpindah ke akun berikutnya
        if index < num_accounts - 1:
            print("Menunggu 5 detik sebelum berpindah ke akun berikutnya...")
            time.sleep(5)

    # Hitung mundur 1 jam setelah semua akun diproses
    print("Semua akun telah diproses. Menunggu 1 jam sebelum memulai ulang...")
    countdown_timer(3600)

    # Memulai ulang kode
    process_accounts(accounts, initial_run=False)

# Membaca data dari data.txt
accounts = read_data('data.txt')

# Memulai proses akun
process_accounts(accounts)
