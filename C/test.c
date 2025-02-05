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
#define FAN_START_TIME (5000) // [ms]

#define FAN_OFF_SPEED (0.0f)
#define FAN_FULL_SPEED (1.0f)
#define FAN_START_SPEED (0.15f)
#define FAN_SPEED_RAMP_RATE (0.000014f)
#define FAN_FULL_SPEED_TEMP (50.0f)
#define FAN_ON_OFF_TEMP (40.0f)
#define FAN_ON_TEMP (40.0f)
#define FAN_OFF_TEMP (35.0f)


/* This task must be suspended until EEPROM has been initialised */
portTASK_FUNCTION(Control_Task, pvParameters)
{
  TickType_t last_wake_time;
  uint32_t cnt_1s = 1;                      // counter to time 1s periods
  uint32_t fan1_on_blank_time = 0;
  uint32_t fan2_on_blank_time = 0;
  bool fan1_on = false;
  bool fan2_on = false;

  ( void ) pvParameters; // Stop compiler warning for unused parameter

  printf("Control Task start.\n");

  adc_hardware_init();

  last_wake_time = xTaskGetTickCount();
  /* drop into the main control loop */
  while (1)
  {
//#if 0 // monitor control
    if (fans_on)
    { // Turn fan(s) on when sent a CM = 1 message
      ramp_fan_up(fan_speed_demand);
    }
    else
    { //// Turn fan(s) off when sent a CM = 0 message (if two ports that have had a CM=1, need both to send a CM=0)
      if (ntc_1_temperature < FAN_ON_OFF_TEMP)
      {
		ramp_fan_down(fan_speed_demand);
      }
      else if (ntc_1_temperature < FAN_FULL_SPEED_TEMP)
      { // When modules are all off but T1 is above [40]degC turn fans on at 15% speed and linearly increase speed to 100% at [50]degC
        fan_speed_demand = adjust_fan_speed_by_temp(ntc_1_temperature);
      }
      else
      { //maintain 100% speed above [50]degC
		ramp_fan_up(fan_speed_demand);
      }
    }
//#else   // temporay control without monitor
    if (ntc_1_temperature >= FAN_ON_TEMP) 
    {   // Turn fan(s) on at [40]degC
		ramp_fan_up(fan_speed_demand);
    }
    else if (ntc_1_temperature <= FAN_OFF_TEMP)
    {   // Turn fan(s) off at [35]degC
		ramp_fan_down(fan_speed_demand);
    } 
//#endif

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

