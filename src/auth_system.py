import tkinter as tk
from tkinter import messagebox
import json
import os
import secrets
import datetime

class AuthenticationSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None
        self.current_user_name = None
        
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def generate_simple_id(self):
        """Generate simple user ID"""
        return secrets.token_hex(8)
    
    def validate_email(self, email):
        """Basic email validation"""
        return "@" in email and "." in email.split("@")[1] and len(email) > 5
    
    def validate_name(self, name):
        """Basic name validation"""
        return len(name.strip()) >= 2 and name.replace(" ", "").isalpha()

class LoginWindow:
    def __init__(self, success_callback):
        self.success_callback = success_callback
        self.auth = AuthenticationSystem()
        self.root = None
        self.name_var = None
        self.email_var = None
        self.name_entry = None
        self.email_entry = None
        self.setup_login_window()
    
    def setup_login_window(self):
        """Create and show login window"""
        self.root = tk.Tk()
        self.root.title("🔐 Secure Password Generator - Welcome")
        self.root.geometry("450x400")
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
                font=("Arial", 11), fg="white", bg="#1a1a1a").pack(pady=(20,5))
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(main_frame, textvariable=self.name_var, 
                                  width=35, font=("Arial", 11),
                                  bg="#404040", fg="white", 
                                  insertbackground="white", relief="flat", bd=5)
        self.name_entry.pack(pady=5)
        
        # Email field
        tk.Label(main_frame, text="Email Address:", 
                font=("Arial", 11), fg="white", bg="#1a1a1a").pack(pady=(15,5))
        
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(main_frame, textvariable=self.email_var, 
                                   width=35, font=("Arial", 11),
                                   bg="#404040", fg="white", 
                                   insertbackground="white", relief="flat", bd=5)
        self.email_entry.pack(pady=5)
        
        # Bind Enter key events for smart navigation
        self.name_entry.bind('<Return>', self.on_name_enter)
        self.email_entry.bind('<Return>', self.on_email_enter)
        
        # Set focus to name field initially
        self.name_entry.focus_set()
        
        # Info text
        info_text = tk.Label(main_frame, 
                            text="✨ Use Tab or Enter to navigate between fields!", 
                            font=("Arial", 9), fg="#ffaa00", bg="#1a1a1a")
        info_text.pack(pady=(15,20))
        
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
            "🔹 Returning user? Enter email and press Enter twice\n"
            "🔹 Your information is stored securely on your device")
        instructions.config(state="disabled")
    
    def on_name_enter(self, event):
        """Handle Enter key in name field"""
        if self.name_var.get().strip():
            # Move focus to email field
            self.email_entry.focus_set()
        else:
            messagebox.showwarning("Name Required", "Please enter your name first!")
    
    def on_email_enter(self, event):
        """Handle Enter key in email field"""
        name = self.name_var.get().strip()
        email = self.email_var.get().strip().lower()
        
        if not email:
            messagebox.showwarning("Email Required", "Please enter your email address!")
            return
        
        # Check if this looks like a returning user (email only)
        if not name and email:
            self.returning_user()
        # Check if this looks like a new user (both name and email)
        elif name and email:
            self.create_account()
        # Name filled but no email
        elif name and not email:
            messagebox.showinfo("Email Needed", "Please enter your email address!")
        # Neither field filled
        else:
            messagebox.showwarning("Information Required", "Please fill in the required fields!")
    
    def create_account(self):
        """Handle new user account creation"""
        name = self.name_var.get().strip()
        email = self.email_var.get().strip().lower()
        
        if not name or not email:
            messagebox.showwarning("Missing Information", "Please enter both name and email!")
            # Focus on the empty field
            if not name:
                self.name_entry.focus_set()
            else:
                self.email_entry.focus_set()
            return
        
        # Validate name
        if not self.auth.validate_name(name):
            messagebox.showerror("Invalid Name", "Please enter a valid name (letters only, 2+ characters)")
            self.name_entry.focus_set()
            self.name_entry.select_range(0, tk.END)
            return
        
        # Validate email format
        if not self.auth.validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address!")
            self.email_entry.focus_set()
            self.email_entry.select_range(0, tk.END)
            return
        
        # Check if user already exists
        users = self.auth.load_users()
        if email in users:
            result = messagebox.askyesno("Account Exists", 
                f"An account with {email} already exists.\n\nWould you like to sign in instead?")
            if result:
                self.returning_user()
            return
        
        # Create user account
        user_id = self.auth.generate_simple_id()
        
        users[email] = {
            'name': name,
            'email': email,
            'user_id': user_id,
            'created_date': str(datetime.datetime.now()),
            'saved_passwords': []
        }
        
        self.auth.save_users(users)
        self.auth.current_user = email
        self.auth.current_user_name = name
        
        messagebox.showinfo("Welcome!", 
            f"Account created successfully!\n\n"
            f"Welcome, {name}!\n"
            f"Email: {email}\n"
            f"User ID: {user_id}")
        
        # Close login window and call success callback
        self.root.destroy()
        self.success_callback(self.auth)
    
    def returning_user(self):
        """Handle returning user login"""
        email = self.email_var.get().strip().lower()
        
        if not email:
            messagebox.showwarning("Missing Email", "Please enter your email address!")
            self.email_entry.focus_set()
            return
        
        # Load users and check if account exists
        users = self.auth.load_users()
        
        if email not in users:
            messagebox.showerror("Account Not Found", 
                f"No account found for {email}.\n\nPlease check your email or create a new account.")
            self.email_entry.focus_set()
            self.email_entry.select_range(0, tk.END)
            return
        
        # Get user data and handle missing name field (backward compatibility)
        user_data = users[email]
        
        # Handle old user data that might not have 'name' field
        if 'name' not in user_data:
            # Ask for name if missing
            name = self.name_var.get().strip()
            if not name:
                messagebox.showinfo("Update Required", "Please enter your name to update your account.")
                self.name_entry.focus_set()
                return
            
            # Update user data with name
            user_data['name'] = name
            users[email] = user_data
            self.auth.save_users(users)
        
        # Successful login
        self.auth.current_user = email
        self.auth.current_user_name = user_data['name']
        
        messagebox.showinfo("Welcome Back!", 
            f"Welcome back, {user_data['name']}!\n\n"
            f"Account found: {email}")
        
        # Close login window and call success callback
        self.root.destroy()
        self.success_callback(self.auth)