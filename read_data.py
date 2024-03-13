import matplotlib.pyplot as plt
import serial
import time
import serial.tools.list_ports
import matplotlib.animation as animation
from functools import partial
import os

SER = serial.Serial()
SERIAL_PORTS = []
PAUSED = False
ACTIVE_SERIAL_PORT = ""

## You can edit thses

ANIMATION_LENGTH = 25  # In seconds
Y_AXIS_MIN = 13
Y_AXIS_MAX = 23
Y_AXIS_LABEL = "pressure (psi)"
X_AXIS_LABEL = "time (s)"
PLOT_TITLE = "Pressure x Time"



def init_serial():
    # Detect OS
    print("Initalizing serial port configuration")
    print("Please select the serial port you would like to listen to: ")
    SERIAL_PORTS = serial.tools.list_ports.comports()

    # list serial ports
    for i, port in enumerate(SERIAL_PORTS):
        print(f"\t{i + 1}. {port}")

    ACTIVE_SERIAL_PORT = SERIAL_PORTS[int(input(":")) - 1].device

    SER.port = ACTIVE_SERIAL_PORT
    SER.baudrate = 9600

    print("SUCCESSFULLY INITALIZED SERIAL PORT!")
    print(f"Active serial port: {SER.port}")
    print(f"Baudrate: {SER.baudrate}")

    print("Connecting to serial port...")
    SER.open()
    # Read a sample line of the serial port to ensure the connection is established
    print(f"Sample line: {SER.readline().decode()}")
    print("Successfully opened, connected, and read serial port!")
    SER.close()
    print("Closed port!")


def show_menu():
    print("Welcome, please select an option: ")
    print("0. Exit")
    print("1. Start live plot")
    print("2. Record plot")
    print("3. Write serial output to file")
    return int(input(": "))


if __name__ == "__main__":
    init_serial()
    menu_selection = show_menu()
    # Run infinitely
    while True:
        match menu_selection:
            case 0:
                print("Closeing serial port")
                SER.close()
                print("Shutting down . . .")
                break
            case 1:
                print(f"Opening port {ACTIVE_SERIAL_PORT}")
                SER.open()
                print("Reading line . . .")
                print(SER.readline().decode().strip().split(","))
                PAUSED = False
                print("Starting live plot!")
                fig, ax = plt.subplots()
                (plot_line,) = ax.plot([], [], lw=0.5)

                def plot_init():
                    _, t = SER.readline().decode().strip().split(",")
                    ax.set_xlim((int(t) // 1000, (int(t) // 1000) + ANIMATION_LENGTH))
                    ax.set_ylim((Y_AXIS_MIN, Y_AXIS_MAX))
                    ax.set_xlabel(X_AXIS_LABEL)
                    ax.set_ylabel(Y_AXIS_LABEL)
                    plt.title(PLOT_TITLE)
                    ax.grid()
                    return (plot_line,)

                def update_plot(_, ln, x, y):
                    p, t = SER.readline().decode().strip().split(",")
                    print([float(p), int(t)])
                    x.append(int(t) / 1000)
                    y.append(float(p))

                    ln.set_data(x, y)
                    return (ln,)

                def toggle_pause(e):
                    global PAUSED
                    if not PAUSED:
                        anim.pause()
                        PAUSED = True
                    else:
                        anim.resume()
                        PAUSED = False

                anim = animation.FuncAnimation(
                    fig,
                    partial(update_plot, ln=plot_line, x=[], y=[]),
                    init_func=plot_init,
                    blit=True,
                    frames=500,
                    interval=20,
                )

                fig.canvas.mpl_connect("key_press_event", toggle_pause)
                plt.show()
                SER.close()
                # anim.save(f"live_plot_{int(time.time())}")
            case 2:
                # take a timed screenshot
                limit = int(input("How many seconds do you want to record?\n : "))
                t = 0
                x, y = [], []
                SER.open()
                while float(t) < (limit * 1000):
                    p, t = SER.readline().decode().strip().split(",")
                    y.append(float(p))
                    x.append((float(t)) / 1000)
                    print(f"Time: {x[-1]}m, Pressure: {y[-1]}")

                fig, ax = plt.subplots()
                (plot_line,) = ax.plot(x, y, lw=0.5)
                ax.grid()
                plt.show()
                SER.close()

            case 3:
                SER.open()
                os.makedirs("output", exist_ok=True)
                with open(os.path.join("output",f"output_log_{int(time.time())}.csv"), "w+") as f:
                    f.writelines("time(ms),pressure(psi)\n")
                    while True:
                        p, t = SER.readline().decode().strip().split(",")
                        l = f"{p},{t}"
                        print(l)
                        f.writelines(l + "\n")
        menu_selection = show_menu()
            