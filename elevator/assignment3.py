import numpy as np
from sim.elevator import sim_run

# Simulator Options
options = {}
options['FIG_SIZE'] = [8, 8] # [Width, Height]
options['PID_DEBUG'] = True

# Physics Options
options['GRAVITY'] = True
options['FRICTION'] = True
options['ELEVATOR_MASS'] = 1000
options['COUNTERWEIGHT_MASS'] = 1000
options['PEOPLE_MASS'] = 50
# Also try 200, 50, and -200.

# Controller Options
options['CONTROLLER'] = True
options['START_LOC'] = 3.0  # Try this set too 27 and
options['SET_POINT'] = 27.0 # set point of 3.
options['OUTPUT_GAIN'] = 2000


class PIDController:
    def __init__(self, reference):
        self.r = reference
        self.prev_time = 0
        self.prev_error = None
        self.integral = 0
        self.output = 0
        self.output_max = 2.5
        self.windup = 4
        # Part of PID DEBUG
        self.output_data = np.array([[0, 0, 0, 0]])

    def run(self, x, t):
        kp = 1
        ki = 0.25
        kd = 5

        # Controller run time.
        if t - self.prev_time < 0.05:
            return self.output
        else:
            dt = t - self.prev_time
            self.prev_time = t
            # INSERT CODE BELOW

            # Calculate error.
            error = self.r - x

            # Calculate proportional control output.
            P_out = kp * error


            # Calculate integral control output.
            # HINT: Use self.integral to store
            # integral values and dt for time difference.
            self.integral += error * dt
            # Prevent windup
            if self.integral > self.windup:
                self.integral = self.windup
            elif self.integral < -1*self.windup:
                self.integral = -1*self.windup
            I_out = self.integral * ki

            # Calculate derivative control output.
            # HINT: Use self.prev_error to store old
            # error values and dt for time difference.
            if self.prev_error != None:
                D_out = kd * ((error - self.prev_error) / dt)
                self.prev_error = error
            else:
                D_out = 0
                # Set this to error.
                self.prev_error = error

            # Calculate final output.
            self.output = P_out + I_out + D_out

            # Set max and min output.
            if self.output > self.output_max:
                self.output = self.output_max
            elif self.output < self.output_max*-1:
                self.output = self.output_max*-1

            # INSERT CODE ABOVE
            self.output_data = np.concatenate((self.output_data, \
                np.array([[t, P_out, I_out, D_out]])))

            return self.output

sim_run(options, PIDController)
