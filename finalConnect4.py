import http.client

import time
import numpy as np
import  math
from timeit import default_timer as timer
CRED = '\33[31m'
CEND = '\033[0m'
CBLUE   = '\33[34m'
def remplirGrille(joueur, jeu):
    for i in range(grilleDim-1,-1,-1):
        if(grille[i][jeu]==0):
            grille[i][jeu]=joueur
            break
# Retourne la grille avec l'action appliquée
def returnGrille(joueur, board, action):
    for i in range(12-1,-1,-1):
        if(board[i][action]==0):
            board[i][action]=joueur
            return board,i,action
# Prend en paramètre un action et verifie si elle est gagnante ou non
def action_win(board,player,r,c) :
    countR = 0
    countC = 0
    countDP = 0
    countDN = 0
    for i in range(-3,4):
        if c-i >= 0 and c-i <= 11 :
            if board[r][c-i] == player : countR = countR + 1
            else :countR = 0
        if r-i>=6 and r-i <= 11 :
            if board[r-i][c] == player : countC = countC + 1
            else : countC = 0
        if c+i>= 0 and c+i <= 11 and r-i >= 6 and r-i <=11 :
            if board[r-i][c+i] == player : countDP = countDP + 1
            else : countDP = 0
        if c-i>=0 and c-i<= 11 and r-i >= 6 and r-i<=11:
            if board[r-i][c-i] == player : countDN = countDN + 1
            else : countDN = 0
        if countC >= 4 or countR >= 4  or countDN >= 4 or countDP >= 4:
            return True
    return False
 
 
 
def printGrille():
    for i in range(grilleDim):
        print("|",end=' ')
        for j in range(grilleDim):
            if(grille[i][j]==1):
                print(CBLUE+'X'+CEND,end=' ')
            elif grille[i][j]==2:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print("|",end=' ')
        print()
    print("|",end=' ')
    for i in range(grilleDim):
        print("_",end=" ")
        print("|",end=' ')
    print()
    print("|",end=' ')
    for i in range(grilleDim):
        print((1+i)%10,end=" ")
        print("|",end=' ')
    print()
