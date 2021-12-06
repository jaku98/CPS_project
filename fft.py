from numpy.lib.function_base import append
import sounddevice as sd
import soundfile as sf
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk
import numpy as np
from matplotlib import pyplot as plt
import csv
import signal_envelope as se

samplerate = 44100
filename = 'wav/output3.wav'

def fft():
    # Wywołanie nagrania i zapis
    samplerate, mydata = wavfile.read(filename)
    duration = len(mydata)/samplerate
    
    # Realizacja FFT
    fft = abs(fftpk.rfft(mydata))
    freqs = fftpk.rfftfreq(len(fft), (1.0/samplerate))

    # Szukanie y dla x dla wykresu
    max_y = max(fft)
    max_x = freqs[fft.argmax()]

    # Oś ox na czas i volt na dB
    time = np.arange(0,duration,1/samplerate)
    mydata = 20*np.log10(mydata / 5.0)

    # Wykres A(t)[s]
    plt.figure('WYKRESY')
    plt.subplot(3,1,1)
    plt.plot(time, mydata)
    plt.xlabel('Czas [t]')
    plt.ylabel('Amplituda [dB]')
    plt.title('PRZEBIEG CZASOWY A[t]')

    # Wykres A(f)[Hz]
    plt.subplot(3, 1, 2)
    plt.scatter(max_x, max_y, c='r')
    plt.plot(freqs[range(len(fft)//2)], fft[range(len(fft)//2)], '-r')
    plt.legend(["Freq: %2.2f [Hz]" %max_x], loc='upper center' )
    plt.xscale('log')
    plt.xlabel('Częstotliwość (Hz)')
    plt.ylabel('Amplituda')
    plt.title("WIDMO SYGNAŁU F[f]")
     
    # Obwiednia do wyznaczenia ch-ki kierunkowej
    W, _ = se.read_wav(filename)
    X_envelope = se.get_frontiers(W, 1)
   
    plt.subplot(3, 1, 3)
    plt.plot(X_envelope, np.abs(W[X_envelope]), '-g')
    plt.title("OBWIEDNIA SYGNAŁU A[t]")
    plt.tight_layout()
    plt.show()

    list_abs =[]
    absx = np.abs(W[X_envelope])
    absx = list(absx)
    for x in range(len(absx)):
        if absx[x] > 150:
            list_abs.append(absx[x])
    
    # Zapis obwiedni do .csv
    with open('exel\data_file2.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(list_abs)
    
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