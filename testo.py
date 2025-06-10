import csv
import datetime
import os
from datetime import date
from typing import List, Tuple


######################################################### C O V E R #############################################################
def clear():
    os.system("cls")
    
def garis(a, b=107):
    print(a * b)

def cover(b=107):
    garis("=", b)
    print("██╗  ██╗███╗   ██╗ █████╗  ██████╗██╗  ██╗██████╗ ██╗      █████╗ ███╗   ██╗".center(b))
    print("██║ ██╔╝████╗  ██║██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██║     ██╔══██╗████╗  ██║".center(b))
    print("█████╔╝ ██╔██╗ ██║███████║██║     █████╔╝ ██████╔╝██║     ███████║██╔██╗ ██║".center(b))
    print("██╔═██╗ ██║╚██╗██║██╔══██║██║     ██╔═██╗ ██╔═══╝ ██║     ██╔══██║██║╚██╗██║".center(b))
    print("██║  ██╗██║ ╚████║██║  ██║╚██████╗██║  ██╗██║     ███████╗██║  ██║██║ ╚████║".center(b))
    print("╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝".center(b))
    garis("=", b)

def enter(a=""):
    input(f"{a}[ENTER] untuk melanjutkan >> ")

def halaman_knackplan():
    print("""
                                                1. REGISTRASI
                                                2. LOGIN SEBAGAI DOSEN
                                                3. LOGIN SEBAGAI MAHASISWA
                                                4. EXIT
""")
    garis("=")
    while True :
        try:
            pilih = int(input("silahkan pilih opsi anda:) >> "))
            if pilih == 1:
                registrasi()
            elif pilih == 2:
                login_dosen()
            elif pilih == 3:
                login_mahasiswa()
            elif pilih == 4:
                exit_program()
            else:
                print("Opsss, opsi yang Anda pilih tidak tersedia:( ")
        except ValueError:
            print("Silahkan pilih opsi anda kembali dalam bentuk angka ^_^")
            continue

def registrasi():
    clear()
    while True:
        username_mahasiswa = input("Username : ")
        while len(username_mahasiswa) == 0:
            clear() 
            print("Username tidak boleh kosong. Silahkan coba lagi")    
            username_mahasiswa = input("Username : ")

        password_mahasiswa = input("Password : ")
        while len(password_mahasiswa) == 0:
            clear() 
            print(f"Username  : {username_mahasiswa}")
            print("Password tidak boleh kosong. Silahkan coba lagi")
            password_mahasiswa = input("Password : ")
           
        while True:
            nim = input("NIM (12 digit) : ")
            if len(nim) == 12 and nim.isdigit():
                break
            else:
                clear()
                print(f"Username : {username_mahasiswa}")
                print(f"Password : {password_mahasiswa}")
                print("NIM harus berupa 12 digit angka. Silahkan coba lagi")

        while True:
            nomor_telepon = input("Nomor Telepon: ")
            if len(nomor_telepon) == 12 and nomor_telepon.isdigit():
                break
            else:
                clear()
                print(f"Username : {username_mahasiswa}")
                print(f"Password : {password_mahasiswa}")
                print(f"Nomor NIM : {nim}")
                print("Nomor Telepon harus berupa 12 digit angka. Silahkan coba lagi")
                
        if cek_duplikasi(username_mahasiswa, nim, nomor_telepon):
            clear()
            print("\nPendaftaran gagal. Username, NIM, atau Nomor Telepon sudah terdaftar :(\n")
        else:
            simpan_data([username_mahasiswa, password_mahasiswa, nim, nomor_telepon])
            clear()
            print("\nPendaftaran berhasil. Silahkan login :D\n")

            while True:
                print("""
                                                1. LOGIN SEBAGAI MAHASISWA
                                                2. EXIT
                """)
                garis("=")
                try:
                    pilih = int(input("Pilih Opsi yang tersedia >> "))
                    if pilih == 1:
                        # clear()
                        login_mahasiswa()
                    elif pilih == 2:
                        exit_program()
                    else:
                        print("Opss, Opsi yang Anda pilih tidak tersedia, silahkan coba lagi")
                except ValueError:
                    print("Maaf anda salah input, tolong masukkan input dalam bentuk angka")
                    continue
            
