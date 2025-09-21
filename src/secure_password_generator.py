import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk
from tkinter import messagebox, simpledialog
import secrets
import string
import datetime
from auth_system import AuthenticationSystem, LoginWindow

class SecurePasswordGenerator:
    def __init__(self):
        # Start with login screen
        print("🚀 Starting Secure Password Generator...")
        LoginWindow(self.on_login_success)
    
    def on_login_success(self, auth_system):
        """Called when user successfully logs in"""
        self.auth = auth_system
        self.setup_main_app()
    
    def setup_main_app(self):
        """Setup the main password generator application"""
        self.app = tk.Tk()
        self.app.geometry("520x650")
        self.app.title(f"🔐 Password Generator - {self.auth.current_user}")
        self.app.configure(bg="#2b2b2b")
        self.app.resizable(True, True)
        self.setup_ui()
        self.center_window()
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()
    
    def center_window(self):
        """Center window on screen"""
        self.app.update_idletasks()
        x = (self.app.winfo_screenwidth() // 2) - (self.app.winfo_width() // 2)
        y = (self.app.winfo_screenheight() // 2) - (self.app.winfo_height() // 2)
        self.app.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        """Setup main application UI"""
        # Header with user info
        header_frame = tk.Frame(self.app, bg="#1a1a1a", relief="ridge", bd=1)
        header_frame.pack(fill="x", pady=(0,10))
        
        user_label = tk.Label(header_frame, 
                             text=f"👋 Welcome, {self.auth.current_user_name}!", 
                             font=("Arial", 12, "bold"), fg="#00ff88", bg="#1a1a1a")
        user_label.pack(side="left", padx=10, pady=5)
        
        email_label = tk.Label(header_frame, 
                              text=f"📧 {self.auth.current_user}", 
                              font=("Arial", 9), fg="#cccccc", bg="#1a1a1a")
        email_label.pack(side="left", padx=5, pady=5)
        
        logout_btn = tk.Button(header_frame, text="🚪 Logout", 
                              command=self.logout,
                              bg="#f44336", fg="white", 
                              font=("Arial", 9), relief="flat", 
                              padx=10, pady=2, cursor="hand2")
        logout_btn.pack(side="right", padx=10, pady=5)

        # Title
        title = tk.Label(self.app, text="🔐 Password Generator", 
                        font=("Arial", 22, "bold"), 
                        fg="#00ff88", bg="#2b2b2b")
        title.pack(pady=15)
        
        # Length frame
        length_frame = tk.Frame(self.app, bg="#2b2b2b")
        length_frame.pack(pady=10)
        
        tk.Label(length_frame, text="Password Length:", 
                font=("Arial", 12), fg="white", bg="#2b2b2b").pack()
        
        self.length_var = tk.IntVar(value=16)
        self.length_label = tk.Label(length_frame, text="16", 
                                    font=("Arial", 14, "bold"), 
                                    fg="#00ff88", bg="#2b2b2b")
        self.length_label.pack(pady=5)
        
        length_slider = tk.Scale(length_frame, from_=8, to=64, 
                               orient="horizontal", variable=self.length_var,
                               command=self.update_length_label,
                               bg="#404040", fg="white", 
                               highlightbackground="#2b2b2b",
                               troughcolor="#606060", length=300)
        length_slider.pack()
        
        # Options frame
        options_frame = tk.LabelFrame(self.app, text="Character Options", 
                                     font=("Arial", 11, "bold"),
                                     fg="#00ff88", bg="#2b2b2b", 
                                     relief="ridge", bd=2)
        options_frame.pack(pady=15, padx=20, fill="x")
        
        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        
        checkbox_frame = tk.Frame(options_frame, bg="#2b2b2b")
        checkbox_frame.pack(pady=8, padx=10)
        
        tk.Checkbutton(checkbox_frame, text="🔤 Uppercase (A-Z)", 
                      variable=self.include_upper, fg="white", bg="#2b2b2b",
                      selectcolor="#404040", font=("Arial", 9),
                      activebackground="#2b2b2b", activeforeground="white").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        tk.Checkbutton(checkbox_frame, text="🔡 Lowercase (a-z)", 
                      variable=self.include_lower, fg="white", bg="#2b2b2b",
                      selectcolor="#404040", font=("Arial", 9),
                      activebackground="#2b2b2b", activeforeground="white").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        tk.Checkbutton(checkbox_frame, text="🔢 Numbers (0-9)", 
                      variable=self.include_numbers, fg="white", bg="#2b2b2b",
                      selectcolor="#404040", font=("Arial", 9),
                      activebackground="#2b2b2b", activeforeground="white").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        tk.Checkbutton(checkbox_frame, text="🔣 Symbols (!@#$%)", 
                      variable=self.include_symbols, fg="white", bg="#2b2b2b",
                      selectcolor="#404040", font=("Arial", 9),
                      activebackground="#2b2b2b", activeforeground="white").grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Generate button
        generate_btn = tk.Button(self.app, text="🎲 Generate Secure Password", 
                               command=self.generate, 
                               bg="#4CAF50", fg="white", 
                               font=("Arial", 13, "bold"),
                               relief="flat", padx=15, pady=10,
                               cursor="hand2")
        generate_btn.pack(pady=15)
        
        # Result frame
        result_frame = tk.LabelFrame(self.app, text="Generated Password", 
                                   font=("Arial", 10, "bold"),
                                   fg="#00ff88", bg="#2b2b2b", 
                                   relief="ridge", bd=2)
        result_frame.pack(pady=10, padx=20, fill="x")
        
        self.result_var = tk.StringVar()
        result_entry = tk.Entry(result_frame, textvariable=self.result_var, 
                              width=45, font=("Courier", 11),
                              bg="#404040", fg="#00ff88", 
                              insertbackground="white",
                              relief="flat", bd=5)
        result_entry.pack(pady=8, padx=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.app, bg="#2b2b2b")
        buttons_frame.pack(pady=15)
        
        copy_btn = tk.Button(buttons_frame, text="📋 Copy", 
                           command=self.copy_password,
                           bg="#2196F3", fg="white", 
                           font=("Arial", 10, "bold"), 
                           relief="flat", padx=15, pady=6,
                           cursor="hand2", width=8)
        copy_btn.pack(side="left", padx=8)
        
        clear_btn = tk.Button(buttons_frame, text="🗑️ Clear", 
                            command=self.clear_password,
                            bg="#f44336", fg="white", 
                            font=("Arial", 10, "bold"), 
                            relief="flat", padx=15, pady=6,
                            cursor="hand2", width=8)
        clear_btn.pack(side="left", padx=8)
        
        save_btn = tk.Button(buttons_frame, text="💾 Save", 
                           command=self.save_password,
                           bg="#9C27B0", fg="white", 
                           font=("Arial", 10, "bold"), 
                           relief="flat", padx=15, pady=6,
                           cursor="hand2", width=8)
        save_btn.pack(side="left", padx=8)
        
        view_btn = tk.Button(buttons_frame, text="👁️ View", 
                           command=self.view_saved_passwords,
                           bg="#FF9800", fg="white", 
                           font=("Arial", 10, "bold"), 
                           relief="flat", padx=15, pady=6,
                           cursor="hand2", width=8)
        view_btn.pack(side="left", padx=8)
        
        # Status label
        self.status_label = tk.Label(self.app, text="Ready to generate password", 
                                   font=("Arial", 9), fg="#888888", bg="#2b2b2b")
        self.status_label.pack(pady=5)
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def generate(self):
        chars = ""
        if self.include_upper.get(): 
            chars += string.ascii_uppercase
        if self.include_lower.get(): 
            chars += string.ascii_lowercase  
        if self.include_numbers.get(): 
            chars += string.digits
        if self.include_symbols.get(): 
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            messagebox.showwarning("⚠️ Warning", "Please select at least one character type!")
            return
            
        length = self.length_var.get()
        password = ''.join(secrets.choice(chars) for _ in range(length))
        self.result_var.set(password)
        
        strength = self.calculate_strength(password)
        self.status_label.config(text=f"Generated! Strength: {strength}")
    
    def calculate_strength(self, password):
        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
        
        if score <= 2: return "🔴 Weak"
        elif score <= 4: return "🟡 Medium"
        elif score <= 5: return "🟢 Strong"
        else: return "💚 Very Strong"
    
    def copy_password(self):
        password = self.result_var.get()
        if password:
            self.app.clipboard_clear()
            self.app.clipboard_append(password)
            self.status_label.config(text="📋 Password copied to clipboard!")
        else:
            messagebox.showwarning("⚠️ Warning", "No password to copy!")
    
    def clear_password(self):
        self.result_var.set("")
        self.status_label.config(text="🗑️ Password cleared")
    
    def save_password(self):
        password = self.result_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to save!")
            return
        
        # Get website/service name
        website = simpledialog.askstring("Save Password", "Enter website/service name:")
        if not website:
            return
        
        username = simpledialog.askstring("Save Password", "Enter username/email (optional):")
        
        # Save to user's account
        users = self.auth.load_users()
        user_data = users[self.auth.current_user]
        
        saved_entry = {
            'website': website,
            'username': username or '',
            'password': password,  # In production, encrypt this
            'created': str(datetime.datetime.now()),
            'strength': self.calculate_strength(password)
        }
        
        user_data.setdefault('saved_passwords', []).append(saved_entry)
        users[self.auth.current_user] = user_data
        self.auth.save_users(users)
        
        messagebox.showinfo("Saved", f"Password saved for {website}!")
        self.status_label.config(text=f"💾 Password saved for {website}")
    
    def view_saved_passwords(self):
        """View saved passwords in a simple list format"""
        users = self.auth.load_users()
        user_data = users[self.auth.current_user]
        saved_passwords = user_data.get('saved_passwords', [])
        
        if not saved_passwords:
            messagebox.showinfo("No Passwords", "No saved passwords found.")
            return
        
        # Create simple view window
        view_window = tk.Toplevel(self.app)
        view_window.title("💾 Saved Passwords")
        view_window.geometry("500x400")
        view_window.configure(bg="#2b2b2b")
        
        # Title
        tk.Label(view_window, text="💾 Your Saved Passwords", 
                font=("Arial", 16, "bold"), 
                fg="#00ff88", bg="#2b2b2b").pack(pady=10)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(view_window, bg="#2b2b2b")
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        text_widget = tk.Text(text_frame, bg="#404040", fg="white", 
                             font=("Courier", 10), wrap="word")
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Display passwords
        content = ""
        for i, entry in enumerate(saved_passwords, 1):
            content += f"═══════════════════════════════════════\n"
            content += f"🌐 Website: {entry['website']}\n"
            content += f"👤 Username: {entry.get('username', 'N/A')}\n"
            content += f"🔑 Password: {entry['password']}\n"
            content += f"💪 Strength: {entry.get('strength', 'Unknown')}\n"
            content += f"📅 Created: {entry['created'][:19]}\n"
            content += f"═══════════════════════════════════════\n\n"
        
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")  # Make read-only
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_btn = tk.Button(view_window, text="✖️ Close", 
                             command=view_window.destroy,
                             bg="#f44336", fg="white", 
                             font=("Arial", 10, "bold"), 
                             relief="flat", padx=20, pady=5)
        close_btn.pack(pady=10)
    
    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.app.destroy()
            # Restart login screen
            SecurePasswordGenerator()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.app.destroy()

# Run the application
if __name__ == "__main__":
    SecurePasswordGenerator()