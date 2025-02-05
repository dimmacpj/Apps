uint32_t ramp_fan_up(uint32_t current_speed_demand)
{
	if (current_speed_demand < FAN_START_SPEED)
    { // Ramp fans up from 15% speed to 100% speed over 60s (if current speed is >15% ramp up at the same rate resulting in getting to 100% faster)
		current_speed_demand = FAN_START_SPEED;
	}
	else if (current_speed_demand < (FAN_FULL_SPEED - FAN_SPEED_RAMP_RATE))
	{
		current_speed_demand += FAN_SPEED_RAMP_RATE;
	}
	else if (current_speed_demand >= (FAN_FULL_SPEED - FAN_SPEED_RAMP_RATE))
	{
		current_speed_demand = FAN_FULL_SPEED;
	}
	return current_speed_demand;
}

uint32_t ramp_fan_down(uint32_t current_speed_demand)
{
	 if (current_speed_demand > (FAN_OFF_SPEED + FAN_SPEED_RAMP_RATE))
	{ //Ramp fans down from 100% speed to 15% speed over 60s then turns off (if current speed is <100% ramp down at the same rate resulting in getting to 15% faster, then off)
		current_speed_demand -= FAN_SPEED_RAMP_RATE;
	}
	else if (current_speed_demand <= (FAN_OFF_SPEED + FAN_SPEED_RAMP_RATE))
	{
		current_speed_demand = FAN_OFF_SPEED;
	}
	return current_speed_demand;
}

uint32_t adjust_fan_speed_by_temp(float32_t ntc_temp)
{
	return ((ntc_temp - FAN_ON_OFF_TEMP) * (FAN_FULL_SPEED - FAN_START_SPEED) / (FAN_FULL_SPEED_TEMP - FAN_ON_OFF_TEMP) + FAN_START_SPEED);
}
