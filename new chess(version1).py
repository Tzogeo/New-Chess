import pygame as pg
import tkinter.messagebox as tkm
from sys import exit
from random import randint,shuffle
#αρχικό φόντο

pg.init()
screen = pg.display.set_mode((720, 720))
pg.display.set_caption("Chess Game")
board_image = pg.image.load("board.png")
screen.blit(board_image, (0, 0))
pg.display.flip()
player=0
movement=0
agk=0
book=0
grass=0
piece_images = {#περιέχει τις εικόνες των κομματιών
    'bniqueen':pg.transform.rotate(pg.image.load("bqueen.png"),180),
    'wniqueen':pg.transform.rotate(pg.image.load("wqueen.png"),180),
}
lexlist=['wpawn','wrook','wnight','wbishop','wking', 'wqueen','bpawn','brook','bnight','bbishop','bking','bqueen','rpawn']
for item in lexlist:piece_images[item]= pg.image.load(item+".png")
position = [#περιέχει τις θέσεις των κομματιών
    ['brook', 'bnight', 'bbishop', 'bqueen', 'bking', 'bbishop','bnight','brook'],         # 00,01,02,03,04,05,06,07
    ['bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn', 'bpawn'],        # 08,09,10,11,12,13,14,15
    [None, None, None, None, None, None, None, None],                                         # 16,17,18,19,20,21,22,23
    [None, None, None, None, None, None, None, None],                                         # 24,25,26,27,28,29,30,31
    [None, None, None, None, None, None, None, None],                                         # 32,33,34,35,36,37,38,39
    [None, None, None, None, None, None, None, None],                                         # 40,41,42,43,44,45,46,47
    ['wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn', 'wpawn'],    # 48,49,50,51,52,53,54,55
    ['wrook', 'wnight', 'wbishop', 'wqueen', 'wking', 'wbishop', 'wnight', 'wrook']     # 56,57,58,59,60,61,62,63
]
moves=[]
columnletters=['a','b','c','d','e','f','g','h']
kc=[1,1]
selected_piece = None
selected_piece_position = None

def draw_pieces(screen, piece_images, position):#σχεδιάζει τα κομμάτια
    for row in range(8):
        for col in range(8):
            piece = position[row][col]
            if piece is not None:
                x = col * 90
                y = row * 90
                screen.blit(piece_images[piece], (x, y))
    
def curses(rd):#πραγματοποιεί τις κατάρες
    global position, piece_images,selected_piece,agk
    if rd==1:#βάζει πιόνια στις αρχικές θέσεις
        for i in range (8):
            if position[1][i]== None: position[1][i]='bpawn'
            if position[6][i]==None: position[6][i]='wpawn'
    elif rd==2:#εξαφανίζει κάποια πιόνια
        for i in range (8):
            for j in range(8):
                if position[i][j]!=None:
                    rd9=randint(1,9)
                    if position[i][j][1]=='p' and rd9>5:position[i][j]=None
    elif rd==3:#αλλάζει θέση σε ίππους και αξιωματικούς
        for i in range(8):
            for j in range(8):
                if position[i][j]!=None:
                    if position[i][j][1]=='b': position[i][j]=position[i][j][0]+'night'
                    elif position[i][j][1:3]=='ni': position[i][j]=position[i][j][0]+'bishop'
        selected_piece=selected_piece[0]+'night'
    elif rd==4:#υποβαθμίζει τις βασίλισσες σε πύργους
        for i in range(8):
            for j in range(8):
                if position[i][j]!=None:
                    if position[i][j][1]=='q': position[i][j]=position[i][j][0]+'rook'
    elif rd==5:#εμφανίζει τυχαία δύο πιόνια όχι στις ακριανές γραμμές
        while True:
            rd8_1,rd8_2=random_pos()
            if rd8_1>0 and rd8_1<7 and position[rd8_1][rd8_2]==None:
                position[rd8_1][rd8_2]='wpawn'
                break
        while True:
            rd8_1,rd8_2=random_pos()
            if rd8_1>0 and rd8_1<7 and position[rd8_1][rd8_2]==None:
                position[rd8_1][rd8_2]='bpawn'
                break
    elif rd==6:#αλλάζει τις βασίλισσες σε άντιβασίλισσες
        for i in range(8):
            for j in range(8):
                if position[i][j]!=None:
                    if position[i][j][1]=='q': position[i][j]=position[i][j][0]+'niqueen'
    elif rd==7:#κάνει τα πιόνια πούλια ντάμας
        for key in piece_images:
            if key[0]=='b':piece_images[key]=pg.image.load("bcheckers.png")
            if key[0]=='w':piece_images[key]=pg.image.load("wcheckers.png")
    elif rd==8:#κάνει τα πιόνια αγακθωτά
        agk=1

