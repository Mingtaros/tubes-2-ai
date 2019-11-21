from experta import *
import numpy as np

class ShapeIdentifier(KnowledgeEngine):
    result = []

    #bentuk-bentuk dasar
    @Rule(Fact(jumlah_sisi = 3))
    def segitiga(self):
        self.result.append("Segitiga")
    
    @Rule(Fact(jumlah_sisi = 4))
    def segiempat(self):
        self.result.append("Segi Empat")
        
    @Rule(Fact(jumlah_sisi = 5))
    def segilima(self):
        self.result.append("Segi Lima")

    @Rule(Fact(jumlah_sisi = 6))
    def segienam(self):
        self.result.append("Segi Enam")

    # nice to have
    @Rule(Fact(jumlah_sisi = BETWEEN(7, 15))) #between bersifat inklusif [7, 15]
    def elips(self):
        self.result.append("Elips")

    #nice to have
    @Rule(Fact(jumlah_sisi = GE(15)))
    def lingkaran(self):
        self.result.append("Lingkaran")

    #bentuk-bentuk advanced
    #....

if __name__ == "__main__":
    while (True):
        shape_detector = ShapeIdentifier()
        shape_detector.reset()
        shape_detector.result = [] #reset
        coordinates = list(input("Koordinat: "))
        shape_detector.declare(Fact(jumlah_sisi = len(coordinates)))
        shape_detector.run()
        print(shape_detector.result)
        