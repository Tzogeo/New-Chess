import pygame as pg
from sys import exit
import tkinter.messagebox as tkm
from random import randint,shuffle

class Piece():#the objects of the class are the pieces on the board
    Piecelex={'wpawn':0,'wnight':0,'wbishop':0,'wrook':0,'wqueen':0,'wking':0,'bpawn':0,'bnight':0,'bbishop':0,'brook':0,'bqueen':0,'bking':0,'rpawn':0}
    checkers=0
    def __init__(self, color, name, xposition, yposition,number,legalmovements,specialmoves=None):
        self.color = color
        self.name = name
        self.xposition = xposition
        self.yposition = yposition
        self.number=number
        chessboard.add_piece(self)
        self.image=pg.image.load(self.color[0]+self.name+".png")
        self.legalmovements=legalmovements
        self.Piecelex[self.color[0]+self.name]+=1
        self.specialmoves=specialmoves
        self.initial_special()
    def numbers(self,piecename):
        return self.Piecelex[piecename]
    def initial_special(self):#some pieces have special moves/images
        if self.specialmoves=='antiqueen':
            self.image=pg.transform.rotate(pg.image.load(self.color[0]+'queen.png'),180)
        if self.checkers==1:
            self.image=pg.image.load(self.color[0]+'checkers.png')

    def captured(self):#changes the board once a piece is captured
        #chessboard.print_board()
        cp=self
        for i in range(self.number,Piece.Piecelex[cp.color[0]+cp.name],1):
            newp=globals()[f'{self.color[0]+self.name}{i+1}']
            cp.xposition,cp.yposition=newp.xposition,newp.yposition
            chessboard.position[cp.yposition][cp.xposition]=cp
            cp=newp
        Piece.Piecelex[self.color[0]+self.name]-=1
        return 0
            

class Chessboard():#contains the chessboard and organises the movement/captures
    def __init__(self):
        self.position = [[None for _ in range(8)] for _ in range(8)]

    def add_piece(self, piece):
        self.position[piece.yposition][piece.xposition] = piece

    def print_board(self):#prints the board (for testing reasons)
        for row in self.position:
                for item in row:
                    if item==None:print("None")
                    else: print(item.name)
                    
    def add_in_position(self,name,xposition,yposition,specialmoves=None):# adds a piece into the board
        movementslex={'wpawn':[0],'bpawn':[1],'king':[2],'night':[3],'rook':[4],'bishop':[5],'queen':[4,5],'nook':[3,4],'rpawn':[]}
        number=wking1.numbers(name)+1
        if name[1]=='p':globals()[f'{name}{number}']=Piece(name[0],name[1:],xposition,yposition,number,movementslex[name])
        else:globals()[f'{name}{number}']=Piece(name[0],name[1:],xposition,yposition,number,movementslex[name[1:]],specialmoves)
        self.position[yposition][xposition] = globals()[f'{name}{number}']
        
    def change_pieces(self,oldlist,newlist,specialmoves=None):#changes a type of pieces into anoother
        for i in range(8):
            for j in range(8):
                if self.position[i][j]!=None:
                    c=self.position[i][j].color[0]
                    for k in range(len(oldlist)):
                        if self.position[i][j].name==oldlist[k]:
                            self.position[i][j].captured()
                            self.add_in_position(c+newlist[k],j,i,specialmoves)
                            break

                            
def draw_pieces(screen):#shows the pieces
    for row in range(8):
        for col in range(8):
            piece = chessboard.position[row][col]
            if piece is not None:
                x = col * 90
                y = row * 90
                screen.blit(piece.image, (x, y))
def random_pos():
    return randint(0,7),randint(0,7)
def pieceplaces():#adds the positions of the pieces into two list to check the legality of the moves
    wlist=[]
    blist=[]
    for i in range(8):#προσθέτει στις λίστες τις θέσεις που βρίσκονται τα κομμάτια
        for j in range(8):
            if chessboard.position[i][j]!=None:
                if chessboard.position[i][j].color[0]=='w': wlist.append(8*i+j)
                if chessboard.position[i][j].color[0]=='b': blist.append(8*i+j)
    return wlist,blist