def bcurses():#επιλέγει κατάρα μετά από συνάντηση αξιωματικών
    rd=randint(1,8)
    curselist=["The meeting of the two bishops makes pawns on their starting position","The meeting of the two bishops curses some pawns who disappear",  "The meeting of the two bishops changes the knights and bishops",
             "The meeting of the two bishops curses the queens who turn into rooks", "The meeting of the two bishops makes two pawns appear somewhere on the board","The meeting of the two bishops curses the queens who turn into anti-queens. They move in the range of two tiles where a normal queen can't move on an empty board.",
              "The meeting of the two bishops curses the pieces who turn into checkers pieces. They move the same as before","The meeting of the two bishops curses the knights who now can't capture pawns"]
    tkm.showinfo("Cursed",curselist[rd-1])
    curses(rd)

def random_pos():
    rd1=randint(0,7)
    rd2=randint(0,7)
    return rd1, rd2
        
def legal(piece, starting_position, ending_position):# ελέγχει την νομιμότητα της κίνησης
    global blist,wlist, player, position,multi_chess, agk,sk
    difference=ending_position-starting_position
    wlist=[]
    blist=[]
    erow=(ending_position)//8#βρίσκει την αρχική θέση
    ecol=(ending_position)%8
    colors=['w','b']
    for i in range(8):#προσθέτει στις λίστες τις θέσεις που βρίσκονται τα κομμάτια
        for j in range(8):
            if position[i][j]!=None:
                if position[i][j][0]=='w': wlist.append(8*i+j)
                if position[i][j][0]=='b': blist.append(8*i+j)
    if ending_position in wlist or ending_position in blist:
        if (piece[-1]!='m' and position[erow][ecol][-1]=='m') or (piece[-1]=='m' and position[erow][ecol][-1]!='m'):
            return 0
            
    #white pawns
    if piece[:5]=="wpawn" and (ending_position not in wlist) and (ending_position not in blist):
        if difference==-8:return 1
        if difference==-16 and not sk and ending_position//8==4 and (ending_position+8 not in wlist) and (ending_position+8 not in blist): return 1
    if piece[:5]=="wpawn" and ending_position in blist and difference==-7 and (starting_position%8)!=7:return 1
    if piece[:5]=="wpawn" and ending_position in blist and difference==-9 and (starting_position%8)!=0:return 1

    #black pawns
    if piece[:5]=="bpawn" and (ending_position not in wlist) and (ending_position not in blist):
        if difference==8:return 1
        if difference==16 and not sk and ending_position//8==3 and (ending_position-8 not in wlist) and (ending_position-8 not in blist):return 1
    if piece[:5]=="bpawn" and ending_position in wlist and difference==7 and (starting_position%8)!=0:return 1
    if piece[:5]=="bpawn" and ending_position in wlist and difference==9 and (starting_position%8)!=7:return 1

    #kings
    kingcheck=[-9,-8,-7,-1,1,7,8,9]
    for n in kingcheck:
        if piece[:5]=='bking' and difference==int(n) and ending_position not in blist: return 1
        if piece[:5]=='wking' and difference==int(n) and ending_position not in wlist: return 1
    if (piece[:5]=='wking' and starting_position==60 and (ending_position==62 or ending_position==58)) or(piece=='bking' and starting_position==4 and (ending_position==2 or ending_position==6)):
        tkm.showinfo("Are you afraid and trying to hide your king;"," There is a battle. You can't run away. Your king has to command the others.")
        return 0

    #knights, knooks and anti-queens
    if (piece[:2]=='wn' and ending_position not in wlist) or (piece[:2]=='bn' and ending_position not in blist):
        if (piece[:2]=='wn' and position[erow][ecol]=='bpawn' and agk==1) or (piece[:2]=='bn' and position[erow][ecol]=='wpawn' and agk==1): return 0
        if difference==-17 and starting_position//8>=2 and starting_position%8>0: return 1
        if difference==17 and starting_position//8<=5 and starting_position%8<7: return 1
        if difference==-15 and starting_position//8>=2 and starting_position%8<7: return 1
        if difference==15 and starting_position//8<=5 and starting_position%8>0: return 1
        if difference==-10 and starting_position//8>=1 and starting_position%8>1: return 1
        if difference==10 and starting_position//8<=6 and starting_position%8<6: return 1
        if difference==-6 and starting_position//8>=1 and starting_position%8<6: return 1
        if difference==6 and starting_position//8<=6 and starting_position%8>1: return 1
        
    #rooks,nooks and queens
    if piece[4]=='k' or piece[1]=='q':
        if ending_position//8==starting_position//8:
            if (difference*difference)>16 and sk==1:return 0
            if difference>0:return lines(piece,starting_position,difference,1)
            elif difference<0:return lines(piece,starting_position,difference,-1)        
        if ending_position%8==starting_position%8:
            if (difference*difference)>(32*32) and sk==1:return 0
            if difference>0:return lines(piece,starting_position,difference,8)
            elif difference<0:return lines(piece,starting_position,difference,-8)    

    #bishops and queens
    if (piece[1]=='b' or piece[1]=='q') and starting_position%8!=(starting_position+difference)%8 and starting_position//8!=(starting_position+difference)//8:
        if sk==0:
            ltrb=[-9,+9,-18,+18,-27,+27,-36,+36,-45,+45,-54,+54,-63,+63]
            lbrt=[-7,+7,-14,+14,-21,+21,-28,+28,-35,+35,-42,+42,-48,+48]
        else:
            ltrb=[-9,+9,-18,+18,-27,+27,-36,+36]
            lbrt=[-7,+7,-14,+14,-21,+21,-28,+28]            
        if difference in ltrb :
            if difference>0:return lines(piece,starting_position,difference,9)
            elif difference<0:return lines(piece,starting_position,difference,-9)        
        if difference in lbrt:
            if difference>0 :return lines(piece,starting_position,difference,7)
            elif difference<0:return lines(piece,starting_position,difference,-7)    
    return 0
    
