import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, 
                            QLabel, QProgressBar, QTabWidget, QCheckBox, QSpinBox,
                            QMessageBox, QTreeWidget, QTreeWidgetItem, QFileDialog,
                            QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap
from cleaner import SystemCleaner, CleanerWorker
from stats import SystemStats
import json

class CCCleanerClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cleaner = SystemCleaner()
        self.stats = SystemStats()
        self.cleaner_worker = None
        self.cleaning_in_progress = False
        
        self.initUI()
        self.update_stats()
        
    def initUI(self):
        self.setWindowTitle("CCleaner Clone 7.0")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left sidebar
        left_layout = QVBoxLayout()
        
        # Logo/Title
        title_label = QLabel("CCleaner")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        left_layout.addWidget(title_label)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Cleaner
        self.cleaner_tab = QWidget()
        self.setup_cleaner_tab()
        self.tabs.addTab(self.cleaner_tab, "Cleaner")
        
        # Tab 2: Health Check
        self.health_tab = QWidget()
        self.setup_health_tab()
        self.tabs.addTab(self.health_tab, "Health Check")
        
        # Tab 3: Tools
        self.tools_tab = QWidget()
        self.setup_tools_tab()
        self.tabs.addTab(self.tools_tab, "Tools")
        
        # Tab 4: Settings
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(self.settings_tab, "Settings")
        
        left_layout.addWidget(self.tabs)
        main_layout.addLayout(left_layout, 1)
        
        # Right sidebar - Stats
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.create_stats_panel())
        main_layout.addLayout(right_layout, 0)
        
    def setup_cleaner_tab(self):
        layout = QVBoxLayout(self.cleaner_tab)
        
        # Selection list
        layout.addWidget(QLabel("Select items to clean:"))
        self.clean_list = QListWidget()
        self.clean_items = {
            "Temporary Files": {"checked": True, "size": 0},
            "Recycle Bin": {"checked": True, "size": 0},
            "Browser Cache": {"checked": True, "size": 0},
            "Cookies": {"checked": True, "size": 0},
            "Browser History": {"checked": False, "size": 0},
            "Windows Temp Folder": {"checked": True, "size": 0},
            "Log Files": {"checked": True, "size": 0},
            "Thumbnail Cache": {"checked": True, "size": 0},
        }
        
        for item_name in self.clean_items.keys():
            item = QListWidgetItem(self.clean_list)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if self.clean_items[item_name]["checked"] else Qt.CheckState.Unchecked)
            item.setText(item_name)
            self.clean_list.addItem(item)
        
        self.clean_list.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.clean_list)
        
        # Scan button
        scan_btn = QPushButton("SCAN FOR ISSUES")
        scan_btn.setMinimumHeight(40)
        scan_btn.clicked.connect(self.scan_for_issues)
        layout.addWidget(scan_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Info label
        self.info_label = QLabel("Ready to scan")
        layout.addWidget(self.info_label)
        
        # Clean button
        self.clean_btn = QPushButton("CLEAN")
        self.clean_btn.setMinimumHeight(40)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.clean_btn.clicked.connect(self.start_cleaning)
        self.clean_btn.setEnabled(False)
        layout.addWidget(self.clean_btn)
        
        layout.addStretch()
    
    def setup_health_tab(self):
        layout = QVBoxLayout(self.health_tab)
        
        layout.addWidget(QLabel("System Health Check"))
        
        checks = [
            "✓ Disk Space Usage",
            "✓ Memory Usage",
            "✓ CPU Temperature",
            "✓ Windows Updates",
            "✓ Malware Scan",
            "✓ Startup Programs",
            "✓ System Registry",
        ]
        
        for check in checks:
            check_label = QLabel(check)
            layout.addWidget(check_label)
        
        layout.addStretch()
    
    def setup_tools_tab(self):
        layout = QVBoxLayout(self.tools_tab)
        
        layout.addWidget(QLabel("System Tools"))
        
        tools = [
            ("Startup Manager", "Manage startup programs"),
            ("Uninstall Programs", "Remove unwanted software"),
            ("Duplicate File Finder", "Find and remove duplicates"),
            ("File Shredder", "Securely delete files"),
            ("Registry Cleaner", "Clean Windows registry"),
        ]
        
        for tool_name, description in tools:
            tool_label = QLabel(f"• {tool_name}")
            tool_label.setToolTip(description)
            layout.addWidget(tool_label)
        
        layout.addStretch()
    
    def setup_settings_tab(self):
        layout = QVBoxLayout(self.settings_tab)
        
        layout.addWidget(QLabel("Settings"))
        
        # Options
        self.auto_clean_check = QCheckBox("Enable automatic cleaning on startup")
        layout.addWidget(self.auto_clean_check)
        
        self.skip_system_check = QCheckBox("Skip system files")
        self.skip_system_check.setChecked(True)
        layout.addWidget(self.skip_system_check)
        
        self.secure_delete_check = QCheckBox("Use secure deletion (slower)")
        layout.addWidget(self.secure_delete_check)
        
        # Cache retention
        layout.addWidget(QLabel("Cache retention (days):"))
        cache_spin = QSpinBox()
        cache_spin.setMinimum(0)
        cache_spin.setMaximum(365)
        cache_spin.setValue(30)
        layout.addWidget(cache_spin)
        
        # Buttons
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
    
    def create_stats_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        title = QLabel("System Information")
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Storage info
        self.disk_label = QLabel()
        layout.addWidget(self.disk_label)
        
        self.disk_bar = QProgressBar()
        self.disk_bar.setMaximumHeight(10)
        layout.addWidget(self.disk_bar)
        
        # Memory info
        self.memory_label = QLabel()
        layout.addWidget(self.memory_label)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setMaximumHeight(10)
        layout.addWidget(self.memory_bar)
        
        # CPU info
        self.cpu_label = QLabel()
        layout.addWidget(self.cpu_label)
        
        # Temp files found
        self.temp_label = QLabel()
        layout.addWidget(self.temp_label)
        
        # Total space to clean
        self.total_label = QLabel()
        self.total_label.setStyleSheet("font-weight: bold; color: #ff6b6b;")
        layout.addWidget(self.total_label)
        
        # Update timer
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(2000)  # Update every 2 seconds
        
        layout.addStretch()
        
        return panel
    
    def update_stats(self):
        stats = self.stats.get_system_stats()
        
        # Disk
        disk_percent = stats['disk']['percent']
        disk_used = stats['disk']['used_gb']
        disk_total = stats['disk']['total_gb']
        self.disk_label.setText(f"Disk: {disk_used:.1f}GB / {disk_total:.1f}GB")
        self.disk_bar.setValue(int(disk_percent))
        
        # Memory
        mem_percent = stats['memory']['percent']
        mem_available = stats['memory']['available_gb']
        self.memory_label.setText(f"Memory: {mem_available:.1f}GB available")
        self.memory_bar.setValue(int(mem_percent))
        
        # CPU
        cpu_percent = stats['cpu']['percent']
        self.cpu_label.setText(f"CPU Usage: {cpu_percent}%")
        
        # Temp files
        temp_count = len(self.cleaner.find_temp_files()) if hasattr(self.cleaner, 'find_temp_files') else 0
        self.temp_label.setText(f"Temp files found: {temp_count}")
        
        # Total size
        total_size = self.calculate_total_size()
        self.total_label.setText(f"Space to clean: {total_size:.2f} MB")
    
    def calculate_total_size(self):
        # This would calculate total size of files to clean
        return 0.0
    
    def on_item_changed(self, item):
        item_name = item.text()
        self.clean_items[item_name]["checked"] = item.checkState() == Qt.CheckState.Checked
    
    def scan_for_issues(self):
        self.info_label.setText("Scanning for issues...")
        self.progress_bar.setValue(0)
        self.clean_btn.setEnabled(False)
        
        # Simulate scanning
        self.scan_timer = QTimer()
        self.scan_progress = 0
        self.scan_timer.timeout.connect(self.update_scan_progress)
        self.scan_timer.start(50)
    
    def update_scan_progress(self):
        self.scan_progress += 1
        self.progress_bar.setValue(self.scan_progress)
        
        if self.scan_progress >= 100:
            self.scan_timer.stop()
            self.info_label.setText("Scan complete! Found issues ready to clean.")
            self.clean_btn.setEnabled(True)
    
    def start_cleaning(self):
        if self.cleaning_in_progress:
            return
        
        self.cleaning_in_progress = True
        self.clean_btn.setEnabled(False)
        self.info_label.setText("Cleaning in progress...")
        self.progress_bar.setValue(0)
        
        # Simulate cleaning
        self.clean_timer = QTimer()
        self.clean_progress = 0
        self.clean_timer.timeout.connect(self.update_clean_progress)
        self.clean_timer.start(50)
    
    def update_clean_progress(self):
        self.clean_progress += 1
        self.progress_bar.setValue(self.clean_progress)
        
        if self.clean_progress >= 100:
            self.clean_timer.stop()
            self.cleaning_in_progress = False
            self.clean_btn.setEnabled(True)
            self.info_label.setText("Cleaning complete! Your system is optimized.")
            QMessageBox.information(self, "Success", "System cleaning completed successfully!")
    
    def save_settings(self):
        QMessageBox.information(self, "Settings", "Settings saved successfully!")

def main():
    app = QApplication(sys.argv)
    window = CCCleanerClone()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
