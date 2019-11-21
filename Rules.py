from experta import *
import numpy as np

class ShapeIdentifier(KnowledgeEngine):
    result = []

    #bentuk-bentuk dasar
    @Rule(Fact(jumlah_sisi = 3))
    def segitiga(self):
        self.result.append(("Segitiga", "(jumlah_sisi == 3) ==> Segitiga"))
    
    @Rule(Fact(jumlah_sisi = 4))
    def segiempat(self):
        self.result.append(("Segi Empat", "(jumlah_sisi == 4) ==> Segi Empat"))
        
    @Rule(Fact(jumlah_sisi = 5))
    def segilima(self):
        self.result.append(("Segi Lima", "(jumlah_sisi == 5) ==> Segi Lima"))

    @Rule(Fact(jumlah_sisi = 6))
    def segienam(self):
        self.result.append(("Segi Enam", "(jumlah_sisi == 6) ==> Segi Enam"))

    #bentuk-bentuk advanced
    #segi tiga
    @Rule(AS.Fact << Fact(jumlah_sisi = 3))
    def segitiga_lancip(self, Fact):
        if (not [x for x in Fact['list_of_angles'] if (x >= 90)]): #tidak ada sudut yang >= 90 derajat
            self.result.append(("Segitiga Lancip", "(jumlah_sisi == 3) && (angles < 90) ==> Segitiga Lancip"))

    @Rule(AS.Fact << Fact(jumlah_sisi = 3))
    def segitiga_tumpul(self, Fact):
        if ([x for x in Fact['list_of_angles'] if (x > 90)]): #ada sudut yang > 90 derajat
            self.result.append(("Segitiga Tumpul", "(jumlah_sisi == 3) && ((angle_1 || angle_2 || angle_3) > 90) ==> Segitiga Tumpul"))

    @Rule(AS.Fact << Fact(jumlah_sisi = 3))
    def segitiga_sikusiku(self, Fact):
        if ([x for x in Fact['list_of_angles'] if (x == 90)]):
            self.result.append(("Segitiga Siku-siku", "(jumlah_sisi == 3) && (90 in angles) ==> Segitiga Siku-siku"))

    @Rule(AS.Fact << Fact(jumlah_sisi = 3))
    def segitiga_sama_kaki(self, Fact):
        # kalo ada duplicate berarti dia sama kaki
        if (len(Fact['list_of_angles']) == len(set(Fact['list_of_angles']))):
            self.result.append(("Segitiga Sama Kaki", "(jumlah_sisi == 3) && (angle_1 == angle_2) ==> Segitiga Sama Kaki"))

            #conditional
            if ([x for x in Fact['list_of_angles'] if (x == 90)]):
                self.result.append(("Segitiga Sama Kaki dan Siku-siku", "(jumlah_sisi == 3) && (angle_1 == angle_2) && (90 in angles) ==> Segitiga Sama Kaki dan Siku-siku"))

            elif (not [x for x in Fact['list_of_angles'] if (x >= 90)]): #tidak ada sudut yang >= 90 derajat
                self.result.append(("Segitiga Sama Kaki dan Lancip", "(jumlah_sisi == 3) && (angle_1 == angle_2) && (angles < 90) ==> Segitiga Sama Kaki dan Lancip"))

            elif ([x for x in Fact['list_of_angles'] if (x > 90)]): #ada sudut yang > 90 derajat
                self.result.append(("Segitiga Tumpul", "(jumlah_sisi == 3) && (angle_1 == angle_2) && ((angle_1 || angle_2 || angle_3) > 90) ==> Segitiga Tumpul"))

    @Rule(AS.Fact << Fact(jumlah_sisi = 3))
    def segitiga_sama_sisi(self, Fact):
        if (len(set(Fact['list_of_angles'])) == 1 and Fact['list_of_angles'][0] == 60):
            self.result.append(("Segitiga Sama Sisi", "(jumlah_sisi == 3) && (angle_1 == angle_2 == angle_3) && (angle_1 == 60) ==> Segitiga Sama Sisi"))

    #segi empat
    @Rule(AS.Fact << Fact(jumlah_sisi = 4))
    def jajaran_genjang(self, Fact):
        if (Fact['list_of_angles'][0] == Fact['list_of_angles'][2] and Fact['list_of_angles'][1] == Fact['list_of_angles'][3]):
            self.result.append(("Jajaran Genjang", "(jumlah_sisi == 4) && (angle_1 == angle_3) && (angle_2 == angle_4) ==> Jajaran Genjang"))

            if (len(set(Fact['list_of_angles'])) == 1 and Fact['list_of_angles'][0] == 90):
                self.result.append(("Segi Empat Beraturan", "(jumlah_sisi == 4) && (angle_1 == angle_3) && (angle_2 == angle_4) && (angle_1 == angle_2 == angle_3 == angle_4) && (angle_1 == 90) ==> Segi Empat Beraturan"))

            elif (len(set(Fact['list_of_angles'])) == 2 and (90 not in Fact['list_of_angles'])):
                self.result.append(("Segi Empat Berbentuk Layang-layang", "(jumlah_sisi == 4) && (angle_1 == angle_3) && (angle_2 == angle_4) && (90 not in angles) ==> Segi Empat Berbentuk Layang-layang"))

    @Rule(AS.Fact << Fact(jumlah_sisi = 4))
    def trapesium_sama_kaki(self, Fact):
        if ((Fact['list_of_angles'][0] == Fact['list_of_angles'][1] and Fact['list_of_angles'][2] == Fact['list_of_angles'][3]) or
            (Fact['list_of_angles'][0] == Fact['list_of_angles'][3] and Fact['list_of_angles'][1] == Fact['list_of_angles'][2])):
            self.result.append(("Trapesium Sama Kaki", "(jumlah_sisi == 4) && (angle_1 == angle_2 && angle_3 == angle_4) || (angle_1 == angle_4 && angle_2 == angle_3) ==> Trapesium Sama Kaki"))

    @Rule(AS.Fact << Fact(jumlah_sisi = 4))
    def trapesium_rata(self, Fact):
        n_siku = len([x for x in Fact['list_of_angles'] if (x == 90)])
        n_tumpul = len([x for x in Fact['list_of_angles'] if (x > 90)])
        n_lancip = len([x for x in Fact['list_of_angles'] if (x < 90)])
        if (n_siku == 2 and n_tumpul == 1 and n_lancip == 1):
            index_tumpul = Fact['list_of_angles'].index(max(Fact['list_of_angles']))
            index_lancip = Fact['list_of_angles'].index(min(Fact['list_of_angles']))
            if (index_tumpul < index_lancip):
                #karena counter-clockwise, maka jika sudut tumpul ditemukan sebelum sudut lancip, maka trapesium rata kiri /__|
                self.result.append(("Trapesium Rata Kiri", "(jumlah_sisi == 4) && (index_tumpul < index_lancip) ==> Trapesium Rata Kiri"))
            else:
                #jika sudut tumpul ditemukan setelah sudut lancip, maka trapesium rata kanan |_\
                assert(index_tumpul > index_lancip)
                self.result.append(("Trapesium Rata Kanan", "(jumlah_sudut == 4) && (index_tumpul > index_lancip) ==> Trapesium Rata Kanan"))

    #segi lima
    @Rule(AS.Fact << Fact(jumlah_sisi = 5))
    def segilima_sama_sisi(self, Fact):
        if (len(set(Fact['list_of_angles'])) == 1 and Fact['list_of_angles'][0] == 108):
            self.result.append(("Segi Lima Sama Sisi", "(jumlah_sisi == 5) && (angle_1 == angle_2 == angle_3 == angle_4 == angle_5) && (angle_1 == 108) ==> Segi Lima Sama Sisi"))

    #segi enam
    @Rule(AS.Fact << Fact(jumlah_sisi = 6))
    def segienam_sama_sisi(self, Fact):
        if (len(set(Fact['list_of_angles'])) == 1 and Fact['list_of_angles'][0] == 120):
            self.result.append(("Segi Enam Sama Sisi", "(jumlah_sisi == 6) && (angle_1 == angle_2 == angle_3 == angle_4 == angle_5 == angle_6) && (angle_1 == 120) ==> Segi Enam Sama Sisi"))


if __name__ == "__main__":
    while (True):
        shape_detector = ShapeIdentifier()
        shape_detector.reset()
        shape_detector.result = [] #reset
        coordinates = list(input("Koordinat: "))
        shape_detector.declare(Fact(jumlah_sisi = len(coordinates)))
        shape_detector.run()
        print(shape_detector.result)
        