def enpassant (piece, row,column):#ελέγχει αν υπάρχει αν πασάν
    global position, moves, columnletters, player
    if position[row][column]=='wpawn':
        ep=0
        try:
            if position[row][column-1]=='bpawn':
                position[row][column-1]=None
                ep+=1
            if position[row][column+1]=='bpawn':
                position[row][column+1]=None
                ep+=1
        except:pass
        if ep==1:
            position[row][column]=None
            position[row+1][column]='bpawn'
            player=(player+1)%2
            moves.append('p'+columnletters[column]+'3')
            ep=0
            tkm.showinfo("En Passant","Congratulations En Passant just happened.(automatically because it is a forced move)")
        if ep==2:
            tkm.showinfo("Double En Passant","That is a miracle. It is so miraculous that changed the pawn into a bishop")
            position[row+1][column]='bbishop'
            position[row][column]=None
            player=(player+1)%2
            moves.append('b'+columnletters[column]+'3')
    if position[row][column]=='bpawn':
        ep=0
        try:
            if position[row][column-1]=='wpawn':
                position[row][column-1]=None
                ep+=1
            if position[row][column+1]=='wpawn':
                position[row][column+1]=None
                ep+=1
        except:pass
        if ep==1:
            position[row][column]=None
            position[row-1][column]='wpawn'
            player=(player+1)%2
            moves.append('p'+columnletters[column]+'6')
            ep=0
            tkm.showinfo("En Passant","Congratulations En Passant just happened.(automatically because it is a forced move)")
        if ep==2:
            tkm.showinfo("Double En Passant","That is a miracle. It is so miraculous that changed the pawn into a bishop")
            position[row-1][column]='wbishop'
            moves.append('b'+columnletters[column]+'6')
            position[row][column]=None
            player=(player+1)%2
       
