import psutil
import platform
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk

try:
    from pynvml import *
    nvmlInit()
    nvml_available = True
except:
    nvml_available = False

class EndXMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("MyMonitor - EndX133")
        self.root.geometry("350x450")
        self.root.configure(bg='#0b0e14')
        self.start_time = time.time()
        style = ttk.Style()
        style.configure("TLabel", background="#0b0e14", foreground="#00ff88", font=("Consolas", 11))
        style.configure("Header.TLabel", background="#0b0e14", foreground="#ffffff", font=("Consolas", 14, "bold"))
        ttk.Label(root, text="SYSTEM STATUS ●", style="Header.TLabel").pack(pady=20)
        self.cpu_val = self.create_row("CPU Usage:")
        self.cpu_temp = self.create_row("CPU Temp:")
        self.gpu_val = self.create_row("GPU Usage:")
        self.gpu_temp = self.create_row("GPU Temp:")
        self.ram_val = self.create_row("RAM Usage:")
        self.uptime_val = self.create_row("PC Uptime:")
        self.session_val = self.create_row("Current Session:")
        self.update_stats()

    def create_row(self, text):
        frame = tk.Frame(self.root, bg='#0b0e14')
        frame.pack(fill='x', padx=30, pady=5)
        ttk.Label(frame, text=text).pack(side='left')
        val_label = ttk.Label(frame, text="...", font=("Consolas", 11, "bold"))
        val_label.pack(side='right')
        return val_label

    def get_gpu_data(self):
        if not nvml_available: return "N/A", "N/A"
        try:
            handle = nvmlDeviceGetHandleByIndex(0)
            util = nvmlDeviceGetUtilizationRates(handle)
            temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
            return f"{util.gpu}%", f"{temp}°C"
        except: return "Error", "Error"

    def update_stats(self):
        self.cpu_val.config(text=f"{psutil.cpu_percent()}%")
        self.ram_val.config(text=f"{psutil.virtual_memory().percent}%")
        try:
            temps = psutil.sensors_temperatures()
            self.cpu_temp.config(text=f"{temps['coretemp'][0].current}°C" if 'coretemp' in temps else "N/A")
        except: self.cpu_temp.config(text="N/A")
        g_usage, g_temp = self.get_gpu_data()
        self.gpu_val.config(text=g_usage)
        self.gpu_temp.config(text=g_temp)
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        self.uptime_val.config(text=str(uptime).split('.')[0])
        session = datetime.now() - datetime.fromtimestamp(self.start_time)
        self.session_val.config(text=str(session).split('.')[0])
        self.root.after(1000, self.update_stats)

if __name__ == "__main__":
    root = tk.Tk()
    app = EndXMonitor(root)
    root.mainloop()
