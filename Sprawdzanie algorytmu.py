from __future__ import division
import numpy as np
from scipy import *
import scipy.io.wavfile
import matplotlib.pyplot as plt

def main():
    plik = scipy.io.wavfile.read('trainmy/005_K.wav')
    print("type(plik) = " + str(type(plik)))
    print("len(plik) = " + str(len(plik)))

    czestotliwoscProbkowania = plik[0]
    print("\ntype(czestotliwoscProbkowania) = " + str(type(czestotliwoscProbkowania)))
    #print("len(signal) = " + str(len(signal)))
    print("czestotliwoscProbkowania = " + str(czestotliwoscProbkowania))

    signal = plik[1]
    print("\ntype(signal) = " + str(type(signal)))
    print("len(signal) = " + str(len(signal)))
    print("signal.shape = " + str(signal.shape))
    print("signal = " + str(signal))
    signal = np.mean(signal, axis=1)
    print("\ntype(signal) = " + str(type(signal)))
    print("len(signal) = " + str(len(signal)))
    print("signal.shape = " + str(signal.shape))
    print("signal = " + str(signal))


    iloscProbek = len(signal)
    okresProbkowania = 1 / czestotliwoscProbkowania
    #czas = np.arange(0, liczbaPrzebiegow * okres, okresProbkowania)
    czas = np.arange(0, iloscProbek)
    czas = czas / czestotliwoscProbkowania


    print("\nTrwa rysowanie wykresu w dziedzinie czasu...")
    fig = plt.figure(figsize=(15, 6), dpi=80)

    ax = fig.add_subplot(121)
    plt.xlabel("Czas [s]", fontsize=13)
    plt.ylabel("Amplituda", fontsize=13)
    ax.plot(czas, signal, '-')
    print("Narysowano!")


    # sygnal w dziedzinie czestotliwosci
    signalHz = fft(signal)

    # modul sygnalu
    signalHz = abs(signalHz)

    # normalizacja:
    # dzielenie przez (ilość próbek/2)
    signalHz /= (iloscProbek / 2)
    # dzielenie wartosci dla 0Hz jeszce przez 2:
    signalHz[0] /= 2

    # ustawienie wartosci na osi x
    freqs = np.arange(0, iloscProbek)
    print(freqs)
    print("min(freqs) = " + str(min(freqs)))
    print("max(freqs) = " + str(max(freqs)))
    freqs = freqs / iloscProbek * czestotliwoscProbkowania
    print(freqs)
    print("min(freqs) = " + str(min(freqs)))
    print("max(freqs) = " + str(max(freqs)))

    print("\nTrwa rysowanie wykresu w dziedzinie częstotliwości...")
    print("len(signalHz[::200] = " + str(len(signalHz[::200])))
    ax = fig.add_subplot(122)
    plt.xlabel("Częstotliwość [Hz]", fontsize=13)
    plt.ylabel("Amplituda", fontsize=13)
    ax.stem(freqs[::200], signalHz[::200], '-*')
    print("Narysowano!")

    plt.show()






    """
    okres = 1 / czestotliwosc
    okresProbkowania = 1 / czestotliwoscProbkowania

    t = np.arange(0, liczbaPrzebiegow * okres, okresProbkowania)
    # generujemy momenty, w których pobieramy próbki

    n = len(t)
    # ilość próbek

    FUNC = lambda t: amplituda * sin(2 * pi * t * czestotliwosc)
    # def. funkcji (tutaj sinus)

    signal = FUNC(t)
    # funkcja sprobkowana

    fig = plt.figure(figsize=(15, 6), dpi=80)
    ax = fig.add_subplot(121)
    xlabel("Czas [s]", fontsize=13)
    ylabel("Amplituda", fontsize=13)

    ## --- POMOCNICZY SYGNAL
    base_t = np.arange(0, liczbaPrzebiegow * okres, 1.0 / 200.0)
    base_signal = FUNC(base_t)
    ax.plot(base_t, base_signal, linestyle='-', color='red')
    ax.set_ylim([min(base_signal), max(base_signal)])
    ## ---

    ax.plot(t, signal, 'o')

    signal1 = fft(signal)
    # sygnal w dziedzinie czestotliwosci
    signal1 = abs(signal1)
    # modul sygnalu

    # normalizacja:
    # dzielenie przez (ilość próbek/2)
    signal1 /= (n / 2)
    # dzielenie wartosci dla 0Hz jeszce przez 2:
    signal1[0] /= 2

    # ustawienie wartosci na osi x
    freqs = np.arange(0, n)
    freqs = freqs * czestotliwoscProbkowania / n
    # freqs = list(range(n))
    # for i in range(len(freqs)):
    #    freqs[i] = i * czestotliwoscProbkowania / n

    # nie rysowanie slupków bliskich zero
    signal1[signal1 < 1 / 1000000] = 0
    freqs[signal1 == 0] = 0

    ax = fig.add_subplot(122)
    xlabel("Częstotliwość [Hz]", fontsize=13)
    ylabel("Amplituda", fontsize=13)
    ymax = max(signal1)
    if (ymax > 3.0):
        ax.set_ylim([0.0, ymax])
    else:
        ax.set_ylim([0.0, 3.0])
    stem(freqs, signal1, '-*')

    show()
    """

main()