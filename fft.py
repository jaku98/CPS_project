import sounddevice as sd
import soundfile as sf
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk
import numpy as np
from matplotlib import pyplot as plt
import csv
# nowa galaz
samplerate = 44100
filename = 'wav\output4.wav'

def fft():
    samplerate, mydata = wavfile.read(filename)
    duration = len(mydata)/samplerate
    time = np.arange(0,duration,1/samplerate)
    
    # Zapis mydata do .csv
    with open('exel\data_file.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(mydata)
 
    # Realizacja FFT
    fft = abs(fftpk.rfft(mydata))
    freqs = fftpk.rfftfreq(len(fft), (1.0/samplerate))

    # Szukanie y dla x dla wykresu
    max_y = max(fft)
    max_x = freqs[fft.argmax()]
    print(max_x)

    # Wykres A(t)[s]
    plt.subplot(2,1,1)
    plt.plot(time, mydata)
    plt.xlabel('Czas [t]')
    plt.ylabel('Amplituda')
    plt.title('PRZEBIEG CZASOWY')

    # Wykres A(f)[Hz]
    plt.subplot(2, 1, 2)
    plt.scatter(max_x, max_y, c='r')
    plt.plot(freqs[range(len(fft)//2)], fft[range(len(fft)//2)], '-r')
    plt.legend(["Freq: %2.2f [Hz]" %max_x], loc='upper center' )
    plt.xscale('log')
    plt.xlabel('Częstotliwość (Hz)')
    plt.ylabel('Amplituda')
    plt.title("WIDMO SYGNAŁU")
    
    plt.tight_layout()
    plt.show()

# Sprawdzenie pliku czy jest w folderze
def check():
    try:
        samplerate, mydata = wavfile.read(filename)
    except IOError:
        print("Z pustego i Salomon nie naleje! Nagraj dźwięk :)")
        exit()    

INP_0 = int(input(" Nagraj - 1 \n FFT poprzedniego nagrania - 2 \n Odegraj poprzednie nagranie - 3 \n"))
if INP_0 == 1:
    duration = int(input(" Podaj czas nagrywania [s]  "))
    print("     START")
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, blocking=True)        
    sf.write(filename, mydata, samplerate)
    print("     STOP")
    fft()
elif INP_0 == 2:
    check()
    fft()
else:
    check()
    samplerate, mydata = sf.read(filename)
    print("     START")
    sd.play(samplerate, mydata)
    sd.wait()
    print("     STOP")
    exit()