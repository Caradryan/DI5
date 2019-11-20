import numpy as np
import matplotlib.pyplot as plt

def printPATH(DIR):
    """
    Tiesiog printinimo f-ja
    """
    print("preferred directions")  
    print("-------------------------------------")
    for i in range(3):
        for j in range(4):
            if j==0:
                print("|", end="")
            print('%13s' % str(DIR[i][j]),"|", end="")
            if j == 3:
                print("\n-------------------------------------")

def printMAP(Map):
	print(Map[1:-1,1:-1])

def TESTMATRIX(n):
	Ropt = [1,2,3]
	Nmin = [5,10,50]
	Ncut = [10,20,60,100]
	gamma = [0.8,0.9,0.95,1.]
	
	#test matrix n matė matrica, kur kiekviena dimensija atitinka pokytį tam tikrame parametre
	TESTm = np.zeros( (n, len(Ropt), len(Nmin), len(Ncut), len(gamma) ))
	return [Ropt, Nmin, Ncut, gamma, TESTm]
	

def sanityCheck(Laukuva, policy):
	
	#if np.abs(Laukuva[1:-1,1]).mean() > 100:
	if ((policy[1:-1,1]==np.array([3,0,0])).sum() == 3) and policy[1,2]==3 and policy[1,3]==3:	
		return 1
	else:
		return 0
def sanityCheck2(Laukuva, policy):
	#if np.abs(Laukuva[1:-1,1]).mean() > 100:
	if ((policy[1:-1,1]==np.array([3,0,0])).sum() == 3) and policy[1,2]==3 and policy[1,3]==3 and ((policy[3,2:-1]==np.array([2,2,2])).sum() == 3) and policy[1,3]==0:	
		return 1
	else:
		return 0
	#if np.abs(Laukuva[1:-1,1]).mean() < 100:
#		return 1
	
	
def Map():
    """
    Laukuvos žemėlapis
    Su labai neigiamom sienom (-np.inf)
    """
    Map = np.zeros((5,6))
    Map[:,0] = -np.inf
    Map[:,-1] = -np.inf
    Map[0,:] = -np.inf
    Map[-1,:] = -np.inf
    Map[2,2] = -np.inf
    Map[1, -2] = 100
    Map[2, -2] = -100

    Mirror_map = Map.copy()
    Mirror_map[Mirror_map == -np.inf] =0
    return [Map, Mirror_map] 


