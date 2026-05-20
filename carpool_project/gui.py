import tkinter as tk
from tkinter import ttk, messagebox
import os
import re


# ─────────────────────────── HELPERS ───────────────────────────
def to_lower(s):
    return s.lower()


def is_valid_time(t):
    if not re.match(r'^\d{2}:\d{2}$', t):
        return False
    h, m = int(t[:2]), int(t[3:])
    return 0 <= h <= 23 and 0 <= m <= 59


def is_valid_phone(p):
    return len(p) == 11 and p.isdigit()


# ═══════════════════════════ USER ═══════════════════════════════
class User:
    def __init__(self):
        self._name = ""
        self._phone = ""

    def set(self, name, phone):
        self._name = name
        self._phone = phone

    def get_name(self):  return self._name
    def get_phone(self): return self._phone


# ═══════════════════════════ DRIVER ═════════════════════════════
class Driver(User):
    def __init__(self):
        super().__init__()
        self._seats = 0
        self._price = 0.0
        self._car_model = ""
        self._plate_number = ""

    def set(self, name, phone, seats, price, car_model="", plate_number=""):
        super().set(name, phone)
        self._seats = seats
        self._price = price
        self._car_model = car_model
        self._plate_number = plate_number

    def get_seats(self):        return self._seats
    def set_seats(self, s):     self._seats = s
    def get_price(self):        return self._price
    def get_car_model(self):    return self._car_model
    def get_plate_number(self): return self._plate_number
    def set_car_model(self, cm): self._car_model = cm
    def set_plate_number(self, pn): self._plate_number = pn

    def display_str(self):
        return (f"Driver: {self._name} | Phone: {self._phone} | "
                f"Seats: {self._seats} | Price: Rs.{self._price} | "
                f"Car: {self._car_model} | Plate: {self._plate_number}")


# ═══════════════════════════ PASSENGER ══════════════════════════
class Passenger(User):
    def __init__(self):
        super().__init__()
        self._booked_src = ""
        self._booked_dst = ""

    def set_booking(self, src, dst):
        self._booked_src = src
        self._booked_dst = dst

    def get_booked_src(self): return self._booked_src
    def get_booked_dst(self): return self._booked_dst


# ═══════════════════════════ ACCOUNT ════════════════════════════
class Account:
    def __init__(self):
        self._username = ""
        self._password = ""
        self._phone = ""
        self._driver_name = ""
        self._driver_phone = ""
        self._car_model = ""
        self._plate_number = ""

    def set(self, username, password, phone=""):
        self._username = username
        self._password = password
        self._phone = phone

    def set_driver_info(self, dn, dp, cm, pn):
        self._driver_name = dn
        self._driver_phone = dp
        self._car_model = cm
        self._plate_number = pn

    def get_username(self):     return self._username
    def get_password(self):     return self._password
    def get_phone(self):        return self._phone
    def get_car_model(self):    return self._car_model
    def get_plate_number(self): return self._plate_number
    def get_driver_name(self):  return self._driver_name
    def get_driver_phone(self): return self._driver_phone


