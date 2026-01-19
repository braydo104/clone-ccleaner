# CCleaner Clone 7

A Python-based system cleaning application inspired by CCleaner 7. This application provides tools to optimize and clean your Windows system.

## Features

- **System Cleaner**: Remove temporary files, cache, and other junk files
- **Browser Cache Cleanup**: Clear Chrome, Firefox, and Edge cache
- **Recycle Bin Management**: Empty recycle bin safely
- **System Health Check**: Monitor disk usage and system status
- **Log File Cleanup**: Remove old system log files
- **Settings Management**: Customize cleaning preferences
- **Real-time Monitoring**: Live system statistics (Disk, Memory, CPU)
- **System Tools**: Additional utilities for system maintenance

## System Requirements

- Windows 7 or later
- Python 3.7 or later
- 100 MB free disk space

## Installation

1. Clone or download this repository
2. Install required dependencies (optional):
```bash
pip install psutil
```

Note: The application uses tkinter (built-in with Python), so no external GUI library is required.

## Running the Application

Simply run:
```bash
python app.py
```

Or double-click the `app.py` file in File Explorer.

## How to Use

### Cleaner Tab
1. Select the items you want to clean from the list (checked items will be cleaned)
2. Click "SCAN FOR ISSUES" to analyze your system and find files to clean
3. Review the number of items and total space that will be freed
4. Click "CLEAN" to start the cleaning process
5. Confirm the action in the dialog that appears

### Health Check Tab
View system health metrics and diagnostics:
- Disk Space Usage
- Memory Usage
- CPU Temperature
- Windows Updates
- Startup Programs
- System Registry Health

### Tools Tab
Access additional system maintenance tools:
- Startup Manager - Manage startup programs
- Uninstall Programs - Remove unwanted software
- Duplicate File Finder - Find and remove duplicates
- File Shredder - Securely delete files
- Registry Cleaner - Clean Windows registry

### Settings Tab
Configure application preferences:
- Enable automatic cleaning on startup
- Skip system files during cleanup (recommended)
- Enable secure deletion (slower but more secure)
- Set cache retention period (0-365 days)

## Cleaning Categories

- **Temporary Files**: System temp files and cache in %TEMP% and %WINDIR%\Temp
- **Recycle Bin**: Permanently delete recycle bin contents
- **Browser Cache**: Cache from Chrome, Firefox, Edge
- **Cookies**: Browser cookies (optional)
- **Browser History**: Browsing history (optional)
- **Windows Temp Folder**: Windows temporary folders
- **Log Files**: System and application log files
- **Thumbnail Cache**: Windows thumbnail cache

## Safety Features

- **Preview before cleaning**: Review what will be deleted before proceeding
- **Selective cleanup**: Choose which categories to clean
- **Skip system files**: Option to avoid deleting critical system files (enabled by default)
- **Secure deletion**: Optional secure overwrite before deletion

## File Structure

```
ccleaner_clone/
├── app.py               # Main application and UI
├── cleaner.py           # System cleaning logic
├── stats.py             # System statistics and monitoring
├── main.py              # PyQt6 version (alternative)
├── main_tkinter.py      # Tkinter version (alternative)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## System Information Panel

The right panel displays real-time information:
- **Disk Usage**: Shows used/total disk space and a progress bar
- **Memory Usage**: Available memory and usage percentage
- **CPU Usage**: Current CPU utilization
- **Items to Clean**: Number of items found during scan
- **Total Space**: Total size of files ready to be cleaned (in MB)

## Disclaimer

This application modifies your system by deleting files. Always backup important data before using any cleaning tool. The author is not responsible for any data loss or system damage caused by this application.

## Future Enhancements

- Registry cleanup
- Duplicate file finder
- File shredder with secure deletion
- Startup manager
- Uninstall assistant
- Cloud sync
- Real-time protection
- Scheduled cleaning

## Troubleshooting

**Issue**: Application won't start
- Ensure Python 3.7+ is installed
- Try running `python app.py` from command prompt
- Check that tkinter is installed (usually included with Python)

**Issue**: "No module named 'tkinter'"
- For Ubuntu/Debian: `sudo apt-get install python3-tk`
- For Fedora: `sudo dnf install python3-tkinter`
- For macOS: Use Python from python.org, not Homebrew

**Issue**: Permission denied when cleaning
- Some files may be in use by the system
- Run the application as Administrator for better results
- The application will skip files it cannot delete

## License

This is a clone project for educational purposes.

## Support

For issues or feature requests, please provide details about:
- Your Windows version
- Python version
- Any error messages
- Steps to reproduce the issue
