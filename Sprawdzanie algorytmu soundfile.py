from __future__ import division
import os
import numpy as np
from scipy import *
import soundfile as sf
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
    plt.close()



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

    #plt.show()
    print("\tTrwa zapisywanie do pliku jpg...")
    fig.savefig('./wyniki/' + tytul[15:] + '.jpg')
    plt.close()



def rysujZle(czas, sygnal, freqs, sygnalHz, tytul=''):
    fig = plt.figure(figsize=(20, 12), dpi=80)
    fig.suptitle(tytul + ' (zle)', fontsize=15)

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

    #plt.show()
    print("\tTrwa zapisywanie do pliku jpg...")
    fig.savefig('./zle/' + tytul[15:] + '.jpg')
    plt.close()





def main():
    #tytulPliku = 'trainall/002_M.wav'
    zlePliki = []
    bledy = 0
    licznikRemisow = 0
    dobre = 0
    #sciezkaZrodlowa = 'trainall/'
    #sciezkaZrodlowa = 'trainmy/'
    sciezkaZrodlowa = 'probki_dzwieku/'
    tytulyPlikow = os.listdir(sciezkaZrodlowa)
    #print(tytulyPlikow)
    #for iTytul in range(len(tytulyPlikow))[1:]:
    for iTytul in range(len(tytulyPlikow)):
    #for iTytul in [9, 34, 38, 44, 52, 66, 83, 86]:
    #for iTytul in [0, 1, 2]:
    #for iTytul in [43]:
        #try:
        tytulPliku = sciezkaZrodlowa + tytulyPlikow[iTytul]
        # print("Probuje otworzyć: " + tytulPliku)
        #plik = scipy.io.wavfile.read(tytulPliku)
        plik = sf.read(tytulPliku)
        print(tytulPliku)
        # print("type(plik) = " + str(type(plik)))
        # print("len(plik) = " + str(len(plik)))

        czestotliwoscProbkowania = plik[1]
        # print("\ntype(czestotliwoscProbkowania) = " + str(type(czestotliwoscProbkowania)))
        # print("len(sygnal) = " + str(len(sygnal)))
        # print("czestotliwoscProbkowania = " + str(czestotliwoscProbkowania))

        sygnal = plik[0]
        # print("\ntype(sygnal) = " + str(type(sygnal)))
        # print("len(sygnal) = " + str(len(sygnal)))
        # print("sygnal.shape = " + str(sygnal.shape))
        # print("sygnal = " + str(sygnal))
        if(len(sygnal.shape) > 1):
            sygnal = np.mean(sygnal, axis=1)
            # print("\ntype(sygnal) = " + str(type(sygnal)))
            # print("len(sygnal) = " + str(len(sygnal)))
            # print("sygnal.shape = " + str(sygnal.shape))
            # print("sygnal = " + str(sygnal))

        dlugoscSygnalu = len(sygnal)
        absolutnySygnal = np.abs(sygnal)
        mediana = np.median(absolutnySygnal)
        # print("mediana = " + str(mediana))
        percentyl = np.percentile(absolutnySygnal, 95)
        # print("percentyl = " + str(percentyl))

        iloscProbek = dlugoscSygnalu
        czas = np.arange(0, iloscProbek)
        czas = czas / czestotliwoscProbkowania

        """
        # sygnal w dziedzinie czestotliwosci
        print("Zaczynam fft...")
        sygnalHz = fft(sygnal)
        print("Skonczylem fft.")

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
        """


        flaga = absolutnySygnal >= percentyl
        #print("sum(flaga) = " + str(sum(flaga)))

        indeksy = np.where(flaga)[0]
        #print("indeksy = " + str(indeksy))

        fragmentSzerokosc = int(czestotliwoscProbkowania / 10)
        # fragmentSzerokosc = czestotliwoscProbkowania

        oknoKaisera = kaiser(fragmentSzerokosc, 5)
        # print("len(oknoKaisera) = " + str(len(oknoKaisera)))
        # print("min(oknoKaisera) = " + str(min(oknoKaisera)))
        # print("max(oknoKaisera) = " + str(max(oknoKaisera)))


        kobieta = 0
        mezczyzna = 0
        wynik = ''
        i = 1
        proba = 1
        while((i <= 20) and (len(indeksy) > 0) and (indeksy[0] + fragmentSzerokosc < dlugoscSygnalu)):
            #print("proba = " + str(proba))
            indeksPoczatek = indeksy[0]
            indeksKoniec = indeksPoczatek + fragmentSzerokosc

            fragmentSygnal = np.zeros((fragmentSzerokosc))
            fragmentSygnal += sygnal[indeksPoczatek : indeksKoniec]
            fragmentSygnal *= oknoKaisera
            fragmentCzas = czas[indeksPoczatek : indeksKoniec]

            iloscProbek = fragmentSzerokosc
            sygnalHz = fft(fragmentSygnal)
            sygnalHz = abs(sygnalHz)
            sygnalHz /= (iloscProbek / 2)
            sygnalHz[0] /= 2
            freqs = np.arange(0, iloscProbek)
            freqs = freqs / iloscProbek * czestotliwoscProbkowania


            malyIndeksPoczatek = sum(freqs < 50)
            malyIndeksKoniec = sum(freqs < 1000)
            malySygnalHz = sygnalHz[malyIndeksPoczatek : malyIndeksKoniec]
            malyFreqs = freqs[malyIndeksPoczatek : malyIndeksKoniec]

            #maxFragmentSygnal = max(fragmentSygnal)
            maxFragmentSygnal = max(np.abs(fragmentSygnal))
            maxMalySygnalHz = max(malySygnalHz)
            # print("maxMalySygnalHz = " + str(maxMalySygnalHz))
            # print("maxFragmentSygnal = " + str(maxFragmentSygnal))



            tytulWykresu = tytulPliku[:-4] + " - fragment " + str(proba)
            #rysuj(fragmentCzas, fragmentSygnal, freqs, sygnalHz, tytul=tytulWykresu)


            if(maxMalySygnalHz / maxFragmentSygnal < 0.075):
                i = i
                print("\t" + tytulWykresu + "\t[" + str(indeksPoczatek) + ", " + str(indeksKoniec) + ") - zle")
                rysujZle(fragmentCzas, fragmentSygnal, freqs, sygnalHz, tytul=tytulWykresu)
            else:

                print("\t" + tytulWykresu + "\t[" + str(indeksPoczatek) + ", " + str(indeksKoniec) + ") - dobre")
                i += 1

                #dominujacaCzestotliwosc = malyFreqs[np.argmax(malySygnalHz)]
                #print("dominujacaCzestotliwosc = " + str(dominujacaCzestotliwosc))
                #if (dominujacaCzestotliwosc < 150):
                #    mezczyzna += 1
                #elif (dominujacaCzestotliwosc < 300):
                #    kobieta += 1
                #else:
                j = 1
                while((j < len(malySygnalHz)) and (malySygnalHz[j] - malySygnalHz[j - 1] < 0.09 * maxMalySygnalHz)):
                    j += 1

                if(j < len(malySygnalHz)):
                    #print(str(malyFreqs[j - 1]) + ': ' + str(malySygnalHz[j - 1]))
                    #print(str(malyFreqs[j]) + ': ' + str(malySygnalHz[j]))

                    if(malyFreqs[j] < 160):
                        mezczyzna += 1
                    #elif(malyFreqs[j] < 400):
                    else:
                        kobieta += 1

                rysuj(fragmentCzas, fragmentSygnal, freqs, sygnalHz, tytul=tytulWykresu)


            indeksy = indeksy[indeksy >= indeksKoniec]
            proba += 1

        if(mezczyzna == kobieta):
            print("\t\tTuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuutaj")
            licznikRemisow += 1
        print('mezczyzna ' + str(mezczyzna) + ' - ' + str(kobieta) + ' kobieta')
        if(mezczyzna > kobieta):
            wynik = 'M'
        else:
            wynik = 'K'

        print('wynik = ' + wynik)
        print('tytulyPlikow[iTytul][-5] = ' + tytulyPlikow[iTytul][-5])
        if(wynik == tytulyPlikow[iTytul][-5]):
            dobre += 1
        else:
            zlePliki.append(tytulyPlikow[iTytul])
        """
        except ValueError:
            print("Błąd dla pliku: " + str(tytulyPlikow[iTytul]))
            bledy += 1
        """

        iTytul += 1

    print("\nBłędnie otworzone pliki: " + str(bledy))
    print(dobre,91,dobre/91)
    print("licznik remisow = " + str(licznikRemisow))
    for tytul in zlePliki:
        print(tytul)




main()