"""
This class is responsible for storing all the information about the current state of a chess game.It will also be
responsible for determining the valid moves at the current state.It will also keep a move Log.
"""

from sys import getallocatedblocks
import numpy as np

class GameState():
    def __init__(self):
        self.resetTable()
        self.rookDirections = ((-1,0),(0,-1),(1,0),(0,1))
        self.knightDirections=((-2,1),(-2,-1),(-1,-2),(-1,2),(1,2),(1,-2),(2,1),(2,-1))
        self.bishopDirections=((1,1),(1,-1),(-1,-1),(-1,1))
        self.kingDirections=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))

        self.moveFunctions={"P":self.get_pawn_moves,"R":self.get_rook_moves,"B":self.get_bishop_moves,
                            "N":self.get_knight_moves,"K":self.get_king_moves,"Q":self.get_queen_moves}

    def resetTable(self):
        self.board=np.array([
        ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        ["bP","bP","bP","bP","bP","bP","bP","bP"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["wP","wP","wP","wP","wP","wP","wP","wP"],
        ["wR","wN","wB","wQ","wK","wB","wN","wR"]])
        self.whiteToMove=True
        self.movelog=[]
        self.wb_movelog={}
        self.undo_movelog = []
        self.white_captured=[]
        self.black_captured=[]

        #FOR CHECK-MATE OPERATIONS                    
        self.whiteKingLocation=(7,4)              
        self.blackKingLocation=(0,4)
        self.inCheck=False
        self.pins=[]
        self.checks=[]

    def rotate(self):
        self.board=np.rot90(self.board,2)
    
    def makemove(self,move):
        piece = move.piece_moved
        target_color = move.piece_moved_to[0]

        if target_color=="w":
            self.black_captured.append(move.piece_moved_to)

        elif target_color=="b":
            self.white_captured.append(move.piece_moved_to)

        
        if piece=="bK":
            self.blackKingLocation=(move.endRow,move.endColumn) 
        
        elif piece=="wK":
            self.whiteKingLocation=(move.endRow,move.endColumn) 
       
                               
        self.board[move.startRow][move.startColumn]="--"
        self.board[move.endRow][move.endColumn]=piece
        self.movelog.append(move)
        self.whiteToMove=not self.whiteToMove
        
        

                                 
    def undomove(self):
        if not self.movelog:
            print("No move to undo!")
            return
        
        move=self.movelog.pop()
        t_piece=move.piece_moved_to
        self.undo_movelog.append(move)
        
        if t_piece[0]=="b" and t_piece!="--":
            self.white_captured.pop()
        elif t_piece[0]=="w" and t_piece!="--":
            self.black_captured.pop()
        if move.piece_moved=="wK":
            self.whiteKingLocation=(move.startRow,move.startCol)
        elif move.piece_moved=="bK":
            self.blackKingLocation=(move.startRow,move.startCol)
        self.board[move.startRow][move.startColumn]=move.piece_moved
        self.board[move.endRow][move.endColumn]=move.piece_moved_to
        
        self.whiteToMove=not self.whiteToMove
        
            
    def resumemove(self):
        if not self.undo_movelog:
            print("No move ahead!")
            return
        
        move = self.undo_movelog.pop()
        self.makemove(move)
        

    def getValidMoves(self):

        return self.getAllPossibleMoves()
 
 
        moves=[]       
        #self.incheck,self.pins,self.checks=self.pins_checks()
        if self.whiteToMove:
            kingRow,kingCol=self.whiteKingLocation
        else:
            kingRow,kingCol=self.blackKingLocation
        #return self.getAllPossibleMoves()

        if self.inCheck:
            if len(self.checks)==1:
                moves=self.getAllPossibleMoves()
                check=self.checks[0]
                checkRow,checkCol=check
                pieceChecking=self.board[checkRow][checkCol]
                valid_squares=[]
                if pieceChecking[1]=="N":
                    valid_squares=[(checkRow,checkCol)]
        return self.getAllPossibleMoves()


    def pins_checks(self,move):
        """
        pins,checks,inCheck=[],[],False
        if self.whiteToMove:
            teamcolor,enemycolor="w","b"
            kingRow,kingCol=self.whiteKingLocation
        else:
            teamcolor,enemycolor="b","w"
            kingRow,kingCol=self.whiteKingLocation
        kingMoves=((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) #0 To 3 Crosswise 4 To 7 Diagonal(Goal is not to iterate over and over)
        for i in range(len(kingMoves)):
            d=kingMoves[i]
            possiblepins=[]
            for l in range(1,8):
                endRow,endCol=kingRow+d[0]*l,kingCol+d[1]*l
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endpiece=self.board[endRow][endCol]
                    if endpiece[0]==teamcolor:
                        possiblepins.append(endpiece)
                    elif endpiece[0]==enemycolor:
                        piece=endpiece[1]
                        conditions=(0<=i<=3 and piece=="R") or (4<=i<=7 and piece=="B")
                        if conditions:
                            pass
        """
        pins,checks,inCheck=[],[],False
        r,c = move.startRow,move.startColumn
        piece = self.board[r][c][1]
        
        enemyColor="b" if self.whiteToMove else "w"
        for d,l in self.rookDirections:
            for i in range(1,8):
                endRow=r+d*i
                endCol=c+l*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece=self.board[endRow][endCol]
        

    def getAllPossibleMoves(self):
        moves=[]
        for r in range(8):
            for c in range(8):
                color=self.board[r][c][0]
                if (color=="w" and self.whiteToMove) or (color=="b" and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    
    def get_pawn_moves(self,r,c,moves):
        if self.whiteToMove:
            try:
                if self.board[r-1][c+1][0]=="b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                if self.board[r-1][c-1][0]=="b":
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            except IndexError:
                None
            if self.board[r-1][c]=="--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))

        else: #For black pawn moves
            try:
                if self.board[r+1][c+1][0]=="w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                if self.board[r+1][c-1][0]=="w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            except IndexError:
                None
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))


    def get_rook_moves(self,r,c,moves):
        enemyColor="b" if self.whiteToMove else "w"
        for d,l in self.rookDirections:
            for i in range(1,8):
                endRow=r+d*i
                endCol=c+l*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: break
                else:break


    def get_knight_moves(self,r,c,moves):
        teamColor="w" if self.whiteToMove else "b"
        for d,l in self.knightDirections:
            endRow=r+d
            endCol=c+l
            if 0<=endRow<=7 and 0<=endCol<=7:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=teamColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


    def get_bishop_moves(self,r,c,moves):
        enemyColor="b" if self.whiteToMove else "w"
        for d,l in self.bishopDirections:
            for i in range(1,8):
                endRow=r+d*i
                endCol=c+l*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: break
                else: break


    def get_queen_moves(self,r,c,moves):
        self.get_bishop_moves(r,c,moves)
        self.get_rook_moves(r,c,moves)


    def get_king_moves(self,r,c,moves):
        teamColor="w" if self.whiteToMove else "b"
        for d,l in self.kingDirections:
            endRow=r+d
            endCol=c+l
            if 0<=endRow<=7 and 0<=endCol<=7:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=teamColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
                
    def pawn_promotion(self,r,c):
        pass


