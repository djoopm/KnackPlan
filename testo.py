import csv
import datetime
import os
from datetime import date
from typing import List, Tuple

FILE_KULIAH = 'mata_kuliah.csv'
FILE_TUGAS = 'tugas.csv'

HARI_DALAM_MINGGU = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

def muat_kuliah():
    kuliah = []
    if os.path.exists(FILE_KULIAH):
        with open(FILE_KULIAH, newline='', encoding='utf-8') as f:
            pembaca = csv.DictReader(f)
            for baris in pembaca:
                baris['WaktuMulai'] = baris['WaktuMulai']
                baris['WaktuSelesai'] = baris['WaktuSelesai']
                baris['Hari'] = baris['Hari']
                baris['IDMataKuliah'] = int(baris['IDMataKuliah'])
                baris['NamaMataKuliah'] = baris['NamaMataKuliah']
                kuliah.append(baris)
    return kuliah

def simpan_kuliah(kuliah: List[dict]):
    with open(FILE_KULIAH, 'w', newline='', encoding='utf-8') as f:
        nama_kolom = ['IDMataKuliah', 'NamaMataKuliah', 'Hari', 'WaktuMulai', 'WaktuSelesai']
        penulis = csv.DictWriter(f, fieldnames=nama_kolom)
        penulis.writeheader()
        for k in kuliah:
            penulis.writerow(k)

def muat_tugas():
    tugas = []
    if os.path.exists(FILE_TUGAS):
        with open(FILE_TUGAS, newline='', encoding='utf-8') as f:
            pembaca = csv.DictReader(f)
            for baris in pembaca:
                baris['IDTugas'] = int(baris['IDTugas'])
                baris['DurasiEstimasi'] = float(baris['DurasiEstimasi'])
                baris['Tenggat'] = baris['Tenggat']
                baris['Status'] = baris['Status']
                baris['NamaTugas'] = baris['NamaTugas']
                tugas.append(baris)
    return tugas

def simpan_tugas(tugas: List[dict]):
    with open(FILE_TUGAS, 'w', newline='', encoding='utf-8') as f:
        nama_kolom = ['IDTugas', 'NamaTugas', 'DurasiEstimasi', 'Tenggat', 'Status']
        penulis = csv.DictWriter(f, fieldnames=nama_kolom)
        penulis.writeheader()
        for t in tugas:
            penulis.writerow(t)

def bersihkan_tugas_selesai():
    tugas = muat_tugas()
    tugas = [t for t in tugas if t['Status'].lower() != 'selesai']
    simpan_tugas(tugas)

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

