import customtkinter as ctk
from tkinter import Canvas, Scrollbar, Frame
from PIL import Image

class HomePage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # --- Latar Belakang ---
        bg_home_page = self.controller.load_image("assets/bg/homepage kosong.png", (1920, 1080))
        home = ctk.CTkLabel(self, image=bg_home_page, text="")
        home.place(x=0, y=0)

        # --- Label Username ---
        self.username_label = ctk.CTkLabel(
            self,
            text="@ !",
            font=("Times", 40, "bold"),
            text_color="black",
            corner_radius=10,
            bg_color="#FFFFFF"
        )
        self.username_label.place(x=310, y=60)
        # Simpan referensi agar controller bisa mengubahnya
        self.controller.username_label = self.username_label

        # --- Tombol Lonceng (Donasi) ---
        # Memuat ikon dan membuat tombol yang mengarah ke halaman Donasi
        lonceng_img = self.controller.load_icon("assets/icon/lonceng.png", (70, 70))
        ctk.CTkButton(self, width=10, height=10, image=lonceng_img, text="", fg_color="#D9D9D9",
                      hover_color="#A79A9A", bg_color="#D9D9D9", command=lambda: self.controller.show_page('DonasiPage')).place(x=1776, y=43)

        # --- Area Scroll Destinasi ---
        self._create_destination_scroll()

        # --- Tombol Diskon ---
        self._create_discount_buttons()

        # --- Tombol Navigasi Bawah ---
        self.controller._create_navigation_buttons(self, active_page="home")

    def _create_destination_scroll(self):
        #membuat area scroll untuk destinasi
        scroll_bar = ctk.CTkFrame(self, width=1920, height=300, fg_color="#ece7d5")
        scroll_bar.place(x=30, y=350)

        canvas_scroll = Canvas(scroll_bar, width=1800, height=330, bg="#ece7d5", highlightthickness=0)
        canvas_scroll.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(scroll_bar, orient="horizontal", command=canvas_scroll.xview)
        scrollbar.pack(side="bottom", fill="x")
        canvas_scroll.configure(xscrollcommand=scrollbar.set)

        scroll_frame = Frame(canvas_scroll, bg="#ece7d5")
        canvas_scroll.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Data untuk kartu destinasi
        destination_cards = [
            {"name": "Borobudur", "img": "assets/button 2/hp 1.png"},
            {"name": "Tanah Lot", "img": "assets/button 2/hp 2.png"},
            {"name": "Raja Ampat", "img": "assets/button 2/hp 3.png"},
            {"name": "Candi Prambanan", "img": "assets/button 2/hp 4.png"},
            {"name": "Gunung Rinjani", "img": "assets/button 2/hp 5.png"},
        ]

        for i, card_data in enumerate(destination_cards):
            img = self.controller.load_icon(card_data["img"], (416, 250))
            btn = ctk.CTkButton(
                scroll_frame, image=img, text="", fg_color="transparent",
                hover_color="#B09C7E",
                command=lambda dest=card_data["name"]: self.controller.show_destination_page(dest)
            )
            btn.grid(row=0, column=i, padx=20)

        scroll_frame.update_idletasks()
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

    def _create_discount_buttons(self):
        """Membuat tombol-tombol diskon."""
        discount_buttons_data = [
            {"dest": "Borobudur", "img": "assets/button 2/disc1.png", "popup": "assets/bg/showdis1.png", "x": 25, "fg": "transparent"},
            {"dest": "Tanah Lot", "img": "assets/button 2/disc2.png", "popup": "assets/bg/showdis2.png", "x": 505, "fg": "transparent"},
            {"dest": "Raja Ampat", "img": "assets/button 2/disc3.png", "popup": "assets/bg/showdis3.png", "x": 985, "fg": "transparent"},
            {"dest": "Gunung Rinjani", "img": "assets/button 2/disc4.png", "popup": "assets/bg/showdis5.png", "x": 1465, "fg": "transparent"}
        ]

        for data in discount_buttons_data:
            img = self.controller.load_icon(data["img"], (450, 150))
            btn = ctk.CTkButton(
                self, image=img, text="", fg_color=data["fg"], hover_color="#B09C7E",
                command=lambda d=data["dest"], p=data["popup"]: (
                    self.controller.activate_discount(d),
                    self.controller.show_discount_image(p)
                )
            )
            btn.place(x=data["x"], y=748)

        