# ═══════════════════════════ AUTH (SINGLETON) ════════════════════
class Auth:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._driver_accounts = []
            cls._instance._passenger_accounts = []
            cls._instance._load_drivers()
            cls._instance._load_passengers()
        return cls._instance

    @staticmethod
    def get_instance():
        return Auth()

    # ── file helpers ──
    def _load_drivers(self):
        self._driver_accounts = []
        if not os.path.exists("driver_acc.txt"):
            return
        with open("driver_acc.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) < 7:
                    continue
                u, p, ph, dn, dp, cm, pn = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
                acc = Account()
                acc.set(u, p, ph)
                acc.set_driver_info(dn, dp, cm, pn)
                self._driver_accounts.append(acc)

    def _save_drivers(self):
        with open("driver_acc.txt", "w") as f:
            for acc in self._driver_accounts:
                f.write(f"{acc.get_username()}|{acc.get_password()}|{acc.get_phone()}|"
                        f"{acc.get_driver_name()}|{acc.get_driver_phone()}|"
                        f"{acc.get_car_model()}|{acc.get_plate_number()}\n")

    def _load_passengers(self):
        self._passenger_accounts = []
        if not os.path.exists("pass_acc.txt"):
            return
        with open("pass_acc.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) < 2:
                    continue
                u, p = parts[0], parts[1]
                ph = parts[2] if len(parts) > 2 else ""
                acc = Account()
                acc.set(u, p, ph)
                self._passenger_accounts.append(acc)

    def _save_passengers(self):
        with open("pass_acc.txt", "w") as f:
            for acc in self._passenger_accounts:
                f.write(f"{acc.get_username()}|{acc.get_password()}|{acc.get_phone()}\n")

    def _exists(self, accounts, username):
        return any(to_lower(a.get_username()) == to_lower(username) for a in accounts)

    def _check(self, accounts, username, password):
        return any(
            to_lower(a.get_username()) == to_lower(username) and a.get_password() == password
            for a in accounts
        )

    # ── public API ──
    def reg_driver(self, username, password, driver_name, driver_phone, car_model, plate_number):
        if self._exists(self._driver_accounts, username):
            return False
        acc = Account()
        acc.set(username, password)
        acc.set_driver_info(driver_name, driver_phone, car_model, plate_number)
        self._driver_accounts.append(acc)
        self._save_drivers()
        return True

    def reg_pass(self, username, password, phone):
        if self._exists(self._passenger_accounts, username):
            return False
        acc = Account()
        acc.set(username, password, phone)
        self._passenger_accounts.append(acc)
        self._save_passengers()
        return True

    def login_driver(self, username, password):
        return self._check(self._driver_accounts, username, password)

    def login_pass(self, username, password):
        return self._check(self._passenger_accounts, username, password)

    def get_pass_phone(self, username):
        for a in self._passenger_accounts:
            if to_lower(a.get_username()) == to_lower(username):
                return a.get_phone()
        return ""

    def get_driver_account(self, username):
        for a in self._driver_accounts:
            if to_lower(a.get_username()) == to_lower(username):
                return a
        return None


# ═══════════════════════════ CARPOOL ════════════════════════════
class Carpool:
    def __init__(self):
        self._src = ""
        self._dst = ""
        self._departure_time = ""
        self._driver_username = ""
        self._driver = Driver()

    def set(self, src, dst, dep_time, name, phone, seats, price, driver_user="", car_model="", plate_number=""):
        self._src = src
        self._dst = dst
        self._departure_time = dep_time
        self._driver_username = driver_user
        self._driver.set(name, phone, seats, price, car_model, plate_number)

    def get_src(self):            return self._src
    def get_dst(self):            return self._dst
    def get_departure_time(self): return self._departure_time
    def get_driver_username(self): return self._driver_username
    def get_driver(self):         return self._driver

    def display_str(self):
        return (f"Route: {self._src} → {self._dst} | Time: {self._departure_time}\n"
                f"Driver: {self._driver.get_name()} | Phone: {self._driver.get_phone()} | "
                f"Seats: {self._driver.get_seats()} | Price: Rs.{self._driver.get_price()} | "
                f"Car: {self._driver.get_car_model()}")


# ═══════════════════════════ CARPOOL SYSTEM (SINGLETON) ══════════
class CarpoolSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._pool = []
            cls._instance._load_file()
        return cls._instance

    @staticmethod
    def get_instance():
        return CarpoolSystem()

    def _save_file(self):
        with open("carpool.txt", "w") as f:
            for cp in self._pool:
                d = cp.get_driver()
                f.write(f"{cp.get_src()}|{cp.get_dst()}|{cp.get_departure_time()}|"
                        f"{d.get_name()}|{d.get_phone()}|{d.get_seats()}|{d.get_price()}|"
                        f"{cp.get_driver_username()}|{d.get_car_model()}|{d.get_plate_number()}\n")

    def _load_file(self):
        self._pool = []
        if not os.path.exists("carpool.txt"):
            return
        with open("carpool.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) < 8:
                    continue
                try:
                    src, dst, dep, name, phone = parts[0], parts[1], parts[2], parts[3], parts[4]
                    seats, price = int(parts[5]), float(parts[6])
                    du = parts[7]
                    cm = parts[8] if len(parts) > 8 else ""
                    pn = parts[9] if len(parts) > 9 else ""
                    cp = Carpool()
                    cp.set(src, dst, dep, name, phone, seats, price, du, cm, pn)
                    self._pool.append(cp)
                except Exception:
                    pass

    def add_carpool(self, driver_user, src, dst, dep_time, seats, price):
        acc = Auth.get_instance().get_driver_account(driver_user)
        if not acc:
            return False, "Driver account not found."
        # ── NEW: duplicate prevention (same driver + same destination + same time) ──
        for existing in self._pool:
            if (existing.get_driver_username() == driver_user and
                    to_lower(existing.get_dst()) == to_lower(dst) and
                    existing.get_departure_time() == dep_time):
                return False, "This carpool is already added for the same destination and time."
        cp = Carpool()
        cp.set(src, dst, dep_time,
               acc.get_driver_name(), acc.get_driver_phone(),
               seats, price, driver_user,
               acc.get_car_model(), acc.get_plate_number())
        self._pool.append(cp)
        self._save_file()
        return True, "Carpool added!"

    def get_all(self):
        return list(self._pool)

    def get_mine(self, username):
        return [cp for cp in self._pool if cp.get_driver_username() == username]

    def search(self, src, dst):
        return [cp for cp in self._pool
                if to_lower(cp.get_src()) == to_lower(src) and
                   to_lower(cp.get_dst()) == to_lower(dst)]

    def get_available(self):
        return [cp for cp in self._pool if cp.get_driver().get_seats() > 0]

    def book_seat(self, passenger, idx_in_available):
        available = self.get_available()
        if idx_in_available >= len(available):
            return False, "Invalid selection."
        cp = available[idx_in_available]
        if (passenger.get_booked_src() == cp.get_src() and
                passenger.get_booked_dst() == cp.get_dst()):
            return False, "You already booked this route!"
        cp.get_driver().set_seats(cp.get_driver().get_seats() - 1)
        passenger.set_booking(cp.get_src(), cp.get_dst())
        self._save_file()
        fully_booked = cp.get_driver().get_seats() == 0
        return True, cp, fully_booked

    def book_seat_by_carpool(self, passenger, cp):
        if (passenger.get_booked_src() == cp.get_src() and
                passenger.get_booked_dst() == cp.get_dst()):
            return False, "You already booked this route!", False
        cp.get_driver().set_seats(cp.get_driver().get_seats() - 1)
        passenger.set_booking(cp.get_src(), cp.get_dst())
        self._save_file()
        fully_booked = cp.get_driver().get_seats() == 0
        return True, cp, fully_booked

    # ── NEW: delete a specific carpool entry ──
    def delete_carpool(self, carpool_obj):
        if carpool_obj in self._pool:
            self._pool.remove(carpool_obj)
            self._save_file()
            return True
        return False


# ═══════════════════════════ FACADE ══════════════════════════════
class CarpoolFacade:
    def start(self):
        app = App()
        app.mainloop()


# ═══════════════════════════ GUI ══════════════════════════════════

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEAD   = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_BTN    = ("Segoe UI", 11, "bold")
FONT_SMALL  = ("Segoe UI", 9)

BG          = "#F0F4FF"
CARD_BG     = "#FFFFFF"
PRIMARY     = "#4F6EF7"
PRIMARY_D   = "#3A56D4"
DANGER      = "#E53E3E"
SUCCESS     = "#2F9E44"
TEXT_DARK   = "#1A1A2E"
TEXT_MED    = "#555577"
BORDER      = "#D0D8F0"


def styled_btn(parent, text, command, color=PRIMARY, fg="white", width=18):
    b = tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                  font=FONT_BTN, relief="flat", bd=0, cursor="hand2",
                  activebackground=PRIMARY_D, activeforeground="white",
                  padx=12, pady=8, width=width)
    b.bind("<Enter>", lambda e: b.config(bg=PRIMARY_D if color == PRIMARY else color))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b


def entry_field(parent, label_text, show="", width=32):
    frame = tk.Frame(parent, bg=CARD_BG)
    tk.Label(frame, text=label_text, font=FONT_SMALL, bg=CARD_BG,
             fg=TEXT_MED, anchor="w").pack(fill="x")
    e = tk.Entry(frame, font=FONT_BODY, show=show, width=width,
                 relief="solid", bd=1, bg="#F8FAFF")
    e.pack(fill="x", ipady=5)
    return frame, e


def card_frame(parent, **kwargs):
    f = tk.Frame(parent, bg=CARD_BG, relief="flat", bd=0,
                 highlightbackground=BORDER, highlightthickness=1, **kwargs)
    return f


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Carpool System")
        self.geometry("820x620")
        self.resizable(True, True)
        self.configure(bg=BG)
        self._current_frame = None
        self.show_main_menu()

    def show_frame(self, frame_class, *args, **kwargs):
        if self._current_frame:
            self._current_frame.destroy()
        self._current_frame = frame_class(self, *args, **kwargs)
        self._current_frame.pack(fill="both", expand=True)

    def show_main_menu(self):
        self.show_frame(MainMenuFrame)

    def show_driver_portal(self):
        self.show_frame(DriverPortalFrame)

    def show_passenger_portal(self):
        self.show_frame(PassengerPortalFrame)

    def show_driver_dashboard(self, username):
        self.show_frame(DriverDashboardFrame, username)

    def show_passenger_dashboard(self, username, passenger):
        self.show_frame(PassengerDashboardFrame, username, passenger)


# ─── MAIN MENU ───────────────────────────────────────────────────
class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="🚗 Carpool System", font=FONT_TITLE,
                 bg=BG, fg=PRIMARY).pack(pady=(60, 10))
        tk.Label(self, text="Share rides. Save money. Travel smart.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED).pack(pady=(0, 50))

        c = card_frame(self)
        c.pack(padx=80, pady=20, ipadx=30, ipady=30)

        tk.Label(c, text="Select your role", font=FONT_HEAD,
                 bg=CARD_BG, fg=TEXT_DARK).pack(pady=(10, 20))

        styled_btn(c, "I'm a Driver", self.master.show_driver_portal).pack(pady=8)
        styled_btn(c, "I'm a Passenger", self.master.show_passenger_portal,
                   color="#6C47FF").pack(pady=8)
        styled_btn(c, "Exit", self.master.destroy,
                   color=DANGER).pack(pady=(16, 8))


# ─── DRIVER PORTAL ───────────────────────────────────────────────
class DriverPortalFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Driver Portal", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(pady=(40, 6))
        tk.Label(self, text="Register or log in to manage your carpools",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED).pack(pady=(0, 30))

        nb = ttk.Notebook(self)
        nb.pack(padx=60, pady=10, fill="both", expand=True)

        login_tab = tk.Frame(nb, bg=CARD_BG, padx=30, pady=20)
        reg_tab   = tk.Frame(nb, bg=CARD_BG, padx=30, pady=20)
        nb.add(login_tab, text="  Login  ")
        nb.add(reg_tab,   text="  Register  ")

        self._build_login(login_tab)
        self._build_register(reg_tab)

        styled_btn(self, "← Back", self.master.show_main_menu,
                   color="#888", width=12).pack(pady=16)

    def _build_login(self, parent):
        tk.Label(parent, text="Driver Login", font=FONT_HEAD, bg=CARD_BG,
                 fg=TEXT_DARK).grid(row=0, column=0, columnspan=2, pady=(0, 16))

        f1, self._l_user = entry_field(parent, "Username")
        f1.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)
        f2, self._l_pass = entry_field(parent, "Password", show="*")
        f2.grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)
        parent.columnconfigure(0, weight=1)

        styled_btn(parent, "Login", self._do_login).grid(row=3, column=0,
                                                          columnspan=2, pady=16)

    def _build_register(self, parent):
        tk.Label(parent, text="Driver Registration", font=FONT_HEAD,
                 bg=CARD_BG, fg=TEXT_DARK).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        fields = [
            ("Username", False), ("Password", True), ("Confirm Password", True),
            ("Full Name", False), ("Phone (11 digits)", False),
            ("Car Model", False), ("Plate Number", False),
        ]
        self._r_entries = {}
        for i, (label, secret) in enumerate(fields):
            f, e = entry_field(parent, label, show="*" if secret else "")
            col = i % 2
            row = 1 + i // 2
            f.grid(row=row, column=col, sticky="ew", padx=6, pady=4)
            self._r_entries[label] = e

        styled_btn(parent, "Register", self._do_register).grid(
            row=1 + len(fields) // 2 + 1, column=0, columnspan=2, pady=16)

    def _do_login(self):
        u = self._l_user.get().strip()
        p = self._l_pass.get()
        if not u or not p:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if Auth.get_instance().login_driver(u, p):
            self.master.show_driver_dashboard(u)
        else:
            messagebox.showerror("Login Failed", "Wrong username or password.")

    def _do_register(self):
        e = self._r_entries
        u    = e["Username"].get().strip()
        pw   = e["Password"].get()
        cpw  = e["Confirm Password"].get()
        name = e["Full Name"].get().strip()
        ph   = e["Phone (11 digits)"].get().strip()
        cm   = e["Car Model"].get().strip()
        pn   = e["Plate Number"].get().strip()

        if not u or not pw:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if pw != cpw:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not is_valid_phone(ph):
            messagebox.showerror("Error", "Phone must be exactly 11 digits.")
            return
        if not cm or not pn:
            messagebox.showerror("Error", "Car model and plate number cannot be empty.")
            return

        ok = Auth.get_instance().reg_driver(u, pw, name, ph, cm, pn)
        if ok:
            messagebox.showinfo("Success", "Registered! Logging you in...")
            self.master.show_driver_dashboard(u)
        else:
            messagebox.showerror("Error", "Username already taken.")


# ─── DRIVER DASHBOARD ────────────────────────────────────────────
class DriverDashboardFrame(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master, bg=BG)
        self._username = username
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=PRIMARY, pady=14)
        top.pack(fill="x")
        tk.Label(top, text=f"Welcome, Driver {self._username}",
                 font=FONT_HEAD, bg=PRIMARY, fg="white").pack(side="left", padx=20)
        styled_btn(top, "Logout", self.master.show_main_menu,
                   color=DANGER, width=10).pack(side="right", padx=20)

        nb = ttk.Notebook(self)
        nb.pack(padx=20, pady=16, fill="both", expand=True)

        add_tab  = tk.Frame(nb, bg=CARD_BG, padx=30, pady=20)
        view_tab = tk.Frame(nb, bg=CARD_BG)
        nb.add(add_tab,  text="  Add Carpool  ")
        nb.add(view_tab, text="  My Carpools  ")
        nb.bind("<<NotebookTabChanged>>", lambda e: self._refresh_my(view_tab)
                if nb.index(nb.select()) == 1 else None)

        self._build_add(add_tab)
        self._build_my(view_tab)

    def _build_add(self, parent):
        tk.Label(parent, text="Add New Carpool", font=FONT_HEAD,
                 bg=CARD_BG, fg=TEXT_DARK).grid(row=0, column=0, columnspan=2, pady=(0, 14))
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        labels = ["Source", "Destination", "Departure Time (HH:MM)", "Seats", "Price per Seat (Rs.)"]
        self._add_entries = {}
        for i, lbl in enumerate(labels):
            f, e = entry_field(parent, lbl)
            col = i % 2
            row = 1 + i // 2
            f.grid(row=row, column=col, sticky="ew", padx=6, pady=5)
            self._add_entries[lbl] = e

        styled_btn(parent, "Add Carpool", self._do_add,
                   color=SUCCESS).grid(row=1 + (len(labels) + 1) // 2, column=0,
                                       columnspan=2, pady=18)

    def _do_add(self):
        e = self._add_entries
        src  = e["Source"].get().strip()
        dst  = e["Destination"].get().strip()
        t    = e["Departure Time (HH:MM)"].get().strip()
        s    = e["Seats"].get().strip()
        pr   = e["Price per Seat (Rs.)"].get().strip()

        if not src or not dst:
            messagebox.showerror("Error", "Source and destination cannot be empty.")
            return
        if not is_valid_time(t):
            messagebox.showerror("Error", "Departure time must be HH:MM (00:00–23:59).")
            return
        try:
            seats = int(s)
            if seats <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Seats must be a positive integer.")
            return
        try:
            price = float(pr)
            if price <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Price must be a positive number.")
            return

        ok, msg = CarpoolSystem.get_instance().add_carpool(
            self._username, src, dst, t, seats, price)
        if ok:
            messagebox.showinfo("Success", msg)
            for ent in self._add_entries.values():
                ent.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)

    def _build_my(self, parent):
        # ── NEW: scrollable canvas to hold per-row Delete buttons ──
        self._my_canvas = tk.Canvas(parent, bg=CARD_BG, highlightthickness=0)
        self._my_scrollbar = ttk.Scrollbar(parent, orient="vertical",
                                           command=self._my_canvas.yview)
        self._my_canvas.configure(yscrollcommand=self._my_scrollbar.set)
        self._my_scrollbar.pack(side="right", fill="y")
        self._my_canvas.pack(side="left", fill="both", expand=True)
        self._my_inner = tk.Frame(self._my_canvas, bg=CARD_BG)
        self._my_canvas_window = self._my_canvas.create_window(
            (0, 0), window=self._my_inner, anchor="nw")
        self._my_inner.bind("<Configure>", lambda e: self._my_canvas.configure(
            scrollregion=self._my_canvas.bbox("all")))
        self._my_canvas.bind("<Configure>", lambda e: self._my_canvas.itemconfig(
            self._my_canvas_window, width=e.width))
        self._refresh_my(parent)

    def _refresh_my(self, _parent=None):
        # ── NEW: rebuild rows with Delete button per carpool ──
        for widget in self._my_inner.winfo_children():
            widget.destroy()
        mine = CarpoolSystem.get_instance().get_mine(self._username)
        if not mine:
            tk.Label(self._my_inner, text="No carpools added yet.",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_MED,
                     pady=20).pack(fill="x", padx=16)
        else:
            for i, cp in enumerate(mine, 1):
                row_frame = tk.Frame(self._my_inner, bg=CARD_BG,
                                     highlightbackground=BORDER, highlightthickness=1)
                row_frame.pack(fill="x", padx=12, pady=6, ipadx=8, ipady=6)

                info_frame = tk.Frame(row_frame, bg=CARD_BG)
                info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=6)

                tk.Label(info_frame,
                         text=f"#{i}  Route: {cp.get_src()} → {cp.get_dst()}  |  Time: {cp.get_departure_time()}",
                         font=FONT_HEAD, bg=CARD_BG, fg=TEXT_DARK,
                         anchor="w").pack(fill="x")
                d = cp.get_driver()
                tk.Label(info_frame,
                         text=(f"Driver: {d.get_name()} | Phone: {d.get_phone()} | "
                               f"Seats: {d.get_seats()} | Price: Rs.{d.get_price()} | "
                               f"Car: {d.get_car_model()} | Plate: {d.get_plate_number()}"),
                         font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MED,
                         anchor="w").pack(fill="x")

                # ── NEW: Delete button bound to this specific carpool object ──
                def make_delete_cmd(carpool_obj):
                    def _do_delete():
                        confirmed = messagebox.askyesno(
                            "Confirm Delete",
                            "Are you sure you want to delete this carpool?")
                        if not confirmed:
                            return
                        ok = CarpoolSystem.get_instance().delete_carpool(carpool_obj)
                        if ok:
                            messagebox.showinfo("Deleted", "Carpool deleted successfully.")
                            self._refresh_my()
                        else:
                            messagebox.showerror("Error", "Could not delete carpool.")
                    return _do_delete

                del_btn = tk.Button(row_frame, text="Delete", command=make_delete_cmd(cp),
                                    bg=DANGER, fg="white", font=FONT_BTN, relief="flat",
                                    cursor="hand2", padx=10, pady=6, width=8)
                del_btn.pack(side="right", padx=10, pady=6)
        self._my_canvas.update_idletasks()
        self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))