def login_dosen():
    clear()
    while True:
        username_dosen = input("Username : ")
        while len(username_dosen) == 0:  
            print("Opss, Username tidak boleh kosong, Silahkan coba lagi")
            username_dosen = input("Username : ")
            
        password_dosen = input("Password : ")
        while len(password_dosen) == 0:  
            print("Opss, Password tidak boleh kosong, Silahkan coba lagi")
            password_dosen = input("Password : ")
            
        if cek_logindosen(username_dosen, password_dosen):
            print("\nLogin berhasil sebagai Admin :D")
            menu_dosen()
        else:
            print("Login gagal, Username atau password salah, Silahkan coba lagi")
            continue

def cek_logindosen(username_dosen, password_dosen):
    file_dosen = "datadosen.csv" 
    try:
        with open(file_dosen, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username_dosen and row[1] == password_dosen:
                    return True
        return False
    except FileNotFoundError:
        print(f"File {file_dosen} tidak ditemukan.")
        return False
    
def login_mahasiswa():
    clear()
    while True:
        username_mahasiswa = input("Username : ")
        password_mahasiswa = input("Password : ")
        if cek_loginmahasiswa(username_mahasiswa, password_mahasiswa):
            print("Login berhasil sebagai Mahasiswa :D")
            while True:
                clear()
                menu_mahasiswa(username_mahasiswa)
                break  
            break 
        else:
            clear()
            print("Login gagal, Username atau password salah, Silahkan coba lagi")
            continue  

def cek_loginmahasiswa(username_mahasiswa, password_mahasiswa):
    file_mahasiswa = "datamahasiswa.csv"  
    try:
        with open(file_mahasiswa, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username_mahasiswa and row[1] == password_mahasiswa:
                    return True
        return False
    except FileNotFoundError:
        print(f"File {file_mahasiswa} tidak ditemukan.")
        return False

def cek_duplikasi(username_mahasiswa, nim, nomor_telepon):
    file_mahasiswa = "datamahasiswa.csv"  
    data = baca_data(file_mahasiswa)  
    for row in data:
        if row[0] == username_mahasiswa or row[2] == nim or row[3] == nomor_telepon:
            return True  
    return False

def simpan_data(data):
    file_mahasiswa = "datamahasiswa.csv"  
    with open(file_mahasiswa, mode='a', newline='') as file: 
        writer = csv.writer(file) 
        writer.writerow(data)

def exit_program():
    clear()
    print("\n")
    print("Terima kasih telah menggunakan KNACKPLAN(●'◡'●)\n\n".center(114))
    garis("=", 114)
    exit()

######################################################### M E N U ######################################################################

FILE_KULIAH = 'mata_kuliah.csv' 
FILE_TUGAS = 'tugas.csv' 
FILE_MAHASISWA = 'data_mahasiswa.csv' 
HARI_DALAM_MINGGU = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'] 

def baca_data(FILE_MAHASISWA):
    try:
        with open(FILE_MAHASISWA, mode='r') as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                if len(row) > 0:
                    data.append(row)
            return data
    except FileNotFoundError:
        print(f"File '{FILE_MAHASISWA}' tidak ditemukan. Membuat file baru...")
        return []


def muat_kuliah():
    kuliah = []

    if os.path.exists(FILE_KULIAH):
        with open(FILE_KULIAH, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Lewati baris header

            for row in csv_reader:
                kuliah.append({
                    'IDMataKuliah': int(row[0]),
                    'NamaMataKuliah': row[1],
                    'Hari': row[2],
                    'WaktuMulai': row[3],
                    'WaktuSelesai': row[4]
                })

    return kuliah

kuliah = muat_kuliah()

def simpan_kuliah(kuliah: List[dict]):
    with open(FILE_KULIAH, 'w', newline='', encoding='utf-8') as file:
        kolom = ['IDMataKuliah', 'NamaMataKuliah', 'Hari', 'WaktuMulai', 'WaktuSelesai']
        csv_writer = csv.writer(file)
        csv_writer.writerow(kolom)  # Header

        for k in kuliah:
            csv_writer.writerow([
                k['IDMataKuliah'],
                k['NamaMataKuliah'],
                k['Hari'],
                k['WaktuMulai'],
                k['WaktuSelesai']
            ])

def muat_tugas():
    tugas = []

    if os.path.exists(FILE_TUGAS):
        with open(FILE_TUGAS, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Lewati header
            for row in csv_reader:
                tugas.append({
                    'IDTugas': int(row[0]),
                    'NamaTugas': row[1],
                    'DurasiEstimasi': float(row[2]),
                    'Tenggat': row[3],
                    'Status': row[4]
                })

    return tugas


tugas = muat_tugas()

def simpan_tugas(tugas: List[dict]):
    with open(FILE_TUGAS, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['IDTugas', 'NamaTugas', 'DurasiEstimasi', 'Tenggat', 'Status'])  # Header
        for t in tugas:
            csv_writer.writerow([
                t['IDTugas'],
                t['NamaTugas'],
                t['DurasiEstimasi'],
                t['Tenggat'],
                t['Status']
            ])


def bersihkan_tugas_selesai():
    tugas = muat_tugas()
    tugas_baru = []
    for t in tugas:
        if t['Status'].lower() != 'selesai':
            tugas_baru.append(t)
    simpan_tugas(tugas_baru) 

def str_ke_waktu(t_str: str):
    return datetime.datetime.strptime(t_str, '%H:%M').time()
    
def waktu_ke_str(t: datetime.time):
    return t.strftime('%H:%M')

def hari_ini():
    hari = datetime.datetime.today().strftime('%A')  
    terjemahan_hari = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }
    return terjemahan_hari.get(hari, hari)  

def cetak_garis():
    print('-'*50)  

def input_waktu(prompt: str):
    while True:  
        t = input(prompt + " (HH:MM, format 24h): ")  
        try:
            datetime.datetime.strptime(t, '%H:%M')  
            return t 
        except ValueError:
            print("Format waktu tidak valid. Silakan masukkan dalam format HH:MM 24-jam.")  

def input_hari():
    while True: 
        hari = input("Masukkan hari dalam seminggu (mis. Senin): ").capitalize()  
        if hari in HARI_DALAM_MINGGU: 
            return hari  
        print("Hari tidak valid. Silakan masukkan nama hari yang valid, mis. Senin.") 

def id_kuliah_selanjutnya(kuliah):
    if kuliah:  
        return max(k['IDMataKuliah'] for k in kuliah) + 1  
    return 1  

def id_tugas_selanjutnya(tugas):
    if tugas:  
        return max(t['IDTugas'] for t in tugas) + 1  
    return 1  

def tumpang_tindih(start1, end1, start2, end2):
    return not (end1 <= start2 or end2 <= start1)  

def cetak_kuliah_hari_ini(kuliah, hari):
    print(f"Jadwal Kuliah untuk {hari}:")  
    terfilter = [k for k in kuliah if k['Hari'] == hari]  
    if not terfilter:  
        print("  Tidak ada kuliah yang dijadwalkan hari ini.")  
        return [] 
    terfilter.sort(key=lambda x: str_ke_waktu(x['WaktuMulai']))  
    for k in terfilter:  
        print(f"  [{k['IDMataKuliah']}] {k['NamaMataKuliah']} dari {k['WaktuMulai']} sampai {k['WaktuSelesai']}")  
    return terfilter 

######################################################## M E N U  D O S E N #################################################################
def menu_dosen():
    while True:
        clear()
        garis("=")
        print("""                               
                                                    MENU DOSEN 

                                                1. Lihat Kuliah untuk hari tertentu
                                                2. Tambah Kuliah
                                                3. Edit Kuliah
                                                4. Hapus Kuliah
                                                5. Kembali ke Halaman KnackPlan
        """)
        garis("=")
        
        try:
            pilih = int(input("Pilih Opsi yang tersedia >> "))
            if pilih == 1:
                clear()
                lihat_kuliah()
                continue
            elif pilih == 2:
                clear()
                tambah_kuliah()
            elif pilih == 3:
                clear()
                edit_kuliah()
            elif pilih == 4:
                clear()
                hapus_kuliah()
            elif pilih == 5:
                halaman_knackplan()
                break
            else:
                print("Opss, Opsi yang Anda pilih tidak tersedia, silahkan  coba lagi")
        except ValueError:
            print("tolong masukkan input dalam bentuk angka.")


def lihat_kuliah():
    global kuliah
    while True:
        hari = input_hari()
        cetak_kuliah_hari_ini(kuliah, hari)
        input()
        break

def tambah_kuliah():
    
    global kuliah

    nama_kuliah = input("Masukkan nama kuliah: ").strip()
    hari = input_hari()
    waktu_mulai = input_waktu("Masukkan waktu mulai")
    waktu_selesai = input_waktu("Masukkan waktu selesai")

    if str_ke_waktu(waktu_selesai) <= str_ke_waktu(waktu_mulai):
        print("Waktu selesai harus setelah waktu mulai. Kuliah tidak ditambahkan.")
        input("Tekan Enter untuk kembali ke menu...")
        return 

    tumpang_tindih_ditemukan = False
    for k in kuliah:
        if k['Hari'] == hari:
            if tumpang_tindih(
                str_ke_waktu(waktu_mulai), str_ke_waktu(waktu_selesai),
                str_ke_waktu(k['WaktuMulai']), str_ke_waktu(k['WaktuSelesai'])
            ):
                print(f"Tumpang tindih dengan kuliah [{k['IDMataKuliah']}] {k['NamaMataKuliah']} {k['WaktuMulai']}–{k['WaktuSelesai']}")
                input("Tekan Enter untuk kembali ke menu...")
                tumpang_tindih_ditemukan = True
                break

    if tumpang_tindih_ditemukan:
        print("Tidak dapat menambahkan kuliah yang tumpang tindih.")
        input("Tekan Enter untuk kembali ke menu...")
        return  

    id_baru = id_kuliah_selanjutnya(kuliah)
    kuliah_baru = {
        'IDMataKuliah': id_baru,
        'NamaMataKuliah': nama_kuliah,
        'Hari': hari,
        'WaktuMulai': waktu_mulai,
        'WaktuSelesai': waktu_selesai
    }
    kuliah.append(kuliah_baru)
    simpan_kuliah(kuliah)
    print(f"Kuliah ditambahkan dengan ID {id_baru}.")
    input("Tekan Enter untuk melanjutkan...")


def edit_kuliah():
    global kuliah
    while True:
        try:
            id_kuliah = int(input("Masukkan ID kuliah untuk diedit: "))
        except ValueError:
            print("ID tidak valid.")
            continue

        kuliah_yang_ditemukan = [k for k in kuliah if k['IDMataKuliah'] == id_kuliah]
        if not kuliah_yang_ditemukan:
            print("Kuliah tidak ditemukan.")
            continue

        kul = kuliah_yang_ditemukan[0]
        print(f"Mengedit Kuliah [{kul['IDMataKuliah']}] {kul['NamaMataKuliah']} {kul['Hari']} {kul['WaktuMulai']}-{kul['WaktuSelesai']}")

        nama_baru = input(f"Nama kuliah baru (biarkan kosong untuk mempertahankan '{kul['NamaMataKuliah']}'): ").strip()
        if nama_baru:
            kul['NamaMataKuliah'] = nama_baru

        hari_baru = input(f"Hari baru (biarkan kosong untuk mempertahankan '{kul['Hari']}'): ").capitalize().strip()
        if hari_baru:
            if hari_baru not in HARI_DALAM_MINGGU:
                print("Hari yang dimasukkan tidak valid. Edit dibatalkan.")
                continue
            kul['Hari'] = hari_baru

        waktu_mulai_baru = input(f"Waktu mulai baru (biarkan kosong untuk mempertahankan '{kul['WaktuMulai']}'): ").strip()
        if waktu_mulai_baru:
            try:
                datetime.datetime.strptime(waktu_mulai_baru, '%H:%M')
                kul['WaktuMulai'] = waktu_mulai_baru
            except:
                print("Format waktu tidak valid. Edit dibatalkan.")
                continue

        waktu_selesai_baru = input(f"Waktu selesai baru (biarkan kosong untuk mempertahankan '{kul['WaktuSelesai']}'): ").strip()
        if waktu_selesai_baru:
            try:
                datetime.datetime.strptime(waktu_selesai_baru, '%H:%M')
                kul['WaktuSelesai'] = waktu_selesai_baru
            except:
                print("Format waktu tidak valid. Edit dibatalkan.")
                continue

        if str_ke_waktu(kul['WaktuSelesai']) <= str_ke_waktu(kul['WaktuMulai']):
            print("Waktu selesai harus setelah waktu mulai. Edit dibatalkan.")
            continue

        # Cek tumpang tindih dengan kuliah lain
        tumpang_tindih_ditemukan = False
        for k in kuliah:
            if k['IDMataKuliah'] != kul['IDMataKuliah'] and k['Hari'] == kul['Hari']:
                if tumpang_tindih(str_ke_waktu(kul['WaktuMulai']), str_ke_waktu(kul['WaktuSelesai']),
                                str_ke_waktu(k['WaktuMulai']), str_ke_waktu(k['WaktuSelesai'])):
                    print(f"Tumpang tindih dengan kuliah yang ada [{k['IDMataKuliah']}] {k['NamaMataKuliah']} {k['WaktuMulai']}–{k['WaktuSelesai']}")
                    tumpang_tindih_ditemukan = True

        if tumpang_tindih_ditemukan:
            print("Edit menghasilkan kuliah yang tumpang tindih. Edit dibatalkan.")
            continue

        # Simpan perubahan ke file dan keluar loop
        simpan_kuliah(kuliah)
        print("Kuliah berhasil diedit.")
        input("Tekan Enter untuk melanjutkan...")
        break

def reset_id_kuliah():
    global kuliah
    for i, k in enumerate(kuliah, start=1):
        k['IDMataKuliah'] = i
    simpan_kuliah(kuliah)
            
def hapus_kuliah():
    global kuliah
    while True:
        try:
            id_kuliah = int(input("Masukkan ID kuliah untuk dihapus: "))
        except ValueError:
            print("ID tidak valid.")
            continue

        sebelum_len = len(kuliah)
        kuliah = [k for k in kuliah if k['IDMataKuliah'] != id_kuliah]

        if len(kuliah) == sebelum_len:
            print("ID kuliah tidak ditemukan.")
        else:
            reset_id_kuliah()
            print(f"Kuliah ID {id_kuliah} berhasil dihapus.")
            input("Tekan Enter untuk melanjutkan...")  # Jeda disini sebelum keluar loop
            break  # keluar dari loop setelah berhasil hapus dan jeda


################################################### M E N U M A H A S I S W A #########################################################
def menu_mahasiswa(username_mahasiswa):
    global tugas, kuliah

    bersihkan_tugas_selesai()
    kuliah = muat_kuliah()
    tugas = muat_tugas()

    tanggal_hari_ini = datetime.date.today()
    for t in tugas:
        if t['Status'].lower() == 'pending':
            try:
                deadline = datetime.datetime.strptime(t['Tenggat'], '%Y-%m-%d').date()
                if deadline < tanggal_hari_ini:
                    t['Status'] = 'Sudah Lewat Tenggat'
            except:
                continue
    simpan_tugas(tugas)

    hari = hari_ini()
    kuliah_hari_ini = [k for k in kuliah if k['Hari'] == hari]
    kuliah_hari_ini.sort(key=lambda x: str_ke_waktu(x['WaktuMulai']))

    cetak_garis()
    print(f"MENU MAHASISWA - Manajemen Tugas (Hari ini adalah {hari})")
    print("Jadwal Kuliah Hari Ini:")
    if not kuliah_hari_ini:
        print("  Tidak ada kuliah hari ini.")
    else:
        for k in kuliah_hari_ini:
            print(f"  {k['NamaMataKuliah']} dari {k['WaktuMulai']} sampai {k['WaktuSelesai']}")
    input("LANJUT?")

    while True:
        clear()
        garis("=")
        print("""                               
                                                    MENU MAHASISWA

                                                1. Lihat semua tugas
                                                2. Tambah tugas
                                                3. Edit tugas
                                                4. Hapus tugas
                                                5. Tandai tugas sebagai selesai
                                                6. Jadwalkan tugas otomatis
                                                7. Kembali ke halaman KnackPlan
        """)
        garis("=")
        
        try:
            pilih = int(input("Pilih Opsi yang tersedia >> "))
            if pilih == 1:
                clear()
                lihat_semua_tugas()
                continue
            elif pilih == 2:
                clear()
                tambah_tugas()
            elif pilih == 3:
                clear()
                edit_tugas()
            elif pilih == 4:
                clear()
                hapus_tugas()
            elif pilih == 5:
                clear()
                tandai_tugas_sebagai_selesai()
            elif pilih == 6:
                clear()
                jadwalkan_tugas_otomatis(kuliah_hari_ini)
            elif pilih == 7:
                clear()
                halaman_knackplan()
                break
            else:
                print("Opss, Opsi yang Anda pilih tidak tersedia, silahkan  coba lagi")
        except ValueError:
            print("tolong masukkan input dalam bentuk angka.")

def lihat_semua_tugas():
    global tugas 
    while True:
        try: 
            if not tugas:
                print("Tidak ada tugas yang terdaftar saat ini.")
            else:
                print("Tugas Terdaftar:")
                for t in tugas:
                    print(f"  [{t['IDTugas']}] {t['NamaTugas']} Durasi:{t['DurasiEstimasi']}h Tenggat:{t['Tenggat']} Status:{t['Status']}")
        except NameError:
            print("Variabel 'tugas' belum didefinisikan.")
            break
        except KeyError as e:
            print(f"Key {e} tidak ditemukan dalam salah satu tugas.")
            break
        except TypeError:
            print("Tipe data 'tugas' tidak sesuai. Pastikan tugas adalah list of dictionary.")
            break
        except Exception as e:
            print(f"Terjadi error tidak terduga: {e}")
            break

        input("Tekan Enter untuk melanjutkan...")
        break


def tambah_tugas():
    global tugas
    nama_tugas = input("Nama tugas: ").strip()

    while True:
        try:
            durasi_estimasi = float(input("Durasi estimasi dalam jam (mis., 1.5): "))
            if durasi_estimasi <= 0:
                print("Harus angka positif.")
                continue
            break
        except:
            print("Input tidak valid, masukkan angka.")

    while True:
        tenggat = input("Tenggat (YYYY-MM-DD, biarkan kosong jika tidak ada): ").strip()
        if tenggat:
            try:
                datetime.datetime.strptime(tenggat, '%Y-%m-%d')
                break
            except:
                print("Format tanggal tidak valid. Tugas tidak ditambahkan.")
                continue
        else:
            tenggat = ''
            break
    
    id_tugas_baru = id_tugas_selanjutnya(tugas)
    tugas.append({
        'IDTugas': id_tugas_baru,
        'NamaTugas': nama_tugas,
        'DurasiEstimasi': durasi_estimasi,
        'Tenggat': tenggat,
        'Status': 'Pending'
    })

    simpan_tugas(tugas)
    print(f"Tugas '{nama_tugas}' ditambahkan dengan ID {id_tugas_baru}.")
    input("Tekan Enter untuk melanjutkan...")


def edit_tugas():
    tugas = muat_tugas()
    while True:
        try:
            id_tugas = int(input("Masukkan ID tugas untuk diedit: "))
        except:
            print("ID tidak valid.")
            continue
        cocok = [t for t in tugas if t['IDTugas'] == id_tugas]
        if not cocok:
            print("Tugas tidak ditemukan.")
            continue
        t = cocok[0]
        print(f"Mengedit Tugas [{t['IDTugas']}] {t['NamaTugas']} Durasi:{t['DurasiEstimasi']}h Tenggat:{t['Tenggat']} Status:{t['Status']}")
        nama_baru = input(f"Nama baru (biarkan kosong untuk mempertahankan '{t['NamaTugas']}'): ").strip()
        if nama_baru:
            t['NamaTugas'] = nama_baru
        durasi_baru = input(f"Durasi estimasi baru (biarkan kosong untuk mempertahankan {t['DurasiEstimasi']}): ").strip()
        if durasi_baru:
            try:
                d = float(durasi_baru)
                if d <= 0:
                    print("Durasi harus positif. Edit dibatalkan.")
                    continue
                t['DurasiEstimasi'] = d
            except:
                print("Durasi tidak valid. Edit dibatalkan.")
                continue
        tenggat_baru = input(f"Tenggat baru (YYYY-MM-DD, kosong untuk mempertahankan '{t['Tenggat']}'): ").strip()
        if tenggat_baru:
            try:
                datetime.datetime.strptime(tenggat_baru, '%Y-%m-%d')
                t['Tenggat'] = tenggat_baru
            except:
                print("Format tanggal tidak valid. Edit dibatalkan.")
                continue
        status_baru = input(f"Status (Pending/Selesai), kosong untuk mempertahankan '{t['Status']}': ").strip().capitalize()
        if status_baru:
            if status_baru not in ['Pending', 'Selesai']:
                print("Status tidak valid. Edit dibatalkan.")
                continue
            t['Status'] = status_baru
        simpan_tugas(tugas)
        print("Tugas berhasil diedit.")
        bersihkan_tugas_selesai()  # Hapus yang selesai segera
        input("Tekan Enter untuk melanjutkan...")
        break

def hapus_tugas():
    tugas = muat_tugas()  
    while True:
        try:
            id_tugas = int(input("Masukkan ID tugas untuk dihapus: "))
        except:
            print("ID tidak valid.")
            continue
        sebelum_len = len(tugas)
        tugas = [t for t in tugas if t['IDTugas'] != id_tugas]
        if len(tugas) == sebelum_len:
            print("ID tugas tidak ditemukan.")
        else:
            simpan_tugas(tugas)
            print(f"Tugas ID {id_tugas} berhasil dihapus.")
            input("Tekan Enter untuk melanjutkan...")
            break

def tandai_tugas_sebagai_selesai():
    tugas = muat_tugas()
    while True :
        try:
            id_tugas = int(input("Masukkan ID tugas untuk menandai selesai: "))
        except:
            print("ID tidak valid.")
            continue
        ditemukan = False
        for t in tugas:
            if t['IDTugas'] == id_tugas:
                t['Status'] = 'Selesai'
                ditemukan = True
                break
        if not ditemukan:
            print("Tugas tidak ditemukan.")
        else:
            simpan_tugas(tugas)
            print(f"Tugas ID {id_tugas} ditandai sebagai selesai dan akan dihapus.")
            bersihkan_tugas_selesai()
            tugas = muat_tugas()
            input("Tekan Enter untuk melanjutkan...")
            break


def jadwalkan_tugas_otomatis(kuliah_hari_ini):
    interval_bebas = ambil_interval_bebas(kuliah_hari_ini)
    if not interval_bebas:
        print("Tidak ada interval waktu kosong hari ini.")
        return

    total_kapasitas = sum(durasi_dalam_jam(a, b) for (a, b) in interval_bebas)
    tugas = muat_tugas()
    tanggal_hari_ini = date.today()

    tugas_pending = []
    for t in tugas:
        if t['Status'].lower() == 'pending':
            if t['Tenggat']:
                try:
                    deadline = datetime.datetime.strptime(t['Tenggat'], "%Y-%m-%d").date()
                    if deadline < tanggal_hari_ini:
                        continue
                except:
                    continue
            tugas_pending.append(t)

    if not tugas_pending:
        print("Tidak ada tugas pending yang valid untuk dijadwalkan.")
        return

    tugas_terpilih = knapsack_01(tugas_pending, total_kapasitas)
    jadwal = jadwal_knapsack(interval_bebas, tugas_terpilih)

    print("📅 Jadwal Otomatis Hari Ini (Knapsack):")
    acara = []

    for kul in kuliah_hari_ini:
        mulai = str_ke_waktu(kul['WaktuMulai'])
        selesai = str_ke_waktu(kul['WaktuSelesai'])
        acara.append(('Kuliah', kul['NamaMataKuliah'], mulai, selesai))

    for sch in jadwal:
        acara.append(('Tugas', sch['task']['NamaTugas'], sch['start_time'], sch['end_time']))

    acara.sort(key=lambda x: x[2])

    for ev in acara:
        st = waktu_ke_str(ev[2])
        et = waktu_ke_str(ev[3])
        label = "📘 Kuliah" if ev[0] == 'Kuliah' else "📝 Tugas"
        print(f"  [{label}] {ev[1]} dari {st} sampai {et}")
    input("Tekan Enter untuk kembali...")

def knapsack_01(tugas: List[dict], kapasitas_jam: float) -> List[dict]:
    kapasitas = int(kapasitas_jam * 10)
    n = len(tugas)
    today = datetime.date.today()

    skor = []
    durasi = []
    for t in tugas:
        try:
            deadline = datetime.datetime.strptime(t['Tenggat'], "%Y-%m-%d").date()
            days_left = (deadline - today).days
            value = max(1, 30 - days_left)  # tenggat makin dekat, nilai makin besar
        except:
            value = 5
        skor.append(value)
        durasi.append(int(float(t['DurasiEstimasi']) * 10))

    dp = [[0] * (kapasitas + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(kapasitas + 1):
            if durasi[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], skor[i - 1] + dp[i - 1][w - durasi[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    w = kapasitas
    hasil = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            hasil.append(tugas[i - 1])
            w -= durasi[i - 1]

    return list(reversed(hasil))


def ambil_interval_bebas(kuliah: List[dict]):
    WAKTU_MULAI_HARI = datetime.time(6, 0)
    WAKTU_SELESAI_HARI = datetime.time(22, 0)
    if not kuliah:
        return [(WAKTU_MULAI_HARI, WAKTU_SELESAI_HARI)]
    interval_bebas = []
    kuliah_terurut = sorted(kuliah, key=lambda x: str_ke_waktu(x['WaktuMulai']))
    if str_ke_waktu(kuliah_terurut[0]['WaktuMulai']) > WAKTU_MULAI_HARI:
        interval_bebas.append((WAKTU_MULAI_HARI, str_ke_waktu(kuliah_terurut[0]['WaktuMulai'])))
    for i in range(len(kuliah_terurut) - 1):
        selesai_sebelumnya = str_ke_waktu(kuliah_terurut[i]['WaktuSelesai'])
        mulai_selanjutnya = str_ke_waktu(kuliah_terurut[i + 1]['WaktuMulai'])
        if mulai_selanjutnya > selesai_sebelumnya:
            interval_bebas.append((selesai_sebelumnya, mulai_selanjutnya))
    if str_ke_waktu(kuliah_terurut[-1]['WaktuSelesai']) < WAKTU_SELESAI_HARI:
        interval_bebas.append((str_ke_waktu(kuliah_terurut[-1]['WaktuSelesai']), WAKTU_SELESAI_HARI))
    return interval_bebas

def durasi_dalam_jam(mulai: datetime.time, selesai: datetime.time):
    dt1 = datetime.datetime.combine(datetime.date.today(), mulai)
    dt2 = datetime.datetime.combine(datetime.date.today(), selesai)
    selisih = dt2 - dt1
    return selisih.total_seconds() / 3600

def tambah_jam(mulai: datetime.time, jam: float):
    dt = datetime.datetime.combine(datetime.date.today(), mulai)
    delta = datetime.timedelta(hours=jam)
    dt_selesai = dt + delta
    return dt_selesai.time()

def jadwal_knapsack(interval_bebas: List[Tuple[datetime.time, datetime.time]], tugas: List[dict]):
    tugas_terurut = sorted(tugas, key=lambda x: x['DurasiEstimasi'], reverse=True)
    jadwal = []
    slot_bebas = [(mulai, selesai, durasi_dalam_jam(mulai, selesai)) for (mulai, selesai) in interval_bebas]

    for tugas in tugas_terurut:
        durasi_tugas = tugas['DurasiEstimasi']
        for idx, (mulai, selesai, durasi_slot) in enumerate(slot_bebas):
            if durasi_slot >= durasi_tugas:
                waktu_mulai_tugas = mulai
                waktu_selesai_tugas = tambah_jam(mulai, durasi_tugas)
                jadwal.append({'task': tugas, 'start_time': waktu_mulai_tugas, 'end_time': waktu_selesai_tugas})
                waktu_mulai_baru = waktu_selesai_tugas
                waktu_selesai_baru = selesai
                durasi_baru = durasi_dalam_jam(waktu_mulai_baru, waktu_selesai_baru)
                if durasi_baru > 0:
                    slot_bebas[idx] = (waktu_mulai_baru, waktu_selesai_baru, durasi_baru)
                else:
                    slot_bebas.pop(idx)
                break
    return jadwal

if __name__ == "__main__":
    clear()
    cover()
    enter("\nSELAMAT DATANG DI TEMPAT SEWA KAMI, KNACKPLAN(oﾟvﾟ)ノ. ")
    halaman_knackplan()
