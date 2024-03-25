from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import tkinter.messagebox as tkm
from random import randint,shuffle

class MyLayout(FloatLayout):
    def __init__(self, **kwargs):
        global chessboard,player
        super(MyLayout, self).__init__(**kwargs)
        chessboard=Chessboard()
        self.image = Image(source="board.png", size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)  # Προσθήκη της εικόνας στο layout        
        namelist=['rook1','night1','bishop1','queen1','king1','bishop2','night2','rook2']
        movelist=[[4],[3],[5],[4,5],[2],[5],[3],[4]]
        collist=[['black','white'],[0,7]]
        
        for j in range(8):
            globals()[f'wpawn{j+1}']=Piece("white", "pawn", j, 6,j+1,[0])
            globals()[f'bpawn{j+1}']=Piece("black", "pawn", j, 1,j+1,[1])
            for i in range(2):
                globals()[f'{collist[0][i][0]}{namelist[j]}']= Piece(collist[0][i], namelist[j][:-1], j, collist[1][i],int(namelist[j][-1]),movelist[j])
        self.selected_piece = None
        self.player=0
        columnletters=['a','b','c','d','e','f','g','h']
        for row in range(8):
            for col in range(8):
                piece = chessboard.position[row][col]
                if piece is not None:
                    x = col * self.width//8
                    y = row * self.height//8
                    self.add_widget(piece.image) 
    def on_size(self, *args):
        #self.img2.pos = (self.x2*self.width / 8 , self.y2*self.height / 8)
        self.draw_pieces()        
    def on_touch_down(self, touch):
        self.col=int(touch.x//(self.width//8))
        self.row=int(touch.y//(self.height//8))
        if chessboard.position[self.row][self.col] is not None:
            self.selected_piece = chessboard.position[self.row][self.col]
            if (self.selected_piece.color[0]=="w" and self.player==0) or (self.selected_piece.color[0]=="b" and self.player==1):            
                self.selected_piece_position = (self.row, self.col)
                self.movement=1
                chessboard.position[self.row][self.col] = None
            else: self.selected_piece=None
            
        #return super(MyLayout, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.selected_piece is not None:
            self.new_x = touch.x - self.selected_piece.image.width / 2
            self.new_y = touch.y - self.selected_piece.image.height / 2
            self.selected_piece.image.pos =(self.new_x, self.new_y)

    def on_touch_up(self, touch):
        self.ocol=self.col
        self.orow=self.row
        if self.selected_piece!=None :
            self.col=int(touch.x//(self.width /8))
            self.row=int(touch.y//(self.height/8))
            if legal(self.selected_piece,8*self.orow+self.ocol,8*self.row+self.col):
                self.player=(self.player+1)%2
                if chessboard.position[self.row][self.col]!=None :# αν υπάρχει κάποιο κομμάτι στην τελική θέση
                    if self.selected_piece.name[0]=='b' and chessboard.position[self.row][self.col].name[0]=='b':
                        bcurses(self.selected_piece)
                    chessboard.position[self.row][self.col].captured()
                chessboard.position[self.row][self.col]=self.selected_piece
            else:
                chessboard.position[self.orow][self.ocol]=self.selected_piece
        self.movement=0
        self.selected_piece_position=None
        self.selected_piece = None
        self.draw_pieces()
        
    def draw_pieces(self): 
        self.clear_widgets()
        self.image = Image(source="board.png", size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)
        for row in range(8):
            for col in range(8):
                piece = chessboard.position[row][col]
                if piece is not None:
                    print(piece.name+str(piece.number)+str(row)+str(col))
                    x = col * self.width // 8
                    y = row * self.height // 8
                    piece.image.pos = (x, y)
                    self.add_widget(piece.image)
                    
class PongApp(App):
    def build(self):
        global window
        window=MyLayout()
        return window
    
class Piece():
    global chessboard
    Piecelex={'wpawn':0,'wnight':0,'wbishop':0,'wrook':0,'wnook':0,'wqueen':0,'wking':0,'bpawn':0,'bnight':0,'bbishop':0,'brook':0,'bnook':0,'bqueen':0,'bking':0,'rpawn':0}
    checkers=0
    def __init__(self, color, name, xposition, yposition,number,legalmovements,specialmoves=None):
        self.color = color
        self.name = name
        self.xposition = xposition
        self.yposition = 7-yposition
        self.number=number
        chessboard.add_piece(self)
        self.image=Image(source=self.color[0]+self.name+'.png', size_hint=(0.125, 0.125))
        self.legalmovements=legalmovements
        self.Piecelex[self.color[0]+self.name]+=1
        self.specialmoves=specialmoves
        #self.initial_special()
    def numbers(self,piecename):
        return self.Piecelex[piecename]
    def captured(self):
        #chessboard.print_board()
        global window
        cp=self
        window.remove_widget(cp.image)
        for i in range(self.number,Piece.Piecelex[cp.color[0]+cp.name],1):
            newp=globals()[f'{self.color[0]+self.name}{i+1}']
            cp.xposition,cp.yposition=newp.xposition,newp.yposition
            chessboard.position[cp.yposition][cp.xposition]=cp
            cp=newp
        Piece.Piecelex[self.color[0]+self.name]-=1
##        for i in range (8):
##            for j in range (8):
##                if chessboard.position[i][j] is not None:
##                    print (chessboard.position[i][j].name+str(chessboard.position[i][j].number))
        return 0

class Chessboard():
    def __init__(self):
        self.position = [[None for _ in range(8)] for _ in range(8)]

    def add_piece(self, piece):
        self.position[piece.yposition][piece.xposition] = piece

    def print_board(self):
        for row in self.position:
                for item in row:
                    if item==None:print("None")
                    else: print(item.name)
                    
    def add_in_position(self,name,xposition,yposition,specialmoves=None):
        movementslex={'wpawn':[0],'bpawn':[1],'king':[2],'night':[3],'rook':[4],'bishop':[5],'queen':[4,5],'nook':[3,4],'rpawn':[]}
        number=wking1.numbers(name)+1
        if name[1]=='p':globals()[f'{name}{number}']=Piece(name[0],name[1:],xposition,yposition,number,movementslex[name])
        else:globals()[f'{name}{number}']=Piece(name[0],name[1:],xposition,yposition,number,movementslex[name[1:]],specialmoves)
        self.position[yposition][xposition] = globals()[f'{name}{number}']
        
    def change_pieces(self,oldlist,newlist,specialmoves=None):
        for i in range(8):
            for j in range(8):
                if self.position[i][j]!=None:
                    c=self.position[i][j].color[0]
                    for k in range(len(oldlist)):
                        if self.position[i][j].name==oldlist[k]:
                            self.position[i][j].captured()
                            self.add_in_position(c+newlist[k],j,i,specialmoves)
                            break
                        
def legal(piece,starting_position, ending_position):# ελέγχει την νομιμότητα της κίνησης
    global player,sk,chessboard
    difference=ending_position-starting_position
    wlist,blist=pieceplaces()
    erow=(ending_position)//8#βρίσκει την αρχική θέση
    ecol=(ending_position)%8
    sk=0
    colors=['w','b']
    letter={'w':wlist,'b':blist}
    print(difference,ending_position,wlist,blist)
    #white pawns
    if 0 in piece.legalmovements and (ending_position not in wlist) and (ending_position not in blist):
        if difference==+8:return 1
        if difference==+16 and not sk and ending_position//8==3 and (ending_position-8 not in wlist) and (ending_position-8 not in blist): return 1
    if 0 in piece.legalmovements and ending_position in blist and difference==+7 and (starting_position%8)!=0:return 1
    if 0 in piece.legalmovements and ending_position in blist and difference==+9 and (starting_position%8)!=7:return 1

    #black pawns
    if 1 in piece.legalmovements and (ending_position not in wlist) and (ending_position not in blist):
        if difference==-8:return 1
        if difference==-16 and not sk and ending_position//8==4 and (ending_position+8 not in wlist) and (ending_position+8 not in blist):return 1
    if 1 in piece.legalmovements and ending_position in wlist and difference==-7 and (starting_position%8)!=7:return 1
    if 1 in piece.legalmovements and ending_position in wlist and difference==-9 and (starting_position%8)!=0:return 1

    #kings
    kingcheck=[-9,-8,-7,-1,1,7,8,9]
    for n in kingcheck:
        if 2 in piece.legalmovements and difference==int(n) and ending_position not in letter[piece.color[0]]: return 1
    if  2 in piece.legalmovements:
        if (piece.color[0]=='w' and starting_position==60 and (ending_position==62 or ending_position==58)) or(piece.color[0]=='b' and starting_position==4 and (ending_position==2 or ending_position==6)):
            tkm.showinfo("Are you afraid and trying to hide your king;"," There is a battle. You can't run away. Your king has to command the others.")
        return 0

    #knights, knooks and anti-queens
    if 3 in piece.legalmovements:
        if (ending_position not in letter[piece.color[0]]) :
            if difference==-17 and starting_position//8>=2 and starting_position%8>0: return 1
            if difference==17 and starting_position//8<=5 and starting_position%8<7: return 1
            if difference==-15 and starting_position//8>=2 and starting_position%8<7: return 1
            if difference==15 and starting_position//8<=5 and starting_position%8>0: return 1
            if difference==-10 and starting_position//8>=1 and starting_position%8>1: return 1
            if difference==10 and starting_position//8<=6 and starting_position%8<6: return 1
            if difference==-6 and starting_position//8>=1 and starting_position%8<6: return 1
            if difference==6 and starting_position//8<=6 and starting_position%8>1: return 1
        elif chessboard.position[erow][ecol].name=="rook"and piece.specialmoves!='antiqueen':
            return 1
        
    #rooks,nooks and queens
    if 4 in piece.legalmovements:
        if ending_position//8==starting_position//8:
            if (difference*difference)>16 and sk==1:return 0
            if difference>0:return lines(piece,starting_position,difference,1)
            elif difference<0:return lines(piece,starting_position,difference,-1)        
        if ending_position%8==starting_position%8:
            if (difference*difference)>(32*32) and sk==1:return 0
            if difference>0:return lines(piece,starting_position,difference,8)
            elif difference<0:return lines(piece,starting_position,difference,-8)    

    #bishops and queens
    if 5 in piece.legalmovements and starting_position%8!=(starting_position+difference)%8 and starting_position//8!=(starting_position+difference)//8:
        ltrb=[-9,+9,-18,+18,-27,+27,-36,+36,-45,+45,-54,+54,-63,+63]
        lbrt=[-7,+7,-14,+14,-21,+21,-28,+28,-35,+35,-42,+42,-48,+48]            
        if difference in ltrb[0:(14-4*sk)] :
            if difference>0:return lines(piece,starting_position,difference,9)
            elif difference<0:return lines(piece,starting_position,difference,-9)        
        if difference in lbrt[0:(14-4*sk)]:
            if difference>0 :return lines(piece,starting_position,difference,7)
            elif difference<0:return lines(piece,starting_position,difference,-7)    
    return 0

def lines(piece, starting_position, difference,dirr):#βρισκει αν υπάρχουν πιόνια σε γραμμές για μετακίνηση
                                                                             #αξιωματικών, πύργων και βασιλισσών
    wlist,blist=pieceplaces()
    for i in range(dirr,difference,dirr):
        if starting_position+i in blist or starting_position+i in wlist:return 0#αν βρει κομμάτι σε κάποια ενδιάμεση θέση
    if starting_position+difference in blist and piece.color[0]=='b':return 0#αν βρει κομμάτι του ίδιου χρώματος στην τελική θέση
    if starting_position+difference in wlist and piece.color[0]=='w':return 0    
    return 1

def pieceplaces():
    global chessboard
    wlist=[]
    blist=[]
    for i in range(8):#προσθέτει στις λίστες τις θέσεις που βρίσκονται τα κομμάτια
        for j in range(8):
            if chessboard.position[i][j]!=None:
                if chessboard.position[i][j].color[0]=='w': wlist.append(8*i+j)
                if chessboard.position[i][j].color[0]=='b': blist.append(8*i+j)
    return wlist,blist

def random_pos():
    return randint(0,7),randint(0,7)

def bcurses(selected_piece):#επιλέγει κατάρα μετά από συνάντηση αξιωματικών
    rd=1#randint(1,7)
    curselist=["The meeting of the two bishops makes pawns on their starting position","The meeting of the two bishops curses some pawns which disappear",  "The meeting of the two bishops changes the knights and bishops",
             "The meeting of the two bishops curses the queens which turn into rooks", "The meeting of the two bishops makes two pawns appear somewhere on the board","The meeting of the two bishops curses the queens who turn into anti-queens. They move in the range of two tiles where a normal queen can't move on an empty board.",
              "The meeting of the two bishops curses the pieces which turn into checkers pieces. They move the same as befoe"]
    tkm.showinfo("Cursed",curselist[rd-1])
    curses(selected_piece,rd)
    
def curses(selected_piece,rd):
    global chessboard
    if rd==1:
        for i in range (8):
            if chessboard.position[1][i]== None: chessboard.add_in_position('bpawn',i,1)
            if chessboard.position[6][i]==None:chessboard.add_in_position('wpawn',i,6)
    if rd==2:
        for i in range (8):
            for j in range(8):
                if chessboard.position[i][j]!=None:
                    rd9=randint(1,9)
                    if chessboard.position[i][j].name[0]=='p' and rd9>5:
                        chessboard.position[i][j].captured()
                        chessboard.position[i][j]=None
    if rd==3:
        chessboard.change_pieces(['bishop','night'],['night','bishop'])        

    if rd==4:
        chessboard.change_pieces(['queen'],['rook'])

    if rd==5:
        while True:
            rd8_1,rd8_2=random_pos()
            if rd8_1>0 and rd8_1<7 and chessboard.position[rd8_1][rd8_2]==None:
                chessboard.add_in_position('wpawn',rd8_2,rd8_1)
                break
        while True:
            rd8_1,rd8_2=random_pos()
            if rd8_1>0 and rd8_1<7 and chessboard.position[rd8_1][rd8_2]==None:
                chessboard.add_in_position('bpawn',rd8_2,rd8_1)
                break
    if rd==6:
        chessboard.change_pieces(['queen'],['night'],'antiqueen')
        
    if rd==7:
        Piece.checkers=1
        for i in range(8):
            for j in range(8):
                if chessboard.position[i][j]!=None:chessboard.position[i][j].image=pg.image.load(chessboard.position[i][j].color[0]+'checkers.png')
        selected_piece.image=pg.image.load(selected_piece.color[0]+'checkers.png')

if __name__ == '__main__':
    PongApp().run()
