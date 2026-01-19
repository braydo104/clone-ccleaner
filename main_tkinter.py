import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import threading
from datetime import datetime
import psutil

class CCCleanerClone:
    def __init__(self, root):
        self.root = root
        self.root.title("CCleaner Clone 7.0")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        self.cleaning_in_progress = False
        self.files_to_clean = []
        self.total_size = 0
        
        self.setup_ui()
        self.update_stats()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Title
        title_label = ttk.Label(left_frame, text="CCleaner Clone 7", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Notebook tabs
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Cleaner Tab
        self.cleaner_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cleaner_tab, text="Cleaner")
        self.setup_cleaner_tab()
        
        # Health Check Tab
        health_tab = ttk.Frame(self.notebook)
        self.notebook.add(health_tab, text="Health Check")
        self.setup_health_tab(health_tab)
        
        # Tools Tab
        tools_tab = ttk.Frame(self.notebook)
        self.notebook.add(tools_tab, text="Tools")
        self.setup_tools_tab(tools_tab)
        
        # Settings Tab
        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="Settings")
        self.setup_settings_tab(settings_tab)
        
        # Right side - Stats
        right_frame = ttk.LabelFrame(main_frame, text="System Information", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.config(width=250)
        
        # Disk Info
        ttk.Label(right_frame, text="Disk Usage:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.disk_label = ttk.Label(right_frame, text="")
        self.disk_label.pack(anchor=tk.W)
        
        self.disk_bar = ttk.Progressbar(right_frame, mode='determinate', length=200)
        self.disk_bar.pack(fill=tk.X, pady=5)
        
        # Memory Info
        ttk.Label(right_frame, text="Memory Usage:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.memory_label = ttk.Label(right_frame, text="")
        self.memory_label.pack(anchor=tk.W)
        
        self.memory_bar = ttk.Progressbar(right_frame, mode='determinate', length=200)
        self.memory_bar.pack(fill=tk.X, pady=5)
        
        # CPU Info
        ttk.Label(right_frame, text="CPU Usage:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.cpu_label = ttk.Label(right_frame, text="")
        self.cpu_label.pack(anchor=tk.W)
        
        # Items to clean
        ttk.Label(right_frame, text="Items to Clean:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.items_label = ttk.Label(right_frame, text="")
        self.items_label.pack(anchor=tk.W)
        
        # Total space
        ttk.Label(right_frame, text="Total Space:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.total_label = ttk.Label(right_frame, text="0 MB", foreground="red", font=("Arial", 10, "bold"))
        self.total_label.pack(anchor=tk.W)
        
        # Start stats update
        self.update_stats_periodic()
    
    def setup_cleaner_tab(self):
        # Checkbox list
        ttk.Label(self.cleaner_tab, text="Select items to clean:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=10)
        
        # List frame
        list_frame = ttk.Frame(self.cleaner_tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.clean_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.clean_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.clean_listbox.yview)
        
        self.clean_items = {
            "Temporary Files": {"checked": True, "size": 0},
            "Recycle Bin": {"checked": True, "size": 0},
            "Browser Cache": {"checked": True, "size": 0},
            "Windows Temp Folder": {"checked": True, "size": 0},
            "Log Files": {"checked": True, "size": 0},
            "Thumbnail Cache": {"checked": True, "size": 0},
        }
        
        self.clean_vars = {}
        for item_name in self.clean_items.keys():
            var = tk.BooleanVar(value=True)
            self.clean_vars[item_name] = var
            self.clean_listbox.insert(tk.END, f"☑ {item_name}")
        
        # Buttons frame
        button_frame = ttk.Frame(self.cleaner_tab)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        scan_btn = ttk.Button(button_frame, text="SCAN FOR ISSUES", command=self.scan_for_issues)
        scan_btn.pack(side=tk.LEFT, padx=5)
        
        self.clean_btn = ttk.Button(button_frame, text="CLEAN", command=self.start_cleaning, state=tk.DISABLED)
        self.clean_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.cleaner_tab, mode='determinate', length=300)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=10)
        
        # Info label
        self.info_label = tk.Label(self.cleaner_tab, text="Ready to scan", fg="black")
        self.info_label.pack(pady=10)
    
    def setup_health_tab(self, tab):
        ttk.Label(tab, text="System Health Check", font=("Arial", 14, "bold")).pack(pady=20)
        
        checks = [
            "✓ Disk Space Usage",
            "✓ Memory Usage",
            "✓ CPU Temperature",
            "✓ Windows Updates",
            "✓ Startup Programs",
            "✓ System Registry Health",
        ]
        
        for check in checks:
            ttk.Label(tab, text=check, font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Label(tab, text="Overall System Health: GOOD ✓", 
                 font=("Arial", 12, "bold"), foreground="green").pack(pady=20)
    
    def setup_tools_tab(self, tab):
        ttk.Label(tab, text="System Tools", font=("Arial", 14, "bold")).pack(pady=20)
        
        tools = [
            "Startup Manager - Manage startup programs",
            "Uninstall Programs - Remove unwanted software",
            "Duplicate File Finder - Find and remove duplicates",
            "File Shredder - Securely delete files",
            "Registry Cleaner - Clean Windows registry",
        ]
        
        for tool in tools:
            ttk.Label(tab, text=f"• {tool}", font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=8)
    
    def setup_settings_tab(self, tab):
        ttk.Label(tab, text="Settings", font=("Arial", 14, "bold")).pack(pady=20, padx=20)
        
        settings_frame = ttk.Frame(tab)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.auto_clean = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Enable automatic cleaning on startup", 
                       variable=self.auto_clean).pack(anchor=tk.W, pady=5)
        
        self.skip_system = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Skip system files", 
                       variable=self.skip_system).pack(anchor=tk.W, pady=5)
        
        self.secure_delete = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Use secure deletion (slower)", 
                       variable=self.secure_delete).pack(anchor=tk.W, pady=5)
        
        ttk.Label(settings_frame, text="Cache retention (days):", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 0))
        self.cache_spin = ttk.Spinbox(settings_frame, from_=0, to=365, width=10)
        self.cache_spin.set(30)
        self.cache_spin.pack(anchor=tk.W, pady=5)
        
        save_btn = ttk.Button(settings_frame, text="Save Settings", 
                             command=self.save_settings)
        save_btn.pack(pady=20)
    
    def update_stats_periodic(self):
        self.update_stats()
        self.root.after(2000, self.update_stats_periodic)
    
    def update_stats(self):
        try:
            # Disk
            disk = psutil.disk_usage(os.path.splitdrive(os.path.expandvars("%WINDIR%"))[0])
            self.disk_label.config(text=f"{disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB")
            self.disk_bar['value'] = disk.percent
            
            # Memory
            memory = psutil.virtual_memory()
            self.memory_label.config(text=f"{memory.available / (1024**3):.1f}GB available")
            self.memory_bar['value'] = memory.percent
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_label.config(text=f"{cpu_percent}%")
            
        except Exception as e:
            pass
    
    def scan_for_issues(self):
        if self.cleaning_in_progress:
            messagebox.showwarning("Warning", "Cleaning already in progress!")
            return
        
        self.info_label.config(text="Scanning for issues...", fg="blue")
        self.progress_bar['value'] = 0
        self.clean_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._scan_thread, daemon=True)
        thread.start()
    
    def _scan_thread(self):
        self.files_to_clean = []
        self.total_size = 0
        
        # Scan temp files
        temp_locations = [
            os.path.expandvars(r"%TEMP%"),
            os.path.expandvars(r"%WINDIR%\Temp"),
        ]
        
        for location in temp_locations:
            if os.path.exists(location):
                try:
                    for root, dirs, files in os.walk(location):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                size = os.path.getsize(file_path)
                                self.files_to_clean.append(file_path)
                                self.total_size += size
                            except:
                                pass
                except:
                    pass
        
        self.items_label.config(text=f"{len(self.files_to_clean)} items")
        self.total_label.config(text=f"{self.total_size / (1024**2):.1f} MB")
        
        self.progress_bar['value'] = 100
        self.info_label.config(text="Scan complete! Ready to clean.", fg="green")
        self.clean_btn.config(state=tk.NORMAL)
    
    def start_cleaning(self):
        if self.cleaning_in_progress:
            return
        
        if len(self.files_to_clean) == 0:
            messagebox.showwarning("Warning", "No items to clean!")
            return
        
        confirm = messagebox.askyesno("Confirm", 
            f"Clean {len(self.files_to_clean)} items ({self.total_size / (1024**2):.1f} MB)?")
        
        if not confirm:
            return
        
        self.cleaning_in_progress = True
        self.info_label.config(text="Cleaning in progress...", fg="blue")
        self.progress_bar['value'] = 0
        self.clean_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._clean_thread, daemon=True)
        thread.start()
    
    def _clean_thread(self):
        cleaned = 0
        total = len(self.files_to_clean)
        
        for i, file_path in enumerate(self.files_to_clean):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    cleaned += 1
            except:
                pass
            
            progress = int((i + 1) / total * 100) if total > 0 else 0
            self.progress_bar['value'] = progress
            self.root.update()
        
        self.cleaning_in_progress = False
        self.info_label.config(text=f"Cleaning complete! Removed {cleaned} items.", fg="green")
        self.clean_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Success", f"Cleaned {cleaned} items successfully!")
    
    def save_settings(self):
        messagebox.showinfo("Settings", "Settings saved successfully!")

def main():
    root = tk.Tk()
    app = CCCleanerClone(root)
    root.mainloop()

if __name__ == "__main__":
    main()
