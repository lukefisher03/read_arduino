import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
import matplotlib.animation as animation
import time
import matplotlib
# matplotlib.use('Qt5Agg')

SER = serial.Serial()
SERIAL_PORTS = []
ACTIVE_SERIAL_PORT = ""

def init():
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

def show_menu():
    print("Welcome, please select an option: ")
    print("0. Exit")
    print("1. Start live plot")
    return int(input(": "))

def init_plot():
    plot_line.set_data([], [])
    return plot_line,

def update_plot(i, times, pressures, ser):
    p, t = ser.readline().decode().strip().split(",")
    print([float(p),int(t)])
    pressures.append(float(p))
    times.append(int(t) / 1000)

    ax.clear()
    plt.title("Pressure x Time")
    ax.grid()
    ax.set_ylabel("pressure (psi)")
    ax.set_xlabel("time (seconds)")
    ax.plot(times, pressures)


if __name__ == "__main__":
    init()
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
                times = []
                pressures = []
                print("Starting live plot!")
                fig = plt.figure()
                ax = plt.axes()
                plot_line, = ax.plot([], [], lw=0.5)
                ax.grid()
                paused = False

                def toggle_pause(i):
                    if paused:
                        anim.resume()
                    else:
                        anim.pause()
                    paused = not paused

                anim = animation.FuncAnimation(fig, update_plot, fargs=(times, pressures, SER), init_func=init_plot, frames=500, interval=10)
                
                fig.canvas.mpl_connect('button_press_event', toggle_pause)
                plt.show()
                # anim.save(f"live_plot_{int(time.time())}")

        menu_selection = show_menu()




