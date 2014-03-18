import pygame, sys


class Spil():

    def __init__(self,sort, gildi, snyr, Stokkurinn):
        self.sort = sort
        self.gildi = gildi
        self.snyr_upp = snyr
        self.bakhlid = None
        self.framhlid = Stokkurinn.fa_mitt_spil(self.sort, self.gildi)


    def snua(self):
        if self.snyr_upp == False:
            self.snyr_upp = True
        else:
            self.snyr_upp = False

    def fa_spil(self):
        return self.framhlid


class Spilamyndir():

    def __init__(self):
        self.spila_breidd = 73
        self.spila_haed = 95
        self.kantur_toppur = 4
        self.kantur_hlidar = 0
        

    def fa_mitt_spil(self, sort, gildi):
        sortir = {'Lauf' : 0,'Spadi': 1 ,'Hjarta' : 2, 'Tigull' : 3}
        rod =  sortir[sort] * (self.spila_haed + self.kantur_toppur)
        dalkur = (gildi-1) * (self.spila_breidd + self.kantur_hlidar)

        return (rod,dalkur)

    def fa_spila_breidd(self):
        return self.spila_breidd

    def fa_spila_haed(self):
        return self.spila_haed

class Stokkur():

    def __init__(self, xHnit, yHnit,Stokkurinn):
        self.stadsetning = pygame.Rect(xHnit, yHnit, Stokkurinn.fa_spila_breidd(), Stokkurinn.fa_spila_haed())
        self.spil_i_stokk = []
        self.fjoldi_spila = 0

    def baeta_vid(self, spil):
        self.spil_i_stokk.append(spil)
        self.fjoldi_spila += 1

    def taka_efsta(self):
        self.fjoldi_spila -= 1
        return self.spil_i_stokk.pop()

    def teikna_efsta(self, skjar, mynd, Stokkurinn):
        if self.fjoldi_spila > 0:
            spil = self.spil_i_stokk[self.fjoldi_spila-1].fa_spil()
            skjar.blit(mynd, self.stadsetning, (spil[1], spil[0], Stokkurinn.fa_spila_breidd(), Stokkurinn.fa_spila_haed()))


class Bunki():

    def __init__(self, Stokkurinn):
        self.bunki_a_hvolfi = Stokkur(50,50, Stokkurinn)
        self.bunki_snyr_upp = Stokkur(150,50, Stokkurinn)

        for i in range(10):
            self.bunki_a_hvolfi.baeta_vid(Spil('Hjarta', i, True, Stokkurinn))

    def faera_yfir(self):
        spil = self.bunki_a_hvolfi.taka_efsta()
        self.bunki_snyr_upp.baeta_vid(spil)

    def teikna(self, skjar, mynd, Stokkurinn):
            self.bunki_a_hvolfi.teikna_efsta(skjar, mynd, Stokkurinn)
            self.bunki_snyr_upp.teikna_efsta(skjar, mynd, Stokkurinn)



pygame.init()


myndir = Spilamyndir()
size = width, height = 1200, 640
black = 0, 0, 0
screen = pygame.display.set_mode(size)
mynd = pygame.image.load("Spil.png")

s1 = Stokkur(300,100, myndir)

s2 = Stokkur(500,100, myndir)

spil1 = Spil('Hjarta', 1, True, myndir)
spil3 = Spil('Hjarta', 2, True, myndir)
spil2 = Spil('Spadi', 1, True, myndir)

b = Bunki(myndir)

s1.baeta_vid(spil1)
s1.baeta_vid(spil3)

s2.baeta_vid(spil2)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            b.faera_yfir()


    screen.fill(black)
    s1.teikna_efsta(screen, mynd, myndir)
    s2.teikna_efsta(screen, mynd, myndir)
    b.teikna(screen, mynd, myndir)

    pygame.display.flip()







