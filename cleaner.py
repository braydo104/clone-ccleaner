import os
import shutil
import tempfile
import glob
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
import psutil

class SystemCleaner:
    def __init__(self):
        self.total_size_cleaned = 0
        self.files_cleaned = 0
        
    def find_temp_files(self):
        """Find temporary files"""
        temp_locations = [
            os.path.expandvars(r"%TEMP%"),
            os.path.expandvars(r"%WINDIR%\Temp"),
            os.path.expandvars(r"%WINDIR%\Prefetch"),
            os.path.expandvars(r"%ProgramData%\Adobe\Common\Media Cache Files"),
        ]
        
        temp_files = []
        for location in temp_locations:
            if os.path.exists(location):
                try:
                    for root, dirs, files in os.walk(location):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                temp_files.append({
                                    'path': file_path,
                                    'size': os.path.getsize(file_path)
                                })
                            except:
                                pass
                except PermissionError:
                    pass
        
        return temp_files
    
    def find_recycle_bin(self):
        """Find recycle bin files"""
        recycle_paths = [
            os.path.expandvars(r"%SYSTEMDRIVE%\$Recycle.bin"),
        ]
        
        recycle_files = []
        for path in recycle_paths:
            if os.path.exists(path):
                try:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                recycle_files.append({
                                    'path': file_path,
                                    'size': os.path.getsize(file_path)
                                })
                            except:
                                pass
                except PermissionError:
                    pass
        
        return recycle_files
    
    def find_browser_cache(self):
        """Find browser cache files"""
        cache_locations = [
            # Chrome
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache"),
            # Firefox
            os.path.expandvars(r"%LOCALAPPDATA%\Mozilla\Firefox\Profiles"),
            # Edge
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache"),
        ]
        
        cache_files = []
        for location in cache_locations:
            if os.path.exists(location):
                try:
                    for root, dirs, files in os.walk(location):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                cache_files.append({
                                    'path': file_path,
                                    'size': os.path.getsize(file_path)
                                })
                            except:
                                pass
                except PermissionError:
                    pass
        
        return cache_files
    
    def find_log_files(self):
        """Find log files"""
        log_locations = [
            os.path.expandvars(r"%WINDIR%\Logs"),
            os.path.expandvars(r"%WINDIR%\System32\LogFiles"),
        ]
        
        log_files = []
        for location in log_locations:
            if os.path.exists(location):
                try:
                    for root, dirs, files in os.walk(location):
                        for file in files:
                            if file.endswith('.log'):
                                file_path = os.path.join(root, file)
                                try:
                                    log_files.append({
                                        'path': file_path,
                                        'size': os.path.getsize(file_path)
                                    })
                                except:
                                    pass
                except PermissionError:
                    pass
        
        return log_files
    
    def clean_files(self, file_list, secure=False):
        """Clean specified files"""
        cleaned = 0
        total_size = 0
        
        for file_info in file_list:
            try:
                if os.path.exists(file_info['path']):
                    if secure:
                        # Secure deletion - overwrite before deleting
                        self._secure_delete(file_info['path'])
                    else:
                        os.remove(file_info['path'])
                    
                    cleaned += 1
                    total_size += file_info.get('size', 0)
            except PermissionError:
                pass
            except Exception as e:
                pass
        
        self.files_cleaned += cleaned
        self.total_size_cleaned += total_size
        
        return {'cleaned': cleaned, 'size': total_size}
    
    def _secure_delete(self, file_path):
        """Securely delete a file by overwriting it"""
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, "ba+") as f:
                f.seek(0)
                f.write(os.urandom(file_size))
            os.remove(file_path)
        except:
            # If secure delete fails, try normal delete
            try:
                os.remove(file_path)
            except:
                pass

class CleanerWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    
    def __init__(self, cleaner, clean_items):
        super().__init__()
        self.cleaner = cleaner
        self.clean_items = clean_items
        
    def run(self):
        """Run cleaning in background"""
        results = {}
        
        for item_name, item_data in self.clean_items.items():
            if not item_data['checked']:
                continue
            
            # Here we would actually clean based on item name
            # For now, just emit progress
            self.progress.emit(50)
        
        self.finished.emit(results)
