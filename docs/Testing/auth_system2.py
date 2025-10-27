import tkinter as tk
from tkinter import messagebox
import json
import os

class AuthenticationSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}

    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def create_account(self, username, password):
        users = self.load_users()
        if username in users:
            return False, "Username already exists!"
        users[username] = {
            "password": password,
            "saved_passwords": []
        }
        self.save_users(users)
        self.current_user = username
        return True, "Account created successfully!"

    def login(self, password):
        users = self.load_users()
        for username, data in users.items():
            if data["password"] == password:
                self.current_user = username
                return True, f"Welcome back, {username}!"
        return False, "Password not found. Try again."

class LoginWindow:
    def __init__(self, on_success_callback):
        self.auth = AuthenticationSystem()
        self.on_success_callback = on_success_callback
        self.root = tk.Tk()
        self.root.title("Secure Login")
        self.root.configure(bg="#1a1a1a")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.center_window()
        self.setup_ui()
        self.root.mainloop()
        self.setup_login_window()

    def setup_login_window(self):
        """Create and show login window"""
        self.root = tk.Tk()
        self.root.title("🔐 Secure Password Generator - Welcome")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)

        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

    def setup_ui(self):
        tk.Label(self.root, text="Welcome", font=("Arial", 24, "bold"),
                 fg="#00ff88", bg="#1a1a1a").pack(pady=20)

        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(pady=10)

        tk.Label(frame, text="Username", font=("Arial", 11),
                 fg="white", bg="#1a1a1a").pack(pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(frame, textvariable=self.username_var,
                                       width=30, font=("Arial", 11),
                                       bg="#404040", fg="white",
                                       insertbackground="white", relief="flat", bd=5)
        self.username_entry.pack(pady=5)
        self.username_entry.bind("<Return>", self.focus_password)

        tk.Label(frame, text="Password", font=("Arial", 11),
                 fg="white", bg="#1a1a1a").pack(pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(frame, textvariable=self.password_var,
                                       width=30, font=("Arial", 11),
                                       bg="#404040", fg="white",
                                       insertbackground="white", relief="flat", bd=5, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", self.auto_login)

        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Sign Up", command=self.sign_up,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  relief="flat", padx=20, pady=8, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Login", command=self.login,
                  bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                  relief="flat", padx=20, pady=8, cursor="hand2").pack(side="left", padx=10)

        instructions = tk.Text(self.root, height=3, width=45,
                               font=("Arial", 9), fg="#cccccc", bg="#2a2a2a",
                               relief="flat", bd=5, wrap="word")
        instructions.pack(pady=10)
        instructions.insert("1.0",
            "• New user? Enter username and password, then click Sign Up\n"
            "• Returning user? Enter password only, then click Login\n"
            "• Use Enter to navigate between fields")
        instructions.config(state="disabled")

        self.username_entry.focus_set()

    def focus_password(self, event):
        if self.username_var.get().strip():
            self.password_entry.focus_set()
        else:
            messagebox.showwarning("Missing Username", "Please enter your username first.")

    def auto_login(self, event):
        if self.username_var.get().strip() and self.password_var.get().strip():
            self.sign_up()
        elif self.password_var.get().strip():
            self.login()
        else:
            messagebox.showwarning("Missing Info", "Please enter your credentials.")

    def sign_up(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter both username and password.")
            return
        success, msg = self.auth.create_account(username, password)
        messagebox.showinfo("Sign Up", msg)
        if success:
            self.root.destroy()
            self.on_success_callback(self.auth.current_user)

    def login(self):
        password = self.password_var.get().strip()
        if not password:
            messagebox.showwarning("Missing Info", "Please enter your password.")
            return
        success, msg = self.auth.login(password)
        if success:
            messagebox.showinfo("Login", msg)
            self.root.destroy()
            self.on_success_callback(self.auth.current_user)
        else:
            messagebox.showerror("Login Failed", msg)