// Compiling: 
// Mac OS: gcc -shared -Wl,-install_name,DPsolver.so -o DPsolver.so -fPIC DPsolver.c
// Linux:  gcc -shared -Wl,-soname,DPsolver.so -o DPsolver.so -fPIC DPsolver.c
#include <time.h>

int		max(int a, int b) {return (a>b)? a:b;}

void solve (int *B, int *D, int T, int num_of_genes, int *f, int *result, double *exec_time){
  
  int i=0, sumw=0,sumv=0;
  for (i=0;i<num_of_genes;i++)
      sumw = sumw + D[i];
  if (sumw <= T){ //the knapsack can hold all objects
      for (i=0;i<num_of_genes;i++){
          sumv = sumv + B[i];
          f[i]=1;
      }
      result [0]=sumv;
      result [1]=sumw;
      result [2]=-1; // coresize
      exec_time [0]=-1;// seconds
      exec_time [1]=-1;//milliseconds
  }
  else{
	
	clock_t begin, end;
	begin = clock();
	
	int K[num_of_genes+1][T+1];
	int i, j;
	for ( i=0;i<=num_of_genes;i++){
		for( j=0; j<=T;j++){
			if(i == 0 || j==0){
				K[i][j]=0;
				continue;
			}
			if(D[i-1]<=j)
				K[i][j]=max(K[i-1][j], B[i-1]+K[i-1][j-D[i-1]]);
			else
				K[i][j]=K[i-1][j];
		}
	}
	
	i=num_of_genes; 
	int k=T; 
	int total_weight=0;
	
	while (i>0 && k>0){
		if (K[i][k] != K[i-1][k]){
			total_weight=total_weight+D[i-1];
			f[i-1]=1;
			i--;
			k=k-D[i];
		}else{
			f[i-1]=0;
			i--;
		}
	}
	end = clock();

	result[0]=K[num_of_genes][T];//TOTAL_VALUE;
	result[1]=total_weight;		//TOTAL_WEIGHT
	result[2]=num_of_genes; //coresize, added just for conformity with minknap() signature
	exec_time[0]= ((double) (end - begin)) / CLOCKS_PER_SEC; // execution time in seconds
	exec_time[1]= (((double) (end - begin)) / CLOCKS_PER_SEC)*1000; // execution time in milliseconds
	//printf ("\nfrom_C:v=%d,w=%d",K[num_of_genes][T],total_weight);
	//printf ("\n%d, %d, %d",result [0],result [1],result [2]);	
	}
}
	
