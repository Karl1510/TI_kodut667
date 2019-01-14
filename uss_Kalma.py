#Panen akna avama enam-vähem kuskile ekraani keskele, er mugavam oleks kasutada
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "400, 100"

import pygame
from random import randint
import random
import math
 
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
ROOSA = (255,20,147)
PUNANE = (255,0,0)
#suvalineVärv = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
skoor = 0
parim_skoor = 0

#värvid = [VALGE, ROOSA, PUNANE]
#Meetod, mis leiab kõik võimalikud käigud
def kõikKäigud(uss_osad, eelmine_suund, seinad):
    käigud = []
    suunad = {"vasak", "parem", "üles", "alla"}
    for suund in suunad:
        kasOn = []
        #viimane sulgudes and kustutada, kui panen käike ettemõtlema, hetkel väldib ühe käigu kauguseid lõkse, tavaliselt tuleb treppidset see
        if suund == "vasak" and not kasOnSein(seinad,uss_osad[0].rect.x-15, uss_osad[0].rect.y) and (not kasOnUss(uss_osad,uss_osad[0].rect.x-30, uss_osad[0].rect.y) or not kasOnUss(uss_osad,uss_osad[0].rect.x-15, uss_osad[0].rect.y+15) or not kasOnUss(uss_osad,uss_osad[0].rect.x-15, uss_osad[0].rect.y-15)):
            if not kasOnUss(uss_osad,uss_osad[0].rect.x-15, uss_osad[0].rect.y):
                käigud.append(suund)
        elif suund == "parem" and not kasOnSein(seinad,uss_osad[0].rect.x+15, uss_osad[0].rect.y) and (not kasOnUss(uss_osad,uss_osad[0].rect.x+30, uss_osad[0].rect.y) or not kasOnUss(uss_osad,uss_osad[0].rect.x+15, uss_osad[0].rect.y+15) or not kasOnUss(uss_osad,uss_osad[0].rect.x+15, uss_osad[0].rect.y-15)):
            if not kasOnUss(uss_osad,uss_osad[0].rect.x+15, uss_osad[0].rect.y):
                käigud.append(suund)
        elif suund == "üles" and not kasOnSein(seinad,uss_osad[0].rect.x, uss_osad[0].rect.y-15) and (not kasOnUss(uss_osad,uss_osad[0].rect.x, uss_osad[0].rect.y-30) or not kasOnUss(uss_osad,uss_osad[0].rect.x+15, uss_osad[0].rect.y-15) or not kasOnUss(uss_osad,uss_osad[0].rect.x-15, uss_osad[0].rect.y-15)):
            if not kasOnUss(uss_osad,uss_osad[0].rect.x, uss_osad[0].rect.y-15):
                käigud.append(suund)
        elif suund == "alla" and not kasOnSein(seinad,uss_osad[0].rect.x, uss_osad[0].rect.y+15) and (not kasOnUss(uss_osad,uss_osad[0].rect.x, uss_osad[0].rect.y+30) or not kasOnUss(uss_osad,uss_osad[0].rect.x+15, uss_osad[0].rect.y+15) or not kasOnUss(uss_osad,uss_osad[0].rect.x-15, uss_osad[0].rect.y+15)):
            if not kasOnUss(uss_osad,uss_osad[0].rect.x, uss_osad[0].rect.y+15):
                käigud.append(suund)
    return käigud
#Meetod, mis leiab esimese pikima tsükli
def tsükkel(seinad, x, y, eelmineSuund, uss_osad, maiustus, praeguneTsükkel):
    if eelmineSuund == "parem":
        if kasOnSein(seinad, x+30,y) and not kasOnSein(seinad, x, y+18):
            return "alla","tsükkel1"
        elif kasOnSein(seinad, x+15,y):
            return "üles","tsükkel1"
        else:
            return "parem","tsükkel1"
    if eelmineSuund == "vasak":
        if kasOnSein(seinad, x-15,y) and not kasOnSein(seinad, x, y+18):
            return "alla","tsükkel1"
        else:
            return "vasak","tsükkel1"
    if eelmineSuund == "alla":
        if kasOnSein(seinad, x-15, y):
            return "parem","tsükkel1"
        else:
            return "vasak","tsükkel1"
    if eelmineSuund == "üles":
        if kasOnSein(seinad, x, y-17):
            return "vasak","tsükkel2"
        else:
            return "üles", "tsükkel1"
