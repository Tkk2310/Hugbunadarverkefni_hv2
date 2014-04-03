#!/usr/bin/env python
# encoding: utf-8

import pygame as pg
import pygame.camera
import pygame.image
import random
import datetime as dt
import inputbox
import pickle

class Spil:

    #Spil er klasi sem heldur utan um hvert spil. Spil tekur við hvaða sort spilið er,
    #hvaða gildi og hvernig það snýr sem viðfangs breytur.

    def __init__(self,sort, gildi, snyr):
        self.sort = sort
        self.gildi = gildi
        self.snyr_upp = snyr
        self.spila_breidd = 71 #beriedd spilanna í pixlum
        self.spila_haed = 96 #hæð spilanna í pxlum
        self.heimili = False #geymir bunkann sem spilið tilheyrir
        self.bakhlid = self.fa_mitt_spil('Auka', 2) #vísir á bakhlið spilins í spil.png myndinni
        self.framhlid = self.fa_mitt_spil(self.sort, self.gildi) #vísir á framhlið spilins í spil.png myndinni
        self.er_med_mynd = False #flag sem segir til um hvort bakliðin sé png mynd eða tupul(vísir á bakliðina)

    #skilar hvaða bunka spilið var í
    def hvar_attu_heima(self):
        return self.heimili

    #gefa spilinu bunka
    def nytt_heimili(self,geymsla):
        self.heimili = geymsla

    #snúa spilinu
    def snua(self):
        if self.snyr_upp == False:
            self.snyr_upp = True
        else:
            self.snyr_upp = False
        return self

    #fá vísanna á spilið, bæði fram- og bakhlið
    def fa_spil(self):
        if self.snyr_upp:
            return self.framhlid
        else:
            return self.bakhlid

    #fall sem býr til vísi á spilið í spil.png myndinni
    def fa_mitt_spil(self, sort, gildi):
        sortir = {'Lauf' : 0,'Spadi': 1 ,'Hjarta' : 2, 'Tigull' : 3, 'Auka' : 4}
        rod =  sortir[sort] * self.spila_haed
        dalkur = (gildi-1) * self.spila_breidd + (gildi-1)
        return (rod,dalkur)

    def breidd(self):
        return self.spila_breidd

    def haed(self):
        return self.spila_haed

    #skilar tupul um gildi og sort spilsins
    def skila_spili(self):
        return (self.sort,self.gildi)

    def hvernig_snyrdu(self):
        return self.snyr_upp

    def breyta_bakhlid(self, numer=1, mynd=False):
        if mynd:
            self.bakhlid = pg.image.load(mynd)
            self.er_med_mynd = True
        else:
            self.bakhlid = self.fa_mitt_spil('Auka',numer)
            self.er_med_mynd = False

    def ertu_med_mynd(self):
        return self.er_med_mynd

    #skilar bakhliðinni ef hún er mynd
    def fa_bakhlid(self):
        return self.bakhlid


class Geymsla:

    #Móðurklasi fyrir geymsluaðferðir okkar. Stokkur og Bunki erfa fá þessum klasa.

    def tomur(self):
        return len(self.spil_i_lista)==0

    #draugur er nokkurskonar placeholder þ.e ef búnkinn er tómur þá setjum við "bull spil" í búnkann
    #til að hann sjáist og fólk viti hvar hann er.
    def setja_draug(self):
        if self.tomur():
            self.setja_a(Spil('Auka',1,True))
            self.draugur = True

    def taka_draug(self):
        if self.draugur and len(self.spil_i_lista) == 1:
            self.spil_i_lista = []
            self.draugur = False

    def draugur_lifandi(self):
        return self.draugur

    #setur spil á stokkinn eða bunkann. getur tekið við lista eða stöku spili.
    def setja_a(self, spil):
        if spil:
            if type(spil)==list:
                self.spil_i_lista += spil
            else:
                self.spil_i_lista.append(spil)

    #fall til að færa stokkinn eða bunkann
    def flytja(self, hnit):
        self.stadsetning = hnit

    def skila_fremsta(self):
        if not self.tomur():
            return self.spil_i_lista[-1]

    #fall sem breytir baklið allra spilanna í tilteknum stokk eða bunka
    def breyta_bakhlid_spila(self,numer=1,mynd=False):
        if not self.draugur_lifandi():
            for i in self.spil_i_lista:
                i.breyta_bakhlid(numer,mynd)


