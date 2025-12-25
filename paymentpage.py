import customtkinter as ctk
from tkinter import StringVar
from tkcalendar import DateEntry
from datetime import date

class PaymentPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # --- Latar Belakang ---
        bg_pay = self.controller.load_image("assets/bg/payment kosong.png", (1920, 1080))
        ctk.CTkLabel(self, image=bg_pay, text="").place(x=0, y=0)
        self.bg_pay_ref = bg_pay # Simpan referensi

        # --- Pop-up QRIS ---
        # Frame ini dibuat di sini, tapi akan di-manage oleh controller
        self.qris_popup_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(self.qris_popup_frame, text="", image=self.controller.qris_code_img).pack()
        self.qris_popup_frame.place_forget()
        # Beri referensi ke controller agar bisa diakses dari luar
        self.controller.qris_popup_frame = self.qris_popup_frame

        # --- Tombol Metode Pembayaran ---
        ctk.CTkButton(self, image=self.controller.metode_btn_img, text="", width=300, height=50, 
                      fg_color="#D78080", bg_color="#D78080", hover_color="#D78080", 
                      command=self.controller.show_qris_on_panel).place(x=700, y=745)

        # --- Label & Entry ---
        # Widget-widget ini dibuat di sini, tapi nilainya akan diubah oleh controller
        self.label_nama_value = ctk.CTkLabel(self, text="", font=("Helvetica", 24, "bold"), text_color="black", bg_color="#FFFFFF")
        self.label_nama_value.place(x=360, y=250)
        self.controller.label_nama_value = self.label_nama_value

        self.label_dest_value = ctk.CTkLabel(self, text="", font=("Helvetica", 24, "bold"), text_color="black", bg_color="#FFFFFF")
        self.label_dest_value.place(x=360, y=330)
        self.controller.label_dest_value = self.label_dest_value

        self.jumlah_var = StringVar(value="1")
        self.entry_jumlah_pay = ctk.CTkEntry(self, width=400, height=40, font=("Helvetica", 24), fg_color="white", border_color="#FFFFFF", text_color="black", textvariable=self.jumlah_var)
        self.entry_jumlah_pay.place(x=360, y=410)
        self.controller.jumlah_var = self.jumlah_var

        self.date_entry = DateEntry(self, width=10, height=60, background="#385FAA", foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd", font=('ITC Avant Garde Gothic', 25, 'bold'), mindate=date.today())
        self.date_entry.place(x=360, y=473)
        self.date_entry.set_date(date.today())
        self.controller.date_entry = self.date_entry

        # --- Rincian Pembayaran ---
        self.label_rincian = ctk.CTkLabel(self, text="", width=535, height=200, font=("ITC Avant Garde Gothic", 20), text_color="black", fg_color="#FFFFFF", corner_radius=30, justify="left", anchor="nw")
        self.label_rincian.place(x=68, y=705)
        self.controller.label_rincian = self.label_rincian

        # --- Bind & Tombol ---
        # Setiap kali jumlah tiket diubah, panggil fungsi update di controller
        self.jumlah_var.trace_add("write", lambda *a: self.controller.update_rincian_pembayaran())
        
        ctk.CTkButton(self, text="Cek", width=165, height=81, font=("Helvetica", 28, "bold"), 
                      fg_color="#E78989", hover_color="#D46F6F", text_color="black", corner_radius=20, 
                      command=self.controller.simpan_tiket_ke_history).place(x=1418, y=835)

        # --- Tombol Navigasi Bawah ---
        self.controller._create_navigation_buttons(self, active_page="pay")
