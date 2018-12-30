import os
import subprocess

def main():
    zlePliki = []
    dobre = 0
    wszystkie = 0
    sciezkaZrodlowa = 'trainall/'
    tytulyPlikow = os.listdir(sciezkaZrodlowa)

    for iTytul in range(len(tytulyPlikow)):
        tytulPliku = sciezkaZrodlowa + tytulyPlikow[iTytul]
        wynik = subprocess.check_output("python inf132216_inf132325.py " + tytulPliku)
        wynik = str(wynik)[2]

        wszystkie += 1
        if (wynik == tytulyPlikow[iTytul][-5]):
            dobre += 1
            print(str(iTytul) + ': ' + tytulyPlikow[iTytul] + '\t' + wynik + ' (' + tytulyPlikow[iTytul][-5] + ')')
        else:
            zlePliki.append(tytulyPlikow[iTytul])
            print(str(iTytul) + ': ' + tytulyPlikow[iTytul] + '\t' + wynik + ' (' + tytulyPlikow[iTytul][-5] + ') \t\tBLAD!!!')

    print(str(dobre) + '/' + str(wszystkie) + ' (' + str(dobre / wszystkie) + ')')
    print("Błędnie rozpoznane pliki:")
    for tytul in zlePliki:
        print(tytul)


main()