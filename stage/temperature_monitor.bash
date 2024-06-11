import os
import time
import tkinter as tk
from tkinter import messagebox

def get_cpu_temperature():
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(temp.replace("temp=", "").replace("'C\n", ""))

def show_alert(message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Temperature Alert", message)
        root.destroy()

def main():
        while True:
                cpu_temp = get_cpu_temperature()
                print(f"CPU Temperature: {cpu_temp}°C")

                if cpu_temp > 70:
                        show_alert("Warning: Haute température detectée!")
                elif cpu_temp > 80:
                        show_alert("Critical: Température trop haute! shutting down.")
                        os.system("sudo shutdown -h now")

                time.sleep(30)

if __name__ == "__main__":
        main()
