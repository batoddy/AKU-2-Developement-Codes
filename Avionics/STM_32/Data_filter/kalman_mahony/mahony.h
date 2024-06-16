


// Include a hardware specific header file to redefine these predetermined values
#ifndef DELTA_T
    #define DELTA_T 1/256f // 100Hz sampling frequency
#endif

#ifndef PI  
    #define PI 3.14159265358979f
#endif

#ifndef kp
    #define kp 1.0f
#endif

#ifndef ki
    #define ki 0.1f
#endif

#ifndef yaw
    #define yaw
#endif

#ifndef pitch
    #define pitch
#endif

#ifndef roll
    #define roll
#endif

#include <math.h>
#include <stdio.h>

float yaw,pitch,roll;


struct quaternion{
    float q1;
    float q2;
    float q3;
    float q4;
};

// global variables
extern struct quaternion q_est;

// Multiply two quaternions and return a copy of the result, prod = L * R
struct quaternion quat_mult (struct quaternion q_L, struct quaternion q_R);

// Multiply a reference of a quaternion by a scalar, q = s*q
static inline void quat_scalar(struct quaternion * q, float scalar){
    q -> q1 *= scalar;
    q -> q2 *= scalar;
    q -> q3 *= scalar;
    q -> q4 *= scalar;
}

struct quaternion quat_mult (struct quaternion L, struct quaternion R){
    
    
    struct quaternion product;
    product.q1 = (L.q1 * R.q1) - (L.q2 * R.q2) - (L.q3 * R.q3) - (L.q4 * R.q4);
    product.q2 = (L.q1 * R.q2) + (L.q2 * R.q1) + (L.q3 * R.q4) - (L.q4 * R.q3);
    product.q3 = (L.q1 * R.q3) - (L.q2 * R.q4) + (L.q3 * R.q1) + (L.q4 * R.q2);
    product.q4 = (L.q1 * R.q4) + (L.q2 * R.q3) - (L.q3 * R.q2) + (L.q4 * R.q1);
    
    return product;
}



// Adds two quaternions together and the sum is the pointer to another quaternion, Sum = L + R
static inline void quat_add(struct quaternion * Sum, struct quaternion L, struct quaternion R){
    Sum -> q1 = L.q1 + R.q1;
    Sum -> q2 = L.q2 + R.q2;
    Sum -> q3 = L.q3 + R.q3;
    Sum -> q4 = L.q4 + R.q4;
}

// Subtracts two quaternions together and the sum is the pointer to another quaternion, sum = L - R
static inline void quat_sub(struct quaternion * Sum, struct quaternion L, struct quaternion R){
    Sum -> q1 = L.q1 - R.q1;
    Sum -> q2 = L.q2 - R.q2;
    Sum -> q3 = L.q3 - R.q3;
    Sum -> q4 = L.q4 - R.q4;
}

static inline float norm1(float a,float b){
    return sqrt(a*a + b*b);
}


void crossProduct(int vect_A[], int vect_B[], int cross_P[])
{
 
    cross_P[0] = vect_A[1] * vect_B[2] - vect_A[2] * vect_B[1];
    cross_P[1] = vect_A[2] * vect_B[0] - vect_A[0] * vect_B[2];
    cross_P[2] = vect_A[0] * vect_B[1] - vect_A[1] * vect_B[0];
}

// the conjugate of a quaternion is it's imaginary component sign changed  q* = [s, -v] if q = [s, v]
static inline struct quaternion quat_conjugate(struct quaternion q){
    q.q2 = -q.q2;
    q.q3 = -q.q3;
    q.q4 = -q.q4;
    return q;
}

// norm of a quaternion is the same as a complex number
// sqrt( q1^2 + q2^2 + q3^2 + q4^2)
// the norm is also the sqrt(q * conjugate(q)), but thats a lot of operations in the quaternion multiplication
static inline float quat_Norm(struct quaternion q)
{
    return sqrt(q.q1*q.q1 + q.q2*q.q2 + q.q3*q.q3 +q.q4*q.q4);
}

// Normalizes pointer q by calling quat_Norm(q),
static inline void quat_Normalization(struct quaternion * q){
    float norm = quat_Norm(*q);
    q -> q1 /= norm;
    q -> q2 /= norm;
    q -> q3 /= norm;
    q -> q4 /= norm;
}

void eulerAngles(struct quaternion q, float* roll, float* pitch, float* yaw){
    
    *yaw = atan2f((2*q.q2*q.q3 - 2*q.q1*q.q4), (2*q.q1*q.q1 + 2*q.q2*q.q2 -1));  // equation (7)
    *pitch = -asinf(2*q.q2*q.q4 + 2*q.q1*q.q3);                                  // equatino (8)
    *roll  = atan2f((2*q.q3*q.q4 - 2*q.q1*q.q2), (2*q.q1*q.q1 + 2*q.q4*q.q4 -1));
    
    *yaw *= (180.0f / PI);
    *pitch *= (180.0f / PI);
    *roll *= (180.0f / PI);

}


static inline void printQuaternion (struct quaternion q){
    printf("%f %f %f %f\n", q.q1, q.q2, q.q3, q.q4);
}


// IMU consists of a Gyroscope plus Accelerometer sensor fusion
void imu_filter(float ax, float ay, float az, float gx, float gy, float gz);

// void marg_filter(void); for future


void eulerAngles(struct quaternion q, float* roll, float* pitch, float* yaw);



#endif /* MADGWICK_FILTER_H */