class Stokkur(Geymsla):

    #geymir spilin í bunka með engu offsetti þ.e hvert spil er ofan á hvort öðru og
    #þú sérð ekki spilið undir. Tekur við x og y hnitum til að gefa honum staðsetningu.
    #hann erfir frá Geymsla klasanum.

    def __init__(self, xHnit, yHnit):
        self.stadsetning = (xHnit, yHnit)
        self.spil_i_lista = []
        self.draugur = False

    #skilar efsta spilinu í stokknum
    def taka_af(self, spil):
        if not self.tomur():
            return [self.spil_i_lista.pop()]

    #teiknar bunkann
    def teikna(self, skjar, mynd):
        if not self.tomur():
            efst = self.spil_i_lista[-1]
            if efst.ertu_med_mynd() and not efst.hvernig_snyrdu():
                kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
                skjar.blit(efst.fa_bakhlid(), kassi)
            else:
                hnit = efst.fa_spil()
                kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
                skjar.blit(mynd, kassi, (hnit[1], hnit[0], efst.breidd(), efst.haed()))


    #tekur við hnitum og athugar hvort þau séu innan stokksins eða ekki. Ef svo er þá sklar það
    #efsta spilun annars ekkert.
    def athuga(self,hnit):
        if not self.tomur():
            efst = self.spil_i_lista[-1]
            kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
            if kassi.collidepoint(hnit):
                return efst

    def snyr_efst_upp(self):
        return True


class Bunki(Geymsla):

    #Geymi spilin í bunka með offsetti, þ.e þú sérð öll spilin í bunkanum. tekur við x og y hnitum
    #til að gefa honum staðsetningu. hann erfir fá Geymsla klasanum.
    def __init__(self, xhnit, yhnit):
        self.stadsetning = (xhnit, yhnit)
        self.spil_i_lista = []
        self.skekkja = 12
        self.draugur = False

    #tekur við spili. skilar lista af spilum með spil viðfaningu og öllum spilum fyrir neðan.
    def taka_af(self, spil):
        if spil:
            hvar = self.spil_i_lista.index(spil)
            losun = self.spil_i_lista[hvar:]
            self.spil_i_lista = self.spil_i_lista[:hvar]
            return losun

    #teiknar stokkinn
    def teikna(self, skjar, mynd):
        if not self.tomur():
            yhnit = self.stadsetning[1]
            for i in self.spil_i_lista:
                if i.ertu_med_mynd() and not i.hvernig_snyrdu():
                    kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                    yhnit += self.skekkja + (18-len(self.spil_i_lista))
                    skjar.blit(i.fa_bakhlid(),kassi)
                else:
                    kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                    yhnit += self.skekkja + (18-len(self.spil_i_lista))
                    hnit = i.fa_spil()
                    skjar.blit(mynd,kassi,(hnit[1], hnit[0], i.breidd(), i.haed()))

    #tekur við hniti, athugar hvort músin sé að ýta á eitthvað spil í bunkanum og skilar því spili sem ýtt er á
    def athuga(self,hnit):
        if not self.tomur():
            yhnit = self.stadsetning[1] + ((len(self.spil_i_lista)-1) * (self.skekkja + (18-len(self.spil_i_lista))))
            ofugt = self.spil_i_lista[::-1]
            for i in ofugt:
                kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                yhnit -= self.skekkja + (18-len(self.spil_i_lista))
                if kassi.collidepoint(hnit):
                    return i
        return False


    def skila_aftasta(self):
        if not self.tomur():
            return self.spil_i_lista[0]

    def snyr_efst_upp(self):
        return self.spil_i_lista[-1].hvernig_snyrdu()

    def snua_efsta(self):
        self.spil_i_lista[-1].snua()

    def fjoldi_spila(self):
        return len(self.spil_i_lista)


