import serial

ser = None

try:
    #ser = serial.Serial(port='COM5', baudrate=115200, timeout=0.1) # Windows
    ser = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0.5) # raspberry pi
    print("Found Micro:Bit")
    
except:
    print("Not Found Micro:bit")
    

while ser:
    if ser.in_waiting > 0:
        print(ser.readline().decode().strip())

    


