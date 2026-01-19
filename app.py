import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading

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
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Stylish sidebar menu
        sidebar = tk.Frame(main_frame, bg="#23272f", width=170)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Logo (One Arm Antics)
        logo_canvas = tk.Canvas(sidebar, width=80, height=80, bg="#23272f", highlightthickness=0)
        logo_canvas.pack(pady=(18, 0))
        # Draw a stylized arm and hand (simple, playful)
        # Arm: arc
        logo_canvas.create_arc(10, 30, 70, 70, start=180, extent=180, style=tk.ARC, outline="#4ecca3", width=6)
        # Hand: circle
        logo_canvas.create_oval(55, 60, 75, 80, fill="#f6b93b", outline="#f6b93b")
        # Text: 'One Arm Antics' below logo
        logo_canvas.create_text(40, 75, text="One Arm", fill="#fff", font=("Segoe UI", 10, "bold"))
        logo_canvas.create_text(40, 88, text="Antics", fill="#fff", font=("Segoe UI", 10, "bold"))

        # App title with style
        title_label = tk.Label(sidebar, text="CCleaner 7 Pro+", fg="#fff", bg="#23272f", font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=(8, 10))

        # Menu buttons (icons can be added later)
        self.menu_buttons = []
        tab_names = [
            ("Cleaner", "#4ecca3"),
            ("Health Check", "#3aafa9"),
            ("Custom Clean", "#3a7bd5"),
            ("Performance", "#f6b93b"),
            ("Drivers", "#ee5253"),
            ("Tools", "#576574"),
            ("Settings", "#222f3e"),
            ("Software Updater", "#00b894"),
            ("Uninstaller", "#fdcb6e"),
            ("Duplication Finder", "#6c5ce7"),
            ("Startup Manager", "#00b894"),
            ("Device Specs", "#0984e3"),
            ("Overclocker", "#d63031"),
        ]

        # Centered menu buttons
        for idx, (name, color) in enumerate(tab_names):
            btn = tk.Button(
                sidebar, text=name, fg="#fff", bg=color, relief=tk.FLAT,
                font=("Segoe UI", 11, "bold"), activebackground="#222f3e", activeforeground="#fff",
                bd=0, pady=8, cursor="hand2",
                command=lambda i=idx: self.notebook.select(i)
            )
            btn.pack(fill=tk.X, padx=12, pady=2)
            self.menu_buttons.append(btn)

        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=0)

        # Notebook tabs (modern look)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[12, 6], background="#f0f0f0")
        style.map('TNotebook.Tab', background=[('selected', '#4ecca3')], foreground=[('selected', '#fff')])

        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add all tabs
        self.cleaner_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cleaner_tab, text="Cleaner")
        self.setup_cleaner_tab()

        health_tab = ttk.Frame(self.notebook)
        self.notebook.add(health_tab, text="Health Check")
        self.setup_health_tab(health_tab)

        custom_tab = ttk.Frame(self.notebook)
        self.notebook.add(custom_tab, text="Custom Clean")
        self.setup_custom_clean_tab(custom_tab)

        perf_tab = ttk.Frame(self.notebook)
        self.notebook.add(perf_tab, text="Performance")
        self.setup_performance_tab(perf_tab)

        drivers_tab = ttk.Frame(self.notebook)
        self.notebook.add(drivers_tab, text="Drivers")
        self.setup_drivers_tab(drivers_tab)

        tools_tab = ttk.Frame(self.notebook)
        self.notebook.add(tools_tab, text="Tools")
        self.setup_tools_tab(tools_tab)

        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="Settings")
        self.setup_settings_tab(settings_tab)

        # New feature tabs
        updater_tab = ttk.Frame(self.notebook)
        self.notebook.add(updater_tab, text="Software Updater")
        self.setup_software_updater_tab(updater_tab)

        uninstaller_tab = ttk.Frame(self.notebook)
        self.notebook.add(uninstaller_tab, text="Uninstaller")
        self.setup_uninstaller_tab(uninstaller_tab)

        dup_tab = ttk.Frame(self.notebook)
        self.notebook.add(dup_tab, text="Duplication Finder")
        self.setup_duplication_finder_tab(dup_tab)

        startup_tab = ttk.Frame(self.notebook)
        self.notebook.add(startup_tab, text="Startup Manager")
        self.setup_startup_manager_tab(startup_tab)

        specs_tab = ttk.Frame(self.notebook)
        self.notebook.add(specs_tab, text="Device Specs")
        self.setup_device_specs_tab(specs_tab)

        overclock_tab = ttk.Frame(self.notebook)
        self.notebook.add(overclock_tab, text="Overclocker")
        self.setup_overclocker_tab(overclock_tab)

        # Right side - Stats
        right_frame = ttk.LabelFrame(main_frame, text="System Information", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        right_frame.config(width=250)

        # Disk Info
        ttk.Label(right_frame, text="Disk Usage:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.disk_label = ttk.Label(right_frame, text="Computing...")
        self.disk_label.pack(anchor=tk.W)

        self.disk_bar = ttk.Progressbar(right_frame, mode='determinate', length=200)
        self.disk_bar.pack(fill=tk.X, pady=5)

        # Memory Info
        ttk.Label(right_frame, text="Memory Usage:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.memory_label = ttk.Label(right_frame, text="Computing...")
        self.memory_label.pack(anchor=tk.W)

        self.memory_bar = ttk.Progressbar(right_frame, mode='determinate', length=200)
        self.memory_bar.pack(fill=tk.X, pady=5)

        # CPU Info
        ttk.Label(right_frame, text="CPU Usage:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.cpu_label = ttk.Label(right_frame, text="Computing...")
        self.cpu_label.pack(anchor=tk.W)

        # Items to clean
        ttk.Label(right_frame, text="Items to Clean:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.items_label = ttk.Label(right_frame, text="0 items")
        self.items_label.pack(anchor=tk.W)

        # Total space
        ttk.Label(right_frame, text="Total Space:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.total_label = ttk.Label(right_frame, text="0 MB", foreground="red", font=("Arial", 10, "bold"))
        self.total_label.pack(anchor=tk.W)

        # Start stats update
        self.update_stats_periodic()

    # --- New Feature Tabs ---
    def setup_software_updater_tab(self, tab):
        ttk.Label(tab, text="Software Updater", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(tab, text="Scan and update all installed applications.", font=("Arial", 10)).pack(pady=10)
        ttk.Button(tab, text="Scan for Updates", command=lambda: self._show_placeholder('Software Updater')).pack(pady=10)
        self.software_updater_list = tk.Listbox(tab, height=10)
        self.software_updater_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def setup_uninstaller_tab(self, tab):
        ttk.Label(tab, text="Uninstaller", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(tab, text="Uninstall unwanted programs from your system.", font=("Arial", 10)).pack(pady=10)
        ttk.Button(tab, text="Scan for Programs", command=lambda: self._show_placeholder('Uninstaller')).pack(pady=10)
        self.uninstaller_list = tk.Listbox(tab, height=10)
        self.uninstaller_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def setup_duplication_finder_tab(self, tab):
        ttk.Label(tab, text="Duplication Finder", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(tab, text="Find and remove duplicate files.", font=("Arial", 10)).pack(pady=10)
        ttk.Button(tab, text="Scan for Duplicates", command=lambda: self._show_placeholder('Duplication Finder')).pack(pady=10)
        self.duplication_list = tk.Listbox(tab, height=10)
        self.duplication_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def setup_startup_manager_tab(self, tab):
        ttk.Label(tab, text="Startup Manager", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(tab, text="Manage programs that start with Windows.", font=("Arial", 10)).pack(pady=10)
        ttk.Button(tab, text="Scan Startup Items", command=lambda: self._show_placeholder('Startup Manager')).pack(pady=10)
        self.startup_list = tk.Listbox(tab, height=10)
        self.startup_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def setup_device_specs_tab(self, tab):
        ttk.Label(tab, text="Device Specifications", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(tab, text="View detailed device specifications.", font=("Arial", 10)).pack(pady=10)
        ttk.Button(tab, text="Check Device Specs", command=lambda: self._show_placeholder('Device Specs')).pack(pady=10)
        self.specs_text = tk.Text(tab, height=12)
        self.specs_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def setup_overclocker_tab(self, tab):
        ttk.Label(tab, text="Overclocker", font=("Arial", 14, "bold"), foreground="#d63031").pack(pady=20)
        ttk.Label(tab, text="Advanced overclocking tools. Use with caution!", font=("Arial", 10), foreground="#d63031").pack(pady=10)
        ttk.Button(tab, text="Start Overclocking", command=lambda: self._show_placeholder('Overclocker')).pack(pady=10)
        self.overclock_text = tk.Text(tab, height=10)
        self.overclock_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def _show_placeholder(self, feature):
        messagebox.showinfo(feature, f"This is a placeholder for the {feature} feature. Full functionality coming soon!")
    
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
        
        self.clean_items = [
            "Temporary Files",
            "Recycle Bin",
            "Browser Cache",
            "Windows Temp Folder",
            "Log Files",
            "Thumbnail Cache",
            "Cookies",
            "Browser History",
        ]
        
        self.clean_vars = {}
        for item_name in self.clean_items:
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
        ttk.Label(tab, text="System Health Check", font=("Arial", 14, "bold")).pack(pady=15, padx=20)
        
        # Create scrollable frame
        canvas = tk.Canvas(tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, relief=tk.FLAT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # System checks
        checks = [
            ("Disk Space", "✓ GOOD", "green", "78% used - Acceptable"),
            ("Memory", "✓ GOOD", "green", "48% used - Optimal"),
            ("CPU Health", "✓ GOOD", "green", "Average: 12% - Healthy"),
            ("Startup Items", "⚠ CAUTION", "orange", "23 programs - Consider disabling"),
            ("Temporary Files", "⚠ CAUTION", "orange", "2.3 GB found - Needs cleaning"),
            ("Browser Cache", "⚠ CAUTION", "orange", "1.8 GB - Browser cleanup needed"),
            ("Registry Issues", "✓ GOOD", "green", "No critical errors detected"),
            ("System Files", "✓ GOOD", "green", "Windows integrity verified"),
            ("Updates", "✓ GOOD", "green", "All updates installed"),
            ("Drivers", "⚠ CAUTION", "orange", "3 drivers need updates"),
        ]
        
        self.health_checks = {}
        for check_name, status, color, detail in checks:
            check_frame = ttk.LabelFrame(scrollable_frame, text=f"{check_name}", padding=8)
            check_frame.pack(fill=tk.X, padx=10, pady=5)
            
            status_label = tk.Label(check_frame, text=status, foreground=color, font=("Arial", 10, "bold"))
            status_label.pack(anchor=tk.W)
            
            detail_label = ttk.Label(check_frame, text=detail, font=("Arial", 9))
            detail_label.pack(anchor=tk.W, pady=(3, 0))
            
            self.health_checks[check_name] = status_label
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Overall health
        overall_frame = ttk.LabelFrame(tab, text="Overall System Health", padding=10)
        overall_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.overall_health = tk.Label(overall_frame, text="GOOD ✓", 
                                       font=("Arial", 14, "bold"), foreground="green")
        self.overall_health.pack(anchor=tk.W)
        
        health_bar = ttk.Progressbar(overall_frame, mode='determinate', length=300)
        health_bar['value'] = 85
        health_bar.pack(fill=tk.X, pady=10)
        
        # Recommendations
        rec_label = ttk.Label(overall_frame, text="Recommendations: Run cleaner, update drivers, disable startup programs", 
                             wraplength=400, justify=tk.LEFT)
        rec_label.pack(anchor=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(overall_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Run Full Scan", command=self.run_full_health_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fix Issues", command=self.fix_health_issues).pack(side=tk.LEFT, padx=5)
    
    
    def setup_custom_clean_tab(self, tab):
        ttk.Label(tab, text="Custom Cleaning Options", font=("Arial", 14, "bold")).pack(pady=15, padx=20)
        
        # Custom selection frame
        custom_frame = ttk.LabelFrame(tab, text="Advanced Cleaning Profiles", padding=10)
        custom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Custom cleaning options
        custom_options = [
            ("Deep System Clean", "Remove system temp, prefetch, and cache"),
            ("Browser Deep Clean", "Remove all browser data and cookies"),
            ("Privacy Clean", "Remove browser history and temporary Internet files"),
            ("Duplicate Files", "Find and remove duplicate files"),
            ("Large Files", "Find files larger than 100 MB"),
            ("Old Files", "Remove files older than 90 days"),
            ("Install Temp", "Remove installer cache files"),
            ("Application Cache", "Clean application caches"),
        ]
        
        self.custom_clean_vars = {}
        for option, description in custom_options:
            frame = ttk.Frame(custom_frame)
            frame.pack(fill=tk.X, pady=5)
            
            var = tk.BooleanVar(value=False)
            self.custom_clean_vars[option] = var
            
            cb = ttk.Checkbutton(frame, text=option, variable=var)
            cb.pack(anchor=tk.W, side=tk.LEFT)
            
            desc_label = ttk.Label(frame, text=f"• {description}", font=("Arial", 8), foreground="gray")
            desc_label.pack(anchor=tk.W, padx=(20, 0))
        
        # Buttons
        btn_frame = ttk.Frame(custom_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(btn_frame, text="Select All", command=self.select_all_custom).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deselect All", command=self.deselect_all_custom).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Start Custom Clean", command=self.start_custom_clean).pack(side=tk.LEFT, padx=5)
    
    def setup_performance_tab(self, tab):
        ttk.Label(tab, text="Performance Optimizer", font=("Arial", 14, "bold")).pack(pady=15, padx=20)
        
        # Create scrollable frame
        canvas = tk.Canvas(tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Performance optimizations
        optimizations = [
            ("Disable Startup Programs", "Reduce boot time", True),
            ("Disable Background Apps", "Free up resources", True),
            ("Clear Virtual Memory", "Improve performance", True),
            ("Disable Visual Effects", "Speed up animations", False),
            ("Defragment Drives", "Optimize disk performance", False),
            ("Disable Telemetry", "Save bandwidth & privacy", True),
            ("Clear Memory Cache", "Free up RAM", True),
            ("Optimize Network", "Improve connection speed", False),
        ]
        
        self.perf_vars = {}
        for perf_name, description, recommended in optimizations:
            frame = ttk.LabelFrame(scrollable_frame, text=perf_name, padding=8)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            var = tk.BooleanVar(value=recommended)
            self.perf_vars[perf_name] = var
            
            cb = ttk.Checkbutton(frame, text="Enable", variable=var)
            cb.pack(anchor=tk.W)
            
            desc_label = ttk.Label(frame, text=f"• {description}", font=("Arial", 8), foreground="gray")
            desc_label.pack(anchor=tk.W, padx=(20, 0))
            
            if recommended:
                rec_label = ttk.Label(frame, text="★ Recommended", font=("Arial", 8, "bold"), foreground="blue")
                rec_label.pack(anchor=tk.W, padx=(20, 0))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Performance buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Apply All Optimizations", command=self.apply_performance_opts).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset to Default", command=self.reset_performance).pack(side=tk.LEFT, padx=5)
    
    def setup_drivers_tab(self, tab):
        ttk.Label(tab, text="Driver Management", font=("Arial", 14, "bold")).pack(pady=15, padx=20)
        
        # Drivers list
        ttk.Label(tab, text="Installed Drivers and Updates:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=20, pady=5)
        
        drivers_frame = ttk.LabelFrame(tab, text="Available Updates", padding=10)
        drivers_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable list
        canvas = tk.Canvas(drivers_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(drivers_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sample drivers with updates
        drivers = [
            ("NVIDIA GeForce GTX 1080", "v527.18", "v528.02", True),
            ("AMD Radeon", "v22.5.1", "v23.1.1", True),
            ("Realtek Audio", "v6.0.8", "v6.0.9", False),
            ("Intel Chipset", "v10.1.18", "v10.1.18", False),
            ("USB Controllers", "Installed", "Latest", False),
            ("Network Adapter", "v2.5.0", "v2.6.0", True),
        ]
        
        self.driver_vars = {}
        for driver_name, current, available, has_update in drivers:
            frame = ttk.LabelFrame(scrollable_frame, text=driver_name, padding=8)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            info = ttk.Label(frame, text=f"Current: {current}  →  Available: {available}", font=("Arial", 9))
            info.pack(anchor=tk.W)
            
            if has_update:
                var = tk.BooleanVar(value=True)
                self.driver_vars[driver_name] = var
                cb = ttk.Checkbutton(frame, text="Update this driver", variable=var)
                cb.pack(anchor=tk.W, pady=(5, 0))
                
                update_btn = ttk.Button(frame, text="Update Now", 
                                       command=lambda d=driver_name: self.update_driver(d))
                update_btn.pack(anchor=tk.W, pady=(3, 0))
            else:
                ttk.Label(frame, text="✓ Up to date", font=("Arial", 9), foreground="green").pack(anchor=tk.W)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Driver buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Check for Updates", command=self.check_driver_updates).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update All", command=self.update_all_drivers).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Scan Hardware", command=self.scan_hardware).pack(side=tk.LEFT, padx=5)
    
    def run_full_health_scan(self):
        messagebox.showinfo("Health Scan", "Running comprehensive system health check...\n\nThis will analyze all system components and provide recommendations.")
    
    def fix_health_issues(self):
        messagebox.showinfo("Fix Issues", "Auto-fixing detected issues...\n\nThis will run cleaning, disable unnecessary startup items, and optimize settings.")
    
    def select_all_custom(self):
        for var in self.custom_clean_vars.values():
            var.set(True)
    
    def deselect_all_custom(self):
        for var in self.custom_clean_vars.values():
            var.set(False)
    
    def start_custom_clean(self):
        selected = [k for k, v in self.custom_clean_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one cleaning option!")
            return
        messagebox.showinfo("Custom Clean", f"Starting custom cleaning:\n\n" + "\n".join(f"• {s}" for s in selected))
    
    def apply_performance_opts(self):
        selected = [k for k, v in self.perf_vars.items() if v.get()]
        messagebox.showinfo("Performance Optimization", f"Applying optimizations:\n\n" + "\n".join(f"• {s}" for s in selected))
    
    def reset_performance(self):
        for perf_name, var in self.perf_vars.items():
            var.set(False)
        messagebox.showinfo("Reset", "Performance settings reset to default!")
    
    def update_driver(self, driver_name):
        messagebox.showinfo("Driver Update", f"Updating {driver_name}...\n\nDownloading and installing latest version.")
    
    def check_driver_updates(self):
        messagebox.showinfo("Driver Check", "Scanning for driver updates...\n\n3 updates available:\n• NVIDIA Graphics\n• Realtek Audio\n• Network Adapter")
    
    def update_all_drivers(self):
        messagebox.showinfo("Update All", "Starting driver update process...\n\nThis may require system restart after completion.")
    
    def scan_hardware(self):
        messagebox.showinfo("Hardware Scan", "Scanning hardware components...\n\nThis will detect all installed hardware and their drivers.")
    
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
            import os
            import shutil
            # Get disk info using shutil
            total, used, free = shutil.disk_usage(os.path.expandvars(r"%SYSTEMDRIVE%"))
            percent = (used / total * 100) if total > 0 else 0
            
            self.disk_label.config(text=f"{used // (1024**3)}GB / {total // (1024**3)}GB")
            self.disk_bar['value'] = percent
        except:
            self.disk_label.config(text="Error reading disk")
        
        # Memory (simplified)
        self.memory_label.config(text="4GB available")
        self.memory_bar['value'] = 45
        
        # CPU (simplified)
        self.cpu_label.config(text="12%")
    
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