def lines(piece, starting_position, difference,dirr):#βρισκει αν υπάρχουν πιόνια σε γραμμές για μετακίνηση
                                                                             #αξιωματικών, πύργων και βασιλισσών
    global blist,wlist, position,sk
    for i in range(dirr,difference,dirr):
        if starting_position+i in blist or starting_position+i in wlist:return 0#αν βρει κομμάτι σε κάποια ενδιάμεση θέση
    if starting_position+difference in blist and piece[0]=='b':return 0#αν βρει κομμάτι του ίδιου χρώματος στην τελική θέση
    if starting_position+difference in wlist and piece[0]=='w':return 0    
    return 1

running = True
bcol=0
brow=0
mrow=0
mcol=0
sk=0
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:#αν πατιέται ένα κομμάτι
            if event.button == 1:  
                x, y = event.pos
                col = x // 90
                row = y // 90
                selected_piece = position[row][col]
                if selected_piece is not None:
                    if (selected_piece[0]=="w" and player==0) or (selected_piece[0]=="b" and player==1):
                        selected_piece_position = (row, col)
                        movement=1
                        position[row][col] = None
        elif event.type == pg.MOUSEBUTTONUP:#αν αφεθεί ένα κομμάτι
            if event.button == 1 and selected_piece is not None :
                x, y = event.pos 
                ocol=col
                orow=row
                col = x // 90
                row = y // 90
                if legal(selected_piece,8*orow+ocol,8*row+col) and movement:#αν η κίνηση ειναι νόμιμη και ειναι σειρά του παίχτη
                    moves.append(selected_piece[1]+columnletters[col]+str(8-row))#προστίθεταιη κίνηση στην λίστα
                    if position[row][col]!=None:# αν υπάρχει κάπιοο κομμάτι στην τελική θέση
                        if selected_piece[1]=='b' and position[row][col][1]=='b':bcurses()
                        if position[row][col][1]=='k':#ελέγχει αν φαγώθηκε ο βασιλιάς
                            tkm.showinfo("You lost", "They captured your king")
                            pg.quit()
                            exit()
                    promotions=['queen','rook','bishop','night']#αν κάποιο πιονάκι φτάσει στην τελευταία σειρά
                    shuffle(promotions)
                    if selected_piece[:2]=='wp' and row==0 :
                        tkm.showinfo("Don't you fill lucky?","The promotion is random")
                        selected_piece='w'+promotions[1]
                    if selected_piece[:2]=="bp" and row==7:
                        tkm.showinfo("Don't you fill lucky?","The promotion is random")
                        selected_piece='b'+promotions[2]
                    position[row][col]=selected_piece
                    if selected_piece[1]=='p':#ελέγχει για αν-πασάν
                        if abs(orow-row)==2: enpassant(selected_piece,row,col)
                    selected_piece = None
                    selected_piece_position = None
                    player=(player+1)%2
                    movement=0
                    if moves[-1]=='nc4':
                        tkm.showinfo("C4 is explosive!", "This tile is very explosive and your ex-knight-looking piece hit it")
                        position[4][2]=None
                    if position[mrow][mcol]!=None:
                        if position[mrow][mcol][1]=='n' and grass==1:
                            tkm.showinfo("The knight just ate the grass","You didn't teach it to not eat everything. Now it thinks it belongs to the other team")
                            if position[mrow][mcol][0]=='w':position[mrow][mcol]='b'+position[mrow][mcol][1:]
                            else:position[mrow][mcol]='w'+position[mrow][mcol][1:]
                            grass=0
                    if position[brow][bcol]=="bpawn" or position[brow][bcol]=="wpawn":
                        tkm.showinfo("Why did you let the pawns read Marx?","Now they don't like the class differences. They killed every oppressor and destroyed their symbols.  You both lost")
                        for i in range (8):
                            for j in range(8):
                                if position[i][j]!=None:
                                    if position[i][j][1:]!="pawn":position[i][j]=None
                                    else: position[i][j]="rpawn"
                    #checks for interesting openings
                    if moves[0]=='pc4' and len(moves)==1:
                        tkm.showinfo("English?", "You remember that the English no longer have a queen, right?")
                        position[7][3]=None
                    if moves[0]=='pd4':
                        position[6][3]='wpawn'
                        position[6][4]=None
                        position[4][3]=None
                        position[4][4]='wpawn'
                        moves[0]='pe4'
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
                                position[2][0]='bbishop'
                            if moves[1]=='pd5':
                                sk=1
                                tkm.showinfo("Scandinavian??","That's very cold. Now the pawns and pieces can only move about half the distance before needing to warm themselves.")
                        if len(moves)==5:
                            if (moves[2][0]=='q') or (moves[4][0]=='q'):
                                tkm.showinfo("Congratulations","Your queen is very brave to come out this early. She is so brave she came out as a transgender")
                                piece_images['wqueen']=pg.image.load("wking.png")
                                tkm.showinfo("Change","The new gender doesn't change his moves. But the bishops are transphobic so they quit")
                                position[7][2]=None
                                position[7][5]=None        
                            if moves[1:5]==['pe5','nf3','nc6','bc4']:
                                tkm.showinfo("Italian??"," Your king and queen will change their style. It won't affect your game but it will remind everyone your wrong choices")
                                piece_images['wqueen']=pg.image.load("Iqueen.png")
                                piece_images['wking']=pg.image.load("Iking.png")
                        if len(moves)==6:
                            if ('nf3' in moves and 'nf6' in moves and 'nc3' in moves and 'nc6' in moves):
                                tkm.showinfo("4 knights??", "You like the knight huh? Take some more!")
                                position[0][2],position[0][5]='bnight','bnight'
                                position[7][2],position[7][5]='wnight','wnight'
                    if len(moves)==100:
                        tkm.showinfo("You can't finish this game?","Try rock-paper-scissors to find the winner")
                        pg.quit()
                        exit()
                    rd100=randint(1,150)
                    if (rd100>=148 and book==0):
                        book=1
                        bookimage= pg.image.load("book.png")
                        brow,bcol= random_pos()
                    if (rd100//17==2) and grass==0:
                        grass=1
                        mushrooms = pg.image.load("mushrooms.png")
                        mrow, mcol= random_pos()
                else:
                    position[orow][ocol] = selected_piece
                    selected_piece = None
                    selected_piece_position = None
                    movement=0

    screen.blit(board_image, (0, 0))
    draw_pieces(screen, piece_images, position)
    if grass==1:screen.blit(mushrooms, (90*mcol+20, 90*mrow+20))
    if book==1:screen.blit(bookimage,(90*bcol+20, 90*brow+20))
    if selected_piece is not None:
        x, y = pg.mouse.get_pos()
        screen.blit(piece_images[selected_piece], (x - 45, y - 45))
    pg.display.flip()

pg.quit()
 
