import pyaudio
import wave 
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CHUNK = 2**11
RATE = 44100

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    print(peak)
    temp_c = peak

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # # Format plot
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.title('TMP102 Temperature over Time')
    # plt.ylabel('Temperature (deg C)')
flag = True
# i = 0
while True: #go for a few seconds
    # Set up plot to call animate() function periodically
    # ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=0)
    # plt.show()
    p = pyaudio.PyAudio()
    if flag:
        stream = p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                frames_per_buffer=CHUNK)
        flag = False
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    # print(peak)
    if peak > 15000:
        print("BANG")
        stream.stop_stream()
        stream.close()
        p.terminate()
        f = wave.open(r"/home/dank-engine/Desktop/file.wav","rb")  
        #open stream  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        #read data  
        data = f.readframes(CHUNK)  

        #play stream  
        while data:  
            stream.write(data)  
            data = f.readframes(CHUNK)  

        #stop stream  
        stream.stop_stream()  
        stream.close()  

        #close PyAudio  
        p.terminate()  
        flag = True