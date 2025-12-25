import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import csv
import os
from tkinter import messagebox
import webbrowser
from datetime import date
from tkcalendar import DateEntry

# Import halaman-halaman aplikasi
from homepage import HomePage
from paymentpage import PaymentPage
from profilepage import ProfilePage

ctk.set_appearance_mode("light")

class TravelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Travel.Id")

        # Data & State Aplikasi
        self.current_destination = ""
        self.current_fullname = ""
        self.payment_method_selected = False
        self._image_references = {} 

        # Konfigurasi Harga & Diskon
        self.TICKET_PRICES = { "Borobudur": 150000, "Tanah Lot": 200000, "Raja Ampat": 500000, "Candi Prambanan": 120000, "Gunung Rinjani": 250000 }
        self.DISCOUNTS = { "Borobudur": 0.10, "Tanah Lot": 0.15, "Raja Ampat": 0.10, "Gunung Rinjani": 0.15, "Candi Prambanan": 0.00 }
        self.active_discounts = { "Borobudur": False, "Tanah Lot": False, "Raja Ampat": False, "Gunung Rinjani": False, "Candi Prambanan": False }
        
        # Data untuk halaman destinasi
        self.DESTINATION_DATA = {
            "Borobudur": {"frame": None, "bg_img": "assets/bg/borobudur.png", "back_color": "#C7B184", "loc_img": "assets/button/loc boro.png", "loc_url": "https://maps.app.goo.gl/8aWVX5Q1JHBGE2j66", "tic_img": "assets/button/tic boro.png", "btn_color": "#D9D9D9", "btn_hover": "#D9D9D9"},
            "Tanah Lot": {"frame": None, "bg_img": "assets/bg/tanah lot.png", "back_color": "#CD5B45", "loc_img": "assets/button/loc tanah.png", "loc_url": "https://maps.app.goo.gl/GVS7gxeoTfBkfpkH6", "tic_img": "assets/button/tic tanah.png", "btn_color": "#D78080", "btn_hover": "#D78080"},
            "Raja Ampat": {"frame": None, "bg_img": "assets/bg/raja ampat.png", "back_color": "#93A3AE", "loc_img": "assets/button/loc raja.png", "loc_url": "https://maps.app.goo.gl/6fzWy5szm5F2RMzP7", "tic_img": "assets/button/tic raja.png", "btn_color": "#80BFD7", "btn_hover": "#80BFD7"},
            "Candi Prambanan": {"frame": None, "bg_img": "assets/bg/prambanan.png", "back_color": "#657187", "loc_img": "assets/button/loc pra.png", "loc_url": "https://maps.app.goo.gl/ofnm6XTfUFdYSR1o7", "tic_img": "assets/button/tic pra.png", "btn_color": "#7B411D", "btn_hover": "#7B411D"},
            "Gunung Rinjani": {"frame": None, "bg_img": "assets/bg/mt rinjani.png", "back_color": "#BF7DA9", "loc_img": "assets/button/loc rin.png", "loc_url": "https://maps.app.goo.gl/nrCCfDuuYdj28dxW9", "tic_img": "assets/button/tic rin.png", "btn_color": "#EA4DDA", "btn_hover": "#EA4DDA"}
        }

        # File Handling
        self.history_csv = "ticket_history.csv"
        self.csv_path = "user_reg.csv"
        self._initialize_csv_files() # >> memastikan file csv ada

        # Setup UI
        self.setup_ui()

    def _initialize_csv_files(self):
        if not os.path.isfile(self.history_csv):
            with open(self.history_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["nama", "destinasi", "jumlah_tiket", "tanggal", "harga_satuan", "total_bayar"])
        if not os.path.isfile(self.csv_path):
            with open(self.csv_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["firstname", "lastname", "email", "password"])

    def load_icon(self, path, size):
        if os.path.isfile(path):
            img = Image.open(path)
            return ctk.CTkImage(light_image=img, size=size)
        print(f"Warning: Icon not found at {path}")
        return None

    def load_image(self, path, size):
        if os.path.isfile(path):
            img = Image.open(path)
            return ctk.CTkImage(light_image=img, size=size)
        print(f"Warning: Image not found at {path}")
        return None

    def load_icons(self):
        self.icon_back = self.load_icon("assets/icon/button back.png", (30, 30))
        self.icon_home = self.load_icon("assets/icon/ikon home.png", (80, 80))
        self.icon_pay = self.load_icon("assets/icon/icon pay.png", (75, 75))
        self.icon_profil = self.load_icon("assets/icon/ikon profile.png", (80, 80))
        self.qris_code_img = self.load_icon("assets/bg/qris.png", (620, 535))
        self.metode_btn_img = self.load_icon("assets/button/qris 2.png", (341, 57))

    def setup_ui(self):
        self.load_icons()

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        # Membuat semua halaman dan menyimpannya di self.pages
        for PageClass in (HomePage, PaymentPage, ProfilePage):
            page_name = PageClass.__name__
            page = PageClass(container, self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Halaman lama juga dibuat sebagai anak dari container
        self.register_page(container)
        self.login_page(container)
        self.donasi_page(container)
        
        for name, data in self.DESTINATION_DATA.items():
            self.create_destination_page(container, name, data)
        
        self.popup_components()
        self.setup_text_popup()

        self.show_page('RegisterPage')

    # =================================================================================
    # 1. UI CREATION METHODS
    # =================================================================================
    
    def donasi_page(self, parent):
        self.donasi_frame = ctk.CTkFrame(parent, width=1920, height=1080)
        self.donasi_frame.grid(row=0, column=0, sticky="nsew")
        self.pages['DonasiPage'] = self.donasi_frame
        
        bg_img = self.load_image("assets/bg/donasi page.png", (1920, 1080))
        ctk.CTkLabel(self.donasi_frame, image=bg_img, text="").place(x=0, y=0)
        
        # Tombol kembali ke HomePage
        ctk.CTkButton(self.donasi_frame, width=10, height=10, image=self.icon_back, text="", fg_color="#D9D9D9", bg_color="#D9D9D9", hover_color="#A79A9A", command=lambda: self.show_page('HomePage')).place(x=80, y=30)

    def register_page(self, parent):
        self.reg_frame = ctk.CTkFrame(parent, width=1920, height=1080)
        self.reg_frame.grid(row=0, column=0, sticky="nsew")
        self.pages['RegisterPage'] = self.reg_frame
        
        bg_img = self.load_image("assets/bg/register.png", (1920, 1080))
        ctk.CTkLabel(self.reg_frame, image=bg_img, text="").place(x=0, y=0)
        self.entry_firstname = ctk.CTkEntry(self.reg_frame, width=200, height=60, placeholder_text=" ", border_color="#F8EFEF", fg_color="#F8EFEF", font=("Arial", 20), text_color="Black", corner_radius=2)
        self.entry_firstname.place(x=1025, y=460.55)
        self.entry_lastname = ctk.CTkEntry(self.reg_frame, width=200, height=60, placeholder_text=" ", border_color="#F8EFEF", fg_color="#F8EFEF", font=("Arial", 20), text_color="Black", corner_radius=2)
        self.entry_lastname.place(x=1305, y=460.55)
        self.entry_email = ctk.CTkEntry(self.reg_frame, width=430, height=50, placeholder_text=" ", border_color="#D9D9D9", fg_color="#D9D9D9", font=("Helvetica", 20), text_color="Black", corner_radius=2)
        self.entry_email.place(x=1103, y=570)
        self.entry_password = ctk.CTkEntry(self.reg_frame, width=360, height=50, placeholder_text="", border_color="#D9D9D9", fg_color="#D9D9D9", font=("Helvetica", 20), text_color="Black", corner_radius=2)
        self.entry_password.place(x=1145, y=680)
        
        def update_email(*args):
            first = self.entry_firstname.get().strip().lower()
            last = self.entry_lastname.get().strip().lower()
            if first and last:
                self.entry_email.delete(0, "end")
                self.entry_email.insert(0, f"{first}.{last}@gmail.com")
        self.entry_firstname.bind("<KeyRelease>", update_email)
        self.entry_lastname.bind("<KeyRelease>", update_email)

        ctk.CTkButton(self.reg_frame, width=555, height=55, text="Register ", fg_color="#D9D9D9", border_color="#D9D9D9", hover_color="#E1C5C5", text_color="black", font=("Helvetica", 20, "bold"), corner_radius=3, command=self.simpen_data).place(x=1010, y=790)
        ctk.CTkButton(self.reg_frame, width=60, height=30, text="Log in", font=("Helvetica", 15, "bold"), text_color="#61A8EB", fg_color="#F8EFEF", bg_color="#F8EFEF", border_width=0, corner_radius=14, command=lambda: self.show_page('LoginPage')).place(x=1324, y=339)
        
        # --- Tombol Contact, Service, About ---
        btn_size = (230, 83)
        
        contact_img = self.load_icon("assets/button/contact.png", btn_size)
        ctk.CTkButton(self.reg_frame, image=contact_img, text="", fg_color="#80BFD7", hover_color="#80BFD7", bg_color="#80BFD7", command=lambda: self.show_text_popup("Contact", "Oleh Kami kelompok 9:\n\n1. Nama Lengkap : Yuan Fasich Tansatrisna\nNIM          : 25031554155\n\n"
                     "2. Nama Lengkap : Wiliyan Surya\n   NIM          : 25031554168\n\n"
                     "3. Nama Lengkap : Dinda Alifia Eka Nirmala\n   NIM          : 25031554257\n\n")).place(x=1090, y=43)

        service_img = self.load_icon("assets/button/service.png", btn_size)
        ctk.CTkButton(self.reg_frame, image=service_img, text="", fg_color="#80BFD7", hover_color="##80BFD7", bg_color= "#80BFD7",command=lambda: self.show_text_popup("Service", "Aplikasi ini dirancang hanya sebagai bahan uji coba,\n pembayaran pemesanan, harga tiket dan invoice yang dihasilkan tidak dihasilkan secara real-time melainkan hanya hasil percobaan uji coba aplikasi")).place(x=1360, y=43)

        about_img = self.load_icon("assets/button/about.png", btn_size)
        ctk.CTkButton(self.reg_frame, image=about_img, text="", fg_color="#80BFD7", hover_color="#80BFD7", bg_color= "#80BFD7", command=lambda: self.show_text_popup("About", "Tentang Travel.Id:\n\nAplikasi pemesanan tiket wisata.\n Aplikasi digunakan dengan mengisi menu login dan registrasi\nmelakukan pemesanan di menu home dan payment page,\nlalu mengecek history tiket pada bagian profile page")).place(x=1656, y=43)

    def login_page(self, parent):
        self.login_frame = ctk.CTkFrame(parent, width=1920, height=1080)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.pages['LoginPage'] = self.login_frame
        
        bg_img = self.load_image("assets/bg/login.png", (1920, 1080))
        ctk.CTkLabel(self.login_frame, image=bg_img, text="").place(x=0, y=0)
        self.login_email = ctk.CTkEntry(self.login_frame, width=680, height=70, placeholder_text=" ", border_color="#D9D9D9", fg_color="#D9D9D9", font=("Helvetica", 25), text_color="Black", corner_radius=2)
        self.login_email.place(x=585, y=465)
        self.login_password = ctk.CTkEntry(self.login_frame, width=700, height=70, placeholder_text=" ", border_color="#D9D9D9", fg_color="#D9D9D9", font=("Helvetica", 25), text_color="Black", corner_radius=2, show="*")
        self.login_password.place(x=585, y=605)
        ctk.CTkButton(self.login_frame, width=10, height=10, image=self.icon_back, text="", fg_color="transparent", bg_color="#82ABC5", command=lambda: self.show_page('RegisterPage')).place(x=85, y=30)
        ctk.CTkButton(self.login_frame, width=410, height=90, text="Log in", fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black", font=("Helvetica", 20, "bold"), corner_radius=3, hover_color="#E1C5C5", command=self.msksemua).place(x=735, y=740)

    def create_destination_page(self, parent, name, data):
        frame = ctk.CTkFrame(parent, width=1920, height=1080)
        frame.grid(row=0, column=0, sticky="nsew")
        self.pages[name] = frame # Simpan frame dengan nama destinasi
        
        bg_img = self.load_image(data["bg_img"], (1920, 1080))
        ctk.CTkLabel(frame, image=bg_img, text="").place(x=0, y=0)
        
        ctk.CTkButton(frame, width=10, height=10, image=self.icon_back, text="", fg_color=data["back_color"], bg_color=data["back_color"], hover_color=data["back_color"], command=lambda: self.show_page('HomePage')).place(x=80, y=30)
        loc_icon = self.load_icon(data["loc_img"], (490, 65))
        ctk.CTkButton(frame, image=loc_icon, text="", fg_color=data["btn_color"], hover_color=data["btn_hover"], bg_color=data["btn_color"], command=lambda u=data["loc_url"]: webbrowser.open(u)).place(x=85, y=920)
        tic_icon = self.load_icon(data["tic_img"], (500, 75))
        ctk.CTkButton(frame, image=tic_icon, text="", fg_color=data["btn_color"], hover_color=data["btn_hover"], bg_color=data["btn_color"], command=lambda n=name: self.open_payment(n)).place(x=1320, y=920)

    def popup_components(self):
        self.popup_frame = ctk.CTkFrame(self, width=1920, height=1080, fg_color="transparent")
        self.popup_frame.place_forget()
        self.popup_img_label = ctk.CTkLabel(self.popup_frame, text="")
        self.popup_img_label.pack()
        ctk.CTkButton(self.popup_frame, text="✕", width=40, height=40, fg_color="#050505", hover_color="#050505", corner_radius=20, command=self.hide_popup).place(relx=0.95, rely=0.05, anchor="center")

    def setup_text_popup(self):
        self.text_popup_frame = ctk.CTkFrame(self, width=600, height=400, corner_radius=20, fg_color="#FFFFFF", border_width=2, border_color="black")
        
        self.popup_title_label = ctk.CTkLabel(self.text_popup_frame, text="Title", font=("Helvetica", 28, "bold"), text_color="black")
        self.popup_title_label.place(relx=0.5, rely=0.2, anchor="center")
        
        self.popup_text_label = ctk.CTkLabel(self.text_popup_frame, text="Content", font=("Helvetica", 20), text_color="black", wraplength=550)
        self.popup_text_label.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkButton(self.text_popup_frame, text="Tutup", width=120, height=40, fg_color="#CD5B45", hover_color="#8B3E2F", command=self.hide_text_popup).place(relx=0.5, rely=0.85, anchor="center")

    def show_text_popup(self, title, content):
        self.popup_title_label.configure(text=title)
        self.popup_text_label.configure(text=content)
        self.text_popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.text_popup_frame.lift()

    def hide_text_popup(self):
        self.text_popup_frame.place_forget()

    def _create_navigation_buttons(self, parent_frame, active_page: str):
        # Hanya tampilkan tombol navigasi jika halaman tersebut TIDAK sedang aktif
        if active_page != "home":
            ctk.CTkButton(parent_frame, width=10, height=10, image=self.icon_home, text="", fg_color="#D9D9D9", bg_color="#D9D9D9", hover_color="#657187", command=lambda: self.show_page('HomePage')).place(x=439, y=960)
        
        if active_page != "pay":
            ctk.CTkButton(parent_frame, width=75, height=75, image=self.icon_pay, text="", fg_color="#D9D9D9", bg_color="#D9D9D9", hover_color="#657187", command=self.open_blank_payment_page).place(x=913, y=960)
            
        if active_page != "profile":
            ctk.CTkButton(parent_frame, width=30, height=30, image=self.icon_profil, text="", fg_color="#D9D9D9", bg_color="#D9D9D9", hover_color="#657187", command=self.open_profile_page).place(x=1411, y=960)

    # =================================================================================
    # 2. EVENT HANDLERS & COMMANDS
    # =================================================================================

    def show_page(self, page_name):
        if page_name in self.pages:
            frame = self.pages[page_name]
            frame.tkraise()
        else:
            print(f"Error: Page '{page_name}' not found.")

    def show_destination_page(self, destination_name):
        self.show_page(destination_name)

    def simpen_data(self):
        first = self.entry_firstname.get().strip()
        last = self.entry_lastname.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        if not all([first, last, email, password]):
            messagebox.showwarning("Peringatan", "Semua kotak harus diisi!")
            return
        with open(self.csv_path, "a", newline="") as file:
            csv.writer(file).writerow([first, last, email, password])
        self.show_page('LoginPage')

    def msksemua(self):
        input_email = self.login_email.get().strip()
        input_password = self.login_password.get().strip()
        if not all([input_email, input_password]):
            messagebox.showwarning("Peringatan", "Silakan isi email dan password!")
            return
        
        with open(self.csv_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["email"].strip() == input_email and row["password"].strip() == input_password:
                    self.set_username(row["firstname"], row["lastname"])
                    self.show_page('HomePage')
                    return
        messagebox.showerror("Gagal", "Email atau password salah!")

    def set_username(self, first, last):
        self.current_fullname = f"{first} {last}"
        if hasattr(self, 'username_label'):
            self.username_label.configure(text=f"@ {first} {last}!")
        if hasattr(self, 'profile_name_label'):
            self.profile_name_label.configure(text=f"@{first} {last}")

    def activate_discount(self, dest):
        if dest in self.active_discounts:
            self.active_discounts[dest] = True
            messagebox.showinfo("Diskon Aktif", f"Diskon untuk {dest} berhasil diaktifkan!")
        else:
            messagebox.showinfo("Info", "Destinasi tidak punya diskon.")

    def show_discount_image(self, img_path):
        try:
            popup_img = self.load_icon(img_path, (1920, 1080))
            self.popup_img_label.configure(image=popup_img)
            self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.popup_frame.lift()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan popup!\n{e}")

    def hide_popup(self):
        self.popup_frame.place_forget()

    def open_payment(self, destination):
        self.current_destination = destination
        self.show_page('PaymentPage')
        self.label_nama_value.configure(text=self.current_fullname or "-")
        self.label_dest_value.configure(text=destination)
        self.jumlah_var.set("1")
        self.date_entry.set_date(date.today())
        self.payment_method_selected = False
        if hasattr(self, 'qris_popup_frame'):
            self.qris_popup_frame.place_forget()
        self.update_rincian_pembayaran()

    def open_blank_payment_page(self):
        self.show_page('PaymentPage')
        self.reset_payment_page()

    def open_profile_page(self):
        if hasattr(self, "profile_name_label"):
            self.profile_name_label.configure(text=f"@{self.current_fullname}" or "@-")
        self.show_page('ProfilePage')

    def format_rupiah(self, angka: int) -> str:
        return f"Rp {int(angka):,.0f}".replace(",", ".")

    # =================================================================================
    # 3. DATA & LOGIC METHODS
    # =================================================================================

    def hitung_total_setelah_diskon(self, dest, qty):
        harga = self.TICKET_PRICES.get(dest, 0)
        diskon = self.DISCOUNTS.get(dest, 0) if self.active_discounts.get(dest, False) else 0
        subtotal = harga * qty
        potongan = subtotal * diskon
        total = subtotal - potongan
        return harga, diskon, subtotal, potongan, total

    def update_rincian_pembayaran(self):
        dest = self.current_destination or "-"
        try:
            qty = int(self.jumlah_var.get()) if self.jumlah_var.get() else 0
        except ValueError:
            qty = 0
        
        harga, diskon, subtotal, potongan, total = self.hitung_total_setelah_diskon(dest, qty)
        teks = (f"Destinasi     : {dest}\n"
                f"Jumlah tiket  : {qty} tiket\n"
                f"Harga/tiket   : {self.format_rupiah(harga)}\n"
                f"Diskon        : {int(diskon * 100)}%\n"
                f"Subtotal      : {self.format_rupiah(subtotal)}\n"
                f"Potongan      : - {self.format_rupiah(potongan)}\n\n"
                f"Total bayar   : {self.format_rupiah(total)}")
        if hasattr(self, 'label_rincian'):
            self.label_rincian.configure(text=teks)

    def simpan_tiket_ke_history(self):
        if not self.current_fullname:
            messagebox.showerror("Error", "User belum login.")
            return
        if not self.current_destination:
            messagebox.showerror("Error", "Silakan pilih destinasi terlebih dahulu.")
            return
        if not self.payment_method_selected:
            messagebox.showinfo("Info", "Selesaikan pembayaran dahulu dengan memilih metode pembayaran.")
            return
        try:
            qty = int(self.jumlah_var.get())
            if qty < 1: raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Jumlah tiket harus berupa angka dan minimal 1.")
            return

        harga, _, _, _, total = self.hitung_total_setelah_diskon(self.current_destination, qty)
        with open(self.history_csv, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([self.current_fullname, self.current_destination, qty, self.date_entry.get(), harga, int(total)])
        
        if self.current_destination in self.active_discounts:
            self.active_discounts[self.current_destination] = False
        
        self.reset_payment_page()
        self.after(50, lambda: messagebox.showinfo("Berhasil", "History tiket bisa dicek di menu Profil!"))
        self.show_page('HomePage')

    def reset_payment_page(self):
        self.current_destination = ""
        if hasattr(self, 'label_dest_value'): self.label_dest_value.configure(text="-")
        if hasattr(self, 'jumlah_var'): self.jumlah_var.set("0")
        if hasattr(self, 'qris_popup_frame'): self.qris_popup_frame.place_forget()
        self.payment_method_selected = False
        self.update_rincian_pembayaran()

    def show_qris_on_panel(self):
        if hasattr(self, 'qris_popup_frame'):
            self.qris_popup_frame.place(x=1173, y=224)
            self.qris_popup_frame.lift()
            self.payment_method_selected = True

if __name__ == "__main__":
    app = TravelApp()
    app.mainloop()
