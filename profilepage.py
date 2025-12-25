import customtkinter as ctk
import csv
import os

class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # --- Latar Belakang & Widget Utama ---
        bg_profile_page = self.controller.load_image("assets/bg/Profile page.png", (1920, 1080))
        ctk.CTkLabel(self, image=bg_profile_page, text="").place(x=0, y=0)
        self.bg_profile_page_ref = bg_profile_page

        self.profile_name_label = ctk.CTkLabel(self, text="", font=("Helvetica", 28, "bold"), text_color="black", bg_color="#FFFFFF", anchor="w")
        self.profile_name_label.place(x=250, y=404)
        # Beri referensi ke controller agar bisa diupdate dari luar
        self.controller.profile_name_label = self.profile_name_label

        logout_icon = self.controller.load_icon("assets/icon/logout.png", (76, 76))
        ctk.CTkButton(self, image=logout_icon, text="", fg_color="#D9D9D9", hover_color="#657187", command=lambda: self.controller.show_page('RegisterPage')).place(x=1800, y=16)

        # --- Tombol-tombol Menu Profil ---
        self._create_menu_buttons()

        # --- Frame Pop-up ---
        self._create_popups()

        # --- Tombol Navigasi Bawah ---
        self.controller._create_navigation_buttons(self, active_page="profile")

    def _create_menu_buttons(self):
        #tombol menu profile
        profinfo_img = self.controller.load_icon("assets/button 2/person info.png", (1750, 78))
        ctk.CTkButton(self, text="", image=profinfo_img, width=1800, height=90, fg_color="#D9D9D9", hover_color="#BAB0B0", command=self.show_person).place(x=60, y=535)
        
        payinfo_img = self.controller.load_icon("assets/button 2/pay info.png", (1750, 78))
        ctk.CTkButton(self, text="", image=payinfo_img, width=1800, height=90, fg_color="#D9D9D9", hover_color="#BAB0B0", command=self.show_payment_history).place(x=57, y=648)

        about_img = self.controller.load_icon("assets/button 2/about info.png", (1750, 78))
        ctk.CTkButton(self, text="", image=about_img, width=1800, height=90, fg_color="#D9D9D9", hover_color="#BAB0B0", command=self.show_kelompok_info).place(x=57, y=760)

    def _create_popups(self):
        # Pop-up Personal Info
        self.profile_info_frame = ctk.CTkFrame(self, width=1200, height=400, fg_color="#FFFFFF", corner_radius=10)
        self.personal_info_list = ctk.CTkFrame(self.profile_info_frame, fg_color="transparent")
        self.personal_info_list.pack(fill="both", expand=True, padx=30, pady=30)
        ctk.CTkButton(self.profile_info_frame, text="✕", width=40, height=40, fg_color="#867B7B", hover_color="#534949", corner_radius=20, command=lambda: self.profile_info_frame.place_forget()).place(relx=0.95, rely=0.07, anchor="center")
        
        # Pop-up Payment History
        self.payhistory_frame = ctk.CTkFrame(self, width=1200, height=360, fg_color="#FFFFFF", corner_radius=10)
        self.history_list = ctk.CTkScrollableFrame(self.payhistory_frame, width=1150, height=300, fg_color="#F5F5F5")
        self.history_list.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        ctk.CTkButton(self.payhistory_frame, text="✕", width=40, height=40, fg_color="#867B7B", hover_color="#534949", corner_radius=20, command=lambda: self.payhistory_frame.place_forget()).place(relx=0.95, rely=0.07, anchor="center")

        # Pop-up Info Kelompok
        self.kelompok_info_frame = ctk.CTkFrame(self, width=800, height=450, fg_color="white", corner_radius=15, border_width=2, border_color="#D9D9D9")
        ctk.CTkLabel(self.kelompok_info_frame, text="Informasi Anggota Kelompok", font=("Helvetica", 24, "bold"), text_color="black").pack(pady=(20, 10))
        self.kelompok_list = ctk.CTkScrollableFrame(self.kelompok_info_frame, width=1150, height=300, fg_color="#F5F5F5")
        self.kelompok_list.pack(padx=20, pady=10)
        ctk.CTkButton(self.kelompok_info_frame, text="Tutup", width=150, fg_color="#E74C3C", hover_color="#C0392B", command=lambda: self.kelompok_info_frame.place_forget()).pack(pady=10)
        self.setup_kelompok_info()

    # untuk menampilkan dan menyembunyikan pop-up
    def hide_profile_panels(self):
        self.profile_info_frame.place_forget()
        self.payhistory_frame.place_forget()
        self.kelompok_info_frame.place_forget()

    def show_person(self):
        self.hide_profile_panels()
        self.load_person_info()
        self.profile_info_frame.place(x=650, y=395)
        self.profile_info_frame.lift()

    def show_payment_history(self):
        self.hide_profile_panels()
        self.load_ticket_history()
        self.payhistory_frame.place(x=360, y=490)
        self.payhistory_frame.lift()

    def show_kelompok_info(self):
        self.hide_profile_panels()
        self.kelompok_info_frame.place(x=360, y=490)
        self.kelompok_info_frame.lift()

    # def berisi pengambilan data dari csv dan menampilkannya pada pop-up
    def load_person_info(self):
        for widget in self.personal_info_list.winfo_children(): widget.destroy()
        try:
            with open(self.controller.csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fullname = f"{row['firstname']} {row['lastname']}"
                    if fullname == self.controller.current_fullname:
                        ctk.CTkLabel(self.personal_info_list, text=f"Nama Lengkap : {fullname}", font=("Helvetica", 28, "bold"), anchor="w").pack(fill="x", pady=(0, 15))
                        ctk.CTkLabel(self.personal_info_list, text=f"Email : {row['email']}", font=("Helvetica", 22), anchor="w").pack(fill="x")
                        return
            ctk.CTkLabel(self.personal_info_list, text="Data user tidak ditemukan.", font=("Helvetica", 18), text_color="gray").pack(pady=20)
        except FileNotFoundError:
            ctk.CTkLabel(self.personal_info_list, text="File user tidak ditemukan.", font=("Helvetica", 18), text_color="gray").pack(pady=20)

    def load_ticket_history(self):
        for widget in self.history_list.winfo_children(): widget.destroy()
        try:
            with open(self.controller.history_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                found = False
                for row in reader:
                    if self.controller.current_fullname.strip() == row["nama"].strip():
                        found = True
                        item = ctk.CTkFrame(self.history_list, fg_color="white", corner_radius=8)
                        item.pack(fill="x", padx=10, pady=6)
                        text = (f"Destinasi : {row['destinasi']}\n"
                                f"Tanggal   : {row['tanggal']}\n"
                                f"Jumlah    : {row['jumlah_tiket']} tiket\n"
                                f"Total     : {self.controller.format_rupiah(int(float(row['total_bayar'])))}")
                        ctk.CTkLabel(item, text=text, font=("Helvetica", 16), text_color="black", justify="left", anchor="w").pack(anchor="w", padx=15, pady=10)
                if not found:
                    ctk.CTkLabel(self.history_list, text="Belum ada transaksi.", font=("Helvetica", 18), text_color="gray").pack(pady=20)
        except FileNotFoundError:
            ctk.CTkLabel(self.history_list, text="File riwayat tidak ditemukan.", font=("Helvetica", 18), text_color="gray").pack(pady=20)

    def setup_kelompok_info(self):
        for widget in self.kelompok_list.winfo_children(): widget.destroy()
        info_text = ("Anggota Kelompok: 10\n\n"
                     "1. Nama Lengkap : Yuan Fasich Tansatrisna\n   NIM          : 25031554155\n\n"
                     "2. Nama Lengkap : Wiliyan Surya\n   NIM          : 25031554168\n\n"
                     "3. Nama Lengkap : Dinda Alifia Eka Nirmala\n   NIM          : 25031554257\n\n")
        ctk.CTkLabel(self.kelompok_list, text=info_text, justify="left", anchor="w", font=("Helvetica", 16), text_color="black").pack(padx=20, pady=10)
