import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x500")
        
        # Initialize Database
        self.conn = sqlite3.connect("hotel_management.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        
        # Create Heading
        self.heading = tk.Label(self.root, text="HOTEL MANAGEMENT SYSTEM", font=("Arial", 16, "bold"))
        self.heading.pack(pady=10)
        
        # Create Main Buttons
        self.create_main_buttons()
    
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Guest (
                                guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                age INTEGER,
                                gender TEXT,
                                phone_no TEXT,
                                room_type TEXT,
                                check_in TEXT,
                                check_out TEXT)
                            ''')
        self.conn.commit()
    
    def create_main_buttons(self):
        self.clear_frame()
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        management_btn = ttk.Button(btn_frame, text="Management", command=self.show_management)
        management_btn.grid(row=0, column=0, padx=20, pady=10)
        
        guest_btn = ttk.Button(btn_frame, text="Guest", command=self.show_guest)
        guest_btn.grid(row=0, column=1, padx=20, pady=10)
    
    def show_management(self):
        self.clear_frame()
        
        back_btn = ttk.Button(self.root, text="← Back", command=self.create_main_buttons)
        back_btn.pack(anchor='w', padx=10, pady=5)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Room Reservation", command=self.show_room_reservation).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Manage Department").grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(btn_frame, text="Manage Staff").grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Guest Information").grid(row=1, column=1, padx=10, pady=5)
    
    def show_guest(self):
        self.clear_frame()
        
        back_btn = ttk.Button(self.root, text="← Back", command=self.create_main_buttons)
        back_btn.pack(anchor='w', padx=10, pady=5)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Book Your Reservation", command=self.show_room_reservation).grid(row=0, column=0, padx=10, pady=5)
    
    def show_room_reservation(self):
        self.clear_frame()
        
        back_btn = ttk.Button(self.root, text="← Back", command=self.show_guest)
        back_btn.pack(anchor='w', padx=10, pady=5)
        
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        age_entry = ttk.Entry(form_frame)
        age_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
        gender_var = tk.StringVar()
        gender_male = ttk.Radiobutton(form_frame, text="Male", variable=gender_var, value="Male")
        gender_female = ttk.Radiobutton(form_frame, text="Female", variable=gender_var, value="Female")
        gender_male.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        gender_female.grid(row=2, column=2, padx=5, pady=5, sticky='w')
        
        ttk.Label(form_frame, text="Phone No:").grid(row=3, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(form_frame)
        phone_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Room Type:").grid(row=4, column=0, padx=5, pady=5)
        room_var = tk.StringVar()
        room_type = ttk.Combobox(form_frame, textvariable=room_var, values=["Normal Room", "Exquisite Room"])
        room_type.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Check-in Date:").grid(row=5, column=0, padx=5, pady=5)
        check_in_entry = DateEntry(form_frame, date_pattern='dd-mm-yyyy')
        check_in_entry.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Check-out Date:").grid(row=6, column=0, padx=5, pady=5)
        check_out_entry = DateEntry(form_frame, date_pattern='dd-mm-yyyy')
        check_out_entry.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Submit", command=lambda: self.book_room(
            name_entry.get(), age_entry.get(), gender_var.get(), phone_entry.get(), 
            room_var.get(), check_in_entry.get(), check_out_entry.get())).grid(row=7, column=0, columnspan=2, pady=10)
    
    def book_room(self, name, age, gender, phone, room_type, check_in, check_out):
        if not name or not age or not gender or not phone or not room_type or not check_in or not check_out:
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not age.isdigit() or int(age) < 18:
            messagebox.showerror("Error", "Age must be a number greater than 18")
            return
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return
        self.cursor.execute("INSERT INTO Guest (name, age, gender, phone_no, room_type, check_in, check_out) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                            (name, age, gender, phone, room_type, check_in, check_out))
        self.conn.commit()
        messagebox.showinfo("Success", "Room Reserved Successfully")
        self.create_main_buttons()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.heading = tk.Label(self.root, text="HOTEL MANAGEMENT SYSTEM", font=("Arial", 16, "bold"))
        self.heading.pack(pady=10)
    
    def __del__(self):
        self.conn.close()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()