class Reglur:

    #Heldur utanum reglur leiksins og athugar hvort músin sé að klikka á eitthvað

    def __init__(self):
        self.stig = 0

    def klikka_a_spil(self,mus):
        geymsla,spil = self.mus_yfir_spili(mus)
        if not geymsla: return
        if self.hond.tomur():
            if geymsla == self.stokkar[0]:
                self.fletta_stokk()
            elif geymsla.draugur_lifandi():
                return
            elif not geymsla.snyr_efst_upp():
                geymsla.snua_efsta()
            elif geymsla in self.stokkar[2:]:
                self.breyta_stigum(-10)
                self.setja_a_hond(geymsla,spil)
            else:
                self.setja_a_hond(geymsla,spil)
        else:
            if geymsla == self.stokkar[0]:
                return
            if (geymsla == self.stokkar[1] and
                self.hond.skila_aftasta().hvar_attu_heima() == self.stokkar[1]):
                    self.taka_af_hond(geymsla)
                    return
            if geymsla == self.stokkar[1]:
                return
            if geymsla == self.hond.skila_aftasta().hvar_attu_heima():
                if geymsla in self.stokkar[2:]:
                    self.breyta_stigum(10)
                self.taka_af_hond(geymsla)
                return
            self.logleg_faersla(geymsla)

    def logleg_faersla(self,geymsla):
        aftast = self.hond.skila_aftasta().skila_spili()
        fremst = geymsla.skila_fremsta().skila_spili()
        if geymsla.draugur_lifandi() and aftast[1] == 13 and geymsla in self.bunkar:
            self.taka_af_hond(geymsla)
        if not self.litur(aftast[0]) == self.litur(fremst[0]):
            if aftast[1]+1 == fremst[1]:
                self.taka_af_hond(geymsla)
        if geymsla in self.stokkar[2:]:
            self.sigur_stokkar(geymsla)

    #passar hvort allt fari rétt fram með stokkanna sem þú raðar á til að vinna
    def sigur_stokkar(self, geymsla):
        spil = self.hond.skila_aftasta().skila_spili()
        if geymsla.draugur_lifandi() and spil[1] == 1:
            self.taka_af_hond(geymsla)
            self.breyta_stigum(10)
        elif self.hond.fjoldi_spila() == 1:
            spil_i_bunka = geymsla.skila_fremsta().skila_spili()
            if spil_i_bunka[0] == spil[0] and spil_i_bunka[1]+1 == spil[1]:
                self.taka_af_hond(geymsla)
                self.breyta_stigum(10)
        self.leikur_buinn()

    #athugar hvort leikurinn sé búinn
    def leikur_buinn(self):
        for i in self.stokkar[2:]:
            if i.draugur_lifandi():
                return
            if not i.skila_fremsta().skila_spili()[1] == 13:
                return
        self.vista_stig_og_tima()
        self.leikir[1] += 1
        self.vista_leiki()


    def litur(self,sort):
        if sort == 'Hjarta' or sort == 'Tigull':
            return 'Rautt'
        else:
            return 'Svart'

    #flettir úr aðal stokknum í hinn
    def fletta_stokk(self):
        if not self.stokkar[0].draugur_lifandi():
            if self.stokkar[1].draugur_lifandi():
                self.stokkar[1].taka_draug()
            self.stokkar[1].setja_a(self.stokkar[0].taka_af(None)[0].snua())
            self.breyta_stigum(-1)
            if self.stokkar[0].tomur():
                self.stokkar[0].setja_draug()
        else:
            self.stokkar[0].taka_draug()
            while not self.stokkar[1].tomur():
                self.stokkar[0].setja_a(self.stokkar[1].taka_af(None)[0].snua())
            self.stokkar[1].setja_draug()

    def setja_a_hond(self,geymsla,spil):
        if geymsla and not geymsla.draugur_lifandi():
            mitt = geymsla.taka_af(spil)
            mitt[0].nytt_heimili(geymsla)
            self.hond.setja_a(mitt)
            geymsla.setja_draug()

    def taka_af_hond(self,geymsla):
        if geymsla:
            geymsla.taka_draug()
            aftasta = self.hond.skila_aftasta()
            aftasta.nytt_heimili(False)
            spil = self.hond.taka_af(aftasta)
            geymsla.setja_a(spil)

    def mus_yfir_spili(self,mus):
        for stk in self.stokkar:
            spil = stk.athuga(mus)
            if spil:
                return stk,spil
        for bnk in self.bunkar:
            spil = bnk.athuga(mus)
            if spil:
                return bnk,spil
        return False,False

    def breyta_stigum(self,stig):
        self.stig = self.stig+stig

    def teikna_stig(self,skjar,stafir):
        skilti = stafir.render('Stig = '+str(self.stig),0,(255,255,255))
        skjar.blit(skilti,(500,450))

