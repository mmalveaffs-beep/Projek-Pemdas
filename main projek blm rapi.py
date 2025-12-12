import customtkinter as ctk
from tkinter import *
from PIL import Image ,ImageTk
import csv
import os
from tkinter import messagebox
import webbrowser
import datetime
from datetime import date 
from tkcalendar import Calendar
from tkcalendar import DateEntry


ctk.set_appearance_mode("light")

window = ctk.CTk()
window.geometry("1920x1080")
window.title('Travel.Id')

current_destination = ""

# harga tiket per destinasi (silakan ganti angka sesuai kebutuhanmu)
TICKET_PRICES = {
    "Borobudur": 150000,
    "Tanah Lot": 200000,
    "Raja Ampat": 500000,
    "Candi Prambanan": 120000,
    "Gunung Rinjani": 250000,
}

DISCOUNTS = {
    "Borobudur": 0.10,        # 10%
    "Tanah Lot": 0.15,        # 15%
    "Raja Ampat": 0.10,       # 10%
    "Gunung Rinjani": 0.15,   # 15%
    "Candi Prambanan": 0.00   # tidak ada diskon
}


history_csv = "ticket_history.csv"

# bikin file history kalau belum ada
if not os.path.isfile(history_csv):
    with open(history_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nama", "destinasi", "jumlah_tiket",
                         "tanggal", "harga_satuan", "total_bayar"])

csv_path = "user_reg.csv"

if not os.path.isfile(csv_path):
    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["firstname", "lastname", "email", "password"])

 # ============ PAGE REGISTER ============

reg_page = ctk.CTkFrame(window, width=1920, height=1080)
reg_page.grid(row=0, column=0, sticky='nsew')

reg_bg = ImageTk.PhotoImage(Image.open("assets/bg/register.png")) 
gb = ctk.CTkLabel(reg_page, image=reg_bg, text='')
gb.place(x=0, y=0)

# ============= Entry Register =================
entry_firstname = ctk.CTkEntry(reg_page, width=200, height=60, placeholder_text=" ",
                         border_color="#F8EFEF", fg_color="#F8EFEF",
                         font=("Arial",20), text_color="Black", corner_radius=2)
entry_firstname.place(x=1025, y=460.55)

entry_lastname = ctk.CTkEntry(reg_page, width=200, height=60, placeholder_text=" ",
                         border_color="#F8EFEF", fg_color="#F8EFEF",
                         font=("Arial",20), text_color="Black", corner_radius=2)
entry_lastname.place(x=1305, y=460.55)

entry_email = ctk.CTkEntry(reg_page, width=430, height=50, placeholder_text=" ",
                         border_color="#D9D9D9", fg_color="#D9D9D9",
                         font=("Helvetica",20), text_color="Black", corner_radius=2)
entry_email.place(x=1103, y=570)

def update_email(*args):
    first = entry_firstname.get().strip().lower()
    last = entry_lastname.get().strip().lower()
    
    if first and last:
        email = f"{first}.{last}@gmail.com"
        entry_email.delete(0, 'end')
        entry_email.insert(0, email)

entry_firstname.bind("<KeyRelease>", update_email)
entry_lastname.bind("<KeyRelease>", update_email)

entry_password = ctk.CTkEntry(reg_page, width=360, height=50, placeholder_text="",
                         border_color="#D9D9D9", fg_color="#D9D9D9",
                         font=("Helvetica",20), text_color="Black", corner_radius=2)
entry_password.place(x=1145, y=680)

