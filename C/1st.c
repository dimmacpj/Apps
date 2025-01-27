#include <stdio.h>
#include <stdbool.h>

#define FAN_RAMP_TIME (60000)  // [ms]
#define FAN_OFF_SPEED (0.0)
#define FAN_FULL_SPEED (1.0)
#define FAN_START_SPEED (0.15)
#define FAN_OFF_TEMP (35.0)
#define FAN_ON_TEMP (40.0)

int main(void)
{
    int fan_ramp_timer = 0;
    float ntc_pcb_temperature = 41.0;
    float ntc_1_temperature = 41.0;
    float ntc_2_temperature = 41.0;
    float fan_speed_demand = 0.0;

    while (1)
    {
        if ((ntc_pcb_temperature > FAN_ON_TEMP) || (ntc_1_temperature > FAN_ON_TEMP) || (ntc_2_temperature > FAN_ON_TEMP))
        {   // Turn fan(s) on at [40]degC
            if ((fan_ramp_timer == 0) && (fan_speed_demand == FAN_OFF_SPEED))
            {   // Fans ramp from 15% speed to 100% speed over 60s
                fan_speed_demand = FAN_START_SPEED;
                fan_ramp_timer++;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }
            else if ((fan_ramp_timer <= FAN_RAMP_TIME) && (fan_ramp_timer > 0)) 
            {
                fan_speed_demand = fan_speed_demand + ((FAN_FULL_SPEED - FAN_START_SPEED)/FAN_RAMP_TIME);
                fan_ramp_timer++;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }
            else if (fan_ramp_timer > FAN_RAMP_TIME)
            {
                fan_speed_demand = FAN_FULL_SPEED;
                fan_ramp_timer = 0;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }  
            else if ((fan_ramp_timer == 0) && (fan_speed_demand == FAN_FULL_SPEED))
            {
                fan_speed_demand = FAN_FULL_SPEED;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }
        }
        else if ((ntc_pcb_temperature < FAN_OFF_TEMP) && (ntc_1_temperature < FAN_OFF_TEMP) && (ntc_2_temperature < FAN_OFF_TEMP))
        {   // Turn fan(s) off at [35]degC
            if (fan_ramp_timer <= FAN_RAMP_TIME)
            {   // Fans ramp from 100% speed to 15% speed over 60s then turns off
                fan_speed_demand = fan_speed_demand - ((FAN_FULL_SPEED - FAN_START_SPEED)/FAN_RAMP_TIME);
                fan_ramp_timer++;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }
            else if (fan_ramp_timer > FAN_RAMP_TIME)
            {
                fan_speed_demand = FAN_OFF_SPEED;
                fan_ramp_timer = 0;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }
            else if ((fan_ramp_timer == 0) && (fan_speed_demand == FAN_OFF_SPEED)) 
            {
                fan_speed_demand = FAN_OFF_SPEED;
                printf("fan ramp timer is %d, fan speed demand is %f", fan_ramp_timer, fan_speed_demand);
            }  
        } 
    }
    
    
}