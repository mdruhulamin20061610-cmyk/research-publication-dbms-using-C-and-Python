# login_gui.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Research DBMS")
        self.root.geometry("400x350")
        self.root.configure(bg="#2c3e50")
        
        # Title
        tk.Label(root, text="RESEARCH PUBLICATION DATABASE",
                font=("Arial", 16, "bold"),
                fg="white", bg="#2c3e50").pack(pady=30)
        
        tk.Label(root, text="Department of Mechanical Engineering, BUET",
                font=("Arial", 11),
                fg="#ecf0f1", bg="#2c3e50").pack()
        
        # Login Frame
        login_frame = tk.Frame(root, bg="#34495e", padx=30, pady=30)
        login_frame.pack(pady=20, padx=40)
        
        # Username
        tk.Label(login_frame, text="Username:", 
                font=("Arial", 11),
                fg="white", bg="#34495e").grid(row=0, column=0, pady=10, sticky="w")
        self.username_entry = tk.Entry(login_frame, font=("Arial", 11), width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        self.username_entry.insert(0, "admin")  # Default for testing
        
        # Password
        tk.Label(login_frame, text="Password:", 
                font=("Arial", 11),
                fg="white", bg="#34495e").grid(row=1, column=0, pady=10, sticky="w")
        self.password_entry = tk.Entry(login_frame, font=("Arial", 11), 
                                      show="*", width=25)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        self.password_entry.insert(0, "admin123")  # Default for testing
        
        # Login Button
        tk.Button(login_frame, text="LOGIN", 
                 font=("Arial", 12, "bold"),
                 bg="#3498db", fg="white",
                 width=20, height=2,
                 command=self.login).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Status
        self.status_label = tk.Label(root, text="", 
                                    font=("Arial", 10),
                                    fg="#e74c3c", bg="#2c3e50")
        self.status_label.pack()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="Please enter both fields")
            return
        
        # Simple authentication (In real system, check against file/database)
        if username == "admin" and password == "admin123":
            self.status_label.config(text="Login successful!", fg="#2ecc71")
            self.root.after(1000, self.open_main_gui)
        elif username == "user" and password == "user123":
            self.status_label.config(text="Login successful!", fg="#2ecc71")
            self.root.after(1000, lambda: self.open_main_gui("user"))
        else:
            self.status_label.config(text="Invalid credentials")
    
    def open_main_gui(self, role="admin"):
        self.root.destroy()  # Close login window
        import main_gui
        root = tk.Tk()
        main_gui.MainGUI(root, role)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    root.mainloop()