def legal(piece,starting_position, ending_position):# checks the legality of a move
    global player,sk
    difference=ending_position-starting_position
    wlist,blist=pieceplaces()
    erow=(ending_position)//8#finds the initial position
    ecol=(ending_position)%8
    colors=['w','b']
    letter={'w':wlist,'b':blist}

    #white pawns
    if 0 in piece.legalmovements and (ending_position not in wlist) and (ending_position not in blist):
        if difference==-8:return 1
        if difference==-16 and not sk and ending_position//8==4 and (ending_position+8 not in wlist) and (ending_position+8 not in blist): return 1
    if 0 in piece.legalmovements and ending_position in blist and difference==-7 and (starting_position%8)!=7:return 1
    if 0 in piece.legalmovements and ending_position in blist and difference==-9 and (starting_position%8)!=0:return 1

    #black pawns
    if 1 in piece.legalmovements and (ending_position not in wlist) and (ending_position not in blist):
        if difference==8:return 1
        if difference==16 and not sk and ending_position//8==3 and (ending_position-8 not in wlist) and (ending_position-8 not in blist):return 1
    if 1 in piece.legalmovements and ending_position in wlist and difference==7 and (starting_position%8)!=0:return 1
    if 1 in piece.legalmovements and ending_position in wlist and difference==9 and (starting_position%8)!=7:return 1

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

def lines(piece, starting_position, difference,dirr):#checks the line that a piece moves
    for i in range(dirr,difference,dirr):
        if starting_position+i in blist or starting_position+i in wlist:return 0#checks the intermediate squares
    if starting_position+difference in blist and piece.color[0]=='b':return 0#checks the destination for pieces of the same color
    if starting_position+difference in wlist and piece.color[0]=='w':return 0    
    return 1

def bcurses(selected_piece):#curses in case a bishop captures another
    rd=randint(1,7)
    curselist=["The meeting of the two bishops makes pawns on their starting position","The meeting of the two bishops curses some pawns which disappear",  "The meeting of the two bishops changes the knights and bishops",
             "The meeting of the two bishops curses the queens which turn into rooks", "The meeting of the two bishops makes two pawns appear somewhere on the board","The meeting of the two bishops curses the queens who turn into anti-queens. They move in the range of two tiles where a normal queen can't move on an empty board.",
              "The meeting of the two bishops curses the pieces which turn into checkers pieces. They move the same as befoe"]
    tkm.showinfo("Cursed",curselist[rd-1])
    curses(selected_piece,rd)
    
def curses(selected_piece,rd):
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

def enpassant (piece, row,column):# checks for en-peassant
    global player, moves, columnletters
    antilex={'b':'w','w':'b'}
    vallex={'w':-1,'b':+1}
    ep=0
    try:
        if chessboard.position[row][column-1].color[0]==antilex[chessboard.position[row][column].color[0]] and chessboard.position[row][column-1].name=='pawn':
            chessboard.position[row][column-1].captured()
            chessboard.position[row][column-1]=None
            ep+=1
    except:pass
    try:
        if chessboard.position[row][column+1].color[0]==antilex[chessboard.position[row][column].color[0]] and chessboard.position[row][column+1].name=='pawn':
            chessboard.position[row][column+1].captured()
            chessboard.position[row][column+1]=None
            ep+=1
    except:pass
    capturercolor=antilex[chessboard.position[row][column].color[0]]
    if ep==1:
        chessboard.add_in_position(capturercolor+'pawn',column,row+vallex[capturercolor])
        print(row+vallex[capturercolor])
        chessboard.position[row][column].captured()
        chessboard.position[row][column]=None
        player=(player+1)%2
        moves.append('p'+columnletters[column]+str(int(-1.5*vallex[capturercolor]+4.5)))
        tkm.showinfo("En Passant","Congratulations En Passant just happened.(automatically because it is a forced move)")
        #chessboard.print_board()
        return chessboard.position[row+vallex[capturercolor]][column],1
    if ep==2:
        tkm.showinfo("Double En Passant","That is a miracle. It is so miraculous that changed the pawn into a bishop")
        chessboard.add_in_position(antilex[chessboard.position[row][column].color[0]]+'bishop',column,row+vallex[capturercolor])
        chessboard.position[row][column]=None
        player=(player+1)%2
        return chessboard.position[row+vallex[capturercolor]][column],1
    return selected_piece,0
    
            
