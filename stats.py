import psutil
import os

class SystemStats:
    def __init__(self):
        self.drive = os.path.splitdrive(os.path.expandvars("%WINDIR%"))[0]
    
    def get_system_stats(self):
        """Get current system statistics"""
        stats = {
            'disk': self.get_disk_stats(),
            'memory': self.get_memory_stats(),
            'cpu': self.get_cpu_stats(),
        }
        return stats
    
    def get_disk_stats(self):
        """Get disk usage statistics"""
        try:
            usage = psutil.disk_usage(self.drive)
            return {
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'percent': usage.percent
            }
        except Exception as e:
            print(f"Error getting disk stats: {e}")
            return {
                'total_gb': 0,
                'used_gb': 0,
                'free_gb': 0,
                'percent': 0
            }
    
    def get_memory_stats(self):
        """Get memory usage statistics"""
        try:
            virtual_memory = psutil.virtual_memory()
            return {
                'total_gb': virtual_memory.total / (1024**3),
                'available_gb': virtual_memory.available / (1024**3),
                'used_gb': virtual_memory.used / (1024**3),
                'percent': virtual_memory.percent
            }
        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return {
                'total_gb': 0,
                'available_gb': 0,
                'used_gb': 0,
                'percent': 0
            }
    
    def get_cpu_stats(self):
        """Get CPU usage statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            return {
                'percent': cpu_percent,
                'count': cpu_count
            }
        except Exception as e:
            print(f"Error getting CPU stats: {e}")
            return {
                'percent': 0,
                'count': 0
            }
