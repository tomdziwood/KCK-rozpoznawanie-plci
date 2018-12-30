from __future__ import division
import os
import numpy as np
from scipy import *
import soundfile as sf
import sys
import math


def main():
    #sciezkaZrodlowa = 'trainall/'
    #sciezkaZrodlowa = 'trainmy/'
    sciezkaZrodlowa = 'probki_dzwieku/'
    tytulyPlikow = os.listdir(sciezkaZrodlowa)
    for iTytul in range(len(tytulyPlikow)):
        wynik = 'K'
        kobietaCzestotliwosc = []
        mezczyznaCzestotliwosc = []
        try:
            tytulPliku = sciezkaZrodlowa + tytulyPlikow[iTytul]
            plik = sf.read(tytulPliku)
            print("\n" + tytulyPlikow[iTytul])

            czestotliwoscProbkowania = plik[1]

            sygnal = plik[0]
            if (len(sygnal.shape) > 1):
                sygnal = np.mean(sygnal, axis=1)

            dlugoscSygnalu = len(sygnal)
            absolutnySygnal = np.abs(sygnal)
            percentyl = np.percentile(absolutnySygnal, 95)  # wartość amplitudy, dla której uznawane jest trwanie głosu

            flaga = absolutnySygnal >= percentyl
            indeksy = np.where(flaga)[0]    # tablica zawiera indeksy wskazujace na miejsca, gdzie przekroczona jest wartość 'percentyl'

            fragmentSzerokosc = int(czestotliwoscProbkowania / 10)  # długość badanego fragmentu będzie wynosić 0.1 sekundy
            oknoKaisera = kaiser(fragmentSzerokosc, 5)

            kobieta = 0
            mezczyzna = 0
            i = 1
            proba = 1
            while ((i <= 20) and (len(indeksy) > 0) and (indeksy[0] + fragmentSzerokosc < dlugoscSygnalu)):
                indeksPoczatek = indeksy[0]
                indeksKoniec = indeksPoczatek + fragmentSzerokosc

                fragmentSygnal = np.zeros((fragmentSzerokosc))
                fragmentSygnal += sygnal[indeksPoczatek: indeksKoniec]
                fragmentSygnal *= oknoKaisera

                iloscProbek = fragmentSzerokosc
                sygnalHz = fft(fragmentSygnal)
                sygnalHz = abs(sygnalHz)
                sygnalHz /= (iloscProbek / 2)
                sygnalHz[0] /= 2
                freqs = np.arange(0, iloscProbek)
                freqs = freqs / iloscProbek * czestotliwoscProbkowania

                malyIndeksPoczatek = sum(freqs < 50)
                malyIndeksKoniec = sum(freqs < 1000)
                malySygnalHz = sygnalHz[malyIndeksPoczatek: malyIndeksKoniec]
                malyFreqs = freqs[malyIndeksPoczatek: malyIndeksKoniec]

                maxFragmentSygnal = max(np.abs(fragmentSygnal))
                maxMalySygnalHz = max(malySygnalHz)

                # dany fragment jest odpowiedni do zbadania, jeśli największa amplituda w dziedzinie częstotliwości
                # jest odpowiednio nie mała w stosunku do amplitudy fragmentu w dziedzinie czasu
                if (maxMalySygnalHz / maxFragmentSygnal >= 0.075):
                    i += 1
                    j = 1
                    # wyszukiwanie momentu, w którym następuje znaczący wzrost amplitudy
                    while ((j < len(malySygnalHz)) and (malySygnalHz[j] - malySygnalHz[j - 1] < 0.09 * maxMalySygnalHz)):
                        j += 1

                    if (j < len(malySygnalHz)):
                        if (malyFreqs[j] < 160):
                            mezczyzna += 1
                            mezczyznaCzestotliwosc.append(malyFreqs[j])
                        else:
                            kobieta += 1
                            kobietaCzestotliwosc.append(malyFreqs[j])

                indeksy = indeksy[indeksy >= indeksKoniec]
                proba += 1


            if (mezczyzna > kobieta):
                wynik = 'M'
                print("Częstotliwość podstawowa: " + str(round(np.mean(mezczyznaCzestotliwosc), 2)) + ' Hz')
            else:
                wynik = 'K'
                print("Częstotliwość podstawowa: " + str(round(np.mean(kobietaCzestotliwosc), 2)) + ' Hz')

        except ValueError:
            # Łapanie wyjatku związanego z problemami z odczytywaniem pliku .wav
            wynik = 'K'
        except Exception:
            # Łapanie wyjatku jakiegokolwiek, no niestety...
            wynik = 'K'


        print(wynik)


main()