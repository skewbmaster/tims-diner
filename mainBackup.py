import pygame, os, sys, json
from pygame.locals import *
pygame.init()

width, height = 800, 800
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|NOFRAME)
pygame.display.set_caption("Tim's Diner")
clock = pygame.time.Clock()

dirprefix = os.getcwd() + ("\\" if os.getcwd()[-11::] == "Tim's Diner" else "\\Tim's Diner\\")

class GUI:
    def __init__(self):
        self.items = self.loadPrices()
        self.easyitems = [[],[]]
        for j in self.items:
            for i in self.items[j]:
                self.easyitems[0].append(i[0])
                self.easyitems[1].append(i[1])

        self.timfont = pygame.font.Font(dirprefix + 'Journal.ttf', 96)
        self.menubfont = pygame.font.Font(dirprefix + 'Hashtag.ttf', 48)
        self.menufont = pygame.font.Font(dirprefix + 'Hashtag.ttf', 28)
        self.biggeneralfont = pygame.font.Font(dirprefix + 'Halogen.ttf', 48)
        self.generalfont = pygame.font.Font(dirprefix + 'Halogen.ttf', 28)
        self.tickimage = pygame.image.load(dirprefix + 'tick.png')
        self.ximage = pygame.image.load(dirprefix + 'cancel.png')

        self.display = 'table'
        self.menutexthover = -1

        self.table = -1
        self.resetOrder()
        self.price = 0.0

        self.tablerects = []
        self.menurects = []
        self.orderrects = [[],[]]
        for y in range(2):
            for x in range(5):
                self.tablerects.append(pygame.Rect((x*100)+(x+1)*50,((y*100)+(y+1)*50)+100, 100, 100))

        for i, title in enumerate(self.items):
            for j, item in enumerate(self.items[title]):
                menutext = self.menufont.render(item[0] + " £" + str(item[1]) + ("0" if str(item[1])[-2] == '.' else ""), True, (255,255,255), (10,10,10))
                self.menurects.append(pygame.Rect((175*i+50+(175-menutext.get_rect().width)/2, 30*j+230), (menutext.get_rect().width, menutext.get_rect().height)))

    def draw(self):
        screen.fill((239, 222, 205))

        timtext = self.timfont.render("Tim's Diner", True, (0,0,0), (239, 222, 205))
        screen.blit(timtext, (width//2-timtext.get_rect().width//2,10))

        if self.display == 'table':
            for i, button in enumerate(self.tablerects):
                pygame.draw.rect(screen, (170,92,55), button)
                numtext = self.generalfont.render(str(i+1), True, (0,0,0), (170,92,55))
                screen.blit(numtext, (button[0]+50-numtext.get_rect().width//2, button[1]+50-numtext.get_rect().height//2))

            choosetabletext = self.biggeneralfont.render("Please choose a table number", True, (0,0,0), (239, 222, 205))
            screen.blit(choosetabletext, (400-choosetabletext.get_rect().width//2, 450))
            pygame.draw.rect(screen, (255,160,60), [width-10,height-10,10,10])

        elif self.display == 'food':
            pygame.draw.rect(screen, (10,10,10), [50, 150, width-100, 250])
            pygame.draw.rect(screen, (10,10,10), [50, 420, width-100, 250])

            if self.price > 0:
                pygame.draw.rect(screen, (30,210,30), [width-250,height-110,90,90])
                pygame.draw.rect(screen, (210,30,30), [width-140,height-110,90,90])
                screen.blit(self.tickimage, (width-245,height-105))
                screen.blit(self.ximage, (width-135,height-105))

            screen.blit(self.generalfont.render("£" + str(self.price) + ("0" if str(self.price)[-2] == '.' else ""), True, (0,0,0), (239, 222, 205)), (60, 720))

            buttoncount = 0
            itemcount = 0
            self.orderrects = [[],[]]

            for i, title in enumerate(self.items):
                titletext = self.menubfont.render(title, True, (255,255,255), (10,10,10))
                screen.blit(titletext, (175*i+50+(175-titletext.get_rect().width)/2,175))

                for j, item in enumerate(self.items[title]):
                    menutext = self.menufont.render(item[0] + " £" + str(item[1]) + ("0" if str(item[1])[-2] == '.' else ""), True, ((128,128,128) if self.menutexthover == buttoncount else (255,255,255)), (10,10,10))
                    screen.blit(menutext, (175*i+50+(175-menutext.get_rect().width)/2, 30*j+230))
                    buttoncount += 1

            for i, item in enumerate(self.order):
                if item > 0:
                    ordertext = self.generalfont.render(self.easyitems[0][i] + " x" + str(item), True, (255,255,255), (10,10,10))
                    textoffset = int(0.15*(itemcount+1))
                    ordertextx, ordertexty = 60 + textoffset*250, 430 + 40*itemcount - 240*textoffset
                    screen.blit(ordertext, (ordertextx, ordertexty))
                    itemcount += 1
                    self.orderrects[0].append(pygame.Rect((ordertextx, ordertexty), (ordertext.get_rect().width, ordertext.get_rect().height)))
                    self.orderrects[1].append(i)

        elif self.display == 'dev':
            pygame.draw.rect(screen, (255,160,60), [width-10,height-10,10,10])


    def logic(self):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.display == 'table':
                    for i, button in enumerate(self.tablerects):
                        if button.collidepoint(mx, my):
                            self.table = i
                            self.display = 'food'

                    if pygame.Rect(width-10,height-10,10,10).collidepoint(mx, my):
                        self.display = 'dev'

                elif self.display == 'food':
                    for i, button in enumerate(self.menurects):
                        if button.collidepoint(mx, my):
                            self.order[i] += 1
                            #print(self.order)

                    for i, button in enumerate(self.orderrects[0]):
                        if button.collidepoint(mx, my):
                            self.order[self.orderrects[1][i]] -= 1

                    if pygame.Rect(width-250,height-110,90,90).collidepoint(mx, my):
                        print('cool accept')
                    elif pygame.Rect(width-140,height-110,90,90).collidepoint(mx, my):
                        self.resetOrder()

                elif self.display == 'dev':
                    if pygame.Rect(width-10,height-10,10,10).collidepoint(mx, my):
                        self.display = 'table'

        if self.display == 'food':
            for i, button in enumerate(self.menurects):
                if button.collidepoint(mx, my):
                    self.menutexthover = i
                    break
            else:
                self.menutexthover = -1


        tempprice = 0.0
        for i, item in enumerate(self.order):
            if item > 0:
                tempprice += self.easyitems[1][i] * item
        self.price = round(tempprice, 2)


    def loadPrices(self):
        with open(dirprefix + "prices.json", 'r') as f:
            return json.load(f)

    def editPrices(self, newdata):
        pass

    def appendHistory(self, more):
        pass

    def resetOrder(self):
        self.order = []
        for title in self.items:
            for i in range(len(self.items[title])):
                self.order.append(0)

    def slideAnim(self, start, end, rate=0.25):
        pass

    def boundInt(mini,maxi,num):
        if num < mini: return mini
        elif num > maxi: return maxi
        return num

gui = GUI()

while True:
    gui.draw()
    gui.logic()

    pygame.display.update()
    clock.tick(60)
