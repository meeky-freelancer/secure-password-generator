import tkinter as tk
from tkinter import messagebox
import json
import os
import secrets
import datetime

class AuthenticationSystem:
    def __init__(self):
        # store users.json next to this module for predictable behavior
        self.users_file = os.path.join(os.path.dirname(__file__), "users.json")
        self.current_user = None
        self.current_user_name = None

    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f) or {}
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def save_users(self, users):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2)
        except OSError:
            # In a simple app show an error dialog could be added if needed
            pass

    def generate_simple_id(self):
        """Generate simple user ID"""
        return secrets.token_hex(8)

    def validate_password(self, password):
        """Password must be exactly 4 digits"""
        return (
            len(password) == 4 and password.isdigit()
        )

    def validate_name(self, name):
        """Basic name validation"""
        return len(name.strip()) >= 2 and name.replace(" ", "").isalpha()

class LoginWindow:
    def __init__(self, success_callback):
        self.success_callback = success_callback
        self.auth = AuthenticationSystem()
        self.root = None
        self.name_var = None
        self.password_var = None
        self.name_entry = None
        self.password_entry = None
        self.setup_login_window()

    def setup_login_window(self):
        """Create and show login window"""
        self.root = tk.Tk()
        self.root.title("🔐 Secure Password Generator - Welcome")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)

        # Center window
        self.center_window()

        self.setup_ui()
        self.root.mainloop()

    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def setup_ui(self):
        """Setup login screen UI"""
        # Title
        title = tk.Label(self.root, text="🔐 Welcome",
                        font=("Arial", 28, "bold"),
                        fg="#00ff88", bg="#1a1a1a")
        title.pack(pady=30)

        subtitle = tk.Label(self.root, text="Secure Password Generator",
                           font=("Arial", 14),
                           fg="#cccccc", bg="#1a1a1a")
        subtitle.pack(pady=5)

        # Main frame
        main_frame = tk.LabelFrame(self.root, text="Get Started",
                                  font=("Arial", 12, "bold"),
                                  fg="#00ff88", bg="#1a1a1a",
                                  relief="ridge", bd=2)
        main_frame.pack(pady=30, padx=40, fill="x")

        # Name field
        tk.Label(main_frame, text="Your Name:",
                font=("Arial", 11), fg="white", bg="#1a1a1a").pack(pady=(20, 5))

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(main_frame, textvariable=self.name_var,
                                  width=35, font=("Arial", 11),
                                  bg="#404040", fg="white",
                                  insertbackground="white", relief="flat", bd=5)
        self.name_entry.pack(pady=5)

        # Password field
        tk.Label(main_frame, text="Password:",
                font=("Arial", 11), fg="white", bg="#1a1a1a").pack(pady=(15, 5))

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(main_frame, textvariable=self.password_var, 
                                   width=35, font=("Arial", 11),
                                   bg="#404040", fg="white",
                                   insertbackground="white", relief="flat", bd=5, show="*")
        self.password_entry.pack(pady=5)

        # Bind Enter key events for smart navigation
        self.name_entry.bind('<Return>', self.on_name_enter)
        self.password_entry.bind('<Return>', self.on_password_enter)

        # Set focus to name field initially
        self.name_entry.focus_set()

        # Info text
        info_text = tk.Label(main_frame,
                            text="✨ Use Tab or Enter to navigate between fields!",
                            font=("Arial", 9), fg="#ffaa00", bg="#1a1a1a")
        info_text.pack(pady=(15, 20))

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#1a1a1a")
        buttons_frame.pack(pady=20)

        # Create Account button
        self.create_btn = tk.Button(buttons_frame, text="🚀 Create Account & Start",
                                   command=self.create_account,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 12, "bold"),
                                   relief="flat", padx=30, pady=10,
                                   cursor="hand2")
        self.create_btn.pack(side="left", padx=10)

        # Returning User button
        self.login_btn = tk.Button(buttons_frame, text="👤 I'm a Returning User",
                                  command=self.returning_user,
                                  bg="#2196F3", fg="white",
                                  font=("Arial", 12, "bold"),
                                  relief="flat", padx=30, pady=10,
                                  cursor="hand2")
        self.login_btn.pack(side="left", padx=10)

        # Instructions
        instructions = tk.Text(self.root, height=3, width=50,
                              font=("Arial", 9), fg="#cccccc", bg="#2a2a2a",
                              relief="flat", bd=5, wrap="word")
        instructions.pack(pady=15, padx=20)
        instructions.insert("1.0",
            "🔹 New user? Fill both fields and press Enter to create account\n"
            "🔹 Returning user? Enter password and press Enter twice\n"
            "🔹 Your information is stored locally on your device")
        instructions.config(state="disabled")

    def on_name_enter(self, event):
        """Handle Enter key in name field"""
        if self.name_var.get().strip():
            # Move focus to password field
            self.password_entry.focus_set()
        else:
            messagebox.showwarning("Name Required", "Please enter your name first!")

    def on_password_enter(self, event):
        """Handle Enter key in password field"""
        name = self.name_var.get().strip()
        password = self.password_var.get().strip()

        if not password:
            messagebox.showwarning("Password Required", "Please enter your password first!")
            return

        # Check if this looks like a returning user (password only)
        if not name and password:
            self.returning_user()
        # Check if this looks like a new user (both name and password)
        elif name and password:
            self.create_account()
        # Name filled but no password
        elif name and not password:
            messagebox.showinfo("Password Needed", "Please enter your password!")
        # Neither field filled
        else:
            messagebox.showwarning("Information Required", "Please fill in the required fields!")

    def create_account(self):
        """Handle new user account creation"""
        name = self.name_var.get().strip()
        password = self.password_var.get().strip()

        if not name or not password:
            messagebox.showwarning("Missing Information", "Please enter both name and password!")
            # Focus on the empty field
            if not name:
                self.name_entry.focus_set()
            else:
                self.password_entry.focus_set()
            return

        # Validate name
        if not self.auth.validate_name(name):
            messagebox.showerror("Invalid Name", "Please enter a valid name (letters only, 2+ characters)")
            self.name_entry.focus_set()
            self.name_entry.select_range(0, tk.END)
            return

        # Validate password format
        if not self.auth.validate_password(password):
            messagebox.showerror(
                "Invalid Password",
                "Please enter a valid password (8+ characters, include letters, numbers and a special character)"
            )
            self.password_entry.focus_set()
            self.password_entry.select_range(0, tk.END)
            return

        # Check if user already exists (password is used as key here)
        users = self.auth.load_users()
        if password in users:
            result = messagebox.askyesno("Account Exists",
                f"An account with this password already exists.\n\nWould you like to sign in instead?")
            if result:
                self.returning_user()
            return

        # Create user account
        user_id = self.auth.generate_simple_id()

        users[password] = {
            'name': name,
            'password': password,
            'user_id': user_id,
            'created_date': str(datetime.datetime.now()),
            'saved_passwords': []
        }

        self.auth.save_users(users)
        self.auth.current_user = password
        self.auth.current_user_name = name

        messagebox.showinfo("Welcome!",
            f"Account created successfully!\n\n"
            f"Welcome, {name}!\n"
            f"User ID: {user_id}")

        # Close login window and call success callback
        self.root.destroy()
        self.success_callback(self.auth)

    def returning_user(self):
        """Handle returning user login"""
        password = self.password_var.get().strip()
        name = self.name_var.get().strip()

        if not password:
            messagebox.showwarning("Missing Information", "Please enter password!")
            self.password_entry.focus_set()
            return

        # Load users and check if account exists
        users = self.auth.load_users()

        if password not in users:
            messagebox.showerror("Account Not Found",
                f"No account found for the provided password.\n\nPlease check your password or create a new account.")
            self.password_entry.focus_set()
            self.password_entry.select_range(0, tk.END)
            return

        # Get user data and handle missing name field
        user_data = users[password]

        # Handle old user data that might not have 'name' field or empty name
        if 'name' not in user_data or not user_data.get('name'):
            if not name:
                messagebox.showinfo("Update Required", "Please enter your name to update your account.")
                self.name_entry.focus_set()
                return

            # Update user data with name
            user_data['name'] = name
            user_data['password'] = password
            users[password] = user_data
            self.auth.save_users(users)

        # Successful login
        self.auth.current_user = user_data.get('password', password)
        self.auth.current_user_name = user_data.get('name', '')

        messagebox.showinfo("Welcome Back!",
            f"Welcome back, {self.auth.current_user_name}!\n\n"
            f"Account found.")

        # Close login window and call success callback
        self.root.destroy()
        self.success_callback(self.auth)