def menu_admin():
    kuliah = muat_kuliah()
    while True:
        cetak_garis()
        print("MENU ADMIN - Mengelola Kuliah")
        print("1. Lihat Kuliah untuk hari tertentu")
        print("2. Tambah Kuliah")
        print("3. Edit Kuliah")
        print("4. Hapus Kuliah")
        print("5. Kembali ke Pemilihan Peran")
        pilihan = input("Pilih opsi: ")
        if pilihan == '1':
            hari = input_hari()
            cetak_kuliah_hari_ini(kuliah, hari)
        elif pilihan == '2':
            nama_kuliah = input("Masukkan nama kuliah: ").strip()
            hari = input_hari()
            waktu_mulai = input_waktu("Masukkan waktu mulai")
            waktu_selesai = input_waktu("Masukkan waktu selesai")
            if str_ke_waktu(waktu_selesai) <= str_ke_waktu(waktu_mulai):
                print("Waktu selesai harus setelah waktu mulai. Kuliah tidak ditambahkan.")
                continue
            tumpang_tindih_ditemukan = False
            for k in kuliah:
                if k['Hari'] == hari:
                    if tumpang_tindih(str_ke_waktu(waktu_mulai), str_ke_waktu(waktu_selesai),
                                      str_ke_waktu(k['WaktuMulai']), str_ke_waktu(k['WaktuSelesai'])):
                        print(f"Tumpang tindih dengan kuliah yang ada [{k['IDMataKuliah']}] {k['NamaMataKuliah']} {k['WaktuMulai']}–{k['WaktuSelesai']}")
                        tumpang_tindih_ditemukan = True
                        break
            if tumpang_tindih_ditemukan:
                print("Tidak dapat menambahkan kuliah yang tumpang tindih.")
                continue
            id_baru = id_kuliah_selanjutnya(kuliah)
            kuliah_baru = {'IDMataKuliah': id_baru, 'NamaMataKuliah': nama_kuliah, 'Hari': hari,
                           'WaktuMulai': waktu_mulai, 'WaktuSelesai': waktu_selesai}
            kuliah.append(kuliah_baru)
            simpan_kuliah(kuliah)
            print(f"Kuliah ditambahkan dengan ID {id_baru}.")
        elif pilihan == '3':
            try:
                id_kuliah = int(input("Masukkan ID kuliah untuk diedit: "))
            except ValueError:
                print("ID tidak valid.")
                continue
            kuliah_yang_ditemukan = [k for k in kuliah if k['IDMataKuliah'] == id_kuliah]
            if not kuliah_yang_ditemukan:
                print("Kuliah tidak ditemukan.")
                continue
            kuliah = kuliah_yang_ditemukan[0]
            print(f"Mengedit Kuliah [{kuliah['IDMataKuliah']}] {kuliah['NamaMataKuliah']} {kuliah['Hari']} {kuliah['WaktuMulai']}-{kuliah['WaktuSelesai']}")
            nama_baru = input(f"Nama kuliah baru (biarkan kosong untuk mempertahankan '{kuliah['NamaMataKuliah']}'): ").strip()
            if nama_baru:
                kuliah['NamaMataKuliah'] = nama_baru
            hari_baru = input(f"Hari baru (biarkan kosong untuk mempertahankan '{kuliah['Hari']}'): ").capitalize().strip()
            if hari_baru:
                if hari_baru not in HARI_DALAM_MINGGU:
                    print("Hari yang dimasukkan tidak valid. Edit dibatalkan.")
                    continue
                kuliah['Hari'] = hari_baru
            waktu_mulai_baru = input(f"Waktu mulai baru (biarkan kosong untuk mempertahankan '{kuliah['WaktuMulai']}'): ").strip()
            if waktu_mulai_baru:
                try:
                    datetime.datetime.strptime(waktu_mulai_baru, '%H:%M')
                    kuliah['WaktuMulai'] = waktu_mulai_baru
                except:
                    print("Format waktu tidak valid. Edit dibatalkan.")
                    continue
            waktu_selesai_baru = input(f"Waktu selesai baru (biarkan kosong untuk mempertahankan '{kuliah['WaktuSelesai']}'): ").strip()
            if waktu_selesai_baru:
                try:
                    datetime.datetime.strptime(waktu_selesai_baru, '%H:%M')
                    kuliah['WaktuSelesai'] = waktu_selesai_baru
                except:
                    print("Format waktu tidak valid. Edit dibatalkan.")
                    continue
            if str_ke_waktu(kuliah['WaktuSelesai']) <= str_ke_waktu(kuliah['WaktuMulai']):
                print("Waktu selesai harus setelah waktu mulai. Edit dibatalkan.")
                continue
            tumpang_tindih_ditemukan = False
            for k in kuliah:
                if k['IDMataKuliah'] != kuliah['IDMataKuliah'] and k['Hari'] == kuliah['Hari']:
                    if tumpang_tindih(str_ke_waktu(kuliah['WaktuMulai']), str_ke_waktu(kuliah['WaktuSelesai']),
                                      str_ke_waktu(k['WaktuMulai']), str_ke_waktu(k['WaktuSelesai'])):
                        print(f"Tumpang tindih dengan kuliah yang ada [{k['IDMataKuliah']}] {k['NamaMataKuliah']} {k['WaktuMulai']}–{k['WaktuSelesai']}")
                        tumpang_tindih_ditemukan = True
                        break
            if tumpang_tindih_ditemukan:
                print("Edit menghasilkan kuliah yang tumpang tindih. Edit dibatalkan.")
                continue
            simpan_kuliah(kuliah)
            print("Kuliah berhasil diedit.")
        elif pilihan == '4':
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
                simpan_kuliah(kuliah)
                print(f"Kuliah ID {id_kuliah} berhasil dihapus.")
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak valid.")

