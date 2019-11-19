from experta import *
from random import choice

class ShapeIdentifier(KnowledgeEngine):
    @Rule(Fact(color = "green", kaki = True))
    def green_Fact(self):
        print("walk")
    
    @Rule(Fact(color = "green", kaki = True))
    def red_Fact(self):
        print("stop")
    
    @Rule(AS.Fact << Fact(color = "yellow", kaki = False))
    def cautious(self, Fact):
        print("Be cautious because light is", Fact["color"])

    @Rule(Fact(color = "yellow"))
    def itsyellow(self):
        print("ya iya itu")
    
    @Rule(AS.Fact << Fact(color = "red", kaki = False))
    def cautious_banget(self, Fact):
        self.cautious(Fact)

if __name__ == "__main__":
    engine = ShapeIdentifier()
    while (True):
        color = input("color: ")
        kaki = bool(input("kaki: ")) #klo mau resultnya false, langsung enter aja
        engine.reset()
        engine.declare(Fact(color = color, kaki = kaki))
        engine.run()

# bisa ngetrigger lebih dari 1 rule
# bisa lebih dari 1 fakta dalam 1 rule ==> Fact(f1 = d1, f2 = d2, f3 = d3, ..., fn = dn) (suatu and)
# bisa juga pake rule lain yang memanggil fungsi yang ditrigger rule lain (suatu or)
# bisa dipanggil terus-terusan
# AS.Fact biar Fact bisa dipanggil sebagai suatu parameter di fungsinya