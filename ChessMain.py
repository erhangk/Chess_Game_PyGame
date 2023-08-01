"""
This is the main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine
import Shapes

WIDTH=HEIGHT=800
DIM=8 #DIMENSION
SQ_SIZE=HEIGHT//DIM
MAX_FPS=60

pieces=["wP","bP","wR","wK","wB","wQ","wK","wB",  #ALL THE PIECES ON THE BOARD
        "wN","wR","bR","bN","bB","bQ","bK","bB","bN","bR"]

IMAGES={}
rect_colors = ("gray","white")
draw = Shapes.draw(HEIGHT,DIM,rect_colors)

def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))

    gs=ChessEngine.GameState()
    valid_moves=gs.getValidMoves()
    moved=False #Flag Variable
    
    load_images() 
    running=True
    sq_selected=()
    playerclicks=[]
    
    while running:
        for i in p.event.get():

            if i.type==p.QUIT:
                running=False

            elif i.type==p.MOUSEBUTTONDOWN:
                mouse_pos=p.mouse.get_pos()
                row,column=(mouse_pos[1]//SQ_SIZE,mouse_pos[0]//SQ_SIZE)
                teamColor="w" if gs.whiteToMove else "b"
                
                if sq_selected!=(row,column):
                    sq_selected=row,column
                    if len(playerclicks)==1 and gs.board[row][column][0]==teamColor:
                        playerclicks[0]=sq_selected
                    else:
                        playerclicks.append(sq_selected)
                        
                """
                else:
                    sq_selected=()
                    playerclicks=[]
                """            
                if len(playerclicks)==2:  
                    startRow,startCol=playerclicks[0]
                    if gs.board[startRow][startCol][0]==teamColor:
                        move=ChessEngine.Move(playerclicks[0],playerclicks[1],gs.board)
                        if move in valid_moves:
                            gs.makemove(move) 
                            moved=True
                            print(move)

                    sq_selected=()
                    playerclicks=[]
                    
            elif i.type==p.KEYDOWN:#UNDO MOVE
                
                if i.key==p.K_q: #QUIT
                    running=False
                elif i.key==p.K_LEFT: #UNDOMOVE
                    gs.undomove()
                    moved=True
                elif i.key==p.K_RIGHT: #RESUME MOVE
                    gs.resumemove()
                    moved=True
                elif i.key==p.K_r:
                    resetTable(gs)
                    moved=True


        if moved:
            valid_moves=gs.getValidMoves()
            moved=False        
        
        Draw_Game_State(screen,gs,sq_selected,valid_moves)
        clock.tick(MAX_FPS)  
        
        x, y = get_square_under_mouse()
        highlight_mouse_pos(screen,x,y)

        p.display.flip()


def load_images():
    path = "images/Classic/"
    try:
        for piece in pieces:
            IMAGES[piece]=p.transform.scale(p.image.load(path+piece+".svg"),(SQ_SIZE ,SQ_SIZE))
    except FileNotFoundError:
        for piece in pieces:
            IMAGES[piece]=p.transform.scale(p.image.load(path+piece+".png"),(SQ_SIZE ,SQ_SIZE))
        
def get_square_under_mouse():
    mouse_pos=p.Vector2(p.mouse.get_pos())
    return (int(v // SQ_SIZE) for v in mouse_pos) #RETURNING X AND Y COORDINATES OF MOUSE

def highlight_mouse_pos(screen,x,y):
    draw.draw_rect(screen,x,y)
    
def highlight_current_square(screen,sq_selected,valid_moves):
    if not sq_selected:
        return
    r,c = sq_selected
    surface = p.Surface((SQ_SIZE,SQ_SIZE))
    surface.set_alpha(100)
    surface.fill(p.Color((121, 173, 253)))
    screen.blit(surface, (c*SQ_SIZE,r*SQ_SIZE))
    
    for move in valid_moves:
        if (move.startRow == r) and (move.startColumn == c):
            screen.blit(surface, (move.endColumn*SQ_SIZE,move.endRow*SQ_SIZE))
      
def Draw_Game_State(screen,gs,sq_selected,valid_moves):
    #ORDER OF DRAWING BOARD AND PIECES IS IMPORTANT
    DrawBoard(screen)
    highlight_current_square(screen,sq_selected,valid_moves)
    DrawPieces(screen,gs.board)

"""Draw the squares on 8x8 board"""
def DrawBoard(screen):
    colors=(p.Color("white"),p.Color("gray"))
    for r in range(DIM):
        for c in range(DIM):
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))            
            
"""Draw Piececs of the current state of board"""
def DrawPieces(screen,board):
    for r in range(DIM):
        for c in range(DIM):
            piece=board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def resetTable(gs):
    gs.resetTable()
    

"""Saves last state of the board at "last state of the board.txt file"""
def SaveBoardState(board):
    f=open("last state of the board.txt","a")
    f.write(str(board.board))
    f.write("\n|\n|__white to move\n\n" if board.whiteToMove else "\n|\n|__black to move\n\n")
    f.close()
    

if __name__=='__main__':
    main()