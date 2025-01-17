import pigpio
import time

# GPIO pins for motors
MOTORS = {
    "back_left": 15,  # CW
    "front_left": 23,  # CCW
    "back_right": 9,   # CCW
    "front_right": 27  # CW
}

# Constants for PWM signals (microseconds)
PWM_MIN = 1000  # Min throttle (Idle)
PWM_MAX = 2000  # Max throttle (Full throttle)
PWM_STEP = 10   # Step size for throttle adjustments

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit()

# Function to initialize motors to full throttle
def initialize_motors():
    print("Initializing motors to full throttle...")
    for motor, pin in MOTORS.items():
        pi.set_servo_pulsewidth(pin, PWM_MAX)  # Set to max throttle
        print(f"{motor} initialized on GPIO {pin} to PWM_MAX ({PWM_MAX})")
    time.sleep(1)  

# Function to control motor throttle
def set_throttle(motor, throttle):
    if motor not in MOTORS:
        print(f"Invalid motor: {motor}")
        return
    if throttle < PWM_MIN or throttle > PWM_MAX:
        print(f"Invalid throttle value: {throttle}. Must be between {PWM_MIN} and {PWM_MAX}.")
        return
    pi.set_servo_pulsewidth(MOTORS[motor], throttle)
    print(f"Set {motor} (GPIO {MOTORS[motor]}) to throttle {throttle} μs")

# Main control loop
def throttle_control():
    current_throttle = PWM_MIN
    print("Use '=' to increase throttle, '-' to decrease throttle, '.' for max throttle, ',' for min throttle, and 'q' to quit.")
    try:
        while True:
            command = input("Enter command ('=', '-', '.', ',', 'q'): ")
            if command == "=":
                current_throttle += PWM_STEP
                if current_throttle > PWM_MAX:
                    current_throttle = PWM_MAX
                print(f"Increasing throttle to {current_throttle}")
            elif command == "-":
                current_throttle -= PWM_STEP
                if current_throttle < PWM_MIN:
                    current_throttle = PWM_MIN
                print(f"Decreasing throttle to {current_throttle}")
            elif command == ".":
                current_throttle = PWM_MAX
                print(f"Throttle set to maximum: {PWM_MAX}")
            elif command == ",":
                current_throttle = PWM_MIN
                print(f"Throttle set to minimum: {PWM_MIN}")
            elif command == "q":
                print("Quitting throttle control.")
                break
            else:
                print("Invalid command. Use '=', '-', '.', ',', or 'q'.")

            # Set throttle for all motors
            for motor in MOTORS:
                set_throttle(motor, current_throttle)

    except KeyboardInterrupt:
        print("\nThrottle control interrupted by user.")

# Cleanup function
def cleanup():
    print("Resetting motors to 0 throttle and cleaning up...")
    for pin in MOTORS.values():
        pi.set_servo_pulsewidth(pin, 0)  # Stop signal
    pi.stop()
    print("Cleanup complete.")

# Main script execution
if __name__ == "__main__":
    try:
        initialize_motors()
        throttle_control()
    finally:
        cleanup()
