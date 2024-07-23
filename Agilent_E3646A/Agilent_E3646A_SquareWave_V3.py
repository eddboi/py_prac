import serial
import time

class PowerSupply:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=2)
        self.channel_limits = {}  # Dictionary to store voltage and current limits for each channel

        if self.ser.isOpen():
            print(f"Connected to power supply on {self.port}")
        else:
            print("Failed to open serial port")
            self.ser = None

    def set_channel_limits(self, channel, voltage_limit, current_limit):
        """
        Selects the output channel and sets its voltage and current limits.

        Args:
        channel (int): The output channel to select.
        voltage_limit (float): The voltage limit for the selected channel.
        current_limit (float): The current limit for the selected channel.
        """
        if self.ser is None or not self.ser.isOpen():
            print("Serial connection is not established.")
            return

        # Send command to select the output channel
        #self.ser.write(f'INST:SEL CH{channel}\n'.encode())

        # Store the voltage and current limits for the channel
        self.channel_limits[channel] = {'voltage_limit': voltage_limit, 'current_limit': current_limit}
        print(f"Output channel {channel} limits set: voltage limit {voltage_limit}V and current limit {current_limit}A.")

    def generate_square_wave(self, channel, voltage, current, duration, cycles):
        if self.ser is None or not self.ser.isOpen():
            print("Serial connection is not established.")
            return

        # Check if the specified voltage and current are within the limits for the channel
        if voltage > self.channel_limits[channel]['voltage_limit'] or current > self.channel_limits[channel]['current_limit']:
            print("Specified voltage/current exceeds the configured limits for this channel.")
            return

        # Select the output channel
        self.ser.write(f'INST:SEL OUT{channel}\n'.encode())

        for cycle in range(cycles):
            # Set to specified voltage and current
            self.ser.write(f'VOLT {voltage}\n'.encode())
            self.ser.write(f'CURR {current}\n'.encode())
            self.ser.write(b'OUTP ON\n')
            time.sleep(duration)

            # Set to 0 volts
            self.ser.write(b'VOLT 0\n')
            time.sleep(duration)

        # Turn off output after completing cycles
        self.ser.write(b'OUTP OFF\n')
        print(f"Completed {cycles} cycles of square wave generation on channel {channel}.")

    def close(self):
        if self.ser is not None:
            self.ser.close()
            print(f"Closed connection on {self.port}")

if __name__ == '__main__':
    # Example usage
    ps = PowerSupply("COM5", 9600)  # Specify COM port and baudrate
    ps.set_channel_limits(1, 8, 3)  # Select channel 1 with voltage limit 8V and current limit 3A
    ps.set_channel_limits(2, 20, 1.5)  # Select channel 2 with voltage limit 20V and current limit 1.5A

    #Enter your desired parameters below.
    ps.generate_square_wave(1, 5, 2, 3, 5)  # Generate a square wave (channel, voltage, current, duration, cycles)
    ps.close()  # Close the connection when done
