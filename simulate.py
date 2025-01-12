import tkinter as tk
from tkinter import ttk
import requests
import random
import threading
import time
from datetime import datetime

class HardwareSimulator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hardware Simulator")
        self.geometry("600x400")

        # Device state
        self.device_id = 1
        self.is_running = False
        self.device_on = False
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize data sending thread
        self.data_thread = None

    def create_widgets(self):
        # Device Control Frame
        control_frame = ttk.LabelFrame(self, text="Device Control")
        control_frame.pack(padx=10, pady=5, fill="x")

        # Power Button
        self.power_btn = ttk.Button(control_frame, text="Turn ON", command=self.toggle_device)
        self.power_btn.pack(side="left", padx=5, pady=5)

        # Status Label
        self.status_label = ttk.Label(control_frame, text="Status: OFF")
        self.status_label.pack(side="left", padx=5, pady=5)

        # Readings Frame
        readings_frame = ttk.LabelFrame(self, text="Current Readings")
        readings_frame.pack(padx=10, pady=5, fill="x")

        # Current reading
        self.current_var = tk.StringVar(value="Current: 0.0 A")
        current_label = ttk.Label(readings_frame, textvariable=self.current_var)
        current_label.pack(pady=2)

        # Voltage reading
        self.voltage_var = tk.StringVar(value="Voltage: 0.0 V")
        voltage_label = ttk.Label(readings_frame, textvariable=self.voltage_var)
        voltage_label.pack(pady=2)

        # Wattage reading
        self.wattage_var = tk.StringVar(value="Wattage: 0.0 W")
        wattage_label = ttk.Label(readings_frame, textvariable=self.wattage_var)
        wattage_label.pack(pady=2)

        # Log Frame
        log_frame = ttk.LabelFrame(self, text="Activity Log")
        log_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Log Text
        self.log_text = tk.Text(log_frame, height=10)
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)

    def toggle_device(self):
        self.device_on = not self.device_on
        if self.device_on:
            try:
                requests.post('http://127.0.0.1:8000/Ecox/initialize/')
                self.power_btn.config(text="Turn OFF")
                self.status_label.config(text="Status: ON")
                self.start_data_sending()
            except Exception as e:
                print(f"Error: {e}")
        else:
            self.power_btn.config(text="Turn ON")
            self.status_label.config(text="Status: OFF")
            self.stop_data_sending()

    def start_data_sending(self):
        self.is_running = True
        self.data_thread = threading.Thread(target=self.send_data_loop)
        self.data_thread.daemon = True
        self.data_thread.start()

    def stop_data_sending(self):
        self.is_running = False
        if self.data_thread:
            self.data_thread.join()

    def send_data_loop(self):
        print("Starting data sending loop")
        while self.is_running:
            try:
                # Generate random readings with some variation
                current = random.uniform(0.8, 1.2) if self.device_on else 0
                voltage = random.uniform(219, 221) if self.device_on else 0
                wattage = current * voltage

                # Update GUI
                self.current_var.set(f"Current: {current:.2f} A")
                self.voltage_var.set(f"Voltage: {voltage:.2f} V")
                self.wattage_var.set(f"Wattage: {wattage:.2f} W")

                # Prepare data
                data = {
                    'device_id': self.device_id,
                    'current': current,
                    'voltage': voltage,
                    'wattage': wattage
                }

                # Send data to backend
                response = requests.post('http://127.0.0.1:8000/Hardware/realtime-data/', json=data)
                print(f"Sent data: {data}")
                print(f"Response status code: {response.status_code}")
                print(f"Response content: {response.content}")
                
                # Log the activity
                timestamp = datetime.now().strftime("%H:%M:%S")
                if response.status_code == 201:
                    self.log_message(f"[{timestamp}] Data sent successfully")
                else:
                    self.log_message(f"[{timestamp}] Error sending data: {response.status_code}")

                time.sleep(1)  # Wait for 1 second before sending next reading

            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                time.sleep(1)

    def log_message(self, message):
        print(message)
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

if __name__ == "__main__":
    app = HardwareSimulator()
    app.mainloop()
