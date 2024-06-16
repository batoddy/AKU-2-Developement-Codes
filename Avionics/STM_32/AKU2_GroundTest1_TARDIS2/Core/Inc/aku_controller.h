
#ifndef INC_AKU_CONTROLLER_H_
#define INC_AKU_CONTROLLER_H_

#include "aku_structure.h"

float yaw_controller(float yaw_data);
float pitch_controller(float pitch_data);
float saturation(float min, float max, float value);

ServoAngle* servo_control(IMU* imu);

#endif
