"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""


import pygame as p
import ChessEngine

WIDTH=HEIGHT=512
DIM=8 #DIMENSION
SQ_SIZE=HEIGHT//DIM
MAX_FPS=60

pieces=["wP","bP","wR","wK","wB","wQ","wK","wB",  #ALL THE PIECES ON THE BOARD
        "wN","wR","bR","bN","bB","bQ","bK","bB","bN","bR"]

IMAGES={}

def load_images():
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE ,SQ_SIZE))


def get_square_under_mouse(board):
    mouse_pos=p.Vector2(p.mouse.get_pos())
    return (int(v // SQ_SIZE) for v in mouse_pos) #RETURNING X AND Y COORDINATES OF MOUSE
    

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
                        selected_sq = (row * SQ_SIZE,column * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                        p.draw.rect(screen,"yellow" , selected_sq, 2)
                        playerclicks[0]=sq_selected
                        continue

                    playerclicks.append(sq_selected)
                
                else:
                    sq_selected=()
                    playerclicks=[]
                    
                if len(playerclicks)==2:  
                    startRow=playerclicks[0][0]
                    startCol=playerclicks[0][1]
                    if gs.board[startRow][startCol][0]==teamColor:
                        move=ChessEngine.Move(playerclicks[0],playerclicks[1],gs.board)
                        print(move.get_chess_notation_pieces())
                        if move in valid_moves:
                            gs.makemove(move) 
                            moved=True

                    sq_selected=()
                    playerclicks=[]
            elif i.type==p.KEYDOWN:#UNDO MOVE
                if i.key==p.K_LEFT:
                    gs.undomove()
                    moved=True
        if moved:
            valid_moves=gs.getValidMoves()
            moved=False
            

        Draw_Game_State(screen,gs)
        clock.tick(MAX_FPS)  

        x, y = get_square_under_mouse(gs.board)
        rect = (x * SQ_SIZE,y * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        colors=("gray","white")
        color=colors[(x+y)%2]
        p.draw.rect(screen,color , rect, 2)
        p.display.flip()
    
def Draw_Game_State(screen,gs):
    #ORDER OF DRAWING BOARD AND PIECES IS IMPORTANT
    DrawBoard(screen)
    DrawPieces(screen,gs.board)

"""Draw the squares on 8x8 board"""
def DrawBoard(screen):
    colors=(p.Color("white"),p.Color("gray"))
    for r in range(DIM):
        for c in range(DIM):
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            #draw_rect_alpha(screen, (255, 255, 0, 128), (c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            
            
"""Draw Piececs of the current state of board"""
def DrawPieces(screen,board):
    for r in range(DIM):
        for c in range(DIM):
            piece=board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


"""Saves last state of the board at "last state of the board.txt file"""
def SaveBoardState(board):
    f=open("last state of the board.txt","a")
    f.write(str(board.board))
    f.write("\n|\n|__white to move\n\n" if board.whiteToMove else "\n|\n|__black to move\n\n")
    f.close()


if __name__=='__main__':
    main()