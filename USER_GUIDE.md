# CCleaner Clone 7 - User Guide

## Quick Start

1. **Run the Application**
   - Windows: Double-click `run.bat` or run `python app.py`
   - Linux/Mac: Run `./run.sh` or `python3 app.py`

2. **Main Interface**
   - Left side: Feature tabs (Cleaner, Health Check, Tools, Settings)
   - Right side: Real-time system information

## Features Overview

### 1. Cleaner Tab

The main cleaning interface with the following features:

#### Cleaning Categories
- **Temporary Files**: Windows %TEMP% and system temp folders
- **Recycle Bin**: Permanently deleted files
- **Browser Cache**: Chrome, Firefox, Edge cache
- **Windows Temp Folder**: System temporary files
- **Log Files**: System and application logs
- **Thumbnail Cache**: Windows thumbnail cache
- **Cookies**: Browser cookies (uncheck if you want to keep them)
- **Browser History**: Browsing history (uncheck if you want to keep it)

#### How to Clean
1. **Select Items**: Check/uncheck items you want to clean
2. **Scan**: Click "SCAN FOR ISSUES" to find files
3. **Review**: Check the "Items to Clean" and "Total Space" in the info panel
4. **Clean**: Click "CLEAN" and confirm
5. **Complete**: Application shows completion status

#### Progress Monitoring
- Progress bar shows cleaning progress
- Status message indicates current action
- Items count and total space updated in real-time

### 2. Health Check Tab

View your system's health status:
- **Disk Space Usage**: How full your disk is
- **Memory Usage**: RAM availability
- **CPU Temperature**: System temperature (if available)
- **Windows Updates**: Update status
- **Startup Programs**: Number of startup items
- **System Registry Health**: Registry status

Overall system health is displayed with a status indicator.

### 3. Tools Tab

Additional utilities for system maintenance:
- **Startup Manager**: Control which programs run at startup
- **Uninstall Programs**: Remove software you don't need
- **Duplicate File Finder**: Find and remove duplicate files
- **File Shredder**: Securely delete files beyond recovery
- **Registry Cleaner**: Fix registry issues

### 4. Settings Tab

Customize the application behavior:

#### General Settings
- **Auto-clean on startup**: Automatically clean when you start Windows
- **Skip system files**: Prevents deletion of critical system files (recommended: ON)
- **Secure deletion**: Overwrites files before deletion (slower but more secure)

#### Advanced Settings
- **Cache retention**: How many days to keep cache files (0-365 days)
- **Save Settings**: Apply your preferences

## System Information Panel

The right panel shows real-time statistics:

### Disk Usage
- Shows used and total disk space
- Progress bar indicates how full the disk is
- Color changes from green to red as it fills up

### Memory Usage
- Available RAM in GB
- Memory usage percentage

### CPU Usage
- Current CPU utilization percentage

### Cleaning Statistics
- **Items to Clean**: Number of files found
- **Total Space**: Total size in MB that will be freed

## Tips for Best Results

### Before Cleaning
1. Close all open programs
2. Back up important files
3. Review what will be cleaned
4. Run a system scan first to see what will be removed

### During Cleaning
1. Don't interrupt the cleaning process
2. Keep the application window open
3. Don't modify files in %TEMP% while cleaning

### After Cleaning
1. Restart your computer for best results
2. Check available disk space
3. Notice improved system performance

## Common Issues & Solutions

### Issue: "Permission denied" errors
**Solution**: 
- Run as Administrator (right-click the app, "Run as administrator")
- Restart computer to release locked files
- Some system files can't be deleted while Windows is running

### Issue: Application won't start
**Solution**:
- Ensure Python 3.7+ is installed
- Try running from command prompt: `python app.py`
- Check that you're in the correct directory

### Issue: Not enough space showing
**Solution**:
- System files that are locked won't show in the scan
- Some files may be in use by the system
- Hidden files might not be included

### Issue: Slow cleaning process
**Solution**:
- This is normal if you have many files to clean
- If using secure deletion, it will be slower
- Reduce the number of items or disable secure deletion

## Safety Information

### What This App DOES Clean
- Temporary cache files
- Old browser cache
- System log files
- Unused Windows files
- Trash/recycle bin

### What This App DOESN'T Touch (with Skip System Files ON)
- Active application files
- Windows system files
- Program data
- Important documents

### Before First Use
1. Create a system restore point
2. Back up important files
3. Run in a test environment if possible
4. Check with "Skip system files" enabled first

## Advanced Usage

### Scheduling Regular Cleaning
1. Enable "Auto-clean on startup" in Settings
2. Or schedule through Windows Task Scheduler
3. Creates a new task with the command: `python app.py`

### Batch Cleaning Script
Create a batch file to run cleaning with specific options:
```batch
@echo off
cd /d C:\path\to\ccleaner_clone
python app.py
```

### Command Line Usage
Currently, the app uses GUI. Future versions may support CLI mode.

## Performance Impact

### Expected Improvements After Cleaning
- ⚡ Faster startup time (10-20% depending on files)
- 💾 More free disk space
- 🎨 Better browser performance
- 📊 Improved system responsiveness

### Disk Space Freed
Typical cleaning results:
- **First clean**: 1-10 GB (depending on Windows age)
- **Regular cleaning**: 100-500 MB
- **Browser cache**: 200-2000 MB depending on usage

## FAQ

**Q: Is it safe to use?**
A: Yes, with "Skip system files" enabled. Always back up important data first.

**Q: Will this delete my personal files?**
A: No, unless you select categories like "Browser History" or "Cookies". System and program files are protected by default.

**Q: How often should I clean?**
A: Weekly for regular use, or when disk space gets low.

**Q: Does it remove viruses?**
A: No. Use antivirus software for malware protection.

**Q: Can I undo the cleaning?**
A: Files are deleted permanently. Use the Recycle Bin setting before final cleanup if unsure.

**Q: Why is some space still showing as used?**
A: Windows reserves space, system files, and currently open files can't be cleaned.

**Q: Can I clean just one category?**
A: Yes, uncheck all others and only select the one you want.

**Q: Does it work on external drives?**
A: Currently only system drive. External drives should be cleaned separately.

## System Requirements

- **Operating System**: Windows 7 or later
- **Python**: 3.7 or later (download from python.org)
- **RAM**: 512 MB minimum
- **Disk Space**: 100 MB for the application
- **Internet**: Not required (except for updates)

## What's Included

- `app.py` - Main application
- `cleaner.py` - Cleaning logic
- `stats.py` - System statistics
- `advanced_cleaner.py` - Advanced features
- `run.bat` - Windows launcher
- `run.sh` - Linux/Mac launcher
- `README.md` - Technical documentation
- `DEPENDENCIES.md` - Dependency information
- `USER_GUIDE.md` - This file

## Updates & Support

**Check for Updates**: Visit the project repository

**Report Issues**: Provide details about:
- Windows version
- Python version
- What were you trying to clean
- Any error messages

**Feature Requests**: Let us know what you'd like added!

## License & Disclaimer

This software is provided as-is for educational purposes. The author is not responsible for:
- Data loss
- System damage
- Performance changes
- Incompatibility issues

Always test in a safe environment first!

---

**Version**: 7.0  
**Last Updated**: 2026-01-19  
**Support**: Check README.md for more information
