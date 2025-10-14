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
        self.app.title(f"🔐 Password Generator - {self.auth.current_user_name}")
        self.app.configure(bg="#2b2b2b")
        self.app.resizable(False, False)
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
                                   fg="#000000", bg="#2b2b2b", 
                                   relief="ridge", bd=2)
        result_frame.pack(pady=10, padx=20, fill="x")
        
        self.result_var = tk.StringVar()
        result_entry = tk.Entry(result_frame, textvariable=self.result_var, 
                              width=45, font=("Courier", 11),
                              bg="#404040", fg="#000000", 
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
        """Save password with website and email/username"""
        password = self.result_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to save!")
            return
        
        # Create a dialog for website and email/username
        save_dialog = tk.Toplevel(self.app)
        save_dialog.title("💾 Save Password")
        save_dialog.geometry("400x250")
        save_dialog.configure(bg="#2b2b2b")
        save_dialog.resizable(False, False)
        
        # Center the dialog
        save_dialog.update_idletasks()
        x = (save_dialog.winfo_screenwidth() // 2) - (save_dialog.winfo_width() // 2)
        y = (save_dialog.winfo_screenheight() // 2) - (save_dialog.winfo_height() // 2)
        save_dialog.geometry(f"+{x}+{y}")
        
        # Make dialog modal
        save_dialog.transient(self.app)
        save_dialog.grab_set()
        
        # Title
        tk.Label(save_dialog, text="💾 Save Password", 
                font=("Arial", 16, "bold"), 
                fg="#00ff88", bg="#2b2b2b").pack(pady=15)
        
        # Website field
        tk.Label(save_dialog, text="🌐 Website/Service:", 
                font=("Arial", 11), fg="white", bg="#2b2b2b").pack(pady=(10,5))
        
        website_var = tk.StringVar()
        website_entry = tk.Entry(save_dialog, textvariable=website_var, 
                               width=35, font=("Arial", 11),
                               bg="#404040", fg="white", 
                               insertbackground="white", relief="flat", bd=5)
        website_entry.pack(pady=5)
        website_entry.focus_set()
        
        # Email/Username field
        tk.Label(save_dialog, text="👤 Email/Username:", 
                font=("Arial", 11), fg="white", bg="#2b2b2b").pack(pady=(15,5))
        
        username_var = tk.StringVar()
        username_entry = tk.Entry(save_dialog, textvariable=username_var, 
                                width=35, font=("Arial", 11),
                                bg="#404040", fg="white", 
                                insertbackground="white", relief="flat", bd=5)
        username_entry.pack(pady=5)
        
        # Buttons
        buttons_frame = tk.Frame(save_dialog, bg="#2b2b2b")
        buttons_frame.pack(pady=20)
        
        def save_and_close():
            website = website_var.get().strip()
            username = username_var.get().strip()
            
            if not website:
                messagebox.showwarning("Missing Info", "Please enter the website/service name!")
                website_entry.focus_set()
                return
            
            if not username:
                messagebox.showwarning("Missing Info", "Please enter your email/username!")
                username_entry.focus_set()
                return
            
            # Save to user's account
            users = self.auth.load_users()
            user_data = users[self.auth.current_user]
            
            saved_entry = {
                'website': website,
                'username': username,
                'password': password,
                'created': str(datetime.datetime.now()),
                'strength': self.calculate_strength(password)
            }
            
            user_data.setdefault('saved_passwords', []).append(saved_entry)
            users[self.auth.current_user] = user_data
            self.auth.save_users(users)
            
            messagebox.showinfo("✅ Saved!", f"Password saved for {website}!")
            self.status_label.config(text=f"💾 Password saved for {website}")
            save_dialog.destroy()
        
        def cancel():
            save_dialog.destroy()
        
        # Enter key binding
        website_entry.bind('<Return>', lambda e: username_entry.focus_set())
        username_entry.bind('<Return>', lambda e: save_and_close())
        
        tk.Button(buttons_frame, text="💾 Save", 
                 command=save_and_close,
                 bg="#4CAF50", fg="white", 
                 font=("Arial", 11, "bold"), 
                 relief="flat", padx=20, pady=8,
                 cursor="hand2").pack(side="left", padx=10)
        
        tk.Button(buttons_frame, text="❌ Cancel", 
                 command=cancel,
                 bg="#f44336", fg="white", 
                 font=("Arial", 11, "bold"), 
                 relief="flat", padx=20, pady=8,
                 cursor="hand2").pack(side="left", padx=10)
    
    def view_saved_passwords(self):
        """View saved passwords with email verification"""
        # Create email verification dialog
        verify_dialog = tk.Toplevel(self.app)
        verify_dialog.title("🔐 Verify Access")
        verify_dialog.geometry("350x200")
        verify_dialog.configure(bg="#2b2b2b")
        verify_dialog.resizable(False, False)
        
        # Center the dialog
        verify_dialog.update_idletasks()
        x = (verify_dialog.winfo_screenwidth() // 2) - (verify_dialog.winfo_width() // 2)
        y = (verify_dialog.winfo_screenheight() // 2) - (verify_dialog.winfo_height() // 2)
        verify_dialog.geometry(f"+{x}+{y}")
        
        # Make dialog modal
        verify_dialog.transient(self.app)
        verify_dialog.grab_set()
        
        # Title
        tk.Label(verify_dialog, text="🔐 Verify Your Identity", 
                font=("Arial", 16, "bold"), 
                fg="#00ff88", bg="#2b2b2b").pack(pady=20)
        
        # Email field
        tk.Label(verify_dialog, text="📧 Enter your email to view saved passwords:", 
                font=("Arial", 10), fg="white", bg="#2b2b2b").pack(pady=(10,5))
        
        email_var = tk.StringVar()
        email_entry = tk.Entry(verify_dialog, textvariable=email_var, 
                              width=30, font=("Arial", 11),
                              bg="#404040", fg="white", 
                              insertbackground="white", relief="flat", bd=5)
        email_entry.pack(pady=10)
        email_entry.focus_set()
        
        def verify_and_show():
            entered_email = email_var.get().strip().lower()
            
            if not entered_email:
                messagebox.showwarning("Missing Email", "Please enter your email!")
                email_entry.focus_set()
                return
            
            # Verify email matches current user
            if entered_email != self.auth.current_user:
                messagebox.showerror("❌ Access Denied", 
                    "Email doesn't match your account! Access denied.")
                email_entry.focus_set()
                email_entry.select_range(0, tk.END)
                return
            
            # Email verified, show passwords
            verify_dialog.destroy()
            self.show_saved_passwords()
        
        def cancel():
            verify_dialog.destroy()
        
        # Enter key binding
        email_entry.bind('<Return>', lambda e: verify_and_show())
        
        # Buttons
        buttons_frame = tk.Frame(verify_dialog, bg="#2b2b2b")
        buttons_frame.pack(pady=15)
        
        tk.Button(buttons_frame, text="✅ Verify", 
                 command=verify_and_show,
                 bg="#4CAF50", fg="white", 
                 font=("Arial", 11, "bold"), 
                 relief="flat", padx=20, pady=8,
                 cursor="hand2").pack(side="left", padx=10)
        
        tk.Button(buttons_frame, text="❌ Cancel", 
                 command=cancel,
                 bg="#f44336", fg="white", 
                 font=("Arial", 11, "bold"), 
                 relief="flat", padx=20, pady=8,
                 cursor="hand2").pack(side="left", padx=10)
    
    def show_saved_passwords(self):
        """Display saved passwords after verification"""
        users = self.auth.load_users()
        user_data = users[self.auth.current_user]
        saved_passwords = user_data.get('saved_passwords', [])
        
        if not saved_passwords:
            messagebox.showinfo("No Passwords", "No saved passwords found.")
            return
        
        # Create passwords view window
        view_window = tk.Toplevel(self.app)
        view_window.title("💾 Your Saved Passwords")
        view_window.geometry("600x450")
        view_window.configure(bg="#2b2b2b")
        
        # Center the window
        view_window.update_idletasks()
        x = (view_window.winfo_screenwidth() // 2) - (view_window.winfo_width() // 2)
        y = (view_window.winfo_screenheight() // 2) - (view_window.winfo_height() // 2)
        view_window.geometry(f"+{x}+{y}")
        
        # Title
        tk.Label(view_window, text=f"💾 Saved Passwords for {self.auth.current_user_name}", 
                font=("Arial", 16, "bold"), 
                fg="#000000", bg="#2b2b2b").pack(pady=15)
        
        # Create scrollable frame
        canvas = tk.Canvas(view_window, bg="#2b2b2b", highlightthickness=0)
        scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2b2b2b")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add saved passwords with better formatting
        for i, entry in enumerate(saved_passwords, 1):
            # Create frame for each password entry
            entry_frame = tk.LabelFrame(scrollable_frame, 
                                       text=f"🌐 {entry['website']}", 
                                       font=("Arial", 12, "bold"),
                                       fg="#00ff88", bg="#2b2b2b",
                                       relief="ridge", bd=2)
            entry_frame.pack(fill="x", padx=15, pady=8)
            
            # Info display
            info_frame = tk.Frame(entry_frame, bg="#2b2b2b")
            info_frame.pack(fill="x", padx=10, pady=8)
            
            # Username/Email
            tk.Label(info_frame, text=f"👤 Username/Email: {entry.get('username', 'N/A')}", 
                    font=("Arial", 10), fg="white", bg="#2b2b2b",
                    anchor="w").pack(fill="x", pady=2)
            
            # Password (hidden by default)
            password_frame = tk.Frame(info_frame, bg="#2b2b2b")
            password_frame.pack(fill="x", pady=5)
            
            tk.Label(password_frame, text="🔑 Password:", 
                    font=("Arial", 10), fg="white", bg="#2b2b2b").pack(side="left")
            
            password_var = tk.StringVar(value="••••••••••••")
            password_display = tk.Entry(password_frame, textvariable=password_var,
                                       font=("Courier", 10), bg="#404040", fg="#000000",
                                       state="readonly", width=25, relief="flat", bd=3)
            password_display.pack(side="left", padx=10)
            
            # Show/Hide button
            def create_toggle_func(pwd=entry['password'], var=password_var):
                def toggle():
                    if var.get() == "••••••••••••":
                        var.set(pwd)
                        toggle_btn.config(text="🙈 Hide")
                    else:
                        var.set("••••••••••••")
                        toggle_btn.config(text="👁️ Show")
                return toggle
            
            toggle_btn = tk.Button(password_frame, text="👁️ Show",
                                  command=create_toggle_func(),
                                  bg="#000000", fg="white", font=("Arial", 8),
                                  relief="flat", padx=8, pady=2, cursor="hand2")
            toggle_btn.pack(side="left", padx=5)
            
            # Additional info
            info_text = f"💪 Strength: {entry.get('strength', 'Unknown')} | 📅 Created: {entry['created'][:19]}"
            tk.Label(info_frame, text=info_text, 
                    font=("Arial", 9), fg="#cccccc", bg="#2b2b2b",
                    anchor="w").pack(fill="x", pady=2)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Close button
        close_btn = tk.Button(view_window, text="✖️ Close", 
                             command=view_window.destroy,
                             bg="#f44336", fg="white", 
                             font=("Arial", 12, "bold"), 
                             relief="flat", padx=25, pady=8,
                             cursor="hand2")
        close_btn.pack(pady=15)
    
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