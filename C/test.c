/**************************************************************************//**
  \file   control.c
  \brief  control and monitoring of the Fan's task

******************************************************************************/
/* FreeRTOS */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#include <stdbool.h>
#include <stdio.h>

#include "ena_datatype.h"
#include "ena_maths.h"

/* Hardware and board configuration */
#include "hardware.h"
#include "variants.h"

#include "events.h"
#include "fan.h"

#define DEFINE_VARS
#include "control.h"                        /* includes global variables */
#undef DEFINE_VARS

#include "main.h"
#include "watchdog.h"
#include "adc.h"
#include "db_table.h"

#define DEBUG 0
#if DEBUG
#define PRINTF(...) printf(__VA_ARGS__)
#else
#define PRINTF(...)
#endif

#define TASK_RATE (1) /* 1ms / 1kHz */
#define TASK_1S_PERIOD (1000)
#define FAN_RAMP_TIME (60000)  // [ms]
#define FAN_START_TIME (5000) // [ms]
#define FAN_OFF_SPEED (0.0)
#define FAN_FULL_SPEED (1.0)
#define FAN_START_SPEED (0.15)
#define FAN_SPEED_INCREAMENT (0.000014)
#define FAN_OFF_TEMP (35.0)
#define FAN_ON_TEMP (40.0)

/* This task must be suspended until EEPROM has been initialised */
portTASK_FUNCTION(Control_Task, pvParameters)
{
  TickType_t last_wake_time;
  uint32_t cnt_1s = 1;                      // counter to time 1s periods
  uint32_t fan1_on_blank_time = 0;
  uint32_t fan2_on_blank_time = 0;
  uint32_t fan_ramp_timer = 0;
  bool fan1_on = false;
  bool fan2_on = false;

  ( void ) pvParameters; // Stop compiler warning for unused parameter

  printf("Control Task start.\n");

  adc_hardware_init();

  last_wake_time = xTaskGetTickCount();
  /* drop into the main control loop */
  while (1)
  {   
    if (ntc_1_temperature >= FAN_ON_TEMP) 
    {   // Turn fan(s) on at [40]degC
      if ((fan_ramp_timer == 0) && (fan_speed_demand < FAN_START_SPEED))
      {   // Fans ramp from 15% speed to 100% speed over 60s
        fan_speed_demand = FAN_START_SPEED;
        fan_ramp_timer++;
      }
      else if ((fan_ramp_timer <= FAN_RAMP_TIME) && (fan_ramp_timer != 0)) 
      {
        fan_speed_demand += FAN_SPEED_INCREAMENT;
        fan_ramp_timer++;
      }
      else if (fan_ramp_timer > FAN_RAMP_TIME)
      {
        fan_speed_demand = FAN_FULL_SPEED;
        fan_ramp_timer = 0;
      }  
      else if ((fan_ramp_timer == 0) && (fan_speed_demand > (FAN_FULL_SPEED - FAN_SPEED_INCREAMENT)))
      {
        fan_speed_demand = FAN_FULL_SPEED;
      }
    }
    else if (ntc_1_temperature <= FAN_OFF_TEMP)
    {   // Turn fan(s) off at [35]degC
      if ((fan_ramp_timer <= FAN_RAMP_TIME) && (fan_speed_demand > (FAN_OFF_SPEED + FAN_SPEED_INCREAMENT)))
      {   // Fans ramp from 100% speed to 15% speed over 60s then turns off
        fan_speed_demand -= FAN_SPEED_INCREAMENT;
        fan_ramp_timer++;
      }
      else if (fan_ramp_timer > FAN_RAMP_TIME)
      {
        fan_speed_demand = FAN_OFF_SPEED;
        fan_ramp_timer = 0;
      }
      else if ((fan_ramp_timer == 0) && (fan_speed_demand < (FAN_OFF_SPEED + FAN_SPEED_INCREAMENT)))
      {
        fan_speed_demand = FAN_OFF_SPEED;
      }  
    } 
    
    set_fan_speed(fan_speed_demand);

    if(fan_speed_demand > FAN_OFF_SPEED)
    {
      if(fan1_on_blank_time >= FAN_START_TIME)
      {  // Delay to give time for the fan to spin up and the tacho to be read
        fan1_on = true;
      }
      else
      {
        fan1_on_blank_time++;
      }

      if(fan2_on_blank_time >= FAN_START_TIME)
      {  // Delay to give time for the fan to spin up and the tacho to be read
        fan2_on = true;
      }
      else
      {
        fan2_on_blank_time++;
      }
    }
    else
    {
      fan1_on = false;
      fan1_on_blank_time = 0;
      fan2_on = false;
      fan2_on_blank_time = 0;
    }

    /* update the fan rpm from the tacho every 1s */
    if(cnt_1s >= TASK_1S_PERIOD)
    {
      fan1_rpm = (int16_t)get_fan1_tacho(fan_pulses_per_rev);
      fan2_rpm = (int16_t)get_fan2_tacho(fan_pulses_per_rev);

      /* if the fans are on then check the fan speed is above min rpm */
      if(fan1_on)
      {
        if(fan1_rpm < fan_min_rpm)
        {
          BB(pbb_alarms, FLT_FAN1_FAIL) = 1;
        }
        else
        {
          BB(pbb_alarms, FLT_FAN1_FAIL) = 0;
        }
      }
      else
      {
        BB(pbb_alarms, FLT_FAN1_FAIL) = 0;
      }

      if(fan2_on)
      {
        if(fan2_rpm < fan_min_rpm)
        {
          BB(pbb_alarms, FLT_FAN2_FAIL) = 1;
        }
        else
        {
          BB(pbb_alarms, FLT_FAN2_FAIL) = 0;
        }
      }
      else
      {
        BB(pbb_alarms, FLT_FAN2_FAIL) = 0;
      }

      cnt_1s = 0;
    }

    cnt_1s++;

    alarms_latched |= alarms;
    update_alarm_mono(&alarms_mono, alarms, false);   // update fault and warning status bit monostables

    vTaskDelayUntil(&last_wake_time, TASK_RATE);
  } /* while (1) */
} /* portTASK_FUNCTION(Control_Task, pvParameters) */

#define CONTROL_TASK_STACK_SIZE (configMINIMAL_STACK_SIZE + 20)

TaskHandle_t control_task_create(void)
{
  static StaticTask_t control_task_buffer;
  static StackType_t control_task_stack[CONTROL_TASK_STACK_SIZE];

  return(xTaskCreateStatic(Control_Task, "MAIN", CONTROL_TASK_STACK_SIZE, NULL, CONTROL_TASK_PRIORITY, control_task_stack, &control_task_buffer));
}

