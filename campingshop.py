import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

data_product = {
    1: "Tenda Dome",
    2: "Tenda Pleton",
    3: "Hand Warmer",
    4: "Sleepingbag",
    5: "Matras",
    6: "Carrier Bag",
    7: "Senter",
    8: "Headlamp",
    9: "Kursi Kemah",
}

daftar_harga = {
    1: 500000,
    2: 2000000,
    3: 150000,
    4: 300000,
    5: 120000,
    6: 500000,
    7: 70000,
    8: 100000,
    9: 180000,
}

daftar_metode_pembayaran = {
    1: "Transfer Bank",
    2: "Virtual Account",
    3: "Cash on Delivery",
    4: "Kartu Kredit",
    5: "Bayar di Supermarket"
}

daftar_gambar = {
    1: "tenda_dome.jpeg",
    2: "tenda_pleton.jpeg",
    3: "hand_warmer.jpg",
    4: "sleepingbag.jpeg",
    5: "matras.jpeg",
    6: "carrier_bag.jpeg",
    7: "senter.jpeg",
    8: "headlamp.jpeg",
    9: "kursi_kemah.jpeg",
}

kurir_options = ["SiCepat", "JnT", "JNE", "Shopee Express", "IDExpress"]

# Menyimpan histori transaksi
histori_transaksi = []

def update_gambar(event):
    pilih_id = combobox_product.current() + 1
    image_path = daftar_gambar.get(pilih_id)
    if image_path:
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label_gambar.config(image=photo)
            label_gambar.image = photo
        except (FileNotFoundError, IOError) as e:
            messagebox.showerror("Error", f"Error loading image {image_path}: {e}")
    update_total_harga()

def tampilkan_detail_pesanan(dict_trx):
    detail_pesanan = (
        f"Nama Penerima    : {dict_trx['nama penerima']}\n"
        f"Alamat Penerima  : {dict_trx['alamat penerima']}\n"
        f"No Handphone     : {dict_trx['No Handphone']}\n"
        f"Kurir Pengiriman : {dict_trx['kurir pengiriman']}\n"
        f"Product          : {data_product[dict_trx['product id']]} - {dict_trx['jumlah']} pcs - Rp {dict_trx['total harga']}\n"
        f"Metode Pembayaran: {dict_trx['metode pembayaran']}\n"
    )
    messagebox.showinfo("Detail Pesanan", detail_pesanan)

def beli():
    pilih_id = combobox_product.current() + 1
    if pilih_id not in data_product:
        messagebox.showerror("Error", "Id product tidak tersedia")
        return

    nama_penerima = entry_nama_penerima.get().strip()
    alamat_penerima = entry_alamat_penerima.get().strip()
    telepon = entry_telepon.get().strip()
    kurir_pengiriman = combobox_kurir.get().strip()
    metode_pembayaran = combobox_metode_pembayaran.get().strip()
    jumlah_barang = entry_jumlah_barang.get().strip()

    if not nama_penerima or not alamat_penerima or not telepon or not kurir_pengiriman or not metode_pembayaran or not jumlah_barang:
        messagebox.showerror("Error", "Semua kolom harus diisi!")
        return

    try:
        jumlah_barang = int(jumlah_barang)
        if jumlah_barang <= 0:
            raise ValueError("Jumlah barang harus lebih dari 0.")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
        return

    total_harga = daftar_harga[pilih_id] * jumlah_barang

    pilih_beli = messagebox.askyesno("Konfirmasi", "Ingin Beli?")
    if not pilih_beli:
        return

    dict_trx = {
        "nama penerima": nama_penerima,
        "alamat penerima": alamat_penerima,
        "No Handphone": telepon,
        "kurir pengiriman": kurir_pengiriman,
        "product id": pilih_id,
        "metode pembayaran": metode_pembayaran,
        "jumlah": jumlah_barang,
        "total harga": total_harga,
    }

    histori_transaksi.append(dict_trx)  # Simpan transaksi ke histori

    if metode_pembayaran == "Cash on Delivery":
        messagebox.showinfo("Berhasil", "Ketika paket sampai jangan lupa melakukan pembayaran ya!")
    else:
        konfirmasi = messagebox.askyesno("Konfirmasi Pembayaran", "Apakah Anda Yakin Ingin Melakukan Pembayaran?")
        if konfirmasi:
            messagebox.showinfo("Berhasil", "Pembayaran berhasil dilakukan!")
        else:
            messagebox.showinfo("Dibatalkan", "Pembayaran dibatalkan.")
    
    tampilkan_detail_pesanan(dict_trx)

def validate_jumlah_barang(char):
    return char.isdigit()

def increment_jumlah_barang():
    try:
        jumlah = int(entry_jumlah_barang.get())
        entry_jumlah_barang.delete(0, tk.END)
        entry_jumlah_barang.insert(0, str(jumlah + 1))
        update_total_harga()
    except ValueError:
        entry_jumlah_barang.delete(0, tk.END)
        entry_jumlah_barang.insert(0, "1")

def decrement_jumlah_barang():
    try:
        jumlah = int(entry_jumlah_barang.get())
        if jumlah > 1:
            entry_jumlah_barang.delete(0, tk.END)
            entry_jumlah_barang.insert(0, str(jumlah - 1))
            update_total_harga()
    except ValueError:
        entry_jumlah_barang.delete(0, tk.END)
        entry_jumlah_barang.insert(0, "1")

