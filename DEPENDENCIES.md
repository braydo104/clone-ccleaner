# No dependencies required!

The CCleaner Clone 7 application uses tkinter, which comes built-in with Python on Windows and macOS.

## Windows

No additional dependencies needed! Just run:
```
python app.py
```

Or double-click `run.bat`

## Linux

If tkinter is not installed, install it with:
```
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

Then run:
```
./run.sh
```

Or:
```
python3 app.py
```

## macOS

If you installed Python from python.org (recommended), tkinter is included.

If you used Homebrew, you may need to install tkinter separately:
```
brew install python-tk@3.11
```

Then run:
```
python3 app.py
```
