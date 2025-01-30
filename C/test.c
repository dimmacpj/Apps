// ... existing code ...

void update_fan_speed(bool fans_on, float32_t ntc_1_temperature)
{
    if (fans_on)
    {
        update_fan_speed_on();
    }
    else
    {
        update_fan_speed_off(ntc_1_temperature);
    }
}

void update_fan_speed_on(void)
{
    if (fan_ramp_timer == 0 && fan_speed_demand < FAN_START_SPEED)
    {
        fan_speed_demand = FAN_START_SPEED;
        fan_ramp_timer++;
        return;
    }

    if (fan_ramp_timer <= FAN_RAMP_TIME && fan_ramp_timer != 0)
    {
        fan_speed_demand += FAN_SPEED_INCREAMENT;
        fan_ramp_timer++;
        return;
    }

    if (fan_ramp_timer > FAN_RAMP_TIME)
    {
        fan_speed_demand = FAN_FULL_SPEED;
        fan_ramp_timer = 0;
        return;
    }

    if (fan_ramp_timer == 0 && fan_speed_demand > (FAN_FULL_SPEED - FAN_SPEED_INCREAMENT))
    {
        fan_speed_demand = FAN_FULL_SPEED;
    }
}

void update_fan_speed_off(float32_t ntc_1_temperature)
{
    if (fan_ramp_timer <= FAN_RAMP_TIME && fan_speed_demand > (FAN_OFF_SPEED + FAN_SPEED_INCREAMENT))
    {
        fan_speed_demand -= FAN_SPEED_INCREAMENT;
        fan_ramp_timer++;
        return;
    }

    if (fan_ramp_timer > FAN_RAMP_TIME)
    {
        fan_speed_demand = FAN_OFF_SPEED;
        fan_ramp_timer = 0;
        return;
    }

    if (fan_ramp_timer == 0 && fan_speed_demand < (FAN_OFF_SPEED + FAN_SPEED_INCREAMENT))
    {
        adjust_fan_speed_by_temperature(ntc_1_temperature);
    }
}

void adjust_fan_speed_by_temperature(float32_t ntc_1_temperature)
{
    if (ntc_1_temperature < FAN_ON_OFF_TEMP)
    {
        fan_speed_demand = FAN_OFF_SPEED;
        return;
    }

    if (ntc_1_temperature <= FAN_FULL_SPEED_TEMP)
    {
        fan_speed_demand = (ntc_1_temperature - FAN_ON_OFF_TEMP) * (FAN_FULL_SPEED - FAN_START_SPEED) / (FAN_FULL_SPEED_TEMP - FAN_ON_OFF_TEMP) + FAN_START_SPEED;
        return;
    }

    fan_speed_demand = FAN_FULL_SPEED;
}

// ... existing code ...

// In the main control loop:
update_fan_speed(fans_on, ntc_1_temperature);

// ... existing code ...


// old code below

    if (fans_on) 
    {   // Turn fan(s) on when sent a CM = 1 message
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
    else
    {   // Turn fan(s) off when sent a CM = 0 message (if two ports that have had a CM=1, need both to send a CM=0)
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
        if (ntc_1_temperature < FAN_ON_OFF_TEMP)
        {
          fan_speed_demand = FAN_OFF_SPEED;
        }
        else if ((ntc_1_temperature >= FAN_ON_OFF_TEMP) && (ntc_1_temperature <= FAN_FULL_SPEED_TEMP)) 
        { // When modules are all off but T1 is above [40]degC turn fans on at 15% speed and linearly increase speed to 100% at [50]degC (maintain 100% speed above [50]degC)
          fan_speed_demand = (ntc_1_temperature - FAN_ON_OFF_TEMP) * (FAN_FULL_SPEED - FAN_START_SPEED) / (FAN_FULL_SPEED_TEMP - FAN_ON_OFF_TEMP) + FAN_START_SPEED;
        } 
        else if (ntc_1_temperature > FAN_FULL_SPEED_TEMP) 
        {
          fan_speed_demand = FAN_FULL_SPEED;
        }
      } 
      
    } 
