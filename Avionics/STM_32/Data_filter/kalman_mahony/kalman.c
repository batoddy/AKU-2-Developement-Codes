
#include <kalman.h>


void kalman(float yaw, float pitch, float roll){

float z[3][1] = {{yaw},{pitch},{roll}};
float xp[3][1];
float Pp[3][3];
float At[3][3];
float Ht[3][3];
float K[3][3];
float decoy1[3][3],decoy2[3][3],decoy3[3][3],decoy4[3][3];

multiplyMatrix(A, x, xp, 3, 3, 1);

multiplyMatrix(A, P, decoy1, 3, 3, 3);

transpose(A,At);

multiplyMatrix(decoy1,At,decoy2,3,3,3);

sum(decoy2,Q,Pp);

//

multiplyMatrix(H, Pp, decoy1,3,3,3);

transpose(H,Ht);

multiplyMatrix(decoy1,Ht,decoy2,3,3,3);

sum(decoy2,R,decoy3,3,3);

cofactor(decoy3,decoy4,3);

multiplyMatrix(Pp,Ht,decoy1,3,3,3);

multiplyMatrix(decoy1,decoy4,K,3,3,3);

//

multiplyMatrix(H, xp,decoy1,3,3,1);

sub(z,decoy1,decoy2,3,1);

multiplyMatrix(K, decoy2, decoy3,3,3,1);

sum(xp,decoy3,x,3,1);

//

multiplyMatrix(K, H, decoy1,3,3,3);

multiplyMatrix(decoy1, Pp, decoy2,3,3,3);

sub(Pp,decoy2,P,3,3);

//  x[1][1] = yaw,  x[2][1] = pitch,  x[3][1] =roll 

}

            