def iterate_vals(Map, mirror, R=-4, gamma=1):
    """
    f-ja kurie pereina per laukuvą vieną kartą.
    Pradeda eiti nuo tikslo, apskaičiuoja gretimų luakelių vertes, tada randa max vertę
    ir apskaičiuoja laukelių prie jo vertes.... 
    pereidamas pažymi jau lankytus laukelius (Counting_map) - kai aplanko visus laukelius gražina 
    Laukuvos būseną ir kryptis.
    """
    
    Counting_map = Map.copy()
    Counting_map[Counting_map == -100] = -999
    Counting_map[Counting_map == 100] = -999
    dir_map = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    counter = 0

    while np.max(Counting_map !=-np.inf):
        counter+=1
        if np.max(Counting_map) == -np.inf:
            return [Map, mirror, dir_map]

        ind = np.where(Counting_map == np.max(Counting_map))
        Counting_map[ind] = -np.inf
        """
        Surandu max verčių laukelius, gali  būti keli.
        Ypač jeigu labai brangus žingsnis.
        """
        for i in range(len(ind[0])):
            """
            Imu vieną iš max laukelių, gaunu gretimu laukelius
            """
            indU = (ind[0][i]-1, ind[1][i])
            indD = (ind[0][i]+1, ind[1][i])
            indL = (ind[0][i], ind[1][i]-1)
            indR = (ind[0][i], ind[1][i]+1)
            adj_ind = [indU, indD, indL, indR]
            adj_ind_mod = np.array(adj_ind)
            directions = ["Up", "Down", "Left", "Right"]
            TvalList = []
            for j in range(len(adj_ind)):
                """
                Atmetu jau žiūrėtus, bei tikslo laukelius
                """
                if Map[adj_ind[j]] == -np.inf or Map[adj_ind[j]] == -100 or Map[adj_ind[j]] == 100 or Counting_map[adj_ind[j]]==-999:
                    continue
                #skai2iuoju naudodamas gretimus values
                TempVal = np.zeros(4)
                
                #surandu aplinkinius laukelius ir jų vertes
                Adj_U_from = (adj_ind_mod[j,0]-1, adj_ind_mod[j,1])
                Adj_D_from = (adj_ind_mod[j,0]+1, adj_ind_mod[j,1])
                Adj_L_from = (adj_ind_mod[j,0], adj_ind_mod[j,1]-1)
                Adj_R_from = (adj_ind_mod[j,0], adj_ind_mod[j,1]+1)
                """
                Jeigu einu į sieną, imu esamo laukelio vertę
                """
                if Map[Adj_U_from] == -np.inf:
                    mirror_val_U = Map[adj_ind[j]]
                    
                if Map[Adj_U_from] != -np.inf:
                    mirror_val_U = mirror[Adj_U_from]
                
                if Map[Adj_D_from] == -np.inf:
                    mirror_val_D = Map[adj_ind[j]]
                    
                if Map[Adj_D_from] != -np.inf:
                    mirror_val_D = mirror[Adj_D_from]

                if Map[Adj_L_from] == -np.inf:
                    mirror_val_L = Map[adj_ind[j]]
                   
                if Map[Adj_L_from] != -np.inf:
                    mirror_val_L = mirror[Adj_L_from]

                if Map[Adj_R_from] == -np.inf:
                    mirror_val_R = Map[adj_ind[j]]
                    #print("val", mirror_val_R)
                if Map[Adj_R_from] != -np.inf:
                    mirror_val_R = mirror[Adj_R_from]

                """
                Skaičiavimas
                """
                for direction in range(len(directions)):
                    if directions[direction]=="Up":
                        TempVal[direction] += gamma*(0.8*mirror_val_U + 0.1*mirror_val_L + 0.1*mirror_val_R) + R
                    if directions[direction]=="Down":
                        TempVal[direction] += gamma*(0.8*mirror_val_D + 0.1*mirror_val_L + 0.1*mirror_val_R) + R
                    if directions[direction]=="Left":
                        TempVal[direction] += gamma*(0.8*mirror_val_L + 0.1*mirror_val_U + 0.1*mirror_val_D) + R
                    if directions[direction]=="Right":
                        TempVal[direction] += gamma*(0.8*mirror_val_R + 0.1*mirror_val_U + 0.1*mirror_val_D) + R
                """
                Atrenku max vertę/vertes
                Parenku kryptis
                """
                DIR_AP = []
                for d in range(len(np.where(TempVal == np.max(TempVal))[0])):
                    if np.max(TempVal) >0:
                        DIR_AP.append(directions[np.where(TempVal == np.max(TempVal))[0][d]])
                #TvalList.append((j, np.max(TempVal), directions[np.where(TempVal == np.max(TempVal))[0][0]] ))
                TvalList.append((j, np.max(TempVal), DIR_AP ))
            
            for l in range(len(TvalList)):
                """
                Atnaujinu vertes
                """
                indd, val, DIR = TvalList[l]
                #print(adj_ind[ind])
                Map[adj_ind[indd]] = val
                mirror[adj_ind[indd]] = val
                if Counting_map[adj_ind[indd]] != -np.inf:
                    Counting_map[adj_ind[indd]] = val
                dir_map[adj_ind[indd][0]-1][adj_ind[indd][1]-1] = DIR

    return [Map, mirror, dir_map]

def wallCheck(Laukuva, init, currDir):
	Y, X = init
	if currDir == "Up":
		XX = X
		YY = Y-1
		
	if currDir == "Down":
		XX = X
		YY = Y+1
		
	if currDir == "Left":
		XX = X-1
		YY = Y
		
	if currDir == "Right":
		XX = X+1
		YY = Y
		
	#print(currDir)
	#print("Gautas Y X", init)
	#print("Pakeistas", (YY, XX))
	#print("lauk.shape",Laukuva.shape)
	
	if (XX!=1 and XX!=4 and XX!=3 and XX!=2 and (YY, XX)==(2,2)  ):
		XX = X
	if (YY!=1 and  YY!=3 and YY!=2 and (YY, XX)==(2,2)):
		YY = Y
	
		 
	if Laukuva[YY, XX] == -np.inf:
		#print("užribis")
		YY = Y
		XX = X
	#print("gražinamas YY, XX", (YY, XX))		
	return (YY, XX)
	