def update_total_harga():
    try:
        jumlah_barang = int(entry_jumlah_barang.get())
        pilih_id = combobox_product.current() + 1
        total_harga = daftar_harga.get(pilih_id, 0) * jumlah_barang
        label_total_harga.config(text=f"Total Pembayaran: Rp {total_harga:,}")
    except ValueError:
        label_total_harga.config(text="Total Pembayaran: Rp 0")

def lihat_histori():
    if not histori_transaksi:
        messagebox.showinfo("Histori Transaksi", "Tidak ada transaksi yang tercatat.")
        return

    histori_text = "Histori Transaksi:\n\n"
    for trx in histori_transaksi:
        histori_text += (
            f"Nama Penerima    : {trx['nama penerima']}\n"
            f"Alamat Penerima  : {trx['alamat penerima']}\n"
            f"No Handphone     : {trx['No Handphone']}\n"
            f"Kurir Pengiriman : {trx['kurir pengiriman']}\n"
            f"Product          : {data_product[trx['product id']]} - {trx['jumlah']} pcs - Rp {trx['total harga']}\n"
            f"Metode Pembayaran: {trx['metode pembayaran']}\n"
            f"{'='*40}\n"
        )

    messagebox.showinfo("Histori Transaksi", histori_text)

# Membuat window Tkinter
root = tk.Tk()
root.title("CAMPING SHOP")

# Mengatur konfigurasi kolom
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

# Membuat label dan combobox untuk memilih produk
tk.Label(root, text="Pilih Produk:").grid(row=0, column=0, sticky="w")
combobox_product = ttk.Combobox(root, values=[f"{data_product[i]} - Rp {daftar_harga[i]}" for i in data_product])
combobox_product.grid(row=0, column=1, sticky="ew")
combobox_product.current(0)
combobox_product.bind("<<ComboboxSelected>>", update_gambar)

# Label untuk menampilkan gambar produk
initial_image_path = daftar_gambar[1]
try:
    image = Image.open(initial_image_path)
    image = image.resize((200, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label_gambar = tk.Label(root, image=photo)
    label_gambar.grid(row=1, column=0, columnspan=2, pady=10)
    label_gambar.image = photo
except FileNotFoundError:
    label_gambar = tk.Label(root, text="Gambar tidak ditemukan")
    label_gambar.grid(row=1, column=0, columnspan=2, pady=10)

# Membuat label dan entry untuk Jumlah Barang
tk.Label(root, text="Jumlah Barang:").grid(row=2, column=0, sticky="w")
frame_jumlah_barang = tk.Frame(root)
frame_jumlah_barang.grid(row=2, column=1, sticky="w")

entry_jumlah_barang = tk.Entry(frame_jumlah_barang, width=5, validate="key")
entry_jumlah_barang.grid(row=0, column=1, padx=5)

vcmd = (root.register(validate_jumlah_barang), "%S")
entry_jumlah_barang.config(validatecommand=vcmd)

tk.Button(frame_jumlah_barang, text="-", command=decrement_jumlah_barang).grid(row=0, column=0)
tk.Button(frame_jumlah_barang, text="+", command=increment_jumlah_barang).grid(row=0, column=2)

label_total_harga = tk.Label(root, text="Total Pembayaran: Rp 0")
label_total_harga.grid(row=3, column=1, sticky="w")

# Membuat label dan entry untuk Nama Penerima
tk.Label(root, text="Nama Penerima:").grid(row=4, column=0, sticky="w")
entry_nama_penerima = tk.Entry(root, width=30)
entry_nama_penerima.grid(row=4, column=1, sticky="ew")

# Membuat label dan entry untuk Alamat Penerima
tk.Label(root, text="Alamat Penerima:").grid(row=5, column=0, sticky="w")
entry_alamat_penerima = tk.Entry(root, width=30)
entry_alamat_penerima.grid(row=5, column=1, sticky="ew")

# Membuat label dan entry untuk No Handphone
tk.Label(root, text="No Handphone:").grid(row=6, column=0, sticky="w")
entry_telepon = tk.Entry(root, width=30)
entry_telepon.grid(row=6, column=1, sticky="ew")

# Membuat label dan combobox untuk Kurir Pengiriman
tk.Label(root, text="Kurir Pengiriman:").grid(row=7, column=0, sticky="w")
combobox_kurir = ttk.Combobox(root, values=kurir_options, width=30)
combobox_kurir.grid(row=7, column=1, sticky="ew")
combobox_kurir.current(0)

# Membuat label dan combobox untuk Metode Pembayaran
tk.Label(root, text="Pilih Metode Pembayaran:").grid(row=8, column=0, sticky="w")
combobox_metode_pembayaran = ttk.Combobox(root, values=list(daftar_metode_pembayaran.values()), width=30)
combobox_metode_pembayaran.grid(row=8, column=1, sticky="ew")
combobox_metode_pembayaran.current(0)

# Membuat tombol Beli
tk.Button(root, text="Beli", command=beli).grid(row=9, column=0, columnspan=2, pady=10)

# Membuat tombol Lihat Histori
tk.Button(root, text="Lihat Histori", command=lihat_histori).grid(row=10, column=0, columnspan=2, pady=10)

# Menjalankan GUI Tkinter
root.mainloop()