def menu_pengguna():
    bersihkan_tugas_selesai()
    kuliah = muat_kuliah()
    tugas = muat_tugas()
    hari = hari_ini()
    kuliah_hari_ini = [k for k in kuliah if k['Hari'] == hari]
    kuliah_hari_ini.sort(key=lambda x: str_ke_waktu(x['WaktuMulai']))
    while True:
        cetak_garis()
        print(f"MENU PENGGUNA - Manajemen Tugas (Hari ini adalah {hari})")
        print("Jadwal Kuliah Hari Ini:")
        if not kuliah_hari_ini:
            print("  Tidak ada kuliah hari ini.")
        else:
            for k in kuliah_hari_ini:
                print(f"  {k['NamaMataKuliah']} dari {k['WaktuMulai']} sampai {k['WaktuSelesai']}")
                
        input('LANJUT?')##########################
        
        cetak_garis()
        print("1. Lihat semua tugas")
        print("2. Tambah tugas")
        print("3. Edit tugas")
        print("4. Hapus tugas")
        print("5. Tandai tugas sebagai selesai")
        print("6. Lihat jadwal hari ini dengan tugas yang dijadwalkan di waktu luang")
        print("7. Kembali ke Pemilihan Peran")
        pilihan = input("Pilih opsi: ")
        if pilihan == '1':
            if not tugas:
                print("Tidak ada tugas yang terdaftar saat ini.")
            else:
                print("Tugas Terdaftar:")
                for t in tugas:
                    print(f"  [{t['IDTugas']}] {t['NamaTugas']} Durasi:{t['DurasiEstimasi']}h Tenggat:{t['Tenggat']} Status:{t['Status']}")
        elif pilihan == '2':
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
            tenggat = input("Tenggat (YYYY-MM-DD, biarkan kosong jika tidak ada): ").strip()
            if tenggat:
                try:
                    datetime.datetime.strptime(tenggat, '%Y-%m-%d')
                except:
                    print("Format tanggal tidak valid. Tugas tidak ditambahkan.")
                    continue
            else:
                tenggat = ''
            id_tugas_baru = id_tugas_selanjutnya(tugas)
            tugas.append({'IDTugas': id_tugas_baru, 'NamaTugas': nama_tugas,
                          'DurasiEstimasi': durasi_estimasi, 'Tenggat': tenggat,
                          'Status': 'Pending'})
            simpan_tugas(tugas)
            print(f"Tugas '{nama_tugas}' ditambahkan dengan ID {id_tugas_baru}.")
        elif pilihan == '3':
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
                if status_baru not in ['Pending', 'Completed']:
                    print("Status tidak valid. Edit dibatalkan.")
                    continue
                t['Status'] = status_baru
            simpan_tugas(tugas)
            print("Tugas berhasil diedit.")
            bersihkan_tugas_selesai()  # Hapus yang selesai segera
        elif pilihan == '4':
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
        elif pilihan == '5':
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
        elif pilihan == '6':
            os.system('cls')###################
            interval_bebas = ambil_interval_bebas(kuliah_hari_ini)

            if not interval_bebas:
                print("Tidak ada interval bebas yang tersedia antara kuliah hari ini.")
                continue
            tanggal_hari_ini = date.today()
            tugas_terfilter = []
            for t in tugas:
                if t['Status'].lower() != 'pending':
                    continue
                if t['Tenggat']:
                    try:
                        dl = datetime.datetime.strptime(t['Tenggat'], '%Y-%m-%d').date()
                        if dl < tanggal_hari_ini:
                            continue
                    except:
                        pass
                tugas_terfilter.append(t)

            if not tugas_terfilter:
                print("Tidak ada tugas yang tertunda tersedia untuk dijadwalkan hari ini.")
                continue

            jadwal = jadwal_knapsack(interval_bebas, tugas_terfilter)

            print("Jadwal Hari Ini dengan Tugas:")
            acara = []
            for kuliah in kuliah_hari_ini:
                mulai = str_ke_waktu(kuliah['WaktuMulai'])
                selesai = str_ke_waktu(kuliah['WaktuSelesai'])
                acara.append(('Kuliah', kuliah['NamaMataKuliah'], mulai, selesai))
            for sch in jadwal:
                acara.append(('Tugas', sch['task']['NamaTugas'], sch['start_time'], sch['end_time']))
            acara.sort(key=lambda x: x[2])  # urutkan berdasarkan waktu mulai

            for ev in acara:
                st = waktu_ke_str(ev[2])
                et = waktu_ke_str(ev[3])
                print(f"  [{ev[0]}] {ev[1]} dari {st} sampai {et}")
            input()

        elif pilihan == '7':
            break
        else:
            print("Pilihan tidak valid.")

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

def pemilihan_peran():
    bersihkan_tugas_selesai()
    while True:
        cetak_garis()
        print("Selamat datang di Sistem Manajemen Kuliah dan Tugas (Versi Konsol)")
        print("Pilih Peran:")
        print("1. Admin (Kelola Kuliah)")
        print("2. Pengguna (Kelola Tugas)")
        print("3. Keluar")
        pilihan = input("Pilih peran: ")
        if pilihan == '1':
            menu_admin()
        elif pilihan == '2':
            menu_pengguna()
        elif pilihan == '3':
            print("Selamat tinggal!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    pemilihan_peran()
