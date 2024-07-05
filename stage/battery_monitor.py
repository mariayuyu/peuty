import smbus2
import time

# I2C address of the MAX1704X
MAX1704X_ADDRESS = 0x36

# Registers
VCELL_REGISTER = 0x02
SOC_REGISTER = 0x04

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)

def read_vcell():
    # Read the voltage from the VCELL register (0x02)
    data = bus.read_i2c_block_data(MAX1704X_ADDRESS, VCELL_REGISTER, 2)
    # Convert the data to a 12-bit value
    vcell = (data[0] << 4) | (data[1] >> 4)
    # Convert to voltage in mV (1 unit = 1.25 mV)
    voltage = vcell * 1.25 / 1000.0
    return voltage

def read_soc():
    # Read the state of charge (SOC) from the SOC register (0x04)
    data = bus.read_i2c_block_data(MAX1704X_ADDRESS, SOC_REGISTER, 2)
    # Convert the data to a percentage
    soc = data[0] + data[1] / 256.0
    return soc

def main():
    while True:
        voltage = read_vcell()
        soc = read_soc()
        print(f"Voltage: {voltage:.2f} V")
        print(f"State of Charge: {soc:.2f} %")
        time.sleep(1)

if __name__ == "__main__":
    main()