# prend en paramètre un board et un jeton et calcule le score associé à ce jeton (les heuristiques)
def scorecell(board,r,c,player,opponent):
    score = 0
    if board[r][c] == player:
        #horizontal
        if c<9:
            if board[r][c]==board[r][c+1] and board[r][c+2] != opponent and board[r][c+3] != opponent:
                score += 4
                if board[r][c]==board[r][c+3] or board[r][c]==board[r][c+2]:
                    score +=20
        #vertical
        if r>8:
            if board[r][c]==board[r-1][c] and board[r-2][c] != opponent and board[r-3][c] != opponent:
                score += 4
                if board[r][c]==board[r-2][c] :
                    score +=20
                    if c<9:
                        if board[r][c]==board[r-1][c+3] and board[r][c]==board[r-2][c+2] and board[r][c]==board[r-3][c+1] :
                            score +=500
                    if c>2:
                        if board[r][c]==board[r-1][c-3] and board[r][c]==board[r-2][c-2] and board[r][c]==board[r-3][c-1] :
                            score +=500
        #diag positiv
        if r>8 and c<9 :
            if board[r][c]==board[r-1][c+1] and board[r-2][c+2] != opponent and board[r-3][c+3] != opponent :
                score += 8
                #cluster win
                if board[r][c]==board[r][c+1] and board[r][c]==board[r-1][c] and board[r-1][c+2] != opponent and board[r-2][c] != opponent and board[r-2][c+1] != opponent:
                    score+=500
                #3 in diag pos
                if board[r][c]==board[r-3][c+3] or board[r][c]==board[r-2][c+2] :
                    score +=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c+3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c+1]:
                        score+=500
                    #triangle win pos
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c+1] and board[r-2][c+3] ==0 and board[r][c]==board[r-2][c+2]:
                        score+=500
        #diag negativ
        if r>8 and c>2 :
            if board[r][c]==board[r-1][c-1] and board[r-2][c-2] != opponent and board[r-3][c-3] != opponent and r>8 and c>3 :
                score += 8
                if board[r][c]==board[r-3][c-3] or board[r][c]==board[r-2][c-2] :
                    score +=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c-3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c-1]:
                        score+=500
                    #triangle win neg
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c-1] and board[r-2][c-3] ==0:
                        score+=500
    if board[r][c] == opponent:
        #horizontal
        if c<9:
            if board[r][c]==board[r][c+1] and board[r][c+2] != player and board[r][c+3] != player:
                score -= 4
                if board[r][c]==board[r][c+3] or board[r][c]==board[r][c+2]  :
                    score -=20
        #vertical
        if r>8:
            if board[r][c]==board[r-1][c] and board[r-2][c] != player and board[r-3][c] != player:
                score -= 4
                if board[r][c]==board[r-2][c]:
                    score -=20
                    if c<9:
                        if board[r][c]==board[r-1][c+3] and board[r][c]==board[r-2][c+2] and board[r][c]==board[r-3][c+1] :
                            score -=500
        #diag positiv
        if r>8 and c<9 :
            if board[r][c]==board[r-1][c+1] and board[r-2][c+2] != player and board[r-3][c+3] != player :
                score -= 8
                #cluster win
                if board[r][c]==board[r][c+1] and board[r][c]==board[r-1][c] and board[r-1][c+2] != opponent and board[r-2][c] != opponent and board[r-2][c+1] != opponent:
                    score-=500
                #3 in diag pos
                if board[r][c]==board[r-3][c+3] or board[r][c]==board[r-2][c+2] :
                    score -=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c+3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c+1]:
                        score-=500
                    #triangle win pos
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c+1] and board[r-2][c+3] ==0:
                        score-=500
 
        #diag negativ
        if r>8 and c>2 :
            if board[r][c]==board[r-1][c-1] and board[r-2][c-2] != player and board[r-3][c-3] != player :
                score -= 8
                if board[r][c]==board[r-3][c-3] or board[r][c]==board[r-2][c-2]  :
                    score -=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c-3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c-1]:
                        score-=500
                    #triangle win neg
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c-1] and board[r-2][c-3] ==0:
                        score-=500
    return score
 
# Retourne le score de chaque plateau
def utility(board, player, opponent):
    #print(board)
    score = 0
    # Check horizontal locations for win
    for c in range(12):
        for r in range(11,5,-1):
            if board[r][c]!=0:
                score += scorecell(board,r,c,player,opponent)
    return score
# Retourne où l'on peut jouer
def actionPossible(board):
    listeActions = []
    for i in range(12):
        if board[6][i] == 0 :
            listeActions.append(i)
    return listeActions
#Voici le minmax avec une récurssion
def minmax(board, depth, alpha, beta, maxplayer,player,opponent):
    list_action = actionPossible(board)
    if depth <= 0:
        t=()
        for ligne in board:
            t+=tuple(ligne)
        h=hash(t)
        if h in dict:
            value = dict[h]
        else:
            value = utility(board,player,opponent)
            dict[h]=value
        return value
    if maxplayer==True:
        value = -math.inf
        for actions in list_action:
            testboard = board.copy()
            lastboard,r,c = returnGrille(player,testboard,actions)
            if action_win(lastboard,player,r,c)==True:
                alpha = 5000
                return 5000+depth
            value = max(value,minmax(lastboard,depth-1,alpha,beta,False,player,opponent))
            alpha = max(alpha,value)
            if alpha>=beta :
                break
        return value
    else:
        value = math.inf
        for actions in list_action:
            testboard = board.copy()
            lastboard,r,c = returnGrille(opponent,testboard,actions)
            if action_win(lastboard,opponent,r,c)==True:
                beta = -5000
                return -5000-depth
            value = min(value,minmax(lastboard,depth-1,alpha,beta,True,player,opponent))
            beta = min(beta,value)
            if alpha>=beta :
                break
        return value
