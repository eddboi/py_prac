import serial
import time

# Replace with your device's COM port and correct settings
port = "COM5"  # Change to the correct port for your setup
baudrate = 9600  # Adjust as needed
timeout = 2  # Adjust as needed

# Open the serial connection
with serial.Serial(port, baudrate, timeout=timeout) as ser:
    if ser.isOpen():
        print(f"Connected to {ser.name}")

        # Clear input and output buffers
        ser.flushInput()
        ser.flushOutput()

        # Set the voltage to 5V
        ser.write(b'VOLT 5\n')
        time.sleep(0.5)

        # Set the current limit to 1A
        ser.write(b'CURR 1\n')
        time.sleep(0.5)

        # Enable the output
        ser.write(b'OUTP ON\n')
        time.sleep(5)  # Output 5V at 1A for 5 seconds

        # Disable the output
        ser.write(b'OUTP OFF\n')
        time.sleep(5)
        
        # Enable the output
        ser.write(b'OUTP ON\n')
        time.sleep(5)  # Output 5V at 1A for 5 seconds
        
        # Disable the output
        ser.write(b'OUTP OFF\n')
        time.sleep(5)
        
        print("Completed voltage and current output sequence.")

    else:
        print("Failed to open serial port")
