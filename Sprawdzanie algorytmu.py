from __future__ import division
from pylab import *
from scipy import *
import scipy.io.wavfile

def main():
    plik = scipy.io.wavfile.read('trainall/002_M.wav')
    print("type(plik) = " + str(type(plik)))
    print("len(plik) = " + str(len(plik)))

    czestotliwoscProbkowania = plik[0]
    print("\ntype(czestotliwoscProbkowania) = " + str(type(czestotliwoscProbkowania)))
    #print("len(signal) = " + str(len(signal)))
    print("czestotliwoscProbkowania = " + str(czestotliwoscProbkowania))

    signal = plik[1]
    print("\ntype(signal) = " + str(type(signal)))
    print("len(signal) = " + str(len(signal)))
    print("signal = " + str(signal))




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