# ─── PASSENGER PORTAL ────────────────────────────────────────────
class PassengerPortalFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Passenger Portal", font=FONT_TITLE,
                 bg=BG, fg="#6C47FF").pack(pady=(40, 6))
        tk.Label(self, text="Register or log in to find and book rides",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED).pack(pady=(0, 30))

        nb = ttk.Notebook(self)
        nb.pack(padx=60, pady=10, fill="both", expand=True)

        login_tab = tk.Frame(nb, bg=CARD_BG, padx=30, pady=20)
        reg_tab   = tk.Frame(nb, bg=CARD_BG, padx=30, pady=20)
        nb.add(login_tab, text="  Login  ")
        nb.add(reg_tab,   text="  Register  ")

        self._build_login(login_tab)
        self._build_register(reg_tab)

        styled_btn(self, "← Back", self.master.show_main_menu,
                   color="#888", width=12).pack(pady=16)

    def _build_login(self, parent):
        tk.Label(parent, text="Passenger Login", font=FONT_HEAD,
                 bg=CARD_BG, fg=TEXT_DARK).grid(row=0, column=0, columnspan=2, pady=(0, 16))
        parent.columnconfigure(0, weight=1)

        f1, self._l_user = entry_field(parent, "Username")
        f1.grid(row=1, column=0, sticky="ew", pady=6)
        f2, self._l_pass = entry_field(parent, "Password", show="*")
        f2.grid(row=2, column=0, sticky="ew", pady=6)
        styled_btn(parent, "Login", self._do_login,
                   color="#6C47FF").grid(row=3, column=0, pady=16)

    def _build_register(self, parent):
        tk.Label(parent, text="Passenger Registration", font=FONT_HEAD,
                 bg=CARD_BG, fg=TEXT_DARK).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        parent.columnconfigure(0, weight=1)

        labels = [("Username", False), ("Password", True),
                  ("Confirm Password", True), ("Phone (11 digits)", False)]
        self._r_entries = {}
        for i, (lbl, secret) in enumerate(labels):
            f, e = entry_field(parent, lbl, show="*" if secret else "")
            f.grid(row=1 + i, column=0, sticky="ew", pady=5)
            self._r_entries[lbl] = e

        styled_btn(parent, "Register", self._do_register,
                   color="#6C47FF").grid(row=1 + len(labels) + 1, column=0, pady=16)

    def _do_login(self):
        u = self._l_user.get().strip()
        p = self._l_pass.get()
        if not u or not p:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if Auth.get_instance().login_pass(u, p):
            passenger = Passenger()
            passenger.set(u, Auth.get_instance().get_pass_phone(u))
            self.master.show_passenger_dashboard(u, passenger)
        else:
            messagebox.showerror("Login Failed", "Wrong username or password.")

    def _do_register(self):
        e = self._r_entries
        u   = e["Username"].get().strip()
        pw  = e["Password"].get()
        cpw = e["Confirm Password"].get()
        ph  = e["Phone (11 digits)"].get().strip()

        if not u or not pw:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if pw != cpw:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not is_valid_phone(ph):
            messagebox.showerror("Error", "Phone must be exactly 11 digits.")
            return

        ok = Auth.get_instance().reg_pass(u, pw, ph)
        if ok:
            messagebox.showinfo("Success", "Registered! Logging you in...")
            passenger = Passenger()
            passenger.set(u, ph)
            self.master.show_passenger_dashboard(u, passenger)
        else:
            messagebox.showerror("Error", "Username already taken.")


