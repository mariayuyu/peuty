import smbus2
import time

# I2C address of the MAX17043
MAX17043_ADDRESS = 0x36

# Register addresses
VCELL_REGISTER = 0x02
SOC_REGISTER = 0x04

def read_register(bus, address, register):
    # Read 2 bytes from the specified register
    data = bus.read_i2c_block_data(address, register, 2)
    # Combine the 2 bytes
    value = (data[0] << 8) | data[1]
    return value

def get_battery_percentage(bus, address):
    soc = read_register(bus, address, SOC_REGISTER)
    # Convert to percentage
    percentage = soc / 256.0
    return percentage

def main():
    # Initialize I2C (SMBus)
    bus = smbus2.SMBus(1)

    while True:
        battery_percentage = get_battery_percentage(bus, MAX17043_ADDRESS)
        print(f"Batterie restante: {battery_percentage:.2f}%")
        time.sleep(5)

if __name__ == "__main__":
    main()
