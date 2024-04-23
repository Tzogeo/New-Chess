from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import tkinter.messagebox as tkm
from random import randint,shuffle

class MyLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.image = Image(source="board.png", size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)
        self.piece_images = {#contains the images of the pieces
        }
        self.piece_imb={}
        self.lexlist=['wpawn','wrook','wnight','wbishop','wking', 'wqueen','bpawn','brook','bnight','bbishop','bking','bqueen','wnook','bnook','wniqueen','bniqueen','rpawn']
        for item in self.lexlist:
            self.piece_imb[item]=item+'.png'
            self.piece_images[item]= Image(source=self.piece_imb[item], size_hint=(0.125, 0.125))
        self.position = [#contains the positions of the pieces
        ['wrook', 'wnight', 'wbishop', 'wqueen', 'wking', 'wbishop', 'wnight', 'wrook'],         # 00,01,02,03,04,05,06,07
        ['wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn'],        # 08,09,10,11,12,13,14,15
        [None, None, None, None, None, None, None, None],                                         # 16,17,18,19,20,21,22,23
        [None, None, None, None, None, None, None, None],                                         # 24,25,26,27,28,29,30,31
        [None, None, None, None, None, None, None, None],                                         # 32,33,34,35,36,37,38,39
        [None, None, None, None, None, None, None, None],                                         # 40,41,42,43,44,45,46,47
        ['bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn'],    # 48,49,50,51,52,53,54,55
        ['brook', 'bnight', 'bbishop', 'bqueen', 'bking', 'bbishop', 'bnight', 'brook']     # 56,57,58,59,60,61,62,63
        ]
        self.moves=[]
        self.player=0

        self.checkers=0
        self.columnletters=['a','b','c','d','e','f','g','h']
        self.kc=[1,1]
        self.selected_piece = None
        self.selected_piece_position = None
        self.running=True
        self.mrow,self.mcol=0,0
        self.brow,self.bcol=0,0
        self.grass=0
        self.book=0
        self.sk=0
    def on_size(self, *args):
        #self.img2.pos = (self.x2*self.width / 8 , self.y2*self.height / 8)
        self.draw_pieces()        
    def on_touch_down(self, touch):
        if not self.running:return 0
        self.col=int(touch.x//(self.width//8))
        self.row=int(touch.y//(self.height//8))
        if self.position[self.row][self.col] is not None:
            self.selected_piece = self.position[self.row][self.col]
            if (self.selected_piece[0]=="w" and self.player==0) or (self.selected_piece[0]=="b" and self.player==1):            
                self.selected_piece_position = (self.row, self.col)
                self.movement=1
                self.selected_imagen = self.piece_imb[self.selected_piece]  # Ορισμός της εικόνας του επιλεγμένου κομματιού
                self.selected_image=Image(source=self.selected_imagen, size_hint=(0.125, 0.125),pos=(self.col*self.width/8,self.row*self.height/8))
                self.position[self.row][self.col] = None
                self.draw_pieces()
                self.add_widget(self.selected_image)
            else: self.selected_piece=None  
        return super(MyLayout, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.selected_piece is not None:
            self.new_x = touch.x - self.selected_image.width / 2
            self.new_y = touch.y - self.selected_image.height / 2
            self.selected_image.pos =(self.new_x, self.new_y)

    def on_touch_up(self, touch):
        self.ocol=self.col
        self.orow=self.row
        if self.selected_piece!=None :
            self.col=int(touch.x//(self.width /8))
            self.row=int(touch.y//(self.height/8))
            if self.legal(8*self.orow+self.ocol,8*self.row+self.col) and self.row>=0 and self.col >=0:
                self.moves.append(self.selected_piece[1]+self.columnletters[self.col]+str(self.row+1))#adds the move to the list
                self.player=(self.player+1)%2
                if self.position[self.row][self.col]!=None :# αν υπάρχει κάποιο κομμάτι στην τελική θέση
                    if self.selected_piece[1]=='b' and self.position[self.row][self.col][1]=='b':
                        self.bcurses()
                    if self.position[self.row][self.col][1]=='k':#ελέγχει αν φαγώθηκε ο βασιλιάς
                        tkm.showinfo("You lost", "They captured your king")
                        self.running=False
                    if self.selected_piece[1]=='n' and self.position[self.row][self.col][1]=='r' and self.selected_piece[0]==self.position[self.row][self.col][0]:self.selected_piece=self.selected_piece[0]+"nook"
                    promotions=['queen','rook','bishop','night']
                    shuffle(promotions)
                    if self.selected_piece[:2]=='wp' and self.row==7 :
                        tkm.showinfo("Don't you fill lucky?","The promotion is random")
                        self.selected_piece='w'+promotions[1]
                    if self.selected_piece[:2]=="bp" and self.row==0:
                        tkm.showinfo("Don't you fill lucky?","The promotion is random")
                        self.selected_piece='b'+promotions[2]    
                self.position[self.row][self.col]=self.selected_piece
                if self.selected_piece[1]=='p':#checks for enpassant
                    if abs(self.orow-self.row)==2: self.enpassant(self.row,self.col)
                #interesting openings
                if self.moves[-1]=='nc4':
                    tkm.showinfo("C4 is explosive!", "This tile is very explosive and your ex-knight-looking piece hit it")
                    self.position[3][2]=None
                if self.position[self.mrow][self.mcol]!=None:
                    if self.position[self.mrow][self.mcol][1]=='n' and self.grass==1:
                        tkm.showinfo("The knight just ate the mushroom","You didn't teach it to not eat everything. Now it thinks it belongs to the other team")
                        if self.position[self.mrow][self.mcol][0]=='w':self.position[self.mrow][self.mcol]='b'+self.position[self.mrow][self.mcol][1:]
                        else:self.position[self.mrow][self.mcol]='w'+self.position[self.mrow][self.mcol][1:]
                        self.grass=0
                if self.position[self.brow][self.bcol]!=None:                
                    if self.position[self.brow][self.bcol][1]=="p" and self.book==1:
                        tkm.showinfo("Why did you let the pawns read Marx?","Now they don't like the class differences. They killed every oppressor and destroyed their symbols.  You both lost")
                        for i in range (8):
                            for j in range(8):
                                if self.position[i][j]!=None:
                                    if self.position[i][j][1:]!="pawn":self.position[i][j]=None
                                    else: self.position[i][j]="rpawn"
                        self.running=False
                if self.moves[0]=='pc4' and len(self.moves)==1:
                    tkm.showinfo("English?", "You remember that the English no longer have a queen, right?")
                    self.position[7][3]=None
                if self.moves[0]=='pd4':
                        self.position[1][3]='wpawn'
                        self.position[1][4]=None
                        self.position[3][3]=None
                        self.position[3][4]='wpawn'
                        self.moves[0]='pe4'
                        tkm.showinfo("What is this?", '''If you want to be considered a human you won't play such things.
For now we will play something normal for you. But be careful! ''')
                if self.moves[0]=='pe4':
                    if len(self.moves)==2:
                        if self.moves[1]=='pe6':
                            tkm.showinfo("French?","You know the French surrendered in WW2. You want to do the same? Fine. Black surrenders and white wins")
                            running=False
                        if self.moves[1]=='pa6':
                            tkm.showinfo("Saint George's defence","The general-saint turns the pawn into a bishop")
                            self.position[5][0]='bbishop'
                        if self.moves[1]=='pd5':
                            self.sk=1
                            tkm.showinfo("Scandinavian??","That's very cold. Now the pawns and pieces can only move about half the distance before needing to warm themselves.")
                    if len(self.moves)==3:
                        if self.moves[-1][0]=='q':
                            tkm.showinfo("Congratulations","Your queen is very brave to come out this early. She is so brave she came out as a transgender")
                            self.piece_imb['wqueen']='wking.png'
                            tkm.showinfo("Change","The new gender doesn't change his moves. But the bishops are transphobic so they quit")
                            self.position[0][2]=None
                            self.position[0][5]=None
                    if len(self.moves)==5:
                        if self.moves[1:5]==['pe5','nf3','nc6','bc4']:
                            tkm.showinfo("Italian??"," Your king and queen will change their style. It won't affect your game but it will remind everyone your wrong choices")
                            self.piece_imb['wqueen']='Iqueen.png'
                            self.piece_imb['wking']='Iking.png'
                    if len(self.moves)==6:
                            if ('nf3' in self.moves and 'nf6' in self.moves and 'nc3' in self.moves and 'nc6' in self.moves):
                                tkm.showinfo("4 knights??", "You like the knights huh? Take some more!")
                                self.position[0][0],self.position[0][7]='wnook','wnook'
                                self.position[0][2],self.position[0][5]='wnight','wnight'
                                self.position[7][0],self.position[7][7]='bnook','bnook'
                                self.position[7][2],self.position[7][5]='bnight','bnight'                               
                    if len(self.moves)==100:
                        tkm.showinfo("You can't finish this game?","Try rock-paper-scissors to find the winner")
                        self.running=False
                rd100=randint(1,150)
                if  self.grass==0 and (rd100//17==2):
                    self.grass=1
                    self.mrow, self.mcol= random_pos()
                if ( self.book==0 and rd100>=148):
                    self.book=1
                    self.brow,self.bcol= random_pos()
            else:
                self.position[self.orow][self.ocol]=self.selected_piece
        self.movement=0
        self.selected_piece_position=None
        self.selected_piece = None         
        self.draw_pieces()

    def draw_pieces(self): 
        self.clear_widgets()  
        self.add_widget(self.image)  
        for row in range(8):
            for col in range(8):
                piece = self.position[row][col]
                if piece is not None:
                    x = col * self.width // 8
                    y = row * self.height // 8
                    piece_image = Image(source=self.piece_imb[piece] , size_hint=(0.125, 0.125),  pos=(x, y))
                    self.add_widget(piece_image) 
        if self.grass==1:
            mush=Image(source="mushrooms.png",size_hint=(0.125, 0.125),pos=(self.mcol*self.width//8,self.mrow*self.height//8))
            self.add_widget(mush)
        if self.book==1:
            book=Image(source="book.png",size_hint=(0.125, 0.125),pos=(self.bcol*self.width//8,self.brow*self.height//8))
            self.add_widget(book)
            
    def legal(self, starting_position, ending_position):# checks the legality of the movemet
        difference=ending_position-starting_position
        self.wlist=[]
        self.blist=[]
        erow=(ending_position)//8# finds the initial position
        ecol=(ending_position)%8
        colors=['w','b']
        #print(difference,ending_position+8)
        for i in range(8):#finds the squares with the pieces
            for j in range(8):
                if self.position[i][j]!=None:
                    if self.position[i][j][0]=='w': self.wlist.append(8*i+j)
                    if self.position[i][j][0]=='b': self.blist.append(8*i+j)
                
        #white pawns
        if self.selected_piece[:5]=="wpawn" and (ending_position not in self.wlist) and (ending_position not in self.blist):
            if difference==8:return 1
            if difference==16 and not self.sk and ending_position//8==3 and (ending_position-8 not in self.wlist) and (ending_position-8 not in self.blist): return 1
        if self.selected_piece[:5]=="wpawn" and ending_position in self.blist and difference==7 and (starting_position%8)!=0:return 1
        if self.selected_piece[:5]=="wpawn" and ending_position in self.blist and difference==9 and (starting_position%8)!=7:return 1

        #black pawns
        if self.selected_piece[:5]=="bpawn" and (ending_position not in self.wlist) and (ending_position not in self.blist):
            if difference==-8:return 1
            if difference==-16 and not self.sk and ending_position//8==4 and (ending_position+8 not in self.wlist) and (ending_position+8 not in self.blist):return 1
        if self.selected_piece[:5]=="bpawn" and ending_position in self.wlist and difference==-7 and (starting_position%8)!=7:return 1
        if self.selected_piece[:5]=="bpawn" and ending_position in self.wlist and difference==-9 and (starting_position%8)!=0:return 1

        #kings
        kingcheck=[-9,-8,-7,-1,1,7,8,9]
        for n in kingcheck:
            if self.selected_piece[:5]=='bking' and difference==int(n) and ending_position not in self.blist: return 1
            if self.selected_piece[:5]=='wking' and difference==int(n) and ending_position not in self.wlist: return 1
        if (self.selected_piece[:5]=='bking' and starting_position==60 and (ending_position==62 or ending_position==58)) or(self.selected_piece=='wking' and starting_position==4 and (ending_position==2 or ending_position==6)):
            tkm.showinfo("Are you afraid and trying to hide your king;"," There is a battle. You can't run away. Your king has to command the others.")
            return 0

        #knights, knooks and anti-queens
        if (self.selected_piece[:2]=='wn' and ending_position not in self.wlist) or (self.selected_piece[:6]=='wnight' and self.position[erow][ecol]=='wrook' ) or (self.selected_piece[:6]=='bnight' and self.position[erow][ecol]=='brook') or (self.selected_piece[:2]=='bn' and ending_position not in self.blist):
            if difference==-17 and starting_position//8>=2 and starting_position%8>0: return 1
            if difference==17 and starting_position//8<=5 and starting_position%8<7: return 1
            if difference==-15 and starting_position//8>=2 and starting_position%8<7: return 1
            if difference==15 and starting_position//8<=5 and starting_position%8>0: return 1
            if difference==-10 and starting_position//8>=1 and starting_position%8>1: return 1
            if difference==10 and starting_position//8<=6 and starting_position%8<6: return 1
            if difference==-6 and starting_position//8>=1 and starting_position%8<6: return 1
            if difference==6 and starting_position//8<=6 and starting_position%8>1: return 1
            
        #rooks,nooks and queens
        if self.selected_piece[4]=='k' or self.selected_piece[1]=='q':
            if ending_position//8==starting_position//8:
                if (difference*difference)>16 and self.sk==1:return 0
                if difference>0:return self.lines(starting_position,difference,1)
                elif difference<0:return self.lines(starting_position,difference,-1)        
            if ending_position%8==starting_position%8:
                if (difference*difference)>(32*32) and self.sk==1:return 0
                if difference>0:return self.lines(starting_position,difference,8)
                elif difference<0:return self.lines(starting_position,difference,-8)    

        #bishops and queens
        if (self.selected_piece[1]=='b' or self.selected_piece[1]=='q') and starting_position%8!=(starting_position+difference)%8 and starting_position//8!=(starting_position+difference)//8:
            if self.sk==0:
                ltrb=[-9,+9,-18,+18,-27,+27,-36,+36,-45,+45,-54,+54,-63,+63]
                lbrt=[-7,+7,-14,+14,-21,+21,-28,+28,-35,+35,-42,+42,-48,+48]
            else:
                ltrb=[-9,+9,-18,+18,-27,+27,-36,+36]
                lbrt=[-7,+7,-14,+14,-21,+21,-28,+28]            
            if difference in ltrb :
                if difference>0:return self.lines(starting_position,difference,9)
                elif difference<0:return self.lines(starting_position,difference,-9)        
            if difference in lbrt:
                if difference>0 :return self.lines(starting_position,difference,7)
                elif difference<0:return self.lines(starting_position,difference,-7)    
        return 0
    
    def lines(self,starting_position, difference,dirr):#checks for pieces in the line that a piece might use
        for i in range(dirr,difference,dirr):
            if starting_position+i in self.blist or starting_position+i in self.wlist:return 0
        if starting_position+difference in self.blist and self.selected_piece[0]=='b':return 0
        if starting_position+difference in self.wlist and self.selected_piece[0]=='w':return 0    
        return 1
    
    def curses(self,rd):#curses
        if rd==1:#spawns pawns in their initial position
            for i in range (8):
                if self.position[6][i]== None: self.position[6][i]='bpawn'
                if self.position[1][i]==None: self.position[1][i]='wpawn'
        elif rd==2:#makes some pawns disappear
            for i in range (8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        rd9=randint(1,9)
                        if self.position[i][j][1]=='p' and rd9>5:self.position[i][j]=None
        elif rd==3:#turns the bishops into knights and vice-versa
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][1]=='b': self.position[i][j]=self.position[i][j][0]+'night'
                        elif self.position[i][j][1:3]=='ni': self.position[i][j]=self.position[i][j][0]+'bishop'
            self.selected_piece=self.selected_piece[0]+'night'
        elif rd==4:#turns the queens into rooks
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][1]=='q': self.position[i][j]=self.position[i][j][0]+'rook'
        elif rd==5:#spawns two pawns randomly (not on the first/last rank)
            while True:
                rd8_1,rd8_2=random_pos()
                if rd8_1>0 and rd8_1<7 and self.position[rd8_1][rd8_2]==None:
                    self.position[rd8_1][rd8_2]='wpawn'
                    break
            while True:
                rd8_1,rd8_2=random_pos()
                if rd8_1>0 and rd8_1<7 and self.position[rd8_1][rd8_2]==None:
                    self.position[rd8_1][rd8_2]='bpawn'
                    break
        elif rd==6:#turns the queens into antiqueens
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][1]=='q': self.position[i][j]=self.position[i][j][0]+'niqueen'
        elif rd==7:#turns the images of the pieces into images of checkers
            for key in self.piece_images:
                self.piece_imb[key]=self.piece_imb[key][0]+'checkers.png'

    def bcurses(self):#chooses the curse after the capture of a bishop from another
        rd=6#randint(1,7)
        curselist=["The meeting of the two bishops makes pawns on their starting position","The meeting of the two bishops curses some pawns who disappear",  "The meeting of the two bishops changes the knights and bishops",
                 "The meeting of the two bishops curses the queens who turn into rooks", "The meeting of the two bishops makes two pawns appear somewhere on the board","The meeting of the two bishops curses the queens who turn into anti-queens. They move in the range of two tiles where a normal queen can't move on an empty board.",
                  "The meeting of the two bishops curses the pieces who turn into checkers pieces. They move the same as before"]
        tkm.showinfo("Cursed",curselist[rd-1])
        self.curses(rd)
        
    def enpassant (self, row,column):#checks for en passant
        if self.position[row][column]=='wpawn':
            ep=0
            try:
                if self.position[row][column-1]=='bpawn':
                    self.position[row][column-1]=None
                    ep+=1
                if self.position[row][column+1]=='bpawn':
                    self.position[row][column+1]=None
                    ep+=1
            except:pass
            if ep==1:
                self.position[row][column]=None
                self.position[row-1][column]='bpawn'
                self.player=(self.player+1)%2
                self.moves.append('p'+self.columnletters[column]+'3')
                ep=0
                tkm.showinfo("En Passant","Congratulations En Passant just happened.(automatically because it is a forced move)")
            if ep==2:
                tkm.showinfo("Double En Passant","That is a miracle. It is so miraculous that changed the pawn into a bishop")
                self.position[row-1][column]='bbishop'
                self.position[row][column]=None
                self.player=(self.player+1)%2
                self.moves.append('b'+self.columnletters[column]+'3')
        if self.position[row][column]=='bpawn':
            ep=0
            try:
                if self.position[row][column-1]=='wpawn':
                    self.position[row][column-1]=None
                    ep+=1
                if self.position[row][column+1]=='wpawn':
                    self.position[row][column+1]=None
                    ep+=1
            except:pass
            if ep==1:
                self.position[row][column]=None
                self.position[row+1][column]='wpawn'
                self.player=(self.player+1)%2
                self.moves.append('p'+self.columnletters[column]+'6')
                ep=0
                tkm.showinfo("En Passant","Congratulations En Passant just happened.(automatically because it is a forced move)")
            if ep==2:
                tkm.showinfo("Double En Passant","That is a miracle. It is so miraculous that changed the pawn into a bishop")
                self.position[row+1][column]='wbishop'
                self.moves.append('b'+self.columnletters[column]+'6')
                self.position[row][column]=None
                self.player=(self.player+1)%2
            
def random_pos():
    return randint(0,7), randint(0,7)

class PongApp(App):
    def build(self):
        global window
        window=MyLayout()
        return window
    
if __name__ == '__main__':
    PongApp().run()
