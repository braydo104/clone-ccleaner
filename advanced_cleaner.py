"""
Advanced Cleaning Features for CCleaner Clone
This module provides additional cleaning capabilities
"""

import os
import winreg
from pathlib import Path

class AdvancedCleaner:
    """Advanced system cleaning features"""
    
    @staticmethod
    def find_duplicate_files(directory, max_depth=3):
        """Find duplicate files in a directory"""
        file_hashes = {}
        duplicates = []
        
        for root, dirs, files in os.walk(directory):
            depth = root[len(directory):].count(os.sep)
            if depth > max_depth:
                del dirs[:]
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size in file_hashes:
                        duplicates.append((file_path, file_hashes[file_size]))
                    else:
                        file_hashes[file_size] = file_path
                except:
                    pass
        
        return duplicates
    
    @staticmethod
    def get_large_files(directory, size_limit_mb=100):
        """Find large files"""
        large_files = []
        size_limit_bytes = size_limit_mb * (1024 ** 2)
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        
                        if file_size > size_limit_bytes:
                            large_files.append({
                                'path': file_path,
                                'size': file_size,
                                'size_mb': file_size / (1024 ** 2)
                            })
                    except:
                        pass
        except:
            pass
        
        return large_files
    
    @staticmethod
    def clean_recycle_bin():
        """Empty Windows Recycle Bin"""
        try:
            import subprocess
            # Use PowerShell to empty recycle bin
            subprocess.run([
                'powershell', '-Command',
                '$shell = New-Object -ComObject Shell.Application; '
                '$shell.Namespace(10).Self.InvokeVerb(\'Empty Recycle Bin\')'
            ], check=False)
            return True
        except:
            return False
    
    @staticmethod
    def get_startup_programs():
        """Get list of startup programs"""
        startup_programs = []
        
        # HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run'
            )
            
            i = 0
            while True:
                try:
                    name, value, type_ = winreg.EnumValue(key, i)
                    startup_programs.append({
                        'name': name,
                        'path': value,
                        'type': 'User'
                    })
                    i += 1
                except OSError:
                    break
            
            winreg.CloseKey(key)
        except:
            pass
        
        # HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'Software\Microsoft\Windows\CurrentVersion\Run'
            )
            
            i = 0
            while True:
                try:
                    name, value, type_ = winreg.EnumValue(key, i)
                    startup_programs.append({
                        'name': name,
                        'path': value,
                        'type': 'System'
                    })
                    i += 1
                except OSError:
                    break
            
            winreg.CloseKey(key)
        except:
            pass
        
        return startup_programs
    
    @staticmethod
    def disable_startup_program(program_name):
        """Disable a startup program"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_WRITE
            )
            winreg.DeleteValue(key, program_name)
            winreg.CloseKey(key)
            return True
        except:
            return False
    
    @staticmethod
    def get_browser_data_locations():
        """Get browser cache and data locations"""
        locations = {
            'Chrome': {
                'cache': os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache'),
                'cookies': os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies'),
                'history': os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History'),
            },
            'Firefox': {
                'cache': os.path.expandvars(r'%LOCALAPPDATA%\Mozilla\Firefox\Profiles'),
            },
            'Edge': {
                'cache': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache'),
                'cookies': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cookies'),
            },
        }
        return locations
    
    @staticmethod
    def get_temp_file_locations():
        """Get all Windows temp file locations"""
        locations = [
            os.path.expandvars(r'%TEMP%'),
            os.path.expandvars(r'%SYSTEMROOT%\Temp'),
            os.path.expandvars(r'%SYSTEMROOT%\Prefetch'),
            os.path.expandvars(r'%SYSTEMROOT%\System32\drivers\etc\hosts'),
            os.path.expandvars(r'%SYSTEMROOT%\SoftwareDistribution\Download'),
            os.path.expandvars(r'%LOCALAPPDATA%\Temp'),
            os.path.expandvars(r'%ProgramData%\Adobe\Common\Media Cache Files'),
        ]
        return [loc for loc in locations if os.path.exists(loc)]
    
    @staticmethod
    def get_disk_usage_by_folder(root_path, top_n=10):
        """Get disk usage by folder"""
        folder_sizes = {}
        
        try:
            for root, dirs, files in os.walk(root_path):
                folder_size = 0
                
                for file in files:
                    try:
                        folder_size += os.path.getsize(os.path.join(root, file))
                    except:
                        pass
                
                folder_name = os.path.basename(root)
                if folder_name in folder_sizes:
                    folder_sizes[folder_name] += folder_size
                else:
                    folder_sizes[folder_name] = folder_size
        except:
            pass
        
        # Return top N folders by size
        sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
        return sorted_folders[:top_n]
    
    @staticmethod
    def secure_delete_file(file_path, passes=3):
        """Securely delete a file by overwriting it multiple times"""
        try:
            file_size = os.path.getsize(file_path)
            
            # Overwrite with random data multiple times
            for _ in range(passes):
                with open(file_path, 'ba+') as f:
                    f.seek(0)
                    f.write(os.urandom(file_size))
            
            # Finally, delete the file
            os.remove(file_path)
            return True
        except:
            return False