def walker(Laukuva, mirror,use_cut=0, R=-4, gamma=1, NMIN=5, ROPT=2, NCUT=60, use_start_policy=0, N_for_sq=1, prt=0, n_step=5000):
	"""
	Reikia policy map ir Q 3D matricos, kurioje saugočiau vertes judėjimo į betkurią pusę
	"""
	#generuoju atisitiktinę pradinę policy
	policyMap = Laukuva.copy()
	LEN_X = policyMap.shape[1] 
	LEN_Y = policyMap.shape[0]
	directions = ["Up", "Down", "Left", "Right"]
	LEN_Z = len(directions)
	for y in range(LEN_Y):
		for x in range(LEN_X):
			if policyMap[y, x]==100 or policyMap[y, x]==-100 or policyMap[y, x]==-np.inf:
				continue
			policyMap[y, x] = np.random.randint(0,4)
	
	#possible predefined initial policies
	if use_start_policy !=0:
		if prt==1:
			print("initial policy:")
		if use_start_policy==1:
			policyMap[2:4,1]=0
			policyMap[1,1]=3
			policyMap[1,2]=3
			policyMap[1,3]=3
		if use_start_policy==2:
			policyMap[3,1]=3
			policyMap[3,2]=3
			policyMap[3,3]=0
			policyMap[2,3]=0
			policyMap[1,3]=3
		printMAP(policyMap)
		if prt==1:
			print("---------------")
	if use_start_policy ==0:
		if prt==1:
			print("random initial policy")
	#printMAP(policyMap)
	#pradinė vieta, negalima pad4ti ant pabaigos ir ant sienos
	init = (np.random.randint(0,LEN_Y), np.random.randint(0,LEN_X))	
	while (policyMap[init]==-100 or policyMap[init]==100 or policyMap[init]==-np.inf ):
		init = (np.random.randint(0,LEN_Y), np.random.randint(0,LEN_X))
	#utility į visas kryptis
	Q = np.zeros((LEN_Z, LEN_Y, LEN_X))
	for z in range(LEN_Z):
		Q[z,:,:] += Laukuva
		
	#Dažniai aplankytų laukelių
	N = np.zeros_like(Q)
	ALPHA = NCUT / (NCUT + N - 1)
	
	#žygiavimas
	for i in range(n_step ):
		#print(policyMap[init])
		dirInd = policyMap[init].astype(int)
		if dirInd == 100 or dirInd==-100:
			init = (np.random.randint(0,LEN_Y), np.random.randint(0,LEN_X))	
			while (policyMap[init]==-100 or policyMap[init]==100 or policyMap[init]==-np.inf ):
				init = (np.random.randint(0,LEN_Y), np.random.randint(0,LEN_X))
		dirInd = policyMap[init].astype(int)
		currDir = directions[dirInd]
		Y, X = init
		#randu ant ko stoviu po judesio
		YY, XX = wallCheck(Laukuva, init, currDir)
		#dabar žiūriu ėjimą į priekį
		ind_for_each = []
		for dr in range(LEN_Z):
			ind_for_each.append(wallCheck(Laukuva, (YY, XX), directions[dr]))
		tempVal = np.zeros((1,LEN_Z))
		for dr in range(LEN_Z):
			if directions[dr] == "Up":
				tempVal[0,dr] = 0.8*Laukuva[ind_for_each[0]] + 0.1*Laukuva[ind_for_each[2]] + 0.1*Laukuva[ind_for_each[3]] + R
			if directions[dr] == "Down":
				tempVal[0,dr] = 0.8*Laukuva[ind_for_each[1]] + 0.1*Laukuva[ind_for_each[2]] + 0.1*Laukuva[ind_for_each[3]] + R
			if directions[dr] == "Left":
				tempVal[0,dr] = 0.8*Laukuva[ind_for_each[2]] + 0.1*Laukuva[ind_for_each[0]] + 0.1*Laukuva[ind_for_each[1]] + R
			if directions[dr] == "Right":
				tempVal[0,dr] = 0.8*Laukuva[ind_for_each[3]] + 0.1*Laukuva[ind_for_each[0]] + 0.1*Laukuva[ind_for_each[1]] + R
		#pasidarau lokalŲ, dėl paprastumo
		N_s = N[:, Y, X]#*np.ones(LEN_Z)
		N_s_a = N_s[dirInd] 
		Q_s = Q[:, Y, X]
		ALPHA_s = ALPHA[:, Y, X]
		#išrenku max vertę
		maxVal = np.max(tempVal)
		if N_s_a <= NMIN:
			maxVal =  ROPT * 100
		#print(R + gamma * ROPT * 100  - Q_s[N_s<= NMIN])
		Q_s[N_s<= NMIN] += ALPHA_s[N_s <= NMIN] * (R + gamma * ROPT * 100  - Q_s[N_s<= NMIN])
		Q[:,Y, X] = Q_s
		
		N[dirInd, Y, X]+=1
		if N_for_sq==1:
			N[dirInd, Y, X]-=1
			N[:, Y, X]+=1
		#paupdatinu Q atitinkamą vertę
		Q[dirInd, Y, X] += ALPHA[dirInd, Y, X] * ( R + gamma * maxVal - Q[dirInd, Y, X])
		#Laukuvoje saugau max vertes
		Laukuva[Y, X] = Q[:, Y, X].max(axis=0) 
		#print(policyMap)
		Qcheck = Q[:, Y, X]
		#print(Qcheck)
		#print(np.argmax(Qcheck))
		
		policyMap[Y, X] = np.argmax(Qcheck)
		prob_for_move = np.random.uniform(0,1)
		if currDir=="Up":
			if prob_for_move <= 0.1:
				actDir="Left"
			if 0.1 < prob_for_move <= 0.2:
				actDir="Right"
			if 0.2 < prob_for_move < 1:
				actDir="Up"
		if currDir=="Down":
			if prob_for_move <= 0.1:
				actDir="Left"
			if 0.1 < prob_for_move <= 0.2:
				actDir="Right"
			if 0.2 < prob_for_move < 1:
				actDir="Down"
		if currDir=="Left":
			if prob_for_move <= 0.1:
				actDir="Down"
			if 0.1 < prob_for_move <= 0.2:
				actDir="Up"
			if 0.2 < prob_for_move < 1:
				actDir="Left"   
		if currDir=="Right":
			if prob_for_move <= 0.1:
				actDir="Down"
			if 0.1 < prob_for_move <= 0.2:
				actDir="Up"
			if 0.2 < prob_for_move < 1:
				actDir="Right"
		#print(policyMap)
		#paupdatinu init vertę (kur stovi atlikęs žingsnį vaikščiotojas)
		#print("init",init)
		YY, XX = wallCheck(Laukuva, init, actDir)
		init = (YY, XX)#šitoje  vietoje reikia įdėtirandom pasirinkimą.
		#padidinu N
		
	return [Laukuva, policyMap, N]
		
		
		
if __name__ == "__main__":
	#TESTING EX
	N_tests = 5
	Ropt, Nmin, Ncut, gamma, TESTm = TESTMATRIX(N_tests)
	for nt in range(N_tests):
		print(nt)
		for ro in range(len(Ropt)):
			for nm in range(len(Nmin)):
				for nc in range(len(Ncut)):
					for g in range(len(gamma)):
		#print("Test ",i)
						Laukuva, mirror = Map()
						Laukuva, policy, N = walker(Laukuva, mirror, R=-3, gamma=gamma[g], NMIN=Nmin[nm], ROPT=Ropt[ro], NCUT=Ncut[nc], use_start_policy=0, N_for_sq=1)
						TESTm[nt, ro, nm, nc, g] = sanityCheck(Laukuva, policy)
		#printMAP(Laukuva)
		#printMAP(policy)
		#print("-------------------")