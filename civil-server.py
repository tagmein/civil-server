#!/usr/bin/env python3
import sys
import os
import json
import time
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QFormLayout, QDialog, QMessageBox,
                             QHBoxLayout, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

CONFIG_FILE = os.path.expanduser("~/.config/civil-server.json")
PID_FILE = os.path.expanduser("~/.cache/civil-server.pid")

class ConfigModal(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Server Configuration")
        self.setFixedWidth(450)
        layout = QFormLayout(self)

        self.port_input = QLineEdit(str(config.get("port", "4567")))
        self.cmd_input = QLineEdit(config.get("command", "npm start"))
        self.dir_input = QLineEdit(config.get("directory", os.getcwd()))

        # Directory Selection Row
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.dir_input)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)

        layout.addRow("Port:", self.port_input)
        layout.addRow("Start Command:", self.cmd_input)
        layout.addRow("Project Folder:", dir_layout)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.accept)
        btn_box.addWidget(save_btn)
        layout.addRow(btn_box)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Project Directory", self.dir_input.text())
        if directory:
            self.dir_input.setText(directory)

class MiniServerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.init_ui()

    def load_config(self):
        self.config = {
            "port": "4567",
            "command": "npm start",
            "directory": os.getcwd()
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config.update(json.load(f))
            except:
                pass

    def save_config(self):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)

    def init_ui(self):
        self.setWindowTitle(" ")
        self.setFixedSize(240, 360)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)

        layout = QVBoxLayout()

        title = QLabel("Civil Server")
        title.setFont(QFont("Sans", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.status_label = QLabel("Status: Stopped")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addSpacing(10)

        self.btn_start = QPushButton("Start Server")
        self.btn_start.clicked.connect(self.start_server)
        layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Stop Server")
        self.btn_stop.clicked.connect(self.stop_server)
        layout.addWidget(self.btn_stop)

        btn_sync = QPushButton("Sync Sessions")
        btn_sync.clicked.connect(lambda: QMessageBox.information(self, "Sync", "Coming Soon"))
        layout.addWidget(btn_sync)

        btn_config = QPushButton("Configuration")
        btn_config.clicked.connect(self.open_config)
        layout.addWidget(btn_config)

        btn_about = QPushButton("About")
        btn_about.clicked.connect(lambda: QMessageBox.about(self, "About", "Civil Server v1.0\nAlways-on dev utility."))
        layout.addWidget(btn_about)

        layout.addStretch()

        btn_quit = QPushButton("Quit")
        btn_quit.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold;")
        btn_quit.clicked.connect(self.close)
        layout.addWidget(btn_quit)

        self.setLayout(layout)

    def open_config(self):
        dialog = ConfigModal(self.config, self)
        if dialog.exec():
            self.config["port"] = dialog.port_input.text()
            self.config["command"] = dialog.cmd_input.text()
            self.config["directory"] = dialog.dir_input.text()
            self.save_config()

    def stop_server(self):
        if os.path.exists(PID_FILE):
            try:
                with open(PID_FILE, 'r') as f:
                    pid = f.read().strip()
                if pid:
                    # Kill the process group
                    subprocess.run(["pkill", "-P", pid], stderr=subprocess.DEVNULL)
                    subprocess.run(["kill", pid], stderr=subprocess.DEVNULL)
                self.status_label.setText("Status: Stopped")
                self.status_label.setStyleSheet("")
            except:
                pass
            finally:
                if os.path.exists(PID_FILE):
                    os.remove(PID_FILE)
        else:
            QMessageBox.warning(self, "Stop", "No server running (no .pidfile).")

    def start_server(self):
        port = self.config["port"]
        cmd = self.config["command"]
        wdir = self.config["directory"]

        if not os.path.isdir(wdir):
            QMessageBox.critical(self, "Error", f"Directory does not exist:\n{wdir}")
            return

        try:
            lsof = subprocess.check_output(["lsof", "-t", "-i", f":{port}", "-sTCP:LISTEN"]).decode().strip()
            child_pid = lsof.split('\n')[0]
        except:
            child_pid = None

        if child_pid:
            try:
                ppid = subprocess.check_output(["ps", "-p", child_pid, "-o", "ppid="]).decode().strip()
                p_name = subprocess.check_output(["ps", "-p", ppid if ppid else child_pid, "-o", "comm="]).decode().strip()
                is_managed = p_name.lower() not in ["bash", "sh", "zsh", "gnome-terminal", "sudo"]
                target_pid = ppid if is_managed else child_pid

                msg = f"Port {port} in use by {p_name}.\n\nTerminate PID {target_pid}?"
                reply = QMessageBox.question(self, "Port Busy", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    subprocess.run(["kill", "-9", target_pid])
                    time.sleep(0.5)
                else:
                    return
            except:
                pass

        try:
            os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
            # Run the command in the specified directory
            proc = subprocess.Popen(f"exec {cmd}", shell=True, cwd=wdir, preexec_fn=os.setsid)

            with open(PID_FILE, 'w') as f:
                f.write(str(proc.pid))

            self.status_label.setText(f"Running on {port}")
            self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start:\n{e}")

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = MiniServerApp()
    window.show()
    sys.exit(app.exec())
