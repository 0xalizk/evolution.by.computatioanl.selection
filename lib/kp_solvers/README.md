Knapsack solvers written in C.

These are compiled into shared libraries and executed from within Python using ctypes. DPSolver.c is pseudopolynomial dynamic programming algorithm (very fast for reasonably small knapsack wight values). minkap.c solver is by Psinger D (original code is modified after having run into delightful segfaults), see its details in this paper  "Pisinger D. Where are the hard knapsack problems? Computers & Operations Research. 2005;32(9):2271–2284".

## Compiling:
 
### Linux:  

`gcc -shared -Wl,-soname,DPsolver.so -o DPsolver.so -fPIC DPsolver.c`

### Mac OS: 

`gcc -shared -Wl,-install_name,DPsolver.so -o DPsolver.so -fPIC DPsolver.c`