class Vidmot:


    #sér um að teikna takkana og það sem þeim fylgir.

    def __init__(self):
        self.tafla = pg.Surface((200,300))
        self.valmynd = pg.Surface((300,500))
        self.valmynd_uppi = False
        self.tafla.fill((150,0,150))
        self.valmynd.fill((0,150,150))
        self.reglur = pg.image.load('Reglur.png').convert()
        self.bua_til_myndir()
        self.stadsetja_takka()

    def bua_til_myndir(self):
        plat_spil = Spil('Auka',3,False)
        staerd = plat_spil.breidd(),plat_spil.haed()
        self.myndir_a_bakhlid = []
        self.kassar_bakhlida = []
        for i in range(9):
            x = i - 3*int(i/3.0)
            y = int(i/3.0)
            hnit = plat_spil.fa_mitt_spil('Auka',i+2)
            kassi = pg.Rect(20+90*x,20+110*y,staerd[0],staerd[1])
            uppl = (self.mynd, kassi, (hnit[1], hnit[0],staerd[0],staerd[1]))
            self.myndir_a_bakhlid.append(uppl)
            self.kassar_bakhlida.append((kassi,i+2))

    def stadsetja_takka(self):
        self.vh = (100,120,460,480)
        self.sm = pg.image.load('stig.png').convert_alpha()
        self.rm = pg.image.load('smerki.png').convert_alpha()
        self.vm = pg.image.load('smerki.png').convert_alpha()
        self.sm_kassi = self.sm.get_rect()
        self.rm_kassi = self.rm.get_rect()
        self.vm_kassi = self.vm.get_rect()
        self.sm_kassi.x = 20
        self.sm_kassi.y = 460
        self.rm_kassi.x = 60
        self.rm_kassi.y = 460
        self.vm_kassi.x = 100
        self.vm_kassi.y = 460

    def sja_stig(self,mus):
        self.gluggi.blit(self.sm,self.sm_kassi)
        if self.sm_kassi.collidepoint(mus):
            self.gluggi.blit(self.tafla,(300,100))
            self.teikna_stigatoflu()

    def sja_reglur(self,mus):
        self.gluggi.blit(self.rm,self.rm_kassi)
        if self.rm_kassi.collidepoint(mus):
            self.teikna_reglur()

    def teikna_stigatoflu(self):
        skilti = self.stafir.render('Sigurvegarar',0,(0,255,255))
        self.tafla.blit(skilti,(60,20))
        for i in sorted(self.sigurvegarar,key=(lambda x: x[0])):
            skilti = self.stafir.render(str(i[0])+': '+i[1]+' '+i[2]+' '+i[3],0,(255,255,255))
            self.tafla.blit(skilti,(20,25*i[0]+30))

    def teikna_reglur(self):
        self.gluggi.blit(self.reglur,(300,100))

    def velja_mynd(self,numer=1,mynd=False):
        for i in self.stokkar:
            i.breyta_bakhlid_spila(numer=numer,mynd=mynd)
        for i in self.bunkar:
            i.breyta_bakhlid_spila(numer=numer,mynd=mynd)

    def teikna_valglugga(self):
        for i in self.myndir_a_bakhlid:
            self.valmynd.blit(*i)
        self.gluggi.blit(self.valmynd,(100,0))

    def sja_valglugga(self,mus):
        if (self.valmynd_uppi == True and
           (mus[0] > 400 or mus[0] < 100)):
                self.valmynd_uppi = False
        if (self.vm_kassi.collidepoint(mus) or
            self.valmynd_uppi == True):
                self.teikna_valglugga()
                self.valmynd_uppi = True
        self.gluggi.blit(self.vm,(self.vh[0],self.vh[2]))

    def klikka_a_mynd(self,mus):
        if self.kassar_bakhlida[-1][0].collidepoint((mus[0]-100,mus[1])):
            self.myndavel()
        else:
            for i in self.kassar_bakhlida:
                if i[0].collidepoint((mus[0]-100,mus[1])):
                    self.velja_mynd(i[1])

    def myndavel(self):
        pygame.camera.init()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        cam.start()
        img = cam.get_image()
        img = pg.transform.scale(img,(71,96))
        pygame.image.save(img, "photo.bmp")
        cam.stop()
        self.velja_mynd(mynd="photo.bmp")