# retourne à l'aide du minmax le meilleur coup à jouer
def bestmoove(board,player,opponent,profondeur):
    a = timer()
    listresult=[]
    action_list=actionPossible(board)
    for actions in action_list:
        testboard=board.copy()
        lastboard,r,c = returnGrille(player,testboard,actions)
        if action_win(lastboard,player,r,c)==True:
            print(timer()-a)
            return c
        listresult.append(minmax(lastboard,profondeur,-math.inf,math.inf,False,player,opponent))
    finalaction = action_list[listresult.index(max(listresult))]
    print(timer()-a)
    print(listresult)
    return finalaction
dict = {}
grilleDim=12
grille=np.zeros((grilleDim,grilleDim),dtype=np.byte)
# bien préviser si vous commencer le jeu ou c'est l'adversaire qui commence
joueurLocalquiCommence=True
#c'est grâce à cette methode que l'on joue elle renvoie le meilleur coup à partir de la grille
def monjeu():
    testgrille = grille.copy()
    return bestmoove(testgrille,joueurLocal,joueurDistant,3)
def monjeuadv():
    testgrille = grille.copy()
    return bestmoove(testgrille,joueurDistant,joueurLocal,3)
 
# cette fonction est à remplacer une qui saisie le jeu de l'adversaire à votre IA
def appliqueJeuAdv(jeu):
    print("jeu de l'adversair est ", jeu)
if(joueurLocalquiCommence):
    joueurLocal=2
    joueurDistant=1
else:
    joueurLocal=1
    joueurDistant=2
 
sommetempsjeu = 0
tour=0
while(True):
 
    if(joueurLocalquiCommence):
        if tour ==0:
            a = timer()
            jeu=5
            temps = timer() - a
            sommetempsjeu += temps
            print("Je joue en 6")
            print("J'ai mis ",str(temps), "secondes pour jouer ce coup")
        elif tour ==1:
            a = timer()
            jeu = jeuAdv
            sommetempsjeu += (timer()-a)
            print("Je joue en " + str(jeu+1) )
            print("J'ai mis ",str(timer()-a), "secondes pour jouer ce coup")
        else :
            a = timer()
            jeu=monjeu()
            sommetempsjeu += timer()-a
            print("Je joue en " + str(jeu+1) )
            print("J'ai mis ",str(timer()-a), "secondes pour jouer ce coup")
        print("temps final = ", str(sommetempsjeu)," secondes" )
        print("tour : ", str(tour) )
        remplirGrille(joueurLocal,jeu)
        printGrille()
        jeuAdv=input("vueillez saisir la colonne de votre jeu entre 1 et "+ str(grilleDim) +" : ")
        jeuAdv = int(jeuAdv) -1
        #c'est ce jeu qu'on doit transmettre à notre IA
        #appliqueJeuAdv(jeuAdv)
        remplirGrille(joueurDistant,jeuAdv)
        printGrille()
    else:
        #jeuAdv=loopToGetJeuAdv( 5,idjeu,idjoueurDistant,tour)
        #c'est ce jeu qu'on doit transmettre à notre IA
        jeuAdv=input("vueillez saisir la colonne de votre jeu entre 1 et "+ str(grilleDim) +" : ")
        jeuAdv = int(jeuAdv) -1
        #appliqueJeuAdv(jeuAdv)
        remplirGrille(joueurDistant,jeuAdv)
        printGrille()
        if tour ==0:
            a = timer()
            jeu=jeuAdv
            temps = timer() - a
            sommetempsjeu += temps
            print("Je joue en " + str(jeu+1) )
            print("J'ai mis ",str(temps), "secondes pour jouer ce coup")
        else :
            a = timer()
            jeu=monjeu()
            sommetempsjeu += (timer()-a)
            print("Je joue en " + str(jeu+1) )
            print("J'ai mis ",str(timer()-a), "secondes pour jouer ce coup")
        print("temps final =", str(sommetempsjeu)," secondes" )
        print("tour : ", str(tour) )
        remplirGrille(joueurLocal,jeu)
        printGrille()
 
    tour+=1