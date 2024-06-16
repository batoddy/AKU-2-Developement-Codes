#include <aku_controller.h>
#include "aku_infrastructure.h"
#include "aku_structure.h"
#include "aku_infra_motor.h"

float pitch_ref, yaw_ref; // istenen yaw ve pitch değerleri
// float pitch_data, yaw_data; // anlık yaw ve pitch değerleri, IMU'dan çekilecek
float pitch_error, yaw_error; // yaw ve pitch hata değerleri
float pitch_error_prev, yaw_error_prev;
float dt = 0.025; // örnekleme zamanı (ne kadar sürede bir çıkış verilecek veya veri çekilecek), servolar için min değer 20 milisaniye, biz 25 diyelim

// Ben her şeyi açı olarak hesaplıyorum, PWM'e çevirme işi sende

float yaw_out, yaw_out_prev;
float pitch_out, pitch_out_prev;
//float Kp, Kd;

// Fark denklemi : U[n+1] = 11E[n+1] - 10.86E[n] + 0.08208U[n]

// Eğer timer ile sabit 0.025 saniyelik bir örnekleme elde edemeyceksen bana bir delta T değişkeni vermen lazım (bir önceki döngü üzerinden ne kadar zaman geçtiği). 
// Kodumu ona göre düzenlicem.

ServoAngle srv_angle;

float saturation(float min, float max, float value)
{
    if (value < min) return min;

    else if (value > max) return max;

    else return value;

}


float yaw_controller(float yaw_data)
{
    yaw_error = yaw_ref - yaw_data; //yaw_data değerini IMU'dan çekmemiz lazım
    yaw_out = 11*yaw_error - 10.86*yaw_error_prev + 0.08208*yaw_out_prev;
    yaw_out_prev = yaw_out;
    yaw_error_prev = yaw_error;
    yaw_out = saturation(-15, 15, yaw_out); 

    // burada derece cinsinden hesapladığım servo çıkışını PWM'e dönüştürüp servoya yollamak sende
    // servoların 0 açısını roket gövdesinin doğrultusunda alıyorum. Yani benim 0 derece olarak hesapladığım açı PWM değerinde aslında 90 derece.
    // PWM'deki 0 derece benim için -90 derece. Hesabını ona göre yap. Alttaki için de aynı mevzu geçerli. 
    return yaw_out;
}

float pitch_controller(float pitch_data)
{
    pitch_error = pitch_ref - pitch_data; //pitch_data değerini IMU'dan çekmemiz lazım
    pitch_out = 11*pitch_error - 10.86*pitch_error_prev + 0.08208*pitch_out_prev;
    pitch_out_prev = pitch_out;
    pitch_error_prev = pitch_error;
    pitch_out = saturation(-15, 15, pitch_out); 

    return pitch_out;
}

//// =================================================================== ////

ServoAngle* servo_control(IMU *imu){


	if(imu->servo_delta > 20){
		float yaw_out, pitch_out;

		srv_angle.control_rate = aku_chronometer(&srv_angle.tick);

		yaw_out = yaw_controller(imu->euler.yaw);
		pitch_out = pitch_controller(imu->euler.pitch);

		srv_angle.srv1 = yaw_out; // Servoların düzenlenmesi lazım
		srv_angle.srv2 = pitch_out; // T delta örnekleme süresü -> imu.dataflow_rate ;

		servo1_pwm(srv_angle.srv1);
		servo2_pwm(srv_angle.srv2);

		imu->servo_delta = imu->dataflow_rate;
	}
	else
		imu->servo_delta += imu->dataflow_rate;
	return &srv_angle;
}