class Move():
    
    ranks_to_rows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rows_to_ranks={v: k for k, v in ranks_to_rows.items()}
    letter_to_colmn={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colmn_to_letter={v: k for k,v in letter_to_colmn.items()}
    
    def __init__(self,start,end,board):
        self.startRow=start[0]
        self.startColumn=start[1]
        self.endRow=end[0]
        self.endColumn=end[1]
        self.piece_moved=board[self.startRow][self.startColumn]
        self.piece_moved_to=board[self.endRow][self.endColumn]
        self.pieces={"P":"Pawn","R":"Rook","N":"Knight","B":"Bishop","Q":"Queen","K":"King"}
  
    def get_chess_notation(self):
        return self.get_rank_letter(self.startRow,self.startColumn)+" to "+self.get_rank_letter(self.endRow,self.endColumn)
    """
    def get_chess_notation_pieces(self):
        return f"{self.pieces[self.piece_moved[1]]} to {self.get_rank_letter(self.endRow,self.endColumn)}"
    """
    def get_rank_letter(self,r,c):
        return self.colmn_to_letter[c]+ self.rows_to_ranks[r]

    def __str__(self):
        return f"{self.pieces[self.piece_moved[1]]} to {self.get_rank_letter(self.endRow,self.endColumn)}"
        
    def __eq__(self,other):
        return (self.startRow,self.startColumn,self.endRow,self.endColumn)==(other.startRow,other.startColumn,other.endRow,other.endColumn)