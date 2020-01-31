import pygame, os, sys, json
from random import randint as rand
from pygame.locals import *
pygame.init()

width, height = 800, 800
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|NOFRAME)
pygame.display.set_caption("Tim's Diner")
clock = pygame.time.Clock()

DEVMODE = False

if DEVMODE:
    dirprefix = os.getcwd() + ("\\" if os.getcwd()[-11::] == "Tim's Diner" else "\\Tim's Diner\\")
else:
    dirprefix = os.getcwd()
    
class GUI:
    def __init__(self):
        # Init the class
        self.items = self.loadPrices()
        self.easyitems = [[],[]]
        for j in self.items:
            for i in self.items[j]:
                self.easyitems[0].append(i[0])
                self.easyitems[1].append(i[1])
        self.itemoftheday = self.easyitems[0][rand(0, len(self.easyitems[0])-1)]

        # Load ttfs and images
        self.timfont = pygame.font.Font(dirprefix + 'files\\Journal.ttf', 96)
        self.menubfont = pygame.font.Font(dirprefix + 'files\\Hashtag.ttf', 48)
        self.menufont = pygame.font.Font(dirprefix + 'files\\Hashtag.ttf', 28)
        self.biggeneralfont = pygame.font.Font(dirprefix + 'files\\Halogen.ttf', 48)
        self.generalfont = pygame.font.Font(dirprefix + 'files\\Halogen.ttf', 28)
        self.boldreceiptfont = pygame.font.Font(dirprefix + 'files\\Consolab.ttf', 18)
        self.bigreceiptfont = pygame.font.Font(dirprefix + 'files\\Consolas.ttf', 32)
        self.receiptfont = pygame.font.Font(dirprefix + 'files\\Consolas.ttf', 18)
        self.tickimage = pygame.image.load(dirprefix + 'files\\tick.png')
        self.ximage = pygame.image.load(dirprefix + 'files\\cancel.png')
        self.backimage = pygame.image.load(dirprefix + 'files\\back.png')

        self.resetOrder()

        self.tablerects = []
        self.menurects = []
        self.orderrects = [[],[]]
        self.ordercount = 0

        # Add the table rects
        for y in range(2):
            for x in range(5):
                self.tablerects.append(pygame.Rect((x*100)+(x+1)*50,((y*100)+(y+1)*50)+100, 100, 100))

        # Add menu text rects
        for i, title in enumerate(self.items):
            for j, item in enumerate(self.items[title]):
                menutext = self.menufont.render(item[0] + " £" + str(item[1]) + ("0" if str(item[1])[-2] == '.' else ""), True, (255,255,255), (10,10,10))
                self.menurects.append(pygame.Rect((175*i+50+(175-menutext.get_rect().width)/2, 30*j+230), (menutext.get_rect().width, menutext.get_rect().height)))

    def draw(self):
        # Fills screen with something, regardless of display
        screen.fill((239, 222, 205))

        # Renders Tom's Dinner text, regardless of display
        timtext = self.timfont.render("Tim's Diner", True, (0,0,0), (239, 222, 205))
        screen.blit(timtext, (width//2-timtext.get_rect().width//2,10))

        if self.display == 'table':
            # Draws the tables to the screen
            for i, button in enumerate(self.tablerects):
                pygame.draw.rect(screen, (170,92,55), button)
                numtext = self.generalfont.render(str(i+1), True, (0,0,0), (170,92,55))
                screen.blit(numtext, (button[0]+50-numtext.get_rect().width//2, button[1]+50-numtext.get_rect().height//2))

            # Other text and dev button
            choosetabletext = self.biggeneralfont.render("Please choose a table number", True, (0,0,0), (239, 222, 205))
            screen.blit(choosetabletext, (400-choosetabletext.get_rect().width//2, 450))
            pygame.draw.rect(screen, (255,160,60), [width-10,height-10,10,10])

        elif self.display == 'food':
            # Draws the 2 black boxes for menu and order
            pygame.draw.rect(screen, (10,10,10), [50, 150, width-100, 250])
            pygame.draw.rect(screen, (10,10,10), [50, 420, width-100, 250])

            screen.blit(self.backimage, (15,5))

            # Add confirm and cancel buttons if there's some price
            if self.price > 0:
                pygame.draw.rect(screen, (30,210,30), [width-250,height-110,90,90])
                pygame.draw.rect(screen, (210,30,30), [width-140,height-110,90,90])
                screen.blit(self.tickimage, (width-245,height-105))
                screen.blit(self.ximage, (width-135,height-105))

            # Draw price
            screen.blit(self.generalfont.render("£" + str(self.price) + ("0" if str(self.price)[-2] == '.' else ""), True, (0,0,0), (239, 222, 205)), (60, 720))

            # Reset the amount of order buttons and items available, along with the menu hover text
            buttoncount = 0
            itemcount = 0
            self.orderrects = [[],[]]

            # Draw all menu items: Menu sections and items
            for i, title in enumerate(self.items):
                titletext = self.menubfont.render(title, True, (255,255,255), (10,10,10))
                screen.blit(titletext, (175*i+50+(175-titletext.get_rect().width)/2,175))

                for j, item in enumerate(self.items[title]):
                    menutext = self.menufont.render(item[0] + " £" + str(item[1]) + ("0" if str(item[1])[-2] == '.' else ""), True, ((128,128,128) if self.menutexthover == buttoncount else (255,255,255)), (10,10,10))
                    screen.blit(menutext, (175*i+50+(175-menutext.get_rect().width)/2, 30*j+230))
                    buttoncount += 1

            # Draw all order items
            for i, item in enumerate(self.order):
                if item > 0:
                    ordertext = self.generalfont.render(self.easyitems[0][i] + " x" + str(item), True, (255,255,255), (10,10,10))
                    textoffset = int(0.15*(itemcount+1))
                    ordertextx, ordertexty = 60 + textoffset*350, 430 + 40*itemcount - 240*textoffset
                    screen.blit(ordertext, (ordertextx, ordertexty))
                    itemcount += 1
                    self.orderrects[0].append(pygame.Rect((ordertextx, ordertexty), (ordertext.get_rect().width, ordertext.get_rect().height)))
                    self.orderrects[1].append(i)

        elif self.display == 'receipt':
            pygame.draw.rect(screen, (255,255,255), [self.receiptrectdata[0], (300, self.receiptheight)])

            dinerrtext = self.bigreceiptfont.render("Tim's Diner", True, (0,0,0), (255,255,255))

            screen.blit(dinerrtext, (width//2-dinerrtext.get_rect().width//2, self.receiptrectdata[0][1]+10))
            pygame.draw.aaline(screen, (170,170,170), (self.receiptrectdata[0][0] + 5, self.receiptrectdata[0][1] + 50), (self.receiptrectdata[0][0] + 295, self.receiptrectdata[0][1] + 50))

            itemcount = 0
            for i, item in enumerate(self.order):
                if item > 0:
                    itemtextstring = str(item) + "x " + self.easyitems[0][i]
                    itemprice = str(round(item*self.easyitems[1][i], 2))
                    itp = itemprice + ("0" if itemprice[-2] == '.' else "")
                    itemtextstring = itemtextstring + (" " * (27-len(itp)-len(itemtextstring))) + "£" + itp

                    itemtext = self.receiptfont.render(itemtextstring, True, (0,0,0), (255,255,255))
                    screen.blit(itemtext, (self.receiptrectdata[0][0] + 10, self.receiptrectdata[0][1] + 60 + itemcount*30))
                    itemcount += 1

            pygame.draw.aaline(screen, (170,170,170), (self.receiptrectdata[0][0] + 5, self.receiptrectdata[0][1] + 60 + itemcount*30), (self.receiptrectdata[0][0] + 295, self.receiptrectdata[0][1] + 60 + itemcount*30))
            totalpricestr = "£" + str(self.price) + ("0" if str(self.price)[-2] == '.' else "")
            totalpricetext = self.boldreceiptfont.render(" "*(28-len(totalpricestr)) + totalpricestr, True, (0,0,0), (255,255,255))
            screen.blit(totalpricetext, (self.receiptrectdata[0][0] + 10, self.receiptrectdata[0][1] + 70 + itemcount*30))

            pleasetexttop = self.receiptfont.render("Thanks for dining at Tim's.", True, (0,0,0), (255,255,255))
            pleasetextmid = self.receiptfont.render("Please take a seat at table:", True, (0,0,0), (255,255,255))
            pleasetextbot = self.bigreceiptfont.render(str(self.table), True, (0,0,0), (255,255,255))

            screen.blit(pleasetexttop, (width//2-pleasetexttop.get_rect().width//2, self.receiptrectdata[0][1] + 110 + itemcount*30))
            screen.blit(pleasetextmid, (width//2-pleasetextmid.get_rect().width//2, self.receiptrectdata[0][1] + 130 + itemcount*30))
            screen.blit(pleasetextbot, (width//2-pleasetextbot.get_rect().width//2, self.receiptrectdata[0][1] + 160 + itemcount*30))

            donetext = self.biggeneralfont.render("Done", True, (0,0,0), (239, 222, 205))
            self.donerect = pygame.Rect((width-150, height-80), (donetext.get_rect().width, donetext.get_rect().height))
            screen.blit(donetext, (width-150, height-80))

        # Developer's eyes only
        elif self.display == 'dev':
            pygame.draw.rect(screen, (255,160,60), [width-10,height-10,10,10])

            devtexts = [self.generalfont.render("Ammend Prices", True, (255,255,255), (30,144,255)), self.generalfont.render("Get Totals", True, (255,255,255), (30,144,255))]

            for i in range(2):
                pygame.draw.rect(screen, (30,144,255), [200, 150*i+150, 400, 100])
                screen.blit(devtexts[i], (width//2-devtexts[i].get_rect().width//2, 150*i+188))


    # All unnecessarily power consuming for loops for logic I could do in that
    # draw function but I don't so it's in this function instead
    def logic(self):
        # Get the mouses position regardless of event
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.display == 'table':
                    for i, button in enumerate(self.tablerects):
                        if button.collidepoint(mx, my):
                            self.table = i + 1
                            self.display = 'food'

                    if pygame.Rect(width-10,height-10,10,10).collidepoint(mx, my):
                        self.display = 'dev'

                elif self.display == 'food':
                    if pygame.Rect(15,17,80,57).collidepoint(mx, my):
                        self.display = 'table'

                    for i, button in enumerate(self.menurects):
                        if button.collidepoint(mx, my):
                            self.order[i] += 1

                    for i, button in enumerate(self.orderrects[0]):
                        if button.collidepoint(mx, my):
                            self.order[self.orderrects[1][i]] -= 1

                    if self.price > 0:
                        if pygame.Rect(width-250,height-110,90,90).collidepoint(mx, my):
                            self.display = 'receipt'
                        elif pygame.Rect(width-140,height-110,90,90).collidepoint(mx, my):
                            self.order = []
                            for title in self.items:
                                for i in range(len(self.items[title])):
                                    self.order.append(0)

                elif self.display == 'receipt':
                    if 850-self.receiptrectdata[0][1] > 400:
                        if self.donerect.collidepoint(mx, my):
                            self.appendHistory()
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

        if self.display == 'receipt':
            if self.receiptrectdata[0][1] > 852-self.receiptheight//2:
                self.receiptrectdata[0] = self.slideAnim(self.receiptrectdata[0], self.receiptrectdata[1], (250,850-self.receiptheight//2), self.receiptspeeds[0])
            elif self.receiptrectdata[0][1] > 852-self.receiptheight:
                self.receiptrectdata[0] = self.slideAnim(self.receiptrectdata[0], self.receiptrectdata[1], (250,850-self.receiptheight), self.receiptspeeds[1])
            else:
                self.receiptrectdata[0] = self.slideAnim(self.receiptrectdata[0], self.receiptrectdata[1], (250,150), self.receiptspeeds[2])

        tempprice = 0.0
        self.ordercount = 0
        for i, item in enumerate(self.order):
            if item > 0:
                tempprice += self.easyitems[1][i] * item
                self.ordercount += 1
        self.price = round(tempprice, 2)
        self.receiptheight = 250 + self.ordercount*30


    def loadPrices(self):
        with open(dirprefix + "prices.json", 'r') as f:
            return json.load(f)

    def editPrices(self, newdata):
        pass

    def appendHistory(self):
        with open(dirprefix + "history.json", 'r') as f:
            self.history = json.load(f)
            f.close()
        #print(history)

        self.history['orders'].append([self.order, self.table, self.price])
        for i, item in enumerate(self.history['totals']):
            self.history['totals'][i] = self.history['totals'][i] + self.order[i]

        #print(history)

        with open(dirprefix + "history.json", 'w') as f:
            f.write(json.dumps(self.history))

    def resetOrder(self):
        self.order = []
        for title in self.items:
            for i in range(len(self.items[title])):
                self.order.append(0)

        self.display = 'table'
        self.menutexthover = -1
        self.table = -1
        self.price = 0.0
        self.receiptspeeds = [rand(-8,-4), rand(-8,-4), rand(-8,-4)]
        self.receiptrectdata = [(250, 800), (250, 801)] # Position, start

    def slideAnim(self, position, start, end, maxspeed=5):
        dx, dy = end[0] - position[0], end[1] - position[1]
        try:
            fx = dx / (end[0]-start[0])
            newspeedx = (-((2*fx - 1)**2) + 1) * maxspeed
        except: newspeedx = 0
        try:
            fy = dy / (end[1]-start[1])
            newspeedy = (-((2*fy - 1)**2) + 1) * maxspeed
        except: newspeedy = 0

        return (position[0]+newspeedx, position[1]+newspeedy)


    def boundInt(mini, maxi, num):
        if num < mini: return mini
        elif num > maxi: return maxi
        return num

gui = GUI() # I'll create a GUI interface using visual basic, to see if I can track an IPV4-IP address. || 69.420.1337 ||

while True:
    gui.draw()
    gui.logic()

    pygame.display.update()
    clock.tick(75)
