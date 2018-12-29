from __future__ import division
import numpy as np
from scipy import *
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt



def rysujKrok(czas, sygnal, freqs, sygnalHz, krok=200, tytul=''):
    fig = plt.figure(figsize=(20, 12), dpi=80)
    fig.suptitle(tytul, fontsize=15)

    # print("\nTrwa rysowanie wykresu w dziedzinie czasu...")
    ax = fig.add_subplot(211)
    plt.xlabel("Czas [s]", fontsize=13)
    plt.ylabel("Amplituda", fontsize=13)
    ax.plot(czas, sygnal, '-')

    # print("Trwa rysowanie wykresu w dziedzinie częstotliwości...")
    ax = fig.add_subplot(212)
    plt.xlabel("Częstotliwość [Hz]", fontsize=13)
    plt.ylabel("Amplituda", fontsize=13)
    ax.stem(freqs[::krok], sygnalHz[::krok], '-*')

    plt.show()



def rysuj(czas, sygnal, freqs, sygnalHz, tytul=''):
    fig = plt.figure(figsize=(20, 12), dpi=80)
    fig.suptitle(tytul, fontsize=15)

    # print("\nTrwa rysowanie wykresu w dziedzinie czasu...")
    ax = fig.add_subplot(211)
    plt.xlabel("Czas [s]", fontsize=13)
    plt.ylabel("Amplituda", fontsize=13)
    ax.plot(czas, sygnal, '-')

    # print("Trwa rysowanie wykresu w dziedzinie częstotliwości...")
    ax = fig.add_subplot(212)
    plt.xlabel("Częstotliwość [Hz]", fontsize=13)
    plt.ylabel("Amplituda", fontsize=13)
    ilePunktow = sum(freqs < 2000)
    ax.plot(freqs[:ilePunktow], sygnalHz[:ilePunktow], '-')

    plt.show()




def main():
    tytulPliku = 'trainall/002_M.wav'
    plik = scipy.io.wavfile.read(tytulPliku)
    # print("type(plik) = " + str(type(plik)))
    # print("len(plik) = " + str(len(plik)))

    czestotliwoscProbkowania = plik[0]
    # print("\ntype(czestotliwoscProbkowania) = " + str(type(czestotliwoscProbkowania)))
    # #print("len(sygnal) = " + str(len(sygnal)))
    # print("czestotliwoscProbkowania = " + str(czestotliwoscProbkowania))

    sygnal = plik[1]
    # print("\ntype(sygnal) = " + str(type(sygnal)))
    print("len(sygnal) = " + str(len(sygnal)))
    # print("sygnal.shape = " + str(sygnal.shape))
    # print("sygnal = " + str(sygnal))
    sygnal = np.mean(sygnal, axis=1)
    dlugoscSygnalu = len(sygnal)
    # print("\ntype(sygnal) = " + str(type(sygnal)))
    # print("len(sygnal) = " + str(len(sygnal)))
    # print("sygnal.shape = " + str(sygnal.shape))
    # print("sygnal = " + str(sygnal))
    absoluteSygnal = np.abs(sygnal)
    mediana = np.median(absoluteSygnal)
    print("mediana = " + str(mediana))
    percentyl = np.percentile(absoluteSygnal, 95)
    print("percentyl = " + str(percentyl))


    iloscProbek = dlugoscSygnalu
    czas = np.arange(0, iloscProbek)
    czas = czas / czestotliwoscProbkowania


    # sygnal w dziedzinie czestotliwosci
    sygnalHz = fft(sygnal)

    # modul sygnalu
    sygnalHz = abs(sygnalHz)

    # normalizacja:
    # dzielenie przez (ilość próbek/2)
    sygnalHz /= (iloscProbek / 2)
    # dzielenie wartosci dla 0Hz jeszce przez 2:
    sygnalHz[0] /= 2

    # ustawienie wartosci na osi x
    freqs = np.arange(0, iloscProbek)
    # print(freqs)
    # print("min(freqs) = " + str(min(freqs)))
    # print("max(freqs) = " + str(max(freqs)))
    freqs = freqs / iloscProbek * czestotliwoscProbkowania
    # print(freqs)
    # print("min(freqs) = " + str(min(freqs)))
    # print("max(freqs) = " + str(max(freqs)))

    rysujKrok(czas, sygnal, freqs, sygnalHz)


    flaga = absoluteSygnal >= percentyl
    print(flaga)
    print("sum(flaga) = " + str(sum(flaga)))

    indeksy = np.where(flaga)[0]
    print("indeksy = " + str(indeksy))

    fragmentSzerokosc = int(czestotliwoscProbkowania / 10)
    # fragmentSzerokosc = czestotliwoscProbkowania

    oknoKaisera = kaiser(fragmentSzerokosc, 5)
    # print("len(oknoKaisera) = " + str(len(oknoKaisera)))
    # print("min(oknoKaisera) = " + str(min(oknoKaisera)))
    # print("max(oknoKaisera) = " + str(max(oknoKaisera)))


    i = 1
    while((i <= 20) and (len(indeksy) > 0) and (indeksy[0] + fragmentSzerokosc < dlugoscSygnalu)):
        indeksPoczatek = indeksy[0]
        indeksKoniec = indeksPoczatek + fragmentSzerokosc

        fragmentSygnal = sygnal[indeksPoczatek : indeksKoniec]
        fragmentSygnal *= oknoKaisera
        fragmentCzas = czas[indeksPoczatek : indeksKoniec]

        iloscProbek = fragmentSzerokosc
        sygnalHz = fft(fragmentSygnal)
        sygnalHz = abs(sygnalHz)
        sygnalHz /= (iloscProbek / 2)
        sygnalHz[0] /= 2
        freqs = np.arange(0, iloscProbek)
        freqs = freqs / iloscProbek * czestotliwoscProbkowania

        tytulWykresu = tytulPliku + " - fragment " + str(i)
        print("\t" + tytulWykresu + "\t[" + str(indeksPoczatek) + ", " + str(indeksKoniec) + "]")
        rysuj(fragmentCzas, fragmentSygnal, freqs, sygnalHz, tytul=tytulWykresu)

        indeksy = indeksy[indeksy >= indeksKoniec]
        i += 1




main()