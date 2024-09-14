from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from random import randint,shuffle
from kivypopup import show_popup,QuestionPopup
import requests

class InnerFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(InnerFloatLayout, self).__init__(**kwargs)
        self.image = Image(source="board.png", size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image)
        self.piece_images = {}
        self.piece_imb={}
        self.lexlist=['wpawn','wrook','wnight','wbishop','wking', 'wqueen','bpawn','brook','bnight','bbishop','bking','bqueen','wniqueen','bniqueen','rpawn']
        for item in self.lexlist:
            self.piece_imb[item]=item+'.png'
        self.position = [
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
        self.suremessage=0
    def on_size(self, *args):
        self.draw_pieces()        
    def on_touch_down(self, touch):
        if not self.running:return 0
        self.col=int(touch.x//(self.width//8))
        self.row=int((touch.y-self.hbc)//(self.width//8))
        if self.col<0 or self.col>7 or self.row<0 or self.row>7:return super(InnerFloatLayout, self).on_touch_down(touch)
        if self.position[self.row][self.col] is not None:
            self.selected_piece = self.position[self.row][self.col]
            if (self.selected_piece[0]=="w" and self.player==0) or (self.selected_piece[0]=="b" and self.player==1):            
                self.selected_piece_position = (self.row, self.col)
                self.movement=1
                self.selected_imagen = self.piece_imb[self.selected_piece]  # The image of the selected piece
                self.selected_image=Image(source=self.selected_imagen, size_hint=(0.125, 0.125),pos=(self.col*self.width/8,self.hbc+self.row*self.width/8))
                self.position[self.row][self.col] = None
                self.draw_pieces()
                self.add_widget(self.selected_image)
            else: self.selected_piece=None  
        return super(InnerFloatLayout, self).on_touch_down(touch)

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
            self.row=int((touch.y-self.hbc)//(self.width/8))
            if self.legal(8*self.orow+self.ocol,8*self.row+self.col) and self.row>=0 and self.col >=0:
                self.moves.append(self.selected_piece[1]+self.columnletters[self.col]+str(self.row+1))#adds the move to the list
                self.player=(self.player+1)%2
                if self.suremessage==1:
                    show_popup("Are you sure?", "Seems suspicious")#just shows this message
                    self.suremessage=0
                if self.position[self.row][self.col]!=None :# checks for a capture
                    if self.selected_piece[1]=='b' and self.position[self.row][self.col][1]=='b':
                        self.bcurses()
                    if self.position[self.row][self.col][1]=='k':#checks for the capture of a king
                        show_popup("You lost", "They captured your king")
                        self.running=False
                if (self.selected_piece[:2]=='wp' and self.row==7) or ( self.selected_piece[:2]=="bp" and self.row==0):
                    promotions=['queen','rook','bishop','night']#for pawns that reach the last rank
                    shuffle(promotions)
                    show_popup("Don't you fill lucky?","The promotion is random")
                    self.selected_piece=self.selected_piece[0]+promotions[1]
                self.position[self.row][self.col]=self.selected_piece
                if self.selected_piece[1]=='p':#checks for en-passant
                    if abs(self.orow-self.row)==2: self.enpassant(self.row,self.col)
                if self.moves[-1]=='nc4':
                    show_popup("C4 is explosive!", "This tile is very explosive and your ex-knight-looking piece hit it")
                    self.position[3][2]=None
                if self.position[self.mrow][self.mcol]!=None:
                    if self.position[self.mrow][self.mcol][1]=='n' and self.grass==1:
                        show_popup("The knight just ate the mushroom","You didn't teach it to not eat everything. Now it thinks it belongs to the other team")
                        if self.position[self.mrow][self.mcol][0]=='w':self.position[self.mrow][self.mcol]='b'+self.position[self.mrow][self.mcol][1:]
                        else:self.position[self.mrow][self.mcol]='w'+self.position[self.mrow][self.mcol][1:]
                        self.grass=0
                if self.position[self.brow][self.bcol]!=None:                
                    if self.position[self.brow][self.bcol][1]=="p" and self.book==1:
                        show_popup("Why did you let the pawns read Marx?","Now they don't like the class differences. They killed every oppressor and destroyed their symbols.  You both lost")
                        for i in range (8):
                            for j in range(8):
                                if self.position[i][j]!=None:
                                    if self.position[i][j][1:]!="pawn":self.position[i][j]=None
                                    else: self.position[i][j]="rpawn"
                        self.running=False
                if len(self.moves)==150:
                    show_popup("You can't finish this game?","Try rock-paper-scissors to find the winner")
                    self.running=False
                    
                self.interesting_openings()                   
                self.randomchanges()

            else:
                self.position[self.orow][self.ocol]=self.selected_piece
        self.movement=0
        self.selected_piece_position=None
        self.selected_piece = None         
        self.draw_pieces()

    def draw_pieces(self): 
        self.clear_widgets()  
        self.add_widget(self.image)
        square_size=self.width//8
        centering_factor=7*self.hbc//8
        def add_image(source,row,col):
            x = col * square_size
            y = row * square_size + centering_factor
            image = Image(source=source, size_hint=(0.125,0.125), pos=(x, y))
            self.add_widget(image)
        for row in range(8):
            for col in range(8):
                piece = self.position[row][col]
                if piece is not None:add_image(self.piece_imb[piece],row,col)
        if self.grass==1:add_image("mushrooms.png",self.mrow,self.mcol)
        if self.book==1:add_image("book.png",self.brow,self.bcol)
            
    def legal(self, starting_position, ending_position):# checks for the legality of the move
        difference=ending_position-starting_position
        self.wlist=[]
        self.blist=[]
        erow=(ending_position)//8
        ecol=(ending_position)%8
        colors=['w','b']
        for i in range(8):#adds the position of the pieces in two lists
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
            show_popup("Are you afraid and trying to hide your king;"," There is a battle. You can't run away. Your king has to command the others.")
            return 0

        #knights and anti-queens
        if (self.selected_piece[:2]=='wn' and ending_position not in self.wlist) or (self.selected_piece[:2]=='bn' and ending_position not in self.blist):
            if difference==-17 and starting_position//8>=2 and starting_position%8>0: return 1
            if difference==17 and starting_position//8<=5 and starting_position%8<7: return 1
            if difference==-15 and starting_position//8>=2 and starting_position%8<7: return 1
            if difference==15 and starting_position//8<=5 and starting_position%8>0: return 1
            if difference==-10 and starting_position//8>=1 and starting_position%8>1: return 1
            if difference==10 and starting_position//8<=6 and starting_position%8<6: return 1
            if difference==-6 and starting_position//8>=1 and starting_position%8<6: return 1
            if difference==6 and starting_position//8<=6 and starting_position%8>1: return 1
            
        #rooks and queens
        if self.selected_piece[4]=='k' or self.selected_piece[1]=='q':
            if ending_position//8==starting_position//8:
                if (difference**2>16 and self.sk==1):return 0
                if difference>0:return self.lines(starting_position,difference,1)
                elif difference<0:return self.lines(starting_position,difference,-1)        
            if ending_position%8==starting_position%8:
                if (difference**2)>(1024) and self.sk==1:return 0
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
    
    def lines(self,starting_position, difference,dirr):#checks for pieces in the line another piece wants to move
                                                                                
        for i in range(dirr,difference,dirr):
            if starting_position+i in self.blist or starting_position+i in self.wlist:return 0
        if starting_position+difference in self.blist and self.selected_piece[0]=='b':return 0
        if starting_position+difference in self.wlist and self.selected_piece[0]=='w':return 0    
        return 1
    
    def curses(self,rd):
        if rd==1:#spawns pawns in their original position
            for i in range (8):
                if self.position[6][i]== None: self.position[6][i]='bpawn'
                if self.position[1][i]==None: self.position[1][i]='wpawn'
        elif rd==2:#makes some pawns disappear
            for i in range (8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        rd9=randint(1,9)
                        if self.position[i][j][1]=='p' and rd9>6:self.position[i][j]=None
        elif rd==3:#changes bishops into knights and vice versa
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][1]=='b': self.position[i][j]=self.position[i][j][0]+'night'
                        elif self.position[i][j][1:3]=='ni': self.position[i][j]=self.position[i][j][0]+'bishop'
            self.selected_piece=self.selected_piece[0]+'night'
        elif rd==4:#demotes the queens into rooks
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][1]=='q': self.position[i][j]=self.position[i][j][0]+'rook'
        elif rd==5:#spawns two pawns randomly
            while True:
                rd8_1,rd8_2=randint(1,6),randint(0,7)
                if  self.position[rd8_1][rd8_2]==None:
                    self.position[rd8_1][rd8_2]='wpawn'
                    break
            while True:
                rd8_1,rd8_2=randint(1,6),randint(0,7)
                if  self.position[rd8_1][rd8_2]==None:
                    self.position[rd8_1][rd8_2]='bpawn'
                    break
        elif rd==6:#turns the queens into anti-queens
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][1]=='q': self.position[i][j]=self.position[i][j][0]+'niqueen'
        elif rd==7:#turns the pieces into checkers pieces
            for key in self.piece_images:
                self.piece_imb[key]=key[0]+'checkers.png'
        elif rd==8:#turns the color of the white pieces to black
            for key in self.piece_images:
                if self.piece_imb[key][0]=='w':self.piece_imb[key]='b'+self.piece_imb[key][1:]

    def bcurses(self):#chooses a curse
        rd=randint(1,8)
        curselist=["The meeting of the two bishops makes pawns on their starting position","The meeting of the two bishops curses some pawns who disappear",  "The meeting of the two bishops changes the knights and bishops",
                 "The meeting of the two bishops curses the queens who turn into rooks", "The meeting of the two bishops makes two pawns appear somewhere on the board","The meeting of the two bishops curses the queens who turn into anti-queens. They move in the range of two tiles where a normal queen can't move on an empty board.",
                  "The meeting of the two bishops curses the pieces who turn into checkers pieces. They move the same as before","The meeting of the two bishops turns the color of the white pieces into black. They move the same but have different color"]
        show_popup("Cursed",curselist[rd-1])
        self.curses(rd)
        
    def enpassant (self, row,column):#checks for enpassant
        reverselex={"w":"b","b":"w"}
        letter=self.position[row][column][0]
        reversepawn=reverselex[letter]+"pawn"
        if letter=="w": numberlist=[ -1,3]
        else:numberlist=[ 1,6]
        ep=0
        try:
            if self.position[row][column-1]==reversepawn:
                self.position[row][column-1]=None
                ep+=1
            if self.position[row][column+1]==reversepawn:
                self.position[row][column+1]=None
                ep+=1
        except:pass
        if ep==1:
            self.position[row][column]=None
            self.position[row+numberlist[0]][column]=reversepawn
            self.player=(self.player+1)%2
            self.moves.append('p'+self.columnletters[column]+str(numberlist[1]))
            ep=0
            show_popup("En Passant","Congratulations En Passant just happened.(automatically because it is a forced move)")
        if ep==2:
            show_popup("Double En Passant","That is a miracle. It is so miraculous that changed the pawn into a bishop")
            self.position[row+numberlist[0]][column]=reversepawn
            self.position[row][column]=None
            self.player=(self.player+1)%2
            self.moves.append('b'+self.columnletters[column]+str(numberlist[1]))

                
    def interesting_openings(self):
        if self.selected_piece[1]=="q" and len(self.moves)<=6:
            for i in range(8):
                for j in range(8):
                    if self.position[i][j]!=None:
                        if self.position[i][j][0]==self.selected_piece[0] and self.position[i][j][1]=="b":
                            self.position[i][j]=None
            show_popup("Change","The new gender doesn't change his moves. But the bishops are transphobic so they quit")#this message will appear second
            self.piece_imb[self.selected_piece]=self.selected_piece[0]+'king.png'
            show_popup("Congratulations","Your queen is very brave to come out this early. She is so brave she came out as a transgender")#this message will appear first
        if self.moves[0]=='pc4' and len(self.moves)==1:
            show_popup("English?", "You remember that the English no longer have a queen, right?")
            self.position[0][3]=None
        if self.moves[0]=='pd4':
                self.position[1][3]='wpawn'
                self.position[1][4]=None
                self.position[3][3]=None
                self.position[3][4]='wpawn'
                self.moves[0]='pe4'
                show_popup("What is this?", '''If you want to be considered a human you won't play such things.
    For now we will play something normal for you. But be careful! ''')
        if self.moves[0]=='pe4':
            if len(self.moves)==2:
                if self.moves[1]=='pe6':
                    show_popup("French?","You know the French surrendered in WW2. You want to do the same? Fine. Black surrenders and white wins")
                    self.running=False
                if self.moves[1]=='pa6':
                    show_popup("Saint George's defence","The general-saint turns the pawn into a bishop")
                    self.position[5][0]='bbishop'
                if self.moves[1]=='pd5':
                    self.sk=1
                    show_popup("Scandinavian??","That's very cold. Now the pawns and pieces can only move about half the distance before needing to warm themselves.")
            if len(self.moves)==5:
                if self.moves[1:5]==['pe5','nf3','nc6','bc4']:
                    show_popup("Italian??"," Your king and queen will change their style. It won't affect your game but it will remind everyone your wrong choices")
                    self.piece_imb['wqueen']='Iqueen.png'
                    self.piece_imb['wking']='Iking.png'
                if self.moves[1:5]==['pe5','nf3','nc6','bb5']:
                    show_popup("Spanish?","Be careful. Nobody expects the spanish Inquisition")
                    for i in range(6,8):
                        self.position[2][i]="wbishop"
                        self.position[3][i]="wbishop"
                        self.position[4][i]="bbishop"
                        self.position[5][i]="bbishop"
        if len(self.moves)==6:
                if ('nf3' in self.moves and 'nf6' in self.moves and 'nc3' in self.moves and 'nc6' in self.moves):
                    show_popup("4 knights??", "You like the knights huh? Take some more!")
                    self.position[0][2],self.position[0][5]='wnight','wnight'
                    self.position[7][2],self.position[7][5]='bnight','bnight'
                    
    def randomchanges(self):
        rd100=randint(1,150)
        if  self.grass==0 and (rd100//17==2):
            self.grass=1
            self.mrow, self.mcol= self.random_pos()
        if ( self.book==0 and rd100>=148):
            self.book=1
            self.brow,self.bcol= self.random_pos()
        if rd100==66:self.suremessage=1
        if (rd100==23 or rd100==123):self.random_fact()
        if (rd100>=2 and rd100<=5):self.multiplechoice()
        
    def random_pos(self):
        return randint(0,7), randint(0,7)

    def random_fact(self):
        try:
            r=requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
            data=r.json()
            show_popup("Fun Fact", data["text"])
        except:
            pass

    def multiplechoice(self):
        try:
            r=requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
            data=r.json()["results"][0]
            def testfunc(result):
                if (result):self.player=(self.player+1)%2
            objecttest=QuestionPopup()
            test=objecttest.show_question_popup(data["question"],data["correct_answer"],data["incorrect_answers"],testfunc)
        except: pass

class OuterFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(OuterFloatLayout, self).__init__(**kwargs)
        self.create_game()
    def create_game(self):
        self.inner_layout = InnerFloatLayout()
        self.inner_layout.hbc=(self.height-self.width)//2
        self.add_widget(self.inner_layout)
        self.bind(size=self._update_inner_layout_size)
    def _update_inner_layout_size(self, instance, value):
        width, height = self.size
        side_length = min(width, height)
        self.inner_layout.size = (side_length, side_length)
        self.inner_layout.pos = ((width - side_length) / 2, (height - side_length) / 2)
        self.inner_layout.hbc=(self.height-self.width)//2
        
class NewChessApp(App):
    def build(self):
        global outer_layout
        outer_layout = OuterFloatLayout()
        return outer_layout

if __name__ == '__main__':
    NewChessApp().run()