# ─── PASSENGER DASHBOARD ─────────────────────────────────────────
class PassengerDashboardFrame(tk.Frame):
    def __init__(self, master, username, passenger):
        super().__init__(master, bg=BG)
        self._username = username
        self._passenger = passenger
        self._build()

    def _build(self):
        top = tk.Frame(self, bg="#6C47FF", pady=14)
        top.pack(fill="x")
        tk.Label(top, text=f"Welcome, Passenger {self._username}",
                 font=FONT_HEAD, bg="#6C47FF", fg="white").pack(side="left", padx=20)
        styled_btn(top, "Logout", self.master.show_main_menu,
                   color=DANGER, width=10).pack(side="right", padx=20)

        nb = ttk.Notebook(self)
        nb.pack(padx=20, pady=16, fill="both", expand=True)

        slider_tab = tk.Frame(nb, bg=CARD_BG)
        search_tab = tk.Frame(nb, bg=CARD_BG, padx=20, pady=20)
        book_tab   = tk.Frame(nb, bg=CARD_BG, padx=20, pady=20)
        nb.add(slider_tab, text="  Browse Rides  ")
        nb.add(book_tab,   text="  Book a Ride  ")

        self._build_slider(slider_tab)
        self._build_search(search_tab)
        self._build_book(book_tab)

    # ── SLIDER ──────────────────────────────────────────
    def _build_slider(self, parent):
        self._slider_idx = 0
        self._slider_available = []

        header = tk.Frame(parent, bg="#6C47FF", pady=10)
        header.pack(fill="x")
        self._slider_counter = tk.Label(header, text="", font=FONT_HEAD,
                                        bg="#6C47FF", fg="white")
        self._slider_counter.pack()

        self._slider_card = card_frame(parent)
        self._slider_card.pack(padx=30, pady=20, fill="both", expand=True)

        self._slider_text = tk.Text(self._slider_card, font=FONT_BODY, bg=CARD_BG,
                                    fg=TEXT_DARK, relief="flat", state="disabled",
                                    wrap="word", padx=20, pady=20, height=10)
        self._slider_text.pack(fill="both", expand=True)

        nav = tk.Frame(parent, bg=BG)
        nav.pack(pady=12)
        styled_btn(nav, "◀ Previous", self._slider_prev, color="#888", width=14).pack(side="left", padx=8)
        styled_btn(nav, "Book This Ride", self._slider_book, color=SUCCESS, width=16).pack(side="left", padx=8)
        styled_btn(nav, "Next ▶", self._slider_next, color="#888", width=14).pack(side="left", padx=8)

        self._refresh_slider()

    def _refresh_slider(self):
        self._slider_available = CarpoolSystem.get_instance().get_available()
        total = len(self._slider_available)
        if self._slider_idx >= total:
            self._slider_idx = max(0, total - 1)

        self._slider_text.config(state="normal")
        self._slider_text.delete("1.0", tk.END)

        if not self._slider_available:
            self._slider_counter.config(text="No available rides")
            self._slider_text.insert(tk.END,
                "No rides available at the moment.")
        else:
            cp = self._slider_available[self._slider_idx]
            d  = cp.get_driver()
            self._slider_counter.config(
                text=f"Ride {self._slider_idx + 1} of {total}")
            self._slider_text.insert(tk.END,
                f"Route:     {cp.get_src()} → {cp.get_dst()}\n"
                f"Departure: {cp.get_departure_time()}\n\n"
                f"Driver:    {d.get_name()}\n"
                f"Phone:     {d.get_phone()}\n"
                f"Car Model: {d.get_car_model()}\n"
                f"Seats Left:{d.get_seats()}\n"
                f"Price:     Rs.{d.get_price()} per seat\n")
        self._slider_text.config(state="disabled")

    def _slider_prev(self):
        if not self._slider_available:
            return
        if self._slider_idx > 0:
            self._slider_idx -= 1
            self._refresh_slider()
        else:
            messagebox.showinfo("Info", "This is the first ride.")

    def _slider_next(self):
        if not self._slider_available:
            return
        if self._slider_idx < len(self._slider_available) - 1:
            self._slider_idx += 1
            self._refresh_slider()
        else:
            messagebox.showinfo("Info", "This is the last ride.")

    def _slider_book(self):
        available = CarpoolSystem.get_instance().get_available()
        if not available:
            messagebox.showinfo("Info", "No rides available to book.")
            return
        if self._slider_idx >= len(available):
            self._slider_idx = len(available) - 1
        cp = available[self._slider_idx]
        ok, result, fully_booked = CarpoolSystem.get_instance().book_seat_by_carpool(
            self._passenger, cp)
        if ok:
            messagebox.showinfo("Booked!", "Seat booked! Please call the driver for confirmation.")
            if fully_booked:
                messagebox.showinfo("Fully Booked",
                                    "All seats are now booked for this ride.")
            self._refresh_slider()
        else:
            messagebox.showerror("Error", result)

    # ── SEARCH ──────────────────────────────────────────
    def _build_search(self, parent):
        tk.Label(parent, text="Search Rides", font=FONT_HEAD, bg=CARD_BG,
                 fg=TEXT_DARK).pack(pady=(0, 12))

        row = tk.Frame(parent, bg=CARD_BG)
        row.pack(fill="x")
        f1, self._search_src = entry_field(row, "From (Source)")
        f1.pack(side="left", padx=8, expand=True, fill="x")
        f2, self._search_dst = entry_field(row, "To (Destination)")
        f2.pack(side="left", padx=8, expand=True, fill="x")
        styled_btn(parent, "Search", self._do_search,
                   color=PRIMARY).pack(pady=10)

        self._search_result = tk.Text(parent, font=FONT_BODY, bg="#F8FAFF",
                                      fg=TEXT_DARK, relief="solid", bd=1,
                                      state="disabled", wrap="word", padx=12, pady=10)
        scroll = ttk.Scrollbar(parent, command=self._search_result.yview)
        self._search_result.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self._search_result.pack(fill="both", expand=True)

    def _do_search(self):
        src = self._search_src.get().strip()
        dst = self._search_dst.get().strip()
        results = CarpoolSystem.get_instance().search(src, dst)
        # Only show available (seats > 0)
        results = [cp for cp in results if cp.get_driver().get_seats() > 0]

        self._search_result.config(state="normal")
        self._search_result.delete("1.0", tk.END)
        if not results:
            self._search_result.insert(tk.END, "No available carpools found for this route.")
        else:
            for i, cp in enumerate(results, 1):
                d = cp.get_driver()
                self._search_result.insert(tk.END,
                    f"#{i}\n"
                    f"Route:      {cp.get_src()} → {cp.get_dst()}\n"
                    f"Departure:  {cp.get_departure_time()}\n"
                    f"Driver:     {d.get_name()} | Phone: {d.get_phone()}\n"
                    f"Car:        {d.get_car_model()}\n"
                    f"Seats Left: {d.get_seats()}\n"
                    f"Price:      Rs.{d.get_price()} per seat\n"
                    f"{'─'*60}\n")
        self._search_result.config(state="disabled")

    # ── BOOK ────────────────────────────────────────────
    def _build_book(self, parent):
        tk.Label(parent, text="Book a Ride", font=FONT_HEAD, bg=CARD_BG,
                 fg=TEXT_DARK).pack(pady=(0, 12))

        row = tk.Frame(parent, bg=CARD_BG)
        row.pack(fill="x")
        f1, self._book_src = entry_field(row, "From (Source)")
        f1.pack(side="left", padx=8, expand=True, fill="x")
        f2, self._book_dst = entry_field(row, "To (Destination)")
        f2.pack(side="left", padx=8, expand=True, fill="x")
        styled_btn(parent, "Find Rides", self._do_find_book,
                   color=PRIMARY).pack(pady=10)

        list_frame = tk.Frame(parent, bg=CARD_BG)
        list_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._book_listbox = tk.Listbox(list_frame, font=FONT_BODY,
                                        bg="#F8FAFF", fg=TEXT_DARK,
                                        selectbackground=PRIMARY,
                                        selectforeground="white",
                                        relief="solid", bd=1,
                                        yscrollcommand=scrollbar.set)
        self._book_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self._book_listbox.yview)

        self._book_matches = []
        styled_btn(parent, "Book Selected Ride", self._do_book_selected,
                   color=SUCCESS).pack(pady=10)

    def _do_find_book(self):
        src = self._book_src.get().strip()
        dst = self._book_dst.get().strip()
        results = CarpoolSystem.get_instance().search(src, dst)
        self._book_matches = [cp for cp in results if cp.get_driver().get_seats() > 0]

        self._book_listbox.delete(0, tk.END)
        if not self._book_matches:
            self._book_listbox.insert(tk.END, "No available rides found for this route.")
        else:
            for i, cp in enumerate(self._book_matches, 1):
                d = cp.get_driver()
                self._book_listbox.insert(
                    tk.END,
                    f"{i}. {cp.get_src()} → {cp.get_dst()} | {cp.get_departure_time()} | "
                    f"Driver: {d.get_name()} | Seats: {d.get_seats()} | Rs.{d.get_price()} | "
                    f"Car: {d.get_car_model()}"
                )

    def _do_book_selected(self):
        if not self._book_matches:
            messagebox.showinfo("Info", "Please search for rides first.")
            return
        sel = self._book_listbox.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a ride from the list.")
            return
        idx = sel[0]
        if idx >= len(self._book_matches):
            messagebox.showerror("Error", "Invalid selection.")
            return

        cp = self._book_matches[idx]
        ok, result, fully_booked = CarpoolSystem.get_instance().book_seat_by_carpool(
            self._passenger, cp)
        if ok:
            messagebox.showinfo("Booked!",
                                "Seat booked successfully!\nPlease call the driver for confirmation.")
            if fully_booked:
                messagebox.showinfo("Fully Booked",
                                    "This ride is now fully booked.")
            self._do_find_book()
        else:
            messagebox.showerror("Error", result)


# ═══════════════════════════ ENTRY POINT ═════════════════════════
if __name__ == "__main__":
    facade = CarpoolFacade()
    facade.start()