#Kuna uss saab täpselt nii palju kordi graafi läbida, et tuleb tagasi teiselt poolt, siis on vaja kahte erinevat tsüklit, mis kordamööda käivad        
def tsükkel2(seinad, x, y, eelmineSuund, uss_osad, maiustus, praeguneTsükkel):
    if eelmineSuund == "parem":
        if kasOnSein(seinad, x+15,y) and not kasOnSein(seinad, x, y+18):
            return "alla","tsükkel2"
        else:
            return "parem","tsükkel2"
    if eelmineSuund == "vasak":
        if kasOnSein(seinad, x-30,y) and not kasOnSein(seinad, x, y+18):
            return "alla","tsükkel2"
        elif kasOnSein(seinad, x-15,y):
            return "üles","tsükkel2"
        else:
            return "vasak","tsükkel2"
    if eelmineSuund == "alla":
        if kasOnSein(seinad, x+15, y):
            return "vasak","tsükkel2"
        else:
            return "parem","tsükkel2"
    if eelmineSuund == "üles":
        if kasOnSein(seinad, x, y-17):
            return "parem","tsükkel1"
        else:
            return "üles", "tsükkel2"
    
#Meetod, mis tuvastab, kas antud asukohal on sein või ei
def kasOnSein(seinad, x, y):
    for sein in seinad:
        if sein.rect.x == x and sein.rect.y == y:
            return True
    return False
#Meetod, mis tuvastab, kas antud asukohal on uss või mitte
def kasOnUss(uss_osad, x, y):
    for osa in uss_osad:
        if osa.rect.x == x and osa.rect.y == y:
            return True
    return False
#Meetod, mis võrdleb etteantud käike ja annab neile kaalud ehk vaatab, mis on lühim tee maiustuseni
def parimadKäigud(uss_osad,maiustus, käigud):
    lähimadKäigud = {}
    for käik in käigud:
        kaugus = math.sqrt(((uss_osad[0].rect.x-maiustus.rect.x)**2)+((uss_osad[0].rect.y-maiustus.rect.y)**2))
        if käik == "vasak":
            kaugus2 = math.sqrt(((uss_osad[0].rect.x-15-maiustus.rect.x)**2)+((uss_osad[0].rect.y-maiustus.rect.y)**2))
            lähimadKäigud["vasak"] = kaugus-kaugus2
        elif käik == "parem":
            kaugus2 = math.sqrt(((uss_osad[0].rect.x+15-maiustus.rect.x)**2)+((uss_osad[0].rect.y-maiustus.rect.y)**2))
            lähimadKäigud["parem"] = kaugus-kaugus2
        elif käik == "üles":
            kaugus2 = math.sqrt(((uss_osad[0].rect.x-maiustus.rect.x)**2)+((uss_osad[0].rect.y-15-maiustus.rect.y)**2))
            lähimadKäigud["üles"] = kaugus-kaugus2
        elif käik == "alla":
            kaugus2 = math.sqrt(((uss_osad[0].rect.x-maiustus.rect.x)**2)+((uss_osad[0].rect.y+15-maiustus.rect.y)**2))
            lähimadKäigud["alla"] = kaugus-kaugus2
    return lähimadKäigud  
#Graafiline algusleht        
def algusleht(skoor, parim_skoor):
    main_surface = pygame.display.get_surface()
    bg = pygame.image.load("taust.jpg")
    main_surface.blit(bg, (0, 0))
    pygame.display.update()
    myfont = pygame.font.SysFont("Marlett",45)
    text = myfont.render((("Eelmine tulemus: " + str(skoor))), True,  (VALGE))
    x,y = 100, 350
    main_surface.blit(text,(x,y))
    text = myfont.render((("Parim tulemus: " + str(parim_skoor))), True,  (VALGE))
    x,y = 100, 450
    main_surface.blit(text,(x,y))
    x,y=100,250
    z = 550
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT :
                pygame.quit()
            if event.type== pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse=pygame.mouse.get_pos()
                if mouse[0]in range (x,x+210) and  mouse[1]in range (y,y+35):
                    skoor = mäng("arvuti")
                    if skoor > parim_skoor:
                        parim_skoor = skoor
                    algusleht(skoor, parim_skoor)
                    return
                if mouse[0]in range (x,x+210) and  mouse[1]in range (z,z+35):
                    pygame.quit()
                    quit()
        textsurface = myfont.render(("Alusta mängu"), True, (VALGE))
        main_surface.blit(textsurface,(x,y))
        textsurface = myfont.render(("Lahku mängust"), True, (VALGE))
        main_surface.blit(textsurface,(x,z))
        pygame.display.update()
