from aux_funkcijos import *


#a dalies testas
TEST_a = 0

#b dalies testas
TEST_b = 0

#vienas laukuvos pravaik62iojimas
TEST_c = 1


if TEST_a == 1:
	print("------")
	print("TEST_a")
	print("------")
	R = [0, -3, -4, -40, -100, -101, -200 ]
	for r in R: 
	    Laukuva , mirror = Map()
	    #Laukuva, mirror, DIR = iterate_vals(Laukuva, mirror, R)
	    print("---------------------------")
	    print("---------------------------")
	    print("\n")
	    print("Laukuva, R ={:3d}".format(r))    
	    print(np.round(Laukuva[1:4,1:5], 3))
	
	    Laukuva, mirror, DIR = iterate_vals(Laukuva, mirror, r)
	    LaukuvaOld=0
	    for i in range(100):
	    #while np.sum(np.abs(LaukuvaOld-Laukuva)) > 0.001: 
	        LaukuvaOld = Laukuva.copy()    
	        Laukuva, mirror, DIR = iterate_vals(Laukuva, mirror, r)
	
	    print("Laukuva, R ={:3d}".format(r))    
	    print(np.round(Laukuva[1:4,1:5]/100, 3))
	    printPATH(DIR)
		
if TEST_b == 1:
	
	#TESTING EX
	print("------")
	print("TEST_b")
	print("------")
	N_tests = 5
	Ropt, Nmin, Ncut, gamma, TESTm = TESTMATRIX(N_tests)
	Ropt, Nmin, Ncut, gamma, TESTm2 = TESTMATRIX(N_tests)
	print("Ropt", Ropt)
	print("Nmin", Nmin)
	print("Ncut", Ncut)
	print("gamma", gamma)
	#Ropt, Nmin, Ncut, gamma, TESTm = TESTMATRIX(N_tests)
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
						TESTm2[nt, ro, nm, nc, g] = sanityCheck2(Laukuva, policy)
	#vidutinė vertė per testus
	print("Pagrindinis kelias")
	aT = TESTm.mean(axis=0)	
	for ro in range(len(Ropt)):
		for nm in range(len(Nmin)):
			print("Ropt =", Ropt[ro],"Nmin =", Nmin[nm], "Ncut-Y",Ncut , "gamma-X", gamma)
			print(aT[ro, nm, :, :])
			
	print("visas policy")
	aT2 = TESTm2.mean(axis=0)	
	for ro in range(len(Ropt)):
		for nm in range(len(Nmin)):
			print("Ropt =", Ropt[ro],"Nmin =", Nmin[nm], "Ncut-Y",Ncut , "gamma-X", gamma)
			print(aT[ro, nm, :, :])
			
if TEST_c == 1:
	#TESTING EX
	N_tests = 5
	print("------")
	print("TEST_c")
	print("------")
	print("legenda")
	print(["0 - Up", "1 - Down", "2 - Left", "3 - Right"])
	Ropt, Nmin, Ncut, gamma, TESTm = TESTMATRIX(N_tests)
	print("Ropt", Ropt)
	print("Nmin", Nmin)
	print("Ncut", Ncut)
	print("gamma", gamma)
	#print("'geras' pvz")
	print("parametrai:", "R=",-3, "gamma=", gamma[-1], "NMIN=",Nmin[1], "ROPT=",Ropt[-1], "NCUT=",Ncut[-1])
	Laukuva, mirror = Map()
	Laukuva, policy, N = walker(Laukuva, mirror, R=-3, gamma=gamma[-1], NMIN=Nmin[2], ROPT=Ropt[-1], NCUT=Ncut[-2], use_start_policy=0, N_for_sq=1, n_step=4000)
	print("Laukuva")
	printMAP(Laukuva)
	print("policy")
	printMAP(policy)	