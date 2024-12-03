## Email License extraction from AD

During Deployment
Include config/key.key: Ensure the key.key file is bundled with the main.exe when you package your application using PyInstaller.
In your PyInstaller spec file or command, include the config/ directory:
bash
Copy code
pyinstaller --onefile --add-data "config/key.key;config" main.py
