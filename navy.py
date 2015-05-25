# -*- coding: utf-8 -*-

import random as R

def afficher_mer( show_navy=True ):
    print()
    for iLigne in range(taille_mer):
        print(" %2i "%(taille_mer-iLigne), end='')
        for iColon in range(taille_mer):
            point = (iColon,iLigne) # Pour votre propre bien, simplifiez l'écriture.

            C = " "
            if point in navires and show_navy: C = "O" # Navire
            if point in tirs:                  C = "^" # A l'eau
            if point in navires & tirs:        C = "X" # Touché    ###

            #if point in navires:
            #    if   point in tirs: C = "X"
            #    elif show_navy :    C = "O"
            #    else:               C = " "
            #elif point in tirs:     C = "^"
            #else:                   C = " "

            #if   point in navires & tirs:        C = "X"
            #elif point in tirs:                  C = "^"
            #elif point in navires and show_navy: C = "O"
            #else:                                C = " "

            print( C+" ", end='' )
        print()
    print(" "*4, end='')
    #for code_ascii in range(ord('A'),ord('A')+taille_mer):
    #    print( chr(code_ascii)+" ", end='' )
    ABC =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for lettre in ABC[:taille_mer]:
        print( lettre+" ", end='' )
    #for lettre in " ".join(chr(i+ord('A'))for i in range(taille_mer)):
    #    print( lettre, end='' )
    print()

def position_occupee( iColon,iLigne ):
    if (iColon,iLigne)==(None,None): return True
    return (iColon,iLigne) in navires

def placer_navires():
    (iColon,iLigne) = (None,None)
    for _ in range(nbr_navires): ### _ pratique pour signifier que cette variable n'est pas utilisée
        while position_occupee(iColon,iLigne):
            iColon = R.randint(0,taille_mer-1)
            iLigne = R.randint(0,taille_mer-1)
        navires.add( (iColon,iLigne) )
        #print( "=>", chr(iColon+ord('A')), taille_mer-iLigne )   ###
        #print( "=>", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[iColon], taille_mer-iLigne )

def afficher_nouvelle_mer():
    global navires, tirs ###
    navires = set()
    tirs    = set()
    placer_navires()
    afficher_mer()

def coordonnees(cmd):
    iColon = ord( cmd[0].upper() ) - ord('A')
    try: ###
        iLigne = taille_mer - int( cmd[1:] )
    except:
        return None  # Voir if point==None dans jouer()
    if iColon not in range(taille_mer) or iLigne not in range(taille_mer): ###
        return None
    return (iColon,iLigne)

def quitter( cmd ): ###
    if len(cmd)>0: return False
    while True:
        cmd = input( "Voulez-vous vraiment quitter ? (Oui/Non) ou Déboguer ? (D)" ).upper()
        if cmd in ('O','OUI'):
            print( "Au revoir" )
            return True
        if cmd in ('N','NON'):
            return False
        if cmd in ('D'): # Option utile pour le TP
            print( "Navires:", navires )
            print( "Tirs   :", tirs    )
            print( "Il reste %i navires à couler."%len(navires-tirs) )
            return False

def jouer():
    afficher_nouvelle_mer() # Oui on voit tout. Ce n'est pas un jeu, c'est un exercice
    cmd = None ###
    while cmd==None or not quitter(cmd):
        cmd = input( "Entrez une commande: " ) ###
        if len(cmd)>0:
            point = coordonnees(cmd)
            #print( "=>", cmd, point, type(point) )
            if point==None:
                print( "Entrez une commande valide (1 lettre + chiffres)" )
            else:
                tirs.add( point )
                afficher_mer()
                if navires - tirs == set():                  ###
                    print( "\n\n === GAME OVER ===\n" )
                    afficher_nouvelle_mer()

# --- main ---

taille_mer  = 10
nbr_navires = 5
navires     = None
tirs        = None

jouer()


### Alternatives:
####################

# Commentez l'appel à jouer(), puis décommentez jouer_2() ou jouer_3()

def jouer_2():
    def tous_les_navires_ne_sont_pas_coulés(): return navires-tirs!=set()
    def tirer():                               tirs.add(point)

    while True:
        afficher_nouvelle_mer()
        while tous_les_navires_ne_sont_pas_coulés():
            cmd = input( "Entrez une commande: " )
            try:
                point = coordonnees(cmd)
                if point != None:
                    tirer()
                    afficher_mer()
                else: print( "Entrez une commande valide (1 lettre + chiffres)" )
            except:
                if quitter_ok(cmd): raise SystemExit
        print( "\n\n === GAME OVER ===\n" )
#jouer_2()

def jouer_3():
    # Attaquez directement la lecture à la boucle while:
    # "Programmation lettrée"
    # http://fr.wikipedia.org/wiki/Programmation_lettrée (de Donald Knuth)
    def on_veut_jouer():                       return True
    def on_veut_quitter():                     return quitter_ok(cmd)
    def tous_les_navires_ne_sont_pas_coulés(): return navires-tirs!=set()
    def demander_une_commande():               return input("Entrez une commande: ")
    def commande_vide():                       return cmd==''
    def le_point_est_valide():                 return point!=None
    def tirer():                               tirs.add(point) # Ça c'est une procédure: ça fait qlq-ch mais ça ne retourne rien

    while on_veut_jouer():
        afficher_nouvelle_mer()
        while tous_les_navires_ne_sont_pas_coulés():
            cmd = demander_une_commande()
            if commande_vide():
                if on_veut_quitter(): break
                else:                 continue
            point = coordonnees( cmd )
            if le_point_est_valide():
                tirer()
                afficher_mer()
            else: print( "Entrez une commande valide (1 lettre + chiffres)" )
        if commande_vide(): break # pour propager le break précédent à l'autre while
        print( "\n\n === GAME OVER ===\n" )
#jouer_3()