#Mäng ise        
def mäng(mängija):
    skoor = 0
    mänguväli = pygame.display.set_mode((1200, 800))
    lisaosad = pygame.sprite.Group()

    laius = 15
    kõrgus = 15

    x_muutus = laius
    y_muutus = 0
     
    class Osa(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
     
            self.image = pygame.Surface([laius, kõrgus])
            self.image.fill(VALGE)
     
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Sein(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            
            self.image = pygame.Surface([laius, kõrgus])
            self.image.fill(ROOSA)
            
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
    class Maiustus(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            
            self.image = pygame.Surface([laius, kõrgus])
            self.image.fill(PUNANE)
            
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    uss_osad = []
    for i in range(2):
        x = 15 - (laius) * i
        y = 617
        osa = Osa(x, y)
        uss_osad.append(osa)
        lisaosad.add(osa)
        
    x = randint(0, 76)*15 + 30
    y = randint(0, 49)*15 + 32
    maiustus = Maiustus(x,y)
    lisaosad.add(maiustus)

    seinad = []
    for i in range(800):
        x = 0
        y = i
        sein = Sein(x,y)
        seinad.append(sein)
        lisaosad.add(sein)
        x = 1185
        sein = Sein(x,y)
        seinad.append(sein)
        lisaosad.add(sein)
        
    for i in range(1200):
        x = i
        y = 0
        sein = Sein(x,y)
        seinad.append(sein)
        lisaosad.add(sein)
        y = 785
        sein = Sein(x,y)
        seinad.append(sein)
        lisaosad.add(sein)

    kell = pygame.time.Clock()
    done = False
    
    eelmineSuund = "parem"
    praeguneTsükkel = "tsükkel1"
     
    while not done:
        if mängija == "inimene":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if eelmineSuund != "parem":
                            eelmineSuund = "vasak"
                            x_muutus = (laius) * -1
                            y_muutus = 0
                            #Breakimata võib see võtta 2 nupuvajutust ühe ticki jooksul ja võid surra nii ära, nüüd iga tickiga vaid üks liigutus
                            break
                    elif event.key == pygame.K_RIGHT:
                        if eelmineSuund != "vasak":
                            eelmineSuund = "parem"
                            x_muutus = (laius)
                            y_muutus = 0
                            break
                    elif event.key == pygame.K_UP:
                        if eelmineSuund != "alla":
                            eelmineSuund = "üles"
                            x_muutus = 0
                            y_muutus = (kõrgus) * -1
                            break
                    elif event.key == pygame.K_DOWN:
                        if eelmineSuund != "üles":
                            eelmineSuund = "alla"
                            x_muutus = 0
                            y_muutus = (kõrgus)
                            break
            vana_osa = uss_osad.pop()
            lisaosad.remove(vana_osa)
         
            x = uss_osad[0].rect.x + x_muutus
            y = uss_osad[0].rect.y + y_muutus
            osa = Osa(x, y)

            uss_osad.insert(0, osa)
            lisaosad.add(osa)
            #Seda on vaja, kuna muidu jäävad kastid ekraanile
            mänguväli.fill(MUST)
            
            if uss_osad[0].rect.x < 15 or uss_osad[0].rect.x > 1170 or uss_osad[0].rect.y < 15 or uss_osad[0].rect.y > 770:
                done = True
                continue
            
            for osa in uss_osad[1:]:
                if uss_osad[0].rect.x == osa.rect.x and uss_osad[0].rect.y == osa.rect.y:
                    done = True
                    continue
            if uss_osad[0].rect.x == maiustus.rect.x and uss_osad[0].rect.y == maiustus.rect.y:
                lisaosad.remove(maiustus)
                x = randint(0, 76)*15 + 30
                y = randint(0, 49)*15 + 32
                maiustus = Maiustus(x,y)
                lisaosad.add(maiustus)
                uss_osad.insert(len(uss_osad), vana_osa)
                lisaosad.add(vana_osa)
                skoor += 1
         
            lisaosad.draw(mänguväli)
            pygame.display.flip()
            kell.tick(20)
            
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            käigud = kõikKäigud(uss_osad, eelmineSuund, seinad)
            if eelmineSuund == "vasak" and "parem" in käigud:
                käigud.remove("parem")
            elif eelmineSuund == "parem" and "vasak" in käigud:
                käigud.remove("vasak")
            elif eelmineSuund == "alla" and "üles" in käigud:
                käigud.remove("üles")
            elif eelmineSuund == "üles" and "alla" in käigud:
                käigud.remove("alla")
            if len(käigud) != 0 and len(uss_osad) < 50:
                käik = max(parimadKäigud(uss_osad, maiustus, käigud), key =parimadKäigud(uss_osad, maiustus, käigud).get)
                if (uss_osad[0].rect.y-17)/15%2 == 0 and eelmineSuund == "vasak":
                    praeguneTsükkel = "tsükkel2"
                elif (uss_osad[0].rect.y-17)/15%2 == 1 and eelmineSuund == "parem":
                    praeguneTsükkel = "tsükkel2"
                else:
                    praeguneTsükkel = "tsükkel1"
            else:
                if praeguneTsükkel == "tsükkel1":
                    käik, praeguneTsükkel = tsükkel(seinad, uss_osad[0].rect.x, uss_osad[0].rect.y, eelmineSuund, uss_osad, maiustus, praeguneTsükkel)
                elif praeguneTsükkel == "tsükkel2":
                    käik, praeguneTsükkel = tsükkel2(seinad, uss_osad[0].rect.x, uss_osad[0].rect.y, eelmineSuund,uss_osad, maiustus, praeguneTsükkel)
            #Kui juhtubki, et tsüklitest tuleb käik, mida teha ei saa, siis valin käigu, mida saab
            if käik not in käigud:
                käik = max(parimadKäigud(uss_osad, maiustus, käigud), key =parimadKäigud(uss_osad, maiustus, käigud).get)
                if (uss_osad[0].rect.y-17)/15%2 == 0 and eelmineSuund == "vasak":
                    praeguneTsükkel = "tsükkel2"
                elif (uss_osad[0].rect.y-17)/15%2 == 1 and eelmineSuund == "parem":
                    praeguneTsükkel = "tsükkel2"
                else:
                    praeguneTsükkel = "tsükkel1"
            if käik == "vasak":
                eelmineSuund = "vasak"
                x_muutus = (laius) * -1
                y_muutus = 0
            elif käik == "parem":
                eelmineSuund = "parem"
                x_muutus = (laius)
                y_muutus = 0
            elif käik == "üles":
                eelmineSuund = "üles"
                x_muutus = 0
                y_muutus = (kõrgus) * -1        
            elif käik == "alla":
                eelmineSuund = "alla"
                x_muutus = 0
                y_muutus = (kõrgus)
         
            vana_osa = uss_osad.pop()
            lisaosad.remove(vana_osa)
         
            x = uss_osad[0].rect.x + x_muutus
            y = uss_osad[0].rect.y + y_muutus
            osa = Osa(x, y)

            uss_osad.insert(0, osa)
            lisaosad.add(osa)
            #Seda on vaja, kuna muidu jäävad kastid ekraanile
            mänguväli.fill(MUST)
            
            if uss_osad[0].rect.x < 15 or uss_osad[0].rect.x > 1170 or uss_osad[0].rect.y < 15 or uss_osad[0].rect.y > 770:
                done = True
                continue
            
            for osa in uss_osad[1:]:
                if uss_osad[0].rect.x == osa.rect.x and uss_osad[0].rect.y == osa.rect.y:
                    done = True
                    continue
            if uss_osad[0].rect.x == maiustus.rect.x and uss_osad[0].rect.y == maiustus.rect.y:
                lisaosad.remove(maiustus)
                while kasOnUss(uss_osad, x,y):
                    x = randint(0, 76)*15 + 30
                    y = randint(0, 49)*15 + 32
                maiustus = Maiustus(x,y)
                lisaosad.add(maiustus)
                uss_osad.insert(len(uss_osad), vana_osa)
                lisaosad.add(vana_osa)
                skoor += 1
         
            lisaosad.draw(mänguväli)
            pygame.display.flip()
            kell.tick(100)
     
    return skoor

pygame.init()
mänguväli = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Ussimäng')
algusleht(skoor, parim_skoor)