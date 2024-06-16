
#include <mahony.h>
 // initialize with as unit vector with real component  = 1

void mahony(float ax, float ay, float az, float gx, float gy, float gz, float mx, float my, float mz){

    struct quaternion q_a ={0,ax,ay,az};
    struct quaternion q_g ={0,gx,gy,gz};
    struct quaternion q_m ={0,mx,my,mz};

    float h = [4];
    float b = [4];


    // Reference direction of Earth's magnetic feild
    h = quat_mult(q, quat_mult([0,mx,my,mz], quat_conjugate(q)));
    b = [0 norm1(h[1], h[2]) 0 h(4)];

    // Estimated direction of gravity and magnetic field
    v = [2*(q[1]*q[3] - q[0]*q[2]), 2*(q[0]*q[1] + q[2]*q[3]),  q[0]^2 - q[1]^2 - q[2]^2 + q[3]^2];
    w = [2*b[1]*(0.5 - q[2]^2 - q[3]^2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]),2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]), 2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]^2 - q[2]^2)]; 
   
   // Error is sum of cross product between estimated direction and measured direction of fields
    float e[3];
    float ca;
    float cm;
    float eInt[3];
    crossProduct([ax,ay,az],v,ca);
    crossProduct([mx,my,mz],w,cm);
    
    e = {ca[0]+cm[0],ca[1]+cm[1],ca[2]+cm[2]}
    
    if(Ki > 0) eInt = eInt + e * DELTA_T; eInt = {eInt[0] + e * DELTA_T,eInt[1] + e * DELTA_T,eInt[2] + e * DELTA_T};
    else eInt = {0, 0, 0};

            
    // Apply feedback terms   
    gx=gx + Kp * e + Ki * eInt;
    gy=gy + Kp * e + Ki * eInt;
    gz=gz + Kp * e + Ki * eInt;

    struct quaternion qDot ={0,0,0,0}

    // Compute rate of change of quaternion
    struct quaternion qDot = quat_mult(q,q_g);
    qDot = qDot*0.5;

    // Integrate to yield quaternion
    quat_add(q, q, quat_scalar(qDot,DELTA_T));
    struct quaternion Quaternion = quat_scalar(q,quat_Norm(q)); // normalise quaternion
    
    eulerAngles(Quaternion ,*roll,*pitch,*yaw);
}

            

