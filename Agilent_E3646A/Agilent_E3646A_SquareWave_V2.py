import serial
import time

# Global variable to hold the serial connection
ser = None

def configure_serial_connection(port, baudrate):
    """
    Configures the serial connection to the power supply.
    
    Args:
    port (str): The COM port to connect to.
    baudrate (int): The baud rate for the serial communication.
    """
    global ser
    ser = serial.Serial(port, baudrate, timeout=2)
    if ser.isOpen():
        print(f"Connected to {ser.name}")
    else:
        print("Failed to open serial port")
        ser = None

def generate_square_wave(voltage, current, duration, cycles):
    """
    Generates a square wave on the power supply output.

    Args:
    voltage (float): The peak voltage of the square wave.
    current (float): The current limit for the power supply.
    duration (float): The duration in seconds for each high and low state.
    cycles (int): The number of cycles to generate.
    """
    global ser
    if ser is None or not ser.isOpen():
        print("Serial connection is not established.")
        return

    for cycle in range(cycles):
        # Set to specified voltage and current
        ser.write(f'VOLT {voltage}\n'.encode())
        ser.write(f'CURR {current}\n'.encode())
        ser.write(b'OUTP ON\n')
        time.sleep(duration)

        # Set to 0 volts
        ser.write(b'VOLT 0\n')
        time.sleep(duration)

    # Turn off output after completing cycles
    ser.write(b'OUTP OFF\n')
    print(f"Completed {cycles} cycles of square wave generation.")

# Example usage
configure_serial_connection("COM5", 9600)  # Replace with your port and baudrate
generate_square_wave(8, 3, 2, 5)  # Volts, Amps, Seconds of duration, n amount of cycles

# Close the serial connection when done
if ser is not None:
    ser.close()
    print("Serial connection closed.")