class Leikur(Reglur,Vidmot):

    #heldur utan um gang leiksins.

    def __init__(self):
        self.undirbua()
        Reglur.__init__(self)
        Vidmot.__init__(self)
        self.leikhringur()

    def undirbua(self):
        pg.init()
        self.stafir = pg.font.SysFont("Arial", 17)
        pg.display.set_caption('awesome-souce')
        self.spilandi = True
        self.lesa_stig()
        self.saekja_leiki()
        self.klukka = pg.time.Clock()
        self.gluggi = pg.display.set_mode((800,500))
        self.gluggi.fill((0,0,0))
        self.mynd = pg.image.load('Spil.png').convert_alpha()
        self.utbytta_spilum()

    def saekja_leiki(self):
        try:
            self.leikir = pickle.load(open('leikir.p','rb'))
        except:
            self.leikir = [0,1];
            pickle.dump(self.leikir,open('leikir.p', 'wb'))

    def vista_leiki(self):
        pickle.dump(self.leikir,open('leikir.p', 'wb'))

    def lesa_stig(self):
        try:
            self.sigurvegarar = pickle.load(open('siggar.p','rb'))
        except:
            self.sigurvegarar = [];
            pickle.dump(self.sigurvegarar,open('siggar.p','wb'))

    def vista_stig_og_tima(self):
        timi = str(dt.timedelta(milliseconds=pg.time.get_ticks()))
        timi = timi.split('.')
        nafn = inputbox.ask(self.gluggi,"Nafn")[:8]
        self.sigurvegarar.append([0,nafn,timi[0],str(self.stig)])
        self.sigurvegarar.sort(key=(lambda x: int(x[3])),reverse=True)
        for i in range(len(self.sigurvegarar)):
            self.sigurvegarar[i][0] = i+1
        pickle.dump( self.sigurvegarar, open('siggar.p','wb'))

    def utbytta_spilum(self):
        spil = [Spil(tegund,numer, False) for tegund in ['Hjarta','Spadi','Tigull','Lauf'] for numer in range(1,14)]
        random.shuffle(spil)
        self.bunkar = (
                Bunki(10,130),
                Bunki(110,130),
                Bunki(210,130),
                Bunki(310,130),
                Bunki(410,130),
                Bunki(510,130),
                Bunki(610,130)
                )
        self.stokkar = (
                Stokkur(10,10),
                Stokkur(110,10),
                Stokkur(310,10),
                Stokkur(410,10),
                Stokkur(510,10),
                Stokkur(610,10)
                )
        for i in range(1,7):
            for j in range(i):
                self.bunkar[i].setja_a(spil.pop())
        for k in self.bunkar:
            snu = spil.pop()
            snu.snua()
            k.setja_a(snu)
        self.stokkar[0].setja_a(spil)
        for l in self.stokkar:
            l.setja_draug()
        self.hond = Bunki(0,0)

    def teikna_stokka(self):
        for stk in self.stokkar:
            stk.teikna(self.gluggi, self.mynd)
        for bnk in self.bunkar:
            bnk.teikna(self.gluggi, self.mynd)
        self.hond.teikna(self.gluggi, self.mynd)

    def samskipti(self):
        mus = pg.mouse.get_pos()
        self.sja_stig(mus)
        self.sja_reglur(mus)
        self.sja_valglugga(mus)
        for atburdur in pg.event.get():
            if atburdur.type == pg.MOUSEBUTTONDOWN:
                if self.valmynd_uppi:
                    self.klikka_a_mynd(mus)
                else:
                    self.klikka_a_spil(mus)
            self.hond.flytja((mus[0]-36,mus[1]-10))
            if (atburdur.type == pg.KEYDOWN and
                atburdur.key == pg.K_ESCAPE or
                atburdur.type == pg.QUIT):
                    self.spilandi = False
                    self.leikir[1] += 1
                    self.vista_leiki()

    def taka_tima(self):
        self.klukka.tick(200)
        timi = str(dt.timedelta(milliseconds=pg.time.get_ticks()))
        timi = timi.split('.')
        skilti = self.stafir.render(timi[0], 0, (255,255,255))
        self.gluggi.blit(skilti, (700,450))

    def teikna_hlutfall(self):
        hlutfall = int((float(self.leikir[0])/self.leikir[1]) * 100)
        skilti = self.stafir.render(str(self.leikir[0])+"/"+str(self.leikir[1])+"="+str(hlutfall)+"%", 0, (255,255,255))
        self.gluggi.blit(skilti, (600,450))
   
    def teikna_bakgrunn(self):
        self.gluggi.fill((0,150,0))

    def leikhringur(self):
        while self.spilandi:
            self.teikna_bakgrunn()
            self.teikna_stokka()
            self.samskipti()
            self.taka_tima()
            self.teikna_hlutfall() 
            self.teikna_stig(self.gluggi,self.stafir)
            pg.display.flip()


if __name__ == '__main__':
    Leikur()
