import time
import serial

def output_voltage_sequence(ser, voltage, duration):
    ser.write(f'VOLT {voltage}\n'.encode())
    time.sleep(0.05)
    ser.write(b'CURR 3\n')
    time.sleep(0.05)
    ser.write(b'OUTP ON\n')
    time.sleep(duration)

def main():
    port = 'COM5'  # Replace with your port
    baudrate = 9600  # Replace with your baudrate
    timeout = 1

    with serial.Serial(port, baudrate, timeout=timeout) as ser:
        if ser.isOpen():
            print(f"Connected to {ser.name}")
            ser.flushInput()
            ser.flushOutput()

            num_repetitions = 5  # Replace with the desired number of repetitions
            for _ in range(num_repetitions):
                output_voltage_sequence(ser, 5, 2)  # Output 5V for 5 seconds
                output_voltage_sequence(ser, 0, 2)  # Output 0V for 5 seconds

            print("Completed voltage and current output sequence.")
        else:
            print("Failed to open serial port")

if __name__ == "__main__":
    main()