# # ========== Simpan data ke CSV ==========
def save_data():
    first = entry_firstname.get().strip()
    last = entry_lastname.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    with open(csv_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([first, last, email, password])

# ========== Pindah ke Login Page ==========
def open_login():
    login_page.tkraise()

# =========== Pindah ke gregistrasi page ==========
def open_reg():
    reg_page.grid()

# =================== Pindah ke home page ===========
def open_home():
    home_page.grid()

# ========== VALIDASI INPUT ==========
def simpen_data():
    first = entry_firstname.get().strip()
    last = entry_lastname.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()  # <-- perbaiki di sini

    if not first or not last or not email or not password:
        messagebox.showwarning("Peringatan", "Semua kotak harus diisi!")
        return

    save_data()
    open_login()


# ========== Tombol Register =============
tombol_Register = ctk.CTkButton(reg_page, width=555, height=55, text="Register ",
                         fg_color="#D9D9D9", border_color="#D9D9D9",
                         text_color="black", font=("Helvetica",20,"bold"),
                         corner_radius=3, hover_color="#E1C5C5",
                         command=simpen_data)
tombol_Register.place(x=1010, y=790)

login_button=ctk.CTkButton( master=reg_page,
                            width=60,
                            height=30,
                            text="Log in",
                            font=("Helvetica", 15,"bold"),
                            text_color="#61A8EB",
                            fg_color="#F8EFEF",
                            bg_color="#F8EFEF",
                            border_width=0,      
                            corner_radius=14,     
                            command=open_login
                           )
login_button.place(x=1324, y=339)
# ================ LOGIN PAGE ================
login_page = ctk.CTkFrame(window, width=1920, height=1080)
login_page.grid(row=0, column=0, sticky='nsew')
login_page.lower()

login_bg = ImageTk.PhotoImage(Image.open("assets/bg/login.png")) 
lgbg = ctk.CTkLabel(login_page, image=login_bg, text='')
lgbg.place(x=0, y=0)

login_email = ctk.CTkEntry(login_page, width=680, height=70, placeholder_text=" ",
                         border_color="#D9D9D9", fg_color="#D9D9D9",
                         font=("Helvetica",25), text_color="Black", corner_radius=2)
login_email.place(x=585, y=465)

login_password = ctk.CTkEntry(login_page, width=700, height=70, placeholder_text=" ",
                            border_color="#D9D9D9", fg_color="#D9D9D9",
                            font=("Helvetica",25), text_color="Black", corner_radius=2)
login_password.place(x=585, y=605)

# ================ Tombol Back di login =============

img = Image.open("assets/icon/button back.png")
img = img.resize((30, 30))
# Buka dan resize gambar
img_back = Image.open("assets/icon/button back.png")
img_back = img_back.resize((30, 30))

# Convert ke CTkImage
icon_back = ctk.CTkImage(light_image=img_back, size=(30, 30))


back_button = ctk.CTkButton(
    master=login_page,width=10,height=10,
    image=icon_back,
    text="",              
    fg_color="transparent",
    bg_color="#82ABC5",
    command=open_reg
)

back_button.place(x=85, y=30)

# ============ cek akun input an ===========
def cek_akun():
    input_email = login_email.get().strip()
    input_password = login_password.get().strip()

    if not input_email or not input_password:
        messagebox.showwarning("Peringatan", "Silakan isi email dan password!")
        return None

    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"].strip() == input_email and row["password"].strip() == input_password:
                # AMBIL FIRSTNAME & LASTNAME
                first = row["firstname"]
                last = row["lastname"]
                return first, last

    messagebox.showerror("Gagal", "Email atau password salah!")
    return None


def masuk_homepage():
    home_page.tkraise()

def msksemua():
    akun = cek_akun()
    if akun:
        first, last = akun
        set_username(first, last)   # <- MASUKKAN USERNAME
        masuk_homepage()

    
tombol_login=ctk.CTkButton(master=login_page,width=410,
                         height=90,text="Log in",
                         fg_color="#D9D9D9",
                         border_color="#D9D9D9",
                         text_color="black",
                         font=("Helvetica",20,"bold"),
                         corner_radius=3,
                         hover_color="#E1C5C5",
                         command=msksemua)
tombol_login.place(x=735, y=740)
tombol_login.lift()


# =============== home page ==============

home_page=ctk.CTkFrame(master=window,width=1920,height=1080)
home_page.grid(row=0, column=0, sticky='nsew')
home_page.lower()

bg_home_page=ImageTk.PhotoImage(Image.open("assets/bg/homepage kosong.png"))
home = ctk.CTkLabel(home_page, image=bg_home_page, text='')
home.place(x=0, y=0)

# LABEL USERNAME DI HOME PAGE
username_label = ctk.CTkLabel(
    home_page,
    text="@ !",
    font=("Times", 40, "bold"),
    text_color="white",
    corner_radius=10,
    bg_color="#ece7d5",
)
username_label.place(x=310, y=60)

current_fullname = ""   # buat nyimpen nama lengkap user

def set_username(first, last):
    global current_fullname
    full = f"@ {first} {last}!"
    current_fullname = f"{first} {last}"
    username_label.configure(text=full)


scroll_bar = ctk.CTkFrame(home_page, width=1920, height=300)
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

scroll_frame.bind("<Configure>", update_scroll)

def masuk_br():
    boro_page.tkraise()

boro_image=ctk.CTkImage(Image.open("assets/button 2/hp 1.png"), size=(416, 250))
boro_btn = ctk.CTkButton(
    scroll_frame,
    image=boro_image,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",
    command=masuk_br)
boro_btn.grid(row=0, column=0, padx=20)

def masuk_lot():
    tanah_page.tkraise()

lot_image=ctk.CTkImage(Image.open("assets/button 2/hp 2.png"), size=(416, 250))
lot_btn = ctk.CTkButton(
    scroll_frame,
    image=lot_image,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",
    command=masuk_lot)
lot_btn.grid(row=0, column=1, padx=20)

def masuk_rj():
    rj_page.tkraise()

raja_image=ctk.CTkImage(Image.open("assets/button 2/hp 3.png"), size=(416, 250))
raja_btn = ctk.CTkButton(
    scroll_frame,
    image=raja_image,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",
    command=masuk_rj)
raja_btn.grid(row=0, column=2, padx=20)

def masuk_pram():
    pram_page.tkraise()

pra_image=ctk.CTkImage(Image.open("assets/button 2/hp 4.png"), size=(416, 250))
pra_btn = ctk.CTkButton(
    scroll_frame,
    image=pra_image,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",
    command=masuk_pram)
pra_btn.grid(row=0, column=3, padx=20)

def masuk_rinjani():
    rin_page.tkraise()

rinjani_image=ctk.CTkImage(Image.open("assets/button 2/hp 5.png"), size=(416, 250))
rinjani_btn = ctk.CTkButton(
    scroll_frame,
    image=rinjani_image,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",  
    command=masuk_rinjani)
rinjani_btn.grid(row=0, column=4, padx=20)

scroll_frame.update_idletasks()
canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

def open_payment(destination):
    global current_destination
    current_destination = destination

    pay_page.tkraise()

    label_nama_value.configure(text=current_fullname or "-")
    label_dest_value.configure(text=destination)

    # default jumlah & tanggal
    jumlah_var.set("1")
    today = datetime.date.today().strftime("%d-%m-%Y")
    date_entry.delete(0, "end")
    date_entry.insert(0, today)

    # langsung isi box rincian pertama kali
    update_rincian_pembayaran()



def open_maps(url):
    webbrowser.open(url)
boro_page=ctk.CTkFrame(master=window,width=1920,height=1080)
boro_page.grid(row=0, column=0, sticky='nsew')
boro_page.lower()

boro_bg=ImageTk.PhotoImage(Image.open("assets/bg/borobudur.png"))
boro = ctk.CTkLabel(boro_page, image=boro_bg, text='')
boro.place(x=0, y=0)

img = Image.open("assets/icon/button back.png")
img = img.resize((30, 30))      
img_back = Image.open("assets/icon/button back.png")
img_back = img_back.resize((30, 30))
icon_back = ctk.CTkImage(light_image=img_back, size=(30, 30))
back_btn = ctk.CTkButton(boro_page, width=10,height=10,
                        image=icon_back, text="",
                        fg_color="#C7B184", bg_color="#C7B184",
                        hover_color="#707C93",
                        command=masuk_homepage)
back_btn.place(x=80, y=30)

brloc = Image.open("assets/button/loc boro.png")
brloc = brloc.resize((500, 70), Image.LANCZOS)
brloc2 = ctk.CTkImage(light_image=brloc, size=(480, 70))
boro_loc=ctk.CTkButton(
    boro_page,
    image=brloc2,
    text="",
    fg_color="#D9D9D9",
    hover_color= "#D9D9D9",           
    command=lambda:open_maps("https://maps.app.goo.gl/8aWVX5Q1JHBGE2j66"))
boro_loc.place(x=85, y=915)

brtic = Image.open("assets/button/tic boro.png")
brtic = brtic.resize((520, 100), Image.LANCZOS)
brtic2 = ctk.CTkImage(light_image=brtic, size=(475, 95))
boro_tic=ctk.CTkButton(
    boro_page,
    image=brtic2,
    text="",
    fg_color="#D9D9D9",
    hover_color= "#D9D9D9",           
    command=lambda: open_payment("Borobudur"))
boro_tic.place(x=1325, y=895)

tanah_page=ctk.CTkFrame(master=window,width=1920,height=1080)
tanah_page.grid(row=0, column=0, sticky='nsew')
tanah_page.lower()

tanah_bg=ImageTk.PhotoImage(Image.open("assets/bg/tanah lot.png"))
tnh = ctk.CTkLabel(tanah_page, image=tanah_bg, text='')
tnh.place(x=0, y=0)

img = Image.open("assets/icon/button back.png")
img = img.resize((30, 30))      
img_back = Image.open("assets/icon/button back.png")
img_back = img_back.resize((30, 30))
icon_back = ctk.CTkImage(light_image=img_back, size=(30, 30))
back_btn = ctk.CTkButton(tanah_page, width=10,height=10,
                        image=icon_back, text="",
                        fg_color="#CD5B45", bg_color="#CD5B45",
                        hover_color="#CD5B45",
                        command=masuk_homepage)
back_btn.place(x=80, y=30)

tnloc = Image.open("assets/button/loc tanah.png")
tnloc = tnloc.resize((500, 70), Image.LANCZOS)
tnloc2 = ctk.CTkImage(light_image=tnloc, size=(480, 70))
tanah_loc=ctk.CTkButton(
    tanah_page,
    image=tnloc2,
    text="",
    fg_color="#D78080",
    bg_color="#D78080",             
    hover_color="#D78080",
    command=lambda: open_maps("https://maps.app.goo.gl/GVS7gxeoTfBkfpkH6"))
tanah_loc.place(x=95, y=915)

tntic = Image.open("assets/button/tic tanah.png")
tntic = tntic.resize((500,90), Image.LANCZOS)
tntic2 = ctk.CTkImage(light_image=tntic, size=(500, 90))
tanah_tic=ctk.CTkButton(
    tanah_page,
    image=tntic2,
    text="",
    fg_color="#D78080",
    bg_color="#D78080",             
    hover_color="#D78080",          
    command=lambda: open_payment("Tanah Lot"))
tanah_tic.place(x=1325, y=900)

rj_page = ctk.CTkFrame(master=window,width=1920,height=1080)
rj_page.grid(row=0, column=0, sticky='nsew')
rj_page.lower()

rj_bg=ImageTk.PhotoImage(Image.open("assets/bg/raja ampat.png"))
rj = ctk.CTkLabel(rj_page, image=rj_bg, text='')
rj.place(x=0, y=0)

img = Image.open("assets/icon/button back.png")
img = img.resize((30, 30))      
img_back = Image.open("assets/icon/button back.png")
img_back = img_back.resize((30, 30))
icon_back = ctk.CTkImage(light_image=img_back, size=(30, 30))
back_btn = ctk.CTkButton(rj_page, width=10,height=10,
                        image=icon_back, text="",
                        fg_color="#93A3AE", bg_color="#93A3AE",
                        hover_color="#93A3AE",
                        command=masuk_homepage)
back_btn.place(x=80, y=30)

rjloc = Image.open("assets/button/loc raja.png")
rjloc = rjloc.resize((500, 70), Image.LANCZOS)
rjloc2 = ctk.CTkImage(light_image=rjloc, size=(480, 70))
rj_loc=ctk.CTkButton(
    rj_page,
    image=rjloc2,
    text="",
    fg_color="#80BFD7",
    bg_color="#80BFD7",             
    hover_color="#80BFD7",
    command=lambda: open_maps("https://maps.app.goo.gl/6fzWy5szm5F2RMzP7"))
rj_loc.place(x=80, y=930)

rjtic = Image.open("assets/button/tic raja.png")
rjtic = rjtic.resize((450, 100), Image.LANCZOS)
rjtic2 = ctk.CTkImage(light_image=rjtic, size=(450, 100))
raja_tic=ctk.CTkButton(
    rj_page,
    image=rjtic2,
    text="",
    fg_color="#80BFD7",
    bg_color="#80BFD7",
    hover_color= "#80BFD7",           
    command=lambda: open_payment("Raja Ampat"))
raja_tic.place(x=1335, y=900)

pram_page = ctk.CTkFrame(master=window,width=1920,height=1080)
pram_page.grid(row=0, column=0, sticky='nsew')
pram_page.lower()

pr_bg=ImageTk.PhotoImage(Image.open("assets/bg/prambanan.png"))
pr = ctk.CTkLabel(pram_page, image=pr_bg, text='')
pr.place(x=0, y=0)

img = Image.open("assets/icon/button back.png")
img = img.resize((30, 30))      
img_back = Image.open("assets/icon/button back.png")
img_back = img_back.resize((30, 30))
icon_back = ctk.CTkImage(light_image=img_back, size=(30, 30))
back_btn = ctk.CTkButton(pram_page, width=10,height=10,
                        image=icon_back, text="",
                        fg_color="#657187", bg_color="#657187",
                        hover_color="#657187",
                        command=masuk_homepage)
back_btn.place(x=80, y=30)

prloc = Image.open("assets/button/loc pra.png")
prloc = prloc.resize((500, 70), Image.LANCZOS)
prloc2 = ctk.CTkImage(light_image=prloc, size=(480, 70))
pr_loc=ctk.CTkButton(
    pram_page,
    image=prloc2,
    text="",
    fg_color="#7B411D",
    bg_color="#7B411D",
    hover_color="#7B411D",
    command=lambda: open_maps("https://maps.app.goo.gl/ofnm6XTfUFdYSR1o7"))
pr_loc.place(x=80, y=909)

prtic = Image.open("assets/button/tic pra.png")
prtic = prtic.resize((500, 90), Image.LANCZOS)
prtic2 = ctk.CTkImage(light_image=prtic, size=(500, 90))
pr_tic=ctk.CTkButton(
    pram_page,
    image=prtic2,
    text="",
    fg_color="#7B411D",
    bg_color="#7B411D",
    hover_color="#7B411D",           
    command=lambda: open_payment("Candi Prambanan"))
pr_tic.place(x=1350, y=900)

rin_page = ctk.CTkFrame(master=window,width=1920,height=1080)
rin_page.grid(row=0, column=0, sticky='nsew')
rin_page.lower()

rin_bg=ImageTk.PhotoImage(Image.open("assets/bg/mt rinjani.png"))
rin = ctk.CTkLabel(rin_page, image=rin_bg, text='')
rin.place(x=0, y=0)

img = Image.open("assets/icon/button back.png")
img = img.resize((30, 30))      
img_back = Image.open("assets/icon/button back.png")
img_back = img_back.resize((30, 30))
icon_back = ctk.CTkImage(light_image=img_back, size=(30, 30))
back_btn = ctk.CTkButton(rin_page, width=10,height=10,
                        image=icon_back, text="",
                        fg_color="#BF7DA9", bg_color="#BF7DA9",
                        hover_color="#BF7DA9",
                        command=masuk_homepage)
back_btn.place(x=80, y=30)

rinloc = Image.open("assets/button/loc rin.png")
rinloc = rinloc.resize((500, 70), Image.LANCZOS)
rinloc2 = ctk.CTkImage(light_image=rinloc, size=(480, 70))
rin_loc=ctk.CTkButton(
    rin_page,
    image=rinloc2,
    text="",
    fg_color="#EA4DDA", 
    bg_color="#EA4DDA",
    hover_color="#EA4DDA",
    command=lambda: open_maps("https://maps.app.goo.gl/nrCCfDuuYdj28dxW9"))
rin_loc.place(x=90, y=909)

rintic = Image.open("assets/button/tic rin.png")
rintic = rintic.resize((470, 90), Image.LANCZOS)
rintic2 = ctk.CTkImage(light_image=rintic, size=(470, 90))
rin_tic=ctk.CTkButton(
    rin_page,
    image=rintic2,
    text="",
    fg_color="#EA4DDA",
    bg_color="#EA4DDA",
    hover_color= "#EA4DDA",           
    command=lambda: open_payment("Gunung Rinjani"))
rin_tic.place(x=1325, y=890)

# =============== POPUP FRAME ==================

popup_frame = ctk.CTkFrame(
    window, width=1920, height=1080,
    fg_color="#050505"
)

popup_frame.place_forget()   

# Label gambar popup
popup_img_label = ctk.CTkLabel(popup_frame, text="")
popup_img_label.pack()

# Tombol close
close_btn = ctk.CTkButton(
    popup_frame, text="✕",
    width=40, height=40,
    fg_color="#050505",
    hover_color="#050505",
    corner_radius=20,
    command=lambda: popup_frame.place_forget()
)
close_btn.place(relx=0.95, rely=0.05, anchor="center")

# FUNGSI MENAMPILKAN DISKON
def show_discount_image(img_path):
    try:
        # Load gambar popup
        popup_img = ctk.CTkImage(
            Image.open(img_path),
            size=(1920, 1080)  # ubah sesuai ukuran popup
        )
        popup_img_label.configure(image=popup_img)
        popup_img_label.image = popup_img  # supaya gambar tidak hilang

        popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        popup_frame.lift()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menampilkan popup!\n{e}")

def show_qris_popup():
    show_discount_image("assets/bg/qris.png")

dis1=ctk.CTkImage(Image.open("assets/button 2/disc1.png"), size=(450, 150))
dis1_btn = ctk.CTkButton(
    home_page,
    image=dis1,
    text="",
    fg_color="#ECE7D5",
    hover_color="#B09C7E",
    command=lambda: show_discount_image("showdis1.png")
)
dis1_btn.place(x=51, y=748)

dis2=ctk.CTkImage(Image.open("assets/button 2/disc2.png"), size=(450, 150))
dis2_btn = ctk.CTkButton(
    home_page,
    image=dis2,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",
    command=lambda: show_discount_image("showdis2.png")
    )
dis2_btn.place(x=530, y=748)

dis3=ctk.CTkImage(Image.open("assets/button 2/disc3.png"), size=(450, 150))
dis3_btn = ctk.CTkButton(
    home_page,
    image=dis3,
    text="",
    fg_color="#ECE7D5",
    hover_color="#B09C7E",
    command=lambda: show_discount_image("showdis3.png")
    )
dis3_btn.place(x=1010, y=748)

dis4=ctk.CTkImage(Image.open("assets/button 2/disc4.png"), size=(450, 150))
dis4_btn = ctk.CTkButton(
    home_page,
    image=dis4,
    text="",
    fg_color="transparent",
    hover_color="#B09C7E",
    command=lambda: show_discount_image("showdis4.png")
    )
dis4_btn.place(x=1490, y=748)

#============= PAYMENT PAGE =============

pay_page=ctk.CTkFrame(master=window,width=1920,height=1080)
pay_page.grid(row=0, column=0, sticky='nsew')
pay_page.lower()

bg_pay=ImageTk.PhotoImage(Image.open("assets/bg/payment kosong.png"))
pay = ctk.CTkLabel(pay_page, image=bg_pay, text='')
pay.place(x=0, y=0)

# ====== AREA QRIS KANAN ======

# (opsional) gambar awal: logo QRIS (bukan kode yang discan)
# ====== AREA QRIS KANAN (KOSONG DULU) ======
qris_label = ctk.CTkLabel(
    master=pay_page,
    text="",                # kosong
    width=687,              # sesuaikan lebar kotak kanan
    height=559,             # sesuaikan tinggi kotak kanan
    fg_color="transparent",
    bg_color="#D9D9D9"  # biar kelihatan background PNG kamu
    # kalau mau panel-nya full pink: fg_color="#D98D8D"
)

# posisikan di tengah kotak kanan (geser x,y kalau belum pas)
qris_label.place(x=1151, y=250)


# gambar QRIS yang bisa discan (punyamu sendiri)
qris_code_img = ctk.CTkImage(
    Image.open("assets/bg/qris.png"),   # ganti dgn nama file kode QRIS-mu
    size=(647, 535)
)
metode_btn_img = ctk.CTkImage(
    Image.open("assets/button/qris 2.png"),    # tombol kecil di tengah (yang di bawah tulisan "Metode")
    size=(320, 57)
)
def show_qris_on_panel():
    """Ganti isi area kanan dengan gambar QRIS yang bisa discan."""
    qris_label.configure(image=qris_code_img)
    qris_label.image = qris_code_img  # supaya gambar tidak hilang

# Tombol metode pembayaran
btn_metode = ctk.CTkButton(
    pay_page,
    image=metode_btn_img,
    text="",
    width=320, height= 57,
    fg_color="#D78080",
    bg_color="#D78080",
    hover_color="#D78080",
    command=show_qris_on_panel  # Panggil fungsi untuk menampilkan QRIS saat tombol ditekan
)

btn_metode.place(x=700, y=750)  # Sesuaikan agar tombol berada di posisi yang diinginkan==     # sesuaikan biar pas di kotak metode

def format_rupiah(angka: int) -> str:
    return f"Rp {angka:,.0f}".replace(",", ".")

def hitung_total_setelah_diskon(dest, qty):
    harga = TICKET_PRICES.get(dest, 0)
    diskon = DISCOUNTS.get(dest, 0)

    subtotal = harga * qty
    potongan = subtotal * diskon
    total = subtotal - potongan

    return harga, diskon, subtotal, potongan, total


# ----- LABEL NILAI RINGKASAN (Nama & Destinasi auto, Jumlah & Tanggal bisa diubah) -----

label_nama_value = ctk.CTkLabel(
    pay_page,
    text="",
    font=("Helvetica", 24, "bold"),
    text_color="black",
    bg_color="#FFFFFF"   # sesuaikan dengan warna kotaknya
)
label_nama_value.place(x=360, y=250)   # atur ulang posisi biar pas

label_dest_value = ctk.CTkLabel(
    pay_page,
    text="",
    font=("Helvetica", 24, "bold"),
    text_color="black",
    bg_color="#FFFFFF"
)
label_dest_value.place(x=360, y=330)

# Jumlah tiket: user bisa isi
jumlah_var = StringVar(value=" ")
entry_jumlah_pay = ctk.CTkEntry(
    pay_page,
    width=400, height=40,
    font=("Helvetica", 24),
    fg_color="white",
    border_color="#FFFFFF",
    text_color="black",
    textvariable=jumlah_var
)
entry_jumlah_pay.place(x=360, y=410)

# Tanggal: bisa auto diisi hari ini, tapi tetap entry biar user bisa ubah
date_entry = DateEntry(pay_page, width=10, height=60, background="#385FAA", foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd", 
            font=('ITC Avant Garde Gothic',25, 'bold'), mindate=date.today())
        
date_entry.place(x=360, y=473)

# Label multiline di dalam kotak "Rincian Pembayaran"
label_rincian = ctk.CTkLabel(
    master=pay_page,
    text="",
    width=535,          # ← pindahin ke sini
    height=218,         # ← dan ini
    font=("ITC Avant Garde Gothic", 25),
    text_color="black",
    fg_color="#FFFFFF",  # ini warna background label (bukan bg_color)
    corner_radius=10,
    justify=LEFT,
    anchor="nw"
)
label_rincian.place(x=68, y=705)   # width & height jangan di sini lagi


def update_rincian_pembayaran():
    dest = current_destination or "-"
    
    try:
        qty = int(jumlah_var.get())
        if qty < 1:
            qty = 0
    except ValueError:
        qty = 0
        jumlah_var.set("0")

    harga, diskon, subtotal, potongan, total = hitung_total_setelah_diskon(dest, qty)

    diskon_persen = int(diskon * 100)

    teks = (
        f"Destinasi     : {dest}\n"
        f"Jumlah tiket  : {qty} tiket\n"
        f"Harga/tiket   : {format_rupiah(harga)}\n"
        f"Diskon        : {diskon_persen}%\n"
        f"Subtotal      : {format_rupiah(subtotal)}\n"
        f"Potongan      : - {format_rupiah(potongan)}\n"
        "\n"
        f"Total bayar   : {format_rupiah(total)}"
    )

    label_rincian.configure(text=teks)


def calculate_total(*args):
    """Menghitung total harga berdasarkan jumlah tiket yang dimasukkan."""
    try:
        qty = int(jumlah_var.get())
        if qty < 1:
            qty = 0  # Anggap 0 jika pengguna tidak memasukkan angka yang valid
        jumlah_var.set(str(qty))  # Set ulang nilai untuk menampilkan 0 jika kosong
    except ValueError:
        qty = 0
        jumlah_var.set("0")  # Set nilai menjadi 0 jika input tidak valid
    update_rincian_pembayaran()


# setiap kali jumlah berubah → hitung ulang total
jumlah_var.trace_add("write", lambda *a: calculate_total())

def simpan_tiket_ke_history():
    nama = current_fullname or "-"
    dest = current_destination or "-"
    tgl = date_entry.get().strip()

    try:
        qty = int(jumlah_var.get())
        if qty < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Jumlah tiket harus berupa angka dan minimal 1.")
        return

    harga, diskon, subtotal, potongan, total = hitung_total_setelah_diskon(dest, qty)

    with open(history_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nama, dest, qty, tgl, harga, total])

    messagebox.showinfo("Berhasil", "Tiket berhasil disimpan ke history!")
    home_page.tkraise()

cek_btn = ctk.CTkButton(
    pay_page,
    text="Cek",
    width=165, height=81,
    font=("Helvetica", 28, "bold"),
    fg_color="#E78989",
    hover_color="#D46F6F",
    text_color="black",
    corner_radius=20,
    command=simpan_tiket_ke_history
)
cek_btn.place(x=1418, y=835)   # geser sampai pas di kotak "Cek"

# # ================= PROFILE PAGE =============
 
# prof_page=ctk.CTkFrame(master=window,width=1920,height=1080)
# prof_page.grid(row=0, column=0, sticky='nsew')
# prof_page.lower()

# ProfilePage_bg = ImageTk.PhotoImage(Image.open("C:\\Users\\ASUS\\Downloads\\Profile page.png"))
# bg_label = ctk.CTkLabel(window, image=ProfilePage_bg, text="")
# bg_label.image = ProfilePage_bg
# bg_label.place(x=0, y=0)

home_page.tkraise()
window.mainloop()