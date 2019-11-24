from experta import *
import numpy as np

degree_epsilon = 2

def isSame(deg1, deg2):
    return (deg2-degree_epsilon <= deg1 <= deg2+degree_epsilon)

def isExistElementInError(li, num, eps):
    return bool([x for x in li if (num-eps <= x <= num+eps)])

class ShapeIdentifier(KnowledgeEngine):
    result = []

    #bentuk-bentuk dasar
    @Rule(Fact(jumlah_sudut = 3))
    def segitiga(self):
        self.result.append(("Segitiga", "(jumlah_sudut == 3) ==> Segitiga"))
    
    @Rule(Fact(jumlah_sudut = 4))
    def segiempat(self):
        self.result.append(("Segi Empat", "(jumlah_sudut == 4) ==> Segi Empat"))
        
    @Rule(Fact(jumlah_sudut = 5))
    def segilima(self):
        self.result.append(("Segi Lima", "(jumlah_sudut == 5) ==> Segi Lima"))

    @Rule(Fact(jumlah_sudut = 6))
    def segienam(self):
        self.result.append(("Segi Enam", "(jumlah_sudut == 6) ==> Segi Enam"))

    #bentuk-bentuk advanced
    #segi tiga
    @Rule(AS.Fact << Fact(jumlah_sudut = L(3)))
    def segitiga_lancip(self, Fact):
        if (not [x for x in Fact['list_of_angles'] if (x >= 90)]): #tidak ada sudut yang >= 90 derajat
            self.result.append(("Segitiga Lancip", "(jumlah_sudut == 3) && (angles < 90) ==> Segitiga Lancip"))

    @Rule(AS.Fact << Fact(jumlah_sudut = L(3)))
    def segitiga_tumpul(self, Fact):
        if ([x for x in Fact['list_of_angles'] if (x > 90)]): #ada sudut yang > 90 derajat
            self.result.append(("Segitiga Tumpul", "(jumlah_sudut == 3) && ((angle_1 || angle_2 || angle_3) > 90) ==> Segitiga Tumpul"))

    @Rule(AS.Fact << Fact(jumlah_sudut = L(3)))
    def segitiga_sikusiku(self, Fact):
        if (isExistElementInError(Fact['list_of_angles'], 90, degree_epsilon)):
            self.result.append(("Segitiga Siku-siku", "(jumlah_sudut == 3) && (90 in angles) ==> Segitiga Siku-siku"))

    @Rule(AS.Fact << Fact(jumlah_sudut = L(3)))
    def segitiga_sama_kaki(self, Fact):
        # kalo ada duplicate berarti dia sama kaki
        if (len(Fact['list_of_angles']) == len(set(Fact['list_of_angles']))):
            self.result.append(("Segitiga Sama Kaki", "(jumlah_sudut == 3) && (angle_1 == angle_2) ==> Segitiga Sama Kaki"))

            #conditional
            if (isExistElementInError(Fact['list_of_angles'], 90, degree_epsilon)):
                self.result.append(("Segitiga Sama Kaki dan Siku-siku", "(jumlah_sudut == 3) && (angle_1 == angle_2) && (90 in angles) ==> Segitiga Sama Kaki dan Siku-siku"))

            elif (not [x for x in Fact['list_of_angles'] if (x >= 90)]): #tidak ada sudut yang >= 90 derajat
                self.result.append(("Segitiga Sama Kaki dan Lancip", "(jumlah_sudut == 3) && (angle_1 == angle_2) && (angles < 90) ==> Segitiga Sama Kaki dan Lancip"))

            elif ([x for x in Fact['list_of_angles'] if (x > 90)]): #ada sudut yang > 90 derajat
                self.result.append(("Segitiga Sama Kaki dan Tumpul", "(jumlah_sudut == 3) && (angle_1 == angle_2) && ((angle_1 || angle_2 || angle_3) > 90) ==> Segitiga Tumpul"))

    @Rule(AS.Fact << Fact(jumlah_sudut = L(3)))
    def segitiga_sama_sisi(self, Fact):
        SUDUT_SEGITIGA_SAMA_SISI = 60
        if (len(set([SUDUT_SEGITIGA_SAMA_SISI for x in Fact['list_of_angles'] if (x-degree_epsilon <= SUDUT_SEGITIGA_SAMA_SISI <= x+degree_epsilon)])) == 1 and isExistElementInError(Fact['list_of_angles'], SUDUT_SEGITIGA_SAMA_SISI, degree_epsilon)):
            self.result.append(("Segitiga Sama Sisi", "(jumlah_sudut == 3) && (angle_1 == angle_2 == angle_3) && (angle_1 == 60) ==> Segitiga Sama Sisi"))

    #segi empat
    @Rule(AS.Fact << Fact(jumlah_sudut = L(4)))
    def jajaran_genjang(self, Fact):
        if (isSame(Fact['list_of_angles'][0], Fact['list_of_angles'][2]) and isSame(Fact['list_of_angles'][1], Fact['list_of_angles'][3])):
            self.result.append(("Jajaran Genjang", "(jumlah_sudut == 4) && (angle_1 == angle_3) && (angle_2 == angle_4) ==> Jajaran Genjang"))

            if (len(set([90 for x in Fact['list_of_angles'] if (x-degree_epsilon <= 90 <= x+degree_epsilon)])) == 1 and isExistElementInError(Fact['list_of_angles'], 90, degree_epsilon)):
                self.result.append(("Segi Empat Beraturan", "(jumlah_sudut == 4) && (angle_1 == angle_3) && (angle_2 == angle_4) && (angle_1 == angle_2 == angle_3 == angle_4) && (angle_1 == 90) ==> Segi Empat Beraturan"))

            elif (len(set([round(x) for x in Fact['list_of_angles']])) == 2 and (not isExistElementInError(Fact['list_of_angles'], 90, degree_epsilon))):
                self.result.append(("Segi Empat Berbentuk Layang-layang", "(jumlah_sudut == 4) && (angle_1 == angle_3) && (angle_2 == angle_4) && (90 not in angles) ==> Segi Empat Berbentuk Layang-layang"))

    @Rule(AS.Fact << Fact(jumlah_sudut = L(4)))
    def trapesium_sama_kaki(self, Fact):
        if (not isExistElementInError(Fact['list_of_angles'], 90, degree_epsilon)) and ((isSame(Fact['list_of_angles'][0], Fact['list_of_angles'][1]) and isSame(Fact['list_of_angles'][2], Fact['list_of_angles'][3]) and not isSame(Fact['list_of_angles'][0], Fact['list_of_angles'][2])) or
            (isSame(Fact['list_of_angles'][0], Fact['list_of_angles'][3]) and isSame(Fact['list_of_angles'][1], Fact['list_of_angles'][2]) and not isSame(Fact['list_of_angles'][0], Fact['list_of_angles'][1]))):
            self.result.append(("Trapesium", "(jumlah_sudut == 4) && ((angle_1 == angle_2 && angle_3 == angle_4) || (angle_1 == angle_4 && angle_2 == angle_3)) || (index_tumpul < index_lancip) || (index_tumpul > index_lancip) ==> Trapesium"))
            self.result.append(("Trapesium Sama Kaki", "(jumlah_sudut == 4) && (angle_1 == angle_2 && angle_3 == angle_4) || (angle_1 == angle_4 && angle_2 == angle_3) ==> Trapesium Sama Kaki"))

    @Rule(AS.Fact << Fact(jumlah_sudut = L(4)))
    def trapesium_rata(self, Fact):
        n_siku = len([x for x in Fact['list_of_angles'] if (90-degree_epsilon <= x <= 90+degree_epsilon)])
        n_tumpul = len([x for x in Fact['list_of_angles'] if (x > 90)])
        n_lancip = len([x for x in Fact['list_of_angles'] if (x < 90)])
        if (n_siku == 2 and n_tumpul == 1 and n_lancip == 1):
            index_tumpul = Fact['list_of_angles'].index(max(Fact['list_of_angles']))
            index_lancip = Fact['list_of_angles'].index(min(Fact['list_of_angles']))
            self.result.append(("Trapesium", "(jumlah_sudut == 4) && ((angle_1 == angle_2 && angle_3 == angle_4) || (angle_1 == angle_4 && angle_2 == angle_3)) || (index_tumpul < index_lancip) || (index_tumpul > index_lancip) ==> Trapesium"))
            if (index_tumpul < index_lancip):
                #karena counter-clockwise, maka jika sudut tumpul ditemukan sebelum sudut lancip, maka trapesium rata kiri /__|
                self.result.append(("Trapesium Rata Kiri", "(jumlah_sudut == 4) && (index_tumpul < index_lancip) ==> Trapesium Rata Kiri"))
            else:
                #jika sudut tumpul ditemukan setelah sudut lancip, maka trapesium rata kanan |_\
                assert(index_tumpul > index_lancip)
                self.result.append(("Trapesium Rata Kanan", "(jumlah_sudut == 4) && (index_tumpul > index_lancip) ==> Trapesium Rata Kanan"))

    #segi lima
    @Rule(AS.Fact << Fact(jumlah_sudut = L(5)))
    def segilima_sama_sisi(self, Fact):
        if (len(set([round(x) for x in Fact['list_of_angles']])) == 1 and (108-degree_epsilon <= Fact['list_of_angles'][0] <= 108+degree_epsilon)):
            self.result.append(("Segi Lima Sama Sisi", "(jumlah_sudut == 5) && (angle_1 == angle_2 == angle_3 == angle_4 == angle_5) && (angle_1 == 108) ==> Segi Lima Sama Sisi"))

    #segi enam
    @Rule(AS.Fact << Fact(jumlah_sudut = L(6)))
    def segienam_sama_sisi(self, Fact):
        if (len(set([120 for x in Fact['list_of_angles'] if (x-degree_epsilon <= 120 <= x+degree_epsilon)])) == 1 and (120-degree_epsilon <= Fact['list_of_angles'][0] <= 120+degree_epsilon)):
            self.result.append(("Segi Enam Sama Sisi", "(jumlah_sudut == 6) && (angle_1 == angle_2 == angle_3 == angle_4 == angle_5 == angle_6) && (angle_1 == 120) ==> Segi Enam Sama Sisi"))


if __name__ == "__main__":
    while (True):
        shape_detector = ShapeIdentifier()
        shape_detector.reset()
        shape_detector.result = [] #reset
        coordinates = list(input("Koordinat: "))
        shape_detector.declare(Fact(jumlah_sudut = len(coordinates)))
        shape_detector.run()
        print(shape_detector.result)
        