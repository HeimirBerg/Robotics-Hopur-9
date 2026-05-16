from pyrplidar import PyRPlidar
import threading
import time


# ------ Stillingar fyrir LiDAR ------
LidarPort = "/dev/ttyUSB0"
Baudrate  = 1000000
MaxRange  = 300  # cm

ScanData = {}
# ------ Uppsetning á threading ------
Lock     = threading.Lock()
Running  = False
_thread  = None

def LiDAR(): # Keyrir LiDARinn í gang og lesur út úr mælingum
    global Running, ScanData # Byrja thread
    lidar = PyRPlidar() #Skilgreina LiDAR
    try:
        # Stilla LiDAR 
        lidar.connect(port=LidarPort, baudrate=Baudrate, timeout=3)
        lidar.reset()
        time.sleep(5)
        lidar.lidar_serial._serial.reset_input_buffer()
        StartScan = None

        # Reyna að skanna 100x
        for attempt in range(100):
            try:
                StartScan = lidar.start_scan()
                print(f"Scan started on attempt {attempt + 1}")
                break
            except Exception:
                time.sleep(0.05)

        # Ef ekki tekst að skanna 100x þá segja notenda það 
        if StartScan is None:
            raise Exception("Could not start scan after 100 attempts")

        CurrentScan = {}

        # Lesa út úr LiDAR gögnum
        for scan in StartScan():
            if not Running: # Athuga hvort að LiDAR sé ennþá í gangi
                break
            angle    = round(scan.angle) % 360 # Námundar gráðuna í næstu heiltölu
            distance = scan.distance / 10.0 # Breytir fjarlægð úr mm í cm

            # Uppfæra ScanData og endurstilla CurrentScan til að hefja nýjar mælingar 
            if angle == 0 and CurrentScan:
                with Lock:
                    ScanData = CurrentScan  
                CurrentScan = {}            

            if 0 < distance <= MaxRange:
                CurrentScan[angle] = distance  

    except Exception as e: #Tilkynna notanda um villu í LiDAR
        print(f"LiDAR error: {e}")
    finally: # Slökkva á LiDAR
        Running = False
        lidar.stop()
        lidar.disconnect()
        print("LiDAR disconnected.")

# Keyra LiDAR í bakgrunni
def StartLidar():
    global Running, _thread
    Running = True
    _thread = threading.Thread(target=LiDAR, daemon=True)
    _thread.start()
    time.sleep(8)  # Bíður eftir reset + fyrsta scan
    print("LiDAR ready.")

# Stoppa LiDAR
def StopLidar():
    global Running
    Running = False
    if _thread:
        _thread.join(timeout=3)

# Læsa gögnunum sem að LiDAR mældi í síðustu umferð
def GetSnapshot():
    with Lock:
        return dict(ScanData)
    

# Athuga hvort að hindrun sé undir lágmarki
def under(snapshot, zone, threshold):
    for a, d in snapshot.items():
        if a in zone:
            if d < threshold:
                return True
    return False

# Athuga hvar næsta hindrun er í ákveðnu svæði
def MinDistance(snapshot, zone):
    distances = []
    for angle, dist in snapshot.items():
        if angle in zone:
            distances.append(dist)
    if distances:
        return min(distances)
    else:
        return MaxRange