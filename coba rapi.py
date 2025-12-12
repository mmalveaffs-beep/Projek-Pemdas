# travel_app_oop.py
import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import csv
import os
from tkinter import messagebox
import webbrowser
import datetime
from datetime import date
from tkcalendar import DateEntry

ctk.set_appearance_mode("light")


class TravelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------- Window ----------
        self.geometry("1920x1080")
        self.title("Travel.Id")

        # ---------- Data ----------
        self.current_destination = ""
        self.current_fullname = ""

        self.TICKET_PRICES = {
            "Borobudur": 150000,
            "Tanah Lot": 200000,
            "Raja Ampat": 500000,
            "Candi Prambanan": 120000,
            "Gunung Rinjani": 250000,
        }

        self.DISCOUNTS = {
            "Borobudur": 0.10,        
            "Tanah Lot": 0.15,         
            "Raja Ampat": 0.10,       
            "Gunung Rinjani": 0.15,  
            "Candi Prambanan": 0.00   
        }

        #tombol disc di aktifkan
        self.active_discounts = {
            "Borobudur": False,
            "Tanah Lot": False,
            "Raja Ampat": False,
            "Gunung Rinjani": False,
            "Candi Prambanan": False
        }

        # ---------- Files ----------
        self.history_csv = "ticket_history.csv"
        self.csv_path = "user_reg.csv"
        
        if not os.path.isfile(self.history_csv):
            with open(self.history_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["nama", "destinasi", "jumlah_tiket",
                                 "tanggal", "harga_satuan", "total_bayar"])
        if not os.path.isfile(self.csv_path):
            with open(self.csv_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["firstname", "lastname", "email", "password"])

        # iki pake if else soale button back kepake di byk page
        back_img_path = "assets/icon/button back.png"
        if os.path.isfile(back_img_path):
            back_img = Image.open(back_img_path).resize((30, 30))
            self.icon_back = ctk.CTkImage(light_image=back_img, size=(30, 30))
        else:
            self.icon_back = None

        # ini buat qris
        qris_path = "assets/bg/qris.png"
        metode_path = "assets/button/qris 2.png"
        if os.path.isfile(qris_path):
            self.qris_code_img = ctk.CTkImage(Image.open(qris_path), size=(647, 535))
        else:
            self.qris_code_img = None
        if os.path.isfile(metode_path):
            self.metode_btn_img = ctk.CTkImage(Image.open(metode_path), size=(320, 57))
        else:
            self.metode_btn_img = None

        # semua page
        self.register_page()
        self.login_page()
        self.home_page()
        self.borobudur_page()
        self.tanah_page()
        self.raja_ampat_page()
        self.prambanan_page()
        self.rinjani_page()
        self.payment_page()

    # ---------------------------
    # Def penting
    # ---------------------------
    def format_rupiah(self, angka: int) -> str:
        return f"Rp {angka:,.0f}".replace(",", ".")

    def hitung_total_setelah_diskon(self, dest, qty):
        harga = self.TICKET_PRICES.get(dest, 0)
        # apply discount only if active_discounts[dest] is True
        diskon = self.DISCOUNTS.get(dest, 0) if self.active_discounts.get(dest, False) else 0
        subtotal = harga * qty
        potongan = subtotal * diskon
        total = subtotal - potongan
        return harga, diskon, subtotal, potongan, total

    def activate_discount(self, dest):
        if dest in self.active_discounts:
            self.active_discounts[dest] = True
            messagebox.showinfo("Diskon Aktif", f"Diskon untuk {dest} berhasil diaktifkan!")
        else:
            messagebox.showinfo("Info", "Destinasi tidak punya diskon.")

    # ---------------------------
    # Register
    # ---------------------------
    def register_page(self):
        # ============ PAGE REGISTER ============
        self.reg_frame = ctk.CTkFrame(self, width=1920, height=1080)
        self.reg_frame.grid(row=0, column=0, sticky="nsew")

        # background (as in original)
        reg_bg = ImageTk.PhotoImage(Image.open("assets/bg/register.png"))
        self._reg_bg_img = reg_bg  # keep reference
        gb = ctk.CTkLabel(self.reg_frame, image=reg_bg, text="")
        gb.place(x=0, y=0)

        # entries
        self.entry_firstname = ctk.CTkEntry(self.reg_frame, width=200, height=60, placeholder_text=" ",
                                           border_color="#F8EFEF", fg_color="#F8EFEF",
                                           font=("Arial", 20), text_color="Black", corner_radius=2)
        self.entry_firstname.place(x=1025, y=460.55)

        self.entry_lastname = ctk.CTkEntry(self.reg_frame, width=200, height=60, placeholder_text=" ",
                                          border_color="#F8EFEF", fg_color="#F8EFEF",
                                          font=("Arial", 20), text_color="Black", corner_radius=2)
        self.entry_lastname.place(x=1305, y=460.55)

        self.entry_email = ctk.CTkEntry(self.reg_frame, width=430, height=50, placeholder_text=" ",
                                        border_color="#D9D9D9", fg_color="#D9D9D9",
                                        font=("Helvetica", 20), text_color="Black", corner_radius=2)
        self.entry_email.place(x=1103, y=570)

        def update_email(*args):
            first = self.entry_firstname.get().strip().lower()
            last = self.entry_lastname.get().strip().lower()
            if first and last:
                email = f"{first}.{last}@gmail.com"
                self.entry_email.delete(0, "end")
                self.entry_email.insert(0, email)

        self.entry_firstname.bind("<KeyRelease>", update_email)
        self.entry_lastname.bind("<KeyRelease>", update_email)

        self.entry_password = ctk.CTkEntry(self.reg_frame, width=360, height=50, placeholder_text="",
                                           border_color="#D9D9D9", fg_color="#D9D9D9",
                                           font=("Helvetica", 20), text_color="Black", corner_radius=2)
        self.entry_password.place(x=1145, y=680)

        def save_data():
            first = self.entry_firstname.get().strip()
            last = self.entry_lastname.get().strip()
            email = self.entry_email.get().strip()
            password = self.entry_password.get().strip()
            with open(self.csv_path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([first, last, email, password])

        def open_login():
            self.login_frame.tkraise()

        def simpen_data():
            first = self.entry_firstname.get().strip()
            last = self.entry_lastname.get().strip()
            email = self.entry_email.get().strip()
            password = self.entry_password.get().strip()
            if not first or not last or not email or not password:
                messagebox.showwarning("Peringatan", "Semua kotak harus diisi!")
                return
            save_data()
            open_login()

        tombol_Register = ctk.CTkButton(self.reg_frame,
                                        width=555, 
                                        height=55, 
                                        text="Register ",
                                        fg_color="#D9D9D9", 
                                        border_color="#D9D9D9",
                                        hover_color="#E1C5C5",
                                        text_color="black",
                                        font=("Helvetica", 20, "bold"),
                                        corner_radius=3,
                                        command=simpen_data)
        tombol_Register.place(x=1010, y=790)

        login_button = ctk.CTkButton(master=self.reg_frame,
                                     width=60,
                                     height=30,
                                     text="Log in",
                                     font=("Helvetica", 15, "bold"),
                                     text_color="#61A8EB",
                                     fg_color="#F8EFEF",
                                     bg_color="#F8EFEF",
                                     border_width=0,
                                     corner_radius=14,
                                     command=open_login
                                     )
        login_button.place(x=1324, y=339)

    # ---------------------------
    # Login
    # ---------------------------
    def login_page(self):
        # ================ LOGIN PAGE ================
        self.login_frame = ctk.CTkFrame(self, width=1920, height=1080)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.login_frame.lower()

        login_bg = ImageTk.PhotoImage(Image.open("assets/bg/login.png"))
        self._login_bg_img = login_bg
        lgbg = ctk.CTkLabel(self.login_frame, image=login_bg, text="")
        lgbg.place(x=0, y=0)

        self.login_email = ctk.CTkEntry(self.login_frame, width=680, height=70, placeholder_text=" ",
                                        border_color="#D9D9D9", fg_color="#D9D9D9",
                                        font=("Helvetica", 25), text_color="Black", corner_radius=2)
        self.login_email.place(x=585, y=465)

        self.login_password = ctk.CTkEntry(self.login_frame, width=700, height=70, placeholder_text=" ",
                                           border_color="#D9D9D9", fg_color="#D9D9D9",
                                           font=("Helvetica", 25), text_color="Black", corner_radius=2)
        self.login_password.place(x=585, y=605)

        # back button 
        back_button = ctk.CTkButton(
            master=self.login_frame, width=10, height=10,
            image=self.icon_back,
            text="",
            fg_color="transparent",
            bg_color="#82ABC5",
            command=lambda: self.reg_frame.tkraise()
        )
        back_button.place(x=85, y=30)

        def cek_akun():
            input_email = self.login_email.get().strip()
            input_password = self.login_password.get().strip()
            if not input_email or not input_password:
                messagebox.showwarning("Peringatan", "Silakan isi email dan password!")
                return None
            with open(self.csv_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["email"].strip() == input_email and row["password"].strip() == input_password:
                        first = row["firstname"]
                        last = row["lastname"]
                        return first, last
            messagebox.showerror("Gagal", "Email atau password salah!")
            return None

        def msksemua():
            akun = cek_akun()
            if akun:
                first, last = akun
                self.set_username(first, last)
                self.masuk_homepage()

        tombol_login = ctk.CTkButton(master=self.login_frame, width=410,
                                     height=90, text="Log in",
                                     fg_color="#D9D9D9",
                                     border_color="#D9D9D9",
                                     text_color="black",
                                     font=("Helvetica", 20, "bold"),
                                     corner_radius=3,
                                     hover_color="#E1C5C5",
                                     command=msksemua)
        tombol_login.place(x=735, y=740)
        tombol_login.lift()

    def home_page(self):
        # =============== home page ==============
        self.home_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.home_frame.lower()

        bg_home_page = ImageTk.PhotoImage(Image.open("assets/bg/homepage kosong.png"))
        self._home_bg_img = bg_home_page
        home = ctk.CTkLabel(self.home_frame, image=bg_home_page, text="")
        home.place(x=0, y=0)

        # LABEL USERNAME DI HOME PAGE
        self.username_label = ctk.CTkLabel(
            self.home_frame,
            text="@ !",
            font=("Times", 40, "bold"),
            text_color="white",
            corner_radius=10,
            bg_color="#ece7d5",
        )
        self.username_label.place(x=310, y=60)

        # scroll area
        scroll_bar = ctk.CTkFrame(self.home_frame, width=1920, height=300)
        scroll_bar.place(x=30, y=350)

        canvas_scroll = Canvas(scroll_bar, width=1800, height=330, bg="#ece7d5", highlightthickness=0)
        canvas_scroll.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(scroll_bar, orient="horizontal", command=canvas_scroll.xview)
        scrollbar.pack(side="bottom", fill="x")
        canvas_scroll.configure(xscrollcommand=scrollbar.set)

        scroll_frame = Frame(canvas_scroll, bg="#ece7d5")
        canvas_scroll.create_window((0, 0), window=scroll_frame, anchor="nw")

        def update_scroll():
            canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

        scroll_frame.bind("<Configure>", lambda e: update_scroll())

        # cards / buttons (images kept same)
        boro_img = ctk.CTkImage(Image.open("assets/button 2/hp 1.png"), size=(416, 250))
        boro_btn = ctk.CTkButton(scroll_frame, image=boro_img, text="", fg_color="transparent",
                                 hover_color="#B09C7E", command=lambda: self.boro_frame.tkraise())
        boro_btn.grid(row=0, column=0, padx=20)

        lot_img = ctk.CTkImage(Image.open("assets/button 2/hp 2.png"), size=(416, 250))
        lot_btn = ctk.CTkButton(scroll_frame, image=lot_img, text="", fg_color="transparent",
                                hover_color="#B09C7E", command=lambda: self.tanah_frame.tkraise())
        lot_btn.grid(row=0, column=1, padx=20)

        rj_img = ctk.CTkImage(Image.open("assets/button 2/hp 3.png"), size=(416, 250))
        rj_btn = ctk.CTkButton(scroll_frame, image=rj_img, text="", fg_color="transparent",
                               hover_color="#B09C7E", command=lambda: self.rj_frame.tkraise())
        rj_btn.grid(row=0, column=2, padx=20)

        pra_img = ctk.CTkImage(Image.open("assets/button 2/hp 4.png"), size=(416, 250))
        pra_btn = ctk.CTkButton(scroll_frame, image=pra_img, text="", fg_color="transparent",
                                hover_color="#B09C7E", command=lambda: self.pram_frame.tkraise())
        pra_btn.grid(row=0, column=3, padx=20)

        rin_img = ctk.CTkImage(Image.open("assets/button 2/hp 5.png"), size=(416, 250))
        rin_btn = ctk.CTkButton(scroll_frame, image=rin_img, text="", fg_color="transparent",
                                hover_color="#B09C7E", command=lambda: self.rin_frame.tkraise())
        rin_btn.grid(row=0, column=4, padx=20)

        scroll_frame.update_idletasks()
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

        dis1 = ctk.CTkImage(Image.open("assets/button 2/disc1.png"), size=(450, 150))
        dis1_btn = ctk.CTkButton(
            self.home_frame,
            image=dis1,
            text="",
            fg_color="#ECE7D5",
            hover_color="#B09C7E",
            command=lambda: (self.activate_discount("Borobudur"),
                             self.show_discount_image("assets/bg/showdis1.png"))
        )
        dis1_btn.place(x=51, y=748)

        dis2 = ctk.CTkImage(Image.open("assets/button 2/disc2.png"), size=(450, 150))
        dis2_btn = ctk.CTkButton(
            self.home_frame,
            image=dis2,
            text="",
            fg_color="transparent",
            hover_color="#B09C7E",
            command=lambda: (self.activate_discount("Tanah Lot"),
                             self.show_discount_image("assets/bg/showdis2.png"))
        )
        dis2_btn.place(x=530, y=748)

        dis3 = ctk.CTkImage(Image.open("assets/button 2/disc3.png"), size=(450, 150))
        dis3_btn = ctk.CTkButton(
            self.home_frame,
            image=dis3,
            text="",
            fg_color="#ECE7D5",
            hover_color="#B09C7E",
            command=lambda: (self.activate_discount("Raja Ampat"),
                             self.show_discount_image("assets/bg/showdis3.png"))
        )
        dis3_btn.place(x=1010, y=748)

        dis4 = ctk.CTkImage(Image.open("assets/button 2/disc4.png"), size=(450, 150))
        dis4_btn = ctk.CTkButton(
            self.home_frame,
            image=dis4,
            text="",
            fg_color="transparent",
            hover_color="#B09C7E",
            command=lambda: (self.activate_discount("Gunung Rinjani"),
                             self.show_discount_image("assets/bg/showdis4.png"))
        )
        dis4_btn.place(x=1490, y=748)

    def show_discount_image(self, img_path):
        try:
            popup_img = ctk.CTkImage(Image.open(img_path), size=(1920, 1080))
            self._popup_img = popup_img
            self.popup_img_label.configure(image=popup_img, text="")
            self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.popup_frame.lift()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan popup!\n{e}")

    def borobudur_page(self):
        self.boro_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.boro_frame.grid(row=0, column=0, sticky="nsew")
        self.boro_frame.lower()

        boro_bg = ImageTk.PhotoImage(Image.open("assets/bg/borobudur.png"))
        self._boro_bg_img = boro_bg
        boro = ctk.CTkLabel(self.boro_frame, image=boro_bg, text="")
        boro.place(x=0, y=0)

        back_btn = ctk.CTkButton(self.boro_frame, width=10, height=10,
                                 image=self.icon_back, text="",
                                 fg_color="#C7B184", bg_color="#C7B184",
                                 hover_color="#707C93",
                                 command=lambda: self.home_frame.tkraise())
        back_btn.place(x=80, y=30)

        brloc = Image.open("assets/button/loc boro.png").resize((500, 70), Image.LANCZOS)
        brloc2 = ctk.CTkImage(light_image=brloc, size=(480, 70))
        boro_loc = ctk.CTkButton(self.boro_frame, image=brloc2, text="", fg_color="#D9D9D9",
                                 hover_color="#D9D9D9", command=lambda: webbrowser.open(
                "https://maps.app.goo.gl/8aWVX5Q1JHBGE2j66"))
        boro_loc.place(x=85, y=915)

        brtic = Image.open("assets/button/tic boro.png").resize((520, 100), Image.LANCZOS)
        brtic2 = ctk.CTkImage(light_image=brtic, size=(475, 95))
        boro_tic = ctk.CTkButton(self.boro_frame, image=brtic2, text="", fg_color="#D9D9D9",
                                 hover_color="#D9D9D9", command=lambda: self.open_payment("Borobudur"))
        boro_tic.place(x=1325, y=895)

    def tanah_page(self):
        self.tanah_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.tanah_frame.grid(row=0, column=0, sticky="nsew")
        self.tanah_frame.lower()

        tn_bg = ImageTk.PhotoImage(Image.open("assets/bg/tanah lot.png"))
        self._tn_bg_img = tn_bg
        tnh = ctk.CTkLabel(self.tanah_frame, image=tn_bg, text="")
        tnh.place(x=0, y=0)

        back_btn = ctk.CTkButton(self.tanah_frame, width=10, height=10,
                                 image=self.icon_back, text="",
                                 fg_color="#CD5B45", bg_color="#CD5B45",
                                 hover_color="#CD5B45", command=lambda: self.home_frame.tkraise())
        back_btn.place(x=80, y=30)

        tnloc = Image.open("assets/button/loc tanah.png").resize((500, 70), Image.LANCZOS)
        tnloc2 = ctk.CTkImage(light_image=tnloc, size=(480, 70))
        tanah_loc = ctk.CTkButton(self.tanah_frame, image=tnloc2, text="", fg_color="#D78080",
                                  hover_color="#D78080", command=lambda: webbrowser.open(
                "https://maps.app.goo.gl/GVS7gxeoTfBkfpkH6"))
        tanah_loc.place(x=95, y=915)

        tntic = Image.open("assets/button/tic tanah.png").resize((500, 90), Image.LANCZOS)
        tntic2 = ctk.CTkImage(light_image=tntic, size=(500, 90))
        tanah_tic = ctk.CTkButton(self.tanah_frame, image=tntic2, text="", fg_color="#D78080",
                                  hover_color="#D78080", command=lambda: self.open_payment("Tanah Lot"))
        tanah_tic.place(x=1325, y=900)

    def raja_ampat_page(self):
        self.rj_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.rj_frame.grid(row=0, column=0, sticky="nsew")
        self.rj_frame.lower()

        rj_bg = ImageTk.PhotoImage(Image.open("assets/bg/raja ampat.png"))
        self._rj_bg_img = rj_bg
        rj = ctk.CTkLabel(self.rj_frame, image=rj_bg, text="")
        rj.place(x=0, y=0)

        back_btn = ctk.CTkButton(self.rj_frame, width=10, height=10,
                                 image=self.icon_back, text="", fg_color="#93A3AE",
                                 bg_color="#93A3AE", hover_color="#93A3AE",
                                 command=lambda: self.home_frame.tkraise())
        back_btn.place(x=80, y=30)

        rjloc = Image.open("assets/button/loc raja.png").resize((500, 70), Image.LANCZOS)
        rjloc2 = ctk.CTkImage(light_image=rjloc, size=(480, 70))
        rj_loc = ctk.CTkButton(self.rj_frame, image=rjloc2, text="", fg_color="#80BFD7",
                              hover_color="#80BFD7", command=lambda: webbrowser.open(
                "https://maps.app.goo.gl/6fzWy5szm5F2RMzP7"))
        rj_loc.place(x=80, y=930)

        rjtic = Image.open("assets/button/tic raja.png").resize((450, 100), Image.LANCZOS)
        rjtic2 = ctk.CTkImage(light_image=rjtic, size=(450, 100))
        raja_tic = ctk.CTkButton(self.rj_frame, image=rjtic2, text="", fg_color="#80BFD7",
                                hover_color="#80BFD7", command=lambda: self.open_payment("Raja Ampat"))
        raja_tic.place(x=1335, y=900)

    def prambanan_page(self):
        self.pram_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.pram_frame.grid(row=0, column=0, sticky="nsew")
        self.pram_frame.lower()

        pr_bg = ImageTk.PhotoImage(Image.open("assets/bg/prambanan.png"))
        self._pr_bg_img = pr_bg
        pr = ctk.CTkLabel(self.pram_frame, image=pr_bg, text="")
        pr.place(x=0, y=0)

        back_btn = ctk.CTkButton(self.pram_frame, width=10, height=10,
                                 image=self.icon_back, text="", fg_color="#657187", bg_color="#657187",
                                 hover_color="#657187", command=lambda: self.home_frame.tkraise())
        back_btn.place(x=80, y=30)

        prloc = Image.open("assets/button/loc pra.png").resize((500, 70), Image.LANCZOS)
        prloc2 = ctk.CTkImage(light_image=prloc, size=(480, 70))
        pr_loc = ctk.CTkButton(self.pram_frame, image=prloc2, text="", fg_color="#7B411D",
                              hover_color="#7B411D", command=lambda: webbrowser.open(
                "https://maps.app.goo.gl/ofnm6XTfUFdYSR1o7"))
        pr_loc.place(x=80, y=909)

        prtic = Image.open("assets/button/tic pra.png").resize((500, 90), Image.LANCZOS)
        prtic2 = ctk.CTkImage(light_image=prtic, size=(500, 90))
        pr_tic = ctk.CTkButton(self.pram_frame, image=prtic2, text="", fg_color="#7B411D",
                              hover_color="#7B411D", command=lambda: self.open_payment("Candi Prambanan"))
        pr_tic.place(x=1350, y=900)

    def rinjani_page(self):
        self.rin_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.rin_frame.grid(row=0, column=0, sticky="nsew")
        self.rin_frame.lower()

        rin_bg = ImageTk.PhotoImage(Image.open("assets/bg/mt rinjani.png"))
        self._rin_bg_img = rin_bg
        rin = ctk.CTkLabel(self.rin_frame, image=rin_bg, text="")
        rin.place(x=0, y=0)

        back_btn = ctk.CTkButton(self.rin_frame, width=10, height=10,
                                 image=self.icon_back, text="", fg_color="#BF7DA9", bg_color="#BF7DA9",
                                 hover_color="#BF7DA9", command=lambda: self.home_frame.tkraise())
        back_btn.place(x=80, y=30)

        rinloc = Image.open("assets/button/loc rin.png").resize((500, 70), Image.LANCZOS)
        rinloc2 = ctk.CTkImage(light_image=rinloc, size=(480, 70))
        rin_loc = ctk.CTkButton(self.rin_frame, image=rinloc2, text="", fg_color="#EA4DDA",
                               hover_color="#EA4DDA", command=lambda: webbrowser.open(
                "https://maps.app.goo.gl/nrCCfDuuYdj28dxW9"))
        rin_loc.place(x=90, y=909)

        rintic = Image.open("assets/button/tic rin.png").resize((470, 90), Image.LANCZOS)
        rintic2 = ctk.CTkImage(light_image=rintic, size=(470, 90))
        rin_tic = ctk.CTkButton(self.rin_frame, image=rintic2, text="", fg_color="#EA4DDA",
                                hover_color="#EA4DDA", command=lambda: self.open_payment("Gunung Rinjani"))
        rin_tic.place(x=1325, y=890)

    def popup_components(self):
        self.popup_frame = ctk.CTkFrame(self, width=900, height=200, fg_color="#050505")
        # ttp sembunyi sampe di klik
        self.popup_frame.place_forget()
        self.popup_img_label = ctk.CTkLabel(self.popup_frame, text="")
        self.popup_img_label.pack()
        close_btn = ctk.CTkButton(self.popup_frame, text="✕", width=40, height=40,
                                 fg_color="#050505", hover_color="#050505", corner_radius=20,
                                 command=lambda: self.popup_frame.place_forget())
        close_btn.place(relx=0.95, rely=0.05, anchor="center")

    def payment_page(self):
        self.popup_components()

        self.pay_frame = ctk.CTkFrame(master=self, width=1920, height=1080)
        self.pay_frame.grid(row=0, column=0, sticky="nsew")
        self.pay_frame.lower()

        bg_pay = ImageTk.PhotoImage(Image.open("assets/bg/payment kosong.png"))
        self._pay_bg_img = bg_pay
        pay = ctk.CTkLabel(self.pay_frame, image=bg_pay, text="")
        pay.place(x=0, y=0)

        # QRIS panel (kanan yang kosong sblm di klik)
        qris_label = ctk.CTkLabel(master=self.pay_frame, text="",
                                  width=687, height=559, fg_color="transparent", bg_color="#D9D9D9")
        qris_label.place(x=1151, y=250)
        self.qris_label = qris_label

        # button metode pembayaran
        self.btn_metode = ctk.CTkButton(self.pay_frame,
                                        image=self.metode_btn_img,
                                        text="",
                                        width=320, height=57,
                                        fg_color="#D78080",
                                        bg_color="#D78080",
                                        hover_color="#D78080",
                                        command=self.show_qris_on_panel)
        self.btn_metode.place(x=700, y=750)

        # Label di payment
        self.label_nama_value = ctk.CTkLabel(self.pay_frame, text="", font=("Helvetica", 24, "bold"),
                                             text_color="black", bg_color="#FFFFFF")
        self.label_nama_value.place(x=360, y=250)

        self.label_dest_value = ctk.CTkLabel(self.pay_frame, text="", font=("Helvetica", 24, "bold"),
                                             text_color="black", bg_color="#FFFFFF")
        self.label_dest_value.place(x=360, y=330)

        # jumlah tiket default "1"
        self.jumlah_var = StringVar(value="1")
        self.entry_jumlah_pay = ctk.CTkEntry(self.pay_frame, width=400, height=40,
                                             font=("Helvetica", 24), fg_color="white",
                                             border_color="#FFFFFF", text_color="black",
                                             textvariable=self.jumlah_var)
        self.entry_jumlah_pay.place(x=360, y=410)

        # date entry 
        self.date_entry = DateEntry(self.pay_frame, width=10, height=60, background="#385FAA",
                                   foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd",
                                   font=('ITC Avant Garde Gothic', 25, 'bold'), mindate=date.today())
        self.date_entry.place(x=360, y=473)
        self.date_entry.set_date(date.today())

        # rincian label
        self.label_rincian = ctk.CTkLabel(master=self.pay_frame, text="", width=535, height=218,
                                          font=("ITC Avant Garde Gothic", 25), text_color="black",
                                          fg_color="#FFFFFF", corner_radius=10, justify=LEFT, anchor="nw")
        self.label_rincian.place(x=68, y=705)

        # bind changes
        self.jumlah_var.trace_add("write", lambda *a: self.update_rincian_pembayaran())

        # cek / save button (save ke history.csv)
        cek_btn = ctk.CTkButton(self.pay_frame, text="Cek", width=165, height=81,
                                font=("Helvetica", 28, "bold"), fg_color="#E78989",
                                hover_color="#D46F6F", text_color="black", corner_radius=20,
                                command=self.simpan_tiket_ke_history)
        cek_btn.place(x=1418, y=835)

    # -------------
    # Payment helpers
    # -------------
    def show_qris_on_panel(self):
        if self.qris_code_img:
            self.qris_label.configure(image=self.qris_code_img)
            self.qris_label.image = self.qris_code_img

    def open_payment(self, destination):
        """Called from destination pages when user presses ticket button."""
        self.current_destination = destination
        # show payment page
        self.pay_frame.tkraise()

        # update nama/destination fields
        self.label_nama_value.configure(text=self.current_fullname or "-")
        self.label_dest_value.configure(text=destination)

        # default jumlah & tanggal
        self.jumlah_var.set("1")
        self.date_entry.set_date(date.today())
        # update rincian immediately
        self.update_rincian_pembayaran()

    def update_rincian_pembayaran(self):
        dest = self.current_destination or "-"
        try:
            qty = int(self.jumlah_var.get())
            if qty < 1:
                qty = 0
        except ValueError:
            qty = 0
            self.jumlah_var.set("0")

        harga, diskon, subtotal, potongan, total = self.hitung_total_setelah_diskon(dest, qty)
        diskon_persen = int(diskon * 100)

        teks = (
            f"Destinasi     : {dest}\n"
            f"Jumlah tiket  : {qty} tiket\n"
            f"Harga/tiket   : {self.format_rupiah(harga)}\n"
            f"Diskon        : {diskon_persen}%\n"
            f"Subtotal      : {self.format_rupiah(subtotal)}\n"
            f"Potongan      : - {self.format_rupiah(potongan)}\n"
            "\n"
            f"Total bayar   : {self.format_rupiah(total)}"
        )
        self.label_rincian.configure(text=teks)

    def simpan_tiket_ke_history(self):
        nama = self.current_fullname or "-"
        dest = self.current_destination or "-"
        tgl = self.date_entry.get().strip()
        try:
            qty = int(self.jumlah_var.get())
            if qty < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Jumlah tiket harus berupa angka dan minimal 1.")
            return

        harga, diskon, subtotal, potongan, total = self.hitung_total_setelah_diskon(dest, qty)

        with open(self.history_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nama, dest, qty, tgl, harga, total])

        messagebox.showinfo("Berhasil", "Tiket berhasil disimpan ke history!")
        if dest in self.active_discounts:
            self.active_discounts[dest] = False
        self.home_frame.tkraise()

    # -------------
    # Utility: set username & show home
    # -------------
    def set_username(self, first, last):
        self.current_fullname = f"{first} {last}"
        self.username_label.configure(text=f"@ {first} {last}!")

    def masuk_homepage(self):
        self.home_frame.tkraise()


if __name__ == "__main__":
    app = TravelApp()
    app.mainloop()
