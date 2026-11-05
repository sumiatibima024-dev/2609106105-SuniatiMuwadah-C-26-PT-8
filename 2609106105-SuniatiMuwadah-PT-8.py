import os
import time
from colorama import Fore, init
from prettytable import PrettyTable

init(autoreset=True)

akun = {
    "9999": {"nama": "Sumi", "saldo": 0, "peran": "admin"},
    "1234": {"nama": "Suniati", "saldo": 500000, "peran": "user"},
    "5678": {"nama": "Suni", "saldo": 750000, "peran": "user"},
}

def clear():  
    os.system("cls" if os.name == "nt" else "clear")

def jeda(detik):
    time.sleep(detik)

def judul(teks):
    clear()
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + teks.center(40))
    print(Fore.CYAN + "=" * 40)

def rupiah(angka):
    return "Rp " + f"{angka:,}".replace(",", ".")

def sukses(teks):
    print(Fore.GREEN + teks)
    jeda(2)

def gagal(teks):
    print(Fore.RED + teks)
    jeda(2)

def tabel_menu(isi):
    t = PrettyTable(["No", "Menu"])
    t.align["Menu"] = "l"
    for i, item in enumerate(isi, 1):
        t.add_row([i, item])
    print(t)

def tabel_saldo(nama, saldo):
    t = PrettyTable(["Keterangan", "Data"])
    t.align = "l"
    t.add_row(["Nama", nama])
    t.add_row(["Saldo", rupiah(saldo)])
    print(t)

def tabel_akun(data):
    t = PrettyTable(["No", "PIN", "Nama", "Saldo", "Peran"])
    t.align["Nama"] = "l"
    t.align["Saldo"] = "r"
    no = 1
    for pin, info in data.items():
        t.add_row([no, pin, info["nama"], rupiah(info["saldo"]), info["peran"]])
        no += 1
    print(t)

def buat_rekening():
    judul("BUAT REKENING")

    pin = input("PIN baru (angka): ").strip()
    if not pin.isdigit():
        gagal("PIN harus berupa angka.")
        return
    if pin in akun:
        gagal("PIN sudah dipakai.")
        return

    nama = input("Nama lengkap: ").strip()
    if nama == "":
        gagal("Nama tidak boleh kosong.")
        return

    try:
        setoran = int(input("Setoran awal: Rp "))
    except ValueError:
        gagal("Setoran harus berupa angka.")
        return
    if setoran < 0:
        gagal("Setoran tidak boleh minus.")
        return

    akun[pin] = {"nama": nama, "saldo": setoran, "peran": "user"}
    sukses("Rekening berhasil dibuat.")

def cek_saldo(pin):
    judul("INFORMASI SALDO")
    tabel_saldo(akun[pin]["nama"], akun[pin]["saldo"])
    jeda(4)

def setor(pin):
    judul("SETOR TUNAI")
    try:
        jumlah = int(input("Jumlah setoran: Rp "))
    except ValueError:
        gagal("Jumlah harus berupa angka.")
        return
    if jumlah <= 0:
        gagal("Setoran harus lebih dari nol.")
        return

    akun[pin]["saldo"] += jumlah
    sukses("Setoran berhasil. Saldo sekarang " + rupiah(akun[pin]["saldo"]))

def tarik(pin):
    judul("TARIK TUNAI")
    try:
        jumlah = int(input("Jumlah penarikan: Rp "))
    except ValueError:
        gagal("Jumlah harus berupa angka.")
        return
    if jumlah <= 0:
        gagal("Penarikan harus lebih dari nol.")
        return
    if jumlah > akun[pin]["saldo"]:
        gagal("Saldo tidak cukup.")
        return

    akun[pin]["saldo"] -= jumlah
    sukses("Penarikan berhasil. Sisa saldo " + rupiah(akun[pin]["saldo"]))

def menu_user(pin):
    while True:
        judul("HALO, " + akun[pin]["nama"].upper())
        tabel_menu(["Cek saldo", "Setor tunai", "Tarik tunai", "Logout"])
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            cek_saldo(pin)
        elif pilih == "2":
            setor(pin)
        elif pilih == "3":
            tarik(pin)
        elif pilih == "4":
            break
        else:
            gagal("Pilihan tidak ada.")

def lihat_akun():
    judul("DAFTAR AKUN")
    tabel_akun(akun)
    jeda(5)

def hapus_akun():
    judul("HAPUS AKUN")
    pin = input("PIN akun yang dihapus: ").strip()

    if pin not in akun:
        gagal("Akun tidak ditemukan.")
        return
    if akun[pin]["peran"] == "admin":
        gagal("Akun admin tidak bisa dihapus.")
        return

    yakin = input("Yakin hapus akun ini? (y/t): ").lower()
    if yakin == "y":
        del akun[pin]
        sukses("Akun berhasil dihapus.")
    else:
        gagal("Dibatalkan.")

def menu_admin(nama):
    while True:
        judul("ADMIN - " + nama.upper())
        tabel_menu(["Lihat semua akun", "Hapus akun", "Logout"])
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            lihat_akun()
        elif pilih == "2":
            hapus_akun()
        elif pilih == "3":
            break
        else:
            gagal("Pilihan tidak ada.")

def login():
    judul("LOGIN")
    pin = input("Masukkan PIN: ").strip()

    if pin not in akun:
        gagal("PIN salah atau akun tidak ditemukan.")
        return

    nama = akun[pin]["nama"]
    sukses("Login berhasil, selamat datang " + nama)

    if akun[pin]["peran"] == "admin":
        menu_admin(nama)
    else:
        menu_user(pin)

def main():
    while True:
        judul("APLIKASI ATM")
        tabel_menu(["Login", "Buat rekening baru", "Keluar"])
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            login()
        elif pilih == "2":
            buat_rekening()
        elif pilih == "3":
            print("Terima kasih.")
            break
        else:
            gagal("Pilihan tidak ada.")

if __name__ == "__main__":
    main()
