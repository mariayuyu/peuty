import os
import time

BATTERY_CAPACITY_MAH = 10000 
AVERAGE_CURRENT_DRAW_MA = 1000
LOW_BATTERY_THRESHOLD = 20
CRITICAL_BATTERY_THRESHOLD = 5
BRIGHTNESS_LEVEL_LOW = 0.2

def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

def calculate_remaining_battery_percentage(uptime_seconds, battery_capacity_mah, average_current_draw_ma):
    uptime_hours = uptime_seconds / 3600
    energy_used_mah = uptime_hours * average_current_draw_ma
    remaining_battery_mah = battery_capacity_mah - energy_used_mah
    remaining_battery_percentage = (remaining_battery_mah / battery_capacity_mah) * 100
    return max(0, min(100, remaining_battery_percentage))
	
def adjust_brightness(level):
    os.system(f"xrandr --output HDMI-1 --brightness {level}")
	
def shutdown_system():
    os.system("sudo shutdown -h now")
	
def main():
    while True:
        uptime_seconds = get_system_uptime()
        remaining_battery_percentage = calculate_remaining_battery_percentage(
            uptime_seconds, BATTERY_CAPACITY_MAH, AVERAGE_CURRENT_DRAW_MA)
        
        print(f"Remaining battery: {remaining_battery_percentage:.2f}%")
        
        if remaining_battery_percentage < CRITICAL_BATTERY_THRESHOLD:
            print("Critical battery level reached. Shutting down.")
            shutdown_system()
        elif remaining_battery_percentage < LOW_BATTERY_THRESHOLD:
            print("Low battery level. Reducing brightness.")
            adjust_brightness(BRIGHTNESS_LEVEL_LOW)
        
        time.sleep(30)  # Print the battery percentage every 30 seconds

if __name__ == "__main__":
    main()