chessboard = Chessboard()
collist=[['black','white'],[0,7]]
namelist=['rook1','night1','bishop1','queen1','king1','bishop2','night2','rook2']
movelist=[[4],[3],[5],[4,5],[2],[5],[3],[4]]
for j in range(8):
    globals()[f'wpawn{j+1}']=Piece("white", "pawn", j, 6,j+1,[0])
    globals()[f'bpawn{j+1}']=Piece("black", "pawn", j, 1,j+1,[1])
    for i in range(2):
        globals()[f'{collist[0][i][0]}{namelist[j]}']= Piece(collist[0][i], namelist[j][:-1], j, collist[1][i],int(namelist[j][-1]),movelist[j])

pg.init()
screen = pg.display.set_mode((720, 720))
pg.display.set_caption("Chess Game")
board_image = pg.image.load("board.png")
screen.blit(board_image, (0, 0))
pg.display.flip()
running=True
selected_piece=None
player=0
moves=[]
sk=0
grass,book=0,0
columnletters=['a','b','c','d','e','f','g','h']
mrow,mcol,brow,bcol=0,0,0,0
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:#if the mousebutton is being pussed
            if event.button == 1:  
                x, y = event.pos
                col = x // 90
                row = y // 90
                selected_piece = chessboard.position[row][col]
                if selected_piece is not None:
                    if (selected_piece.color[0]=="w" and player==0) or (selected_piece.color[0]=="b" and player==1):
                        selected_piece_position = (row, col)
                        movement=1
                        chessboard.position[row][col] = None
        elif event.type == pg.MOUSEBUTTONUP:#if the mousebutton goes up
            if event.button == 1 and selected_piece is not None :
                x, y = event.pos
                ocol=col
                orow=row
                col = x // 90
                row = y // 90
                enpas=0
                if legal(selected_piece,8*orow+ocol,8*row+col) and movement:#if the movement is legal
                    moves.append(selected_piece.name[0]+columnletters[col]+str(8-row))#adds the move to the list
                    if chessboard.position[row][col]!=None:# if there is a piece captured
                        chessboard.position[row][col].captured()
                        if selected_piece.name[0]=='b' and chessboard.position[row][col].name[0]=='b':bcurses(selected_piece)
                        if chessboard.position[row][col].name=='king':#checks for the capture of the king
                            tkm.showinfo("You lost", "They captured your king")
                            pg.quit()
                            exit()
                    promotions=['queen','rook','bishop','night']#if a pawn reaches the promotion row
                    shuffle(promotions)
                    if (selected_piece.color[0]+selected_piece.name[0]=='wp' and row==0) or (selected_piece.color[0]+selected_piece.name[0]=='bp' and row==7):
                        tkm.showinfo("Don't you fill lucky?","The promotion is random")
                        chessboard.add_in_position(selected_piece.color[0]+promotions[0],col,row);                   
                        selected_piece=chessboard.position[row][col]
                    chessboard.position[row][col]=selected_piece
                    if selected_piece.name=='pawn' and abs(orow-row)==2 :selected_piece,enpas=enpassant(selected_piece,row,col)
                    if not enpas:
                        selected_piece.yposition=row
                        selected_piece.xposition=col
                    player=(player+1)%2
                    movement=0
                    if moves[-1]=='nc4':
                        tkm.showinfo("C4 is explosive!", "This tile is very explosive and your ex-knight-looking piece hit it")
                        chessboard.position[4][2].captured()
                        chessboard.position[4][2]=None
                    if chessboard.position[mrow][mcol]!=None:
                        if chessboard.position[mrow][mcol].name[0]=='n' and grass==1:
                            tkm.showinfo("The knight just ate the grass","You didn't teach it to not eat everything. Now it thinks it belongs to the other team")
                            spec=chessboard.position[mrow][mcol].specialmoves
                            if chessboard.position[mrow][mcol].color[0]=='w':
                                chessboard.position[mrow][mcol].captured()
                                chessboard.add_in_position('bnight',col,row,spec)
                            else:
                                chessboard.position[mrow][mcol].captured()
                                chessboard.add_in_position('wnight',col,row,spec)
                            grass=0
                    if chessboard.position[brow][bcol]!=None:
                        if chessboard.position[brow][bcol].name=="pawn" :
                            tkm.showinfo("Why did you let the pawns read Marx?","Now they don't like the class differences. They killed every oppressor and destroyed their symbols.  You both lost")
                            for i in range (8):
                                for j in range(8):
                                    if chessboard.position[i][j]!=None:
                                        if chessboard.position[i][j].name!="pawn":
                                            chessboard.position[i][j].captured()
                                            chessboard.position[i][j]=None
                                        else: chessboard.add_in_position("rpawn",j,i)
                        #checks for interesting openings
                    if moves[0]=='pc4' and len(moves)==1:
                        tkm.showinfo("English?", "You remember that the English no longer have a queen, right?")
                        chessboard.position[7][3].captured()
                        chessboard.position[7][3]=None
                    if moves[0]=='pd4' and len(moves)==1:
                        wpawn4.yposition=6
                        wpawn5.yposition=4
                        chessboard.position[6][3]=wpawn4
                        chessboard.position[4][4]=wpawn5
                        chessboard.position[6][4]=None
                        chessboard.position[4][3]=None
                        tkm.showinfo("What is this?", '''If you want to be considered a human you won't play such things.
For now we will play something normal for you. But be careful! ''')
                    if moves[0]=='pe4':
                        if len(moves)==2:
                            if moves[1]=='pe6':
                                tkm.showinfo("French?","You know the French surrendered in WW2. You want to do the same? Fine. Black surrenders and white wins")
                                pg.quit()
                                exit()
                            if moves[1]=='pa6':
                                tkm.showinfo("Saint George's defence","The general-saint turns the pawn into a bishop")
                                chessboard.position[2][0].captured()
                                chessboard.add_in_position('bbishop',0,2)
                            if moves[1]=='pd5':
                                sk=1
                                tkm.showinfo("Scandinavian??","That's very cold. Now the pawns and pieces can only move about half the distance before needing to warm themselves.")                                
                        if len(moves)==5:
                            if (moves[2][0]=='q' or moves[4][0]=='q'):
                                tkm.showinfo("Congratulations","Your queen is very brave to come out this early. She is so brave she came out as a transgender")
                                wqueen1.image=pg.image.load('wking.png')
                                tkm.showinfo("Change","The new gender doesn't change his moves. But the bishops are transphobic so they quit")
                                wbishop1.captured()
                                wbishop1.captured()
                                chessboard.position[7][2]=None
                                chessboard.position[7][5]=None                                
                            if moves[1:5]==['pe5','nf3','nc6','bc4']:
                                tkm.showinfo("Italian??"," Your king and queen will change their style. It won't affect your game but it will remind everyone your wrong choices")
                                wqueen1.image=pg.image.load("Iqueen.png")
                                wking1.image=pg.image.load("Iking.png")
                        if len(moves)==6:
                            if ('nf3' in moves and 'nf6' in moves and 'nc3' in moves and 'nc6' in moves):
                                tkm.showinfo("4 knights??", "You like the knight huh? Take some more!")
                                chessboard.change_pieces(['bishop'],['night'])
                    if len(moves)==100:
                        tkm.showinfo("You can't finish this game?","Try rock-paper-scissors to find the winner")
                        pg.quit()
                        exit()
                    rd150=randint(1,150)
                    if (rd150>=148 and book==0):
                        book=1
                        bookimage= pg.image.load("book.png")
                        brow,bcol= random_pos()
                    if (rd150//7==2) and grass==0:
                        grass=1
                        mushrooms = pg.image.load("mushrooms.png")
                        mrow, mcol= random_pos()
                else: chessboard.position[orow][ocol]=selected_piece
                selected_piece = None
                selected_piece_position = None
                movement=0

    screen.blit(board_image,(0,0))
    draw_pieces(screen)
    if grass==1:screen.blit(mushrooms, (90*mcol+20, 90*mrow+20))
    if book==1:screen.blit(bookimage,(90*bcol+20, 90*brow+20))

    if selected_piece is not None:
        x, y = pg.mouse.get_pos()
        screen.blit(selected_piece.image, (x - 45, y - 45))
    pg.display.flip()
pg.quit()
