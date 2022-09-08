from .base import *
from .stimuli import *
from .sensors import *
from .motors import *

# the base class for differential drive robots. with default parameters, its morphology is like that of a Braitenberg
# vehicle type robot
class Robot(Agent):

    # construct robot
    def __init__(self, x, y, controller, left_light_sources=[],
                 right_light_sources=[], radius=1, theta=0,
                 left_sensor_angle=np.pi/4,
                 right_sensor_angle=-np.pi/4,
                 left_sensor_noisemaker=None, right_sensor_noisemaker=None, field_of_view=2*np.pi, max_speed=1, inertia_coeff=0,
                 left_motor_noisemaker=None, right_motor_noisemaker=None,
                 left_motor_max_speed=2, right_motor_max_speed=2,
                 left_motor_inertia=0, right_motor_inertia=0,
                 left_motor_reversed=False, right_motor_reversed=False
                 ):
        super().__init__(x, y, theta)  # call Agent constructor
        self.controller = controller  # the controller for the robot, which will set motor speeds according to how stimulated the robot's sensors are
        self.radius = radius  # the radius of the robot's body
        self.state = np.array([x, y, theta]) # the robot's state: position and orientation
        self.left_sensor_angle = left_sensor_angle # sensor orientations
        self.right_sensor_angle = right_sensor_angle
        self.left_sensor = LightSensor(light_sources=left_light_sources, x=x, y=y, noisemaker=left_sensor_noisemaker, field_of_view=field_of_view) # construct left sensor. at this point, dummy positions are given for light sensors. they will be fixed when self.update_sensor_postions() is called
        self.right_sensor = LightSensor(light_sources=right_light_sources, x=x, y=y, noisemaker=right_sensor_noisemaker, field_of_view=field_of_view) # construct right sensor
        self.update_sensor_postions()  # update sensor positions according to robot's state
        self.left_motor = Motor(max_speed=left_motor_max_speed, motor_inertia_coeff=left_motor_inertia, reversed=left_motor_reversed, noisemaker=left_motor_noisemaker)
        self.right_motor = Motor(max_speed=right_motor_max_speed, motor_inertia_coeff=right_motor_inertia, reversed=right_motor_reversed, noisemaker=right_motor_noisemaker)

    # update sensor positions according to robot's state
    def update_sensor_postions(self):
        self.left_sensor.x = self.state[0] + (self.radius * np.cos(self.state[2] + self.left_sensor_angle))
        self.left_sensor.y = self.state[1] + (self.radius * np.sin(self.state[2] + self.left_sensor_angle))
        self.left_sensor.theta = self.thetas[-1] + self.left_sensor_angle
        self.right_sensor.x = self.state[0] + (self.radius * np.cos(self.state[2] + self.right_sensor_angle))
        self.right_sensor.y = self.state[1] + (self.radius * np.sin(self.state[2] + self.right_sensor_angle))
        self.right_sensor.theta = self.thetas[-1] + self.right_sensor_angle

    # step the robot in time
    def step(self, dt):
        # calculate light sensor positions
        self.update_sensor_postions()

        # get motor speeds from control method
        controller_left_speed, controller_right_speed = self.control(dt)


        left_speed = self.left_motor.step(controller_left_speed, dt)
        right_speed = self.right_motor.step(controller_right_speed, dt)

        self.integrate(left_speed, right_speed, dt)

        super().step(dt)  # step is not implemented in Agent, so this call goes to System
        self.thetas.append(self.state[2])  # store orientation

    # this is separated from the step method in case we want to override it
    # - one example of why we might want to do this is if we wanted to add collisions
    #   to the simulation. to achieve this, we could do something like create a subclass of
    #   Robot, with its own integrate method, which calls this one and then superimposes
    #   an additional movement due to collisions
    def integrate(self, left_speed, right_speed, dt):

        """Applies a motor activation vector to an agent state, and simulates
        the consequences using Euler integration over a dt interval."""
        # calculate the linear speed and angular speed
        v = np.mean([left_speed, right_speed])
        omega = (right_speed - left_speed) / (2.0 * self.radius)

        # calculate time derivative of state
        deriv = [v * np.cos(self.state[2]), v * np.sin(self.state[2]), omega]

        # perform Euler integration
        self.state = dt * np.array(deriv) + self.state

        # store robot state
        self.x = self.state[0]
        self.y = self.state[1]

    # this is separated from the step method as it is easier to override in any subclasses of Robot than step, which
    # should be the same for all Robots
    # - the reason we would do this is if we wanted to change the number or kinds of input
    #   which the Robot would have (e.g. because we want to use more than two sensors)
    def control(self, dt):
        # update sensor measurements
        left_activation = self.left_sensor.step(dt)
        right_activation = self.right_sensor.step(dt)

        # get motor speeds from controller
        left_speed, right_speed = self.controller.step([left_activation, right_activation], dt)
        # return speeds to step method
        return left_speed, right_speed

    # draw robot in the specified matplotlib axes
    def draw(self, ax):
        ax.plot([self.state[0], self.state[0]+self.radius*np.cos(self.state[2])],
                 [self.state[1], self.state[1]+self.radius*np.sin(self.state[2])], 'k--', linewidth='2')
        ax.add_artist(mpatches.Circle((self.state[0], self.state[1]), self.radius))
        wheels = [mpatches.Rectangle((-0.5*self.radius, y), width=self.radius, height=0.2*self.radius, color="black") for y in (-1.1*self.radius, 0.9*self.radius)]
        tr = mtransforms.Affine2D().rotate(self.state[2]).translate(self.state[0], self.state[1]) + ax.transData
        for wheel in wheels:
            wheel.set_transform(tr)
            ax.add_artist(wheel)

        self.left_sensor.draw(ax)
        self.right_sensor.draw(ax)

        self.draw_fov(self.left_sensor, ax)
        self.draw_fov(self.right_sensor, ax)

    # draw lines indicating field of view in matplotlib axes
    def draw_fov(self, sensor, ax):
        left_end_x, left_end_y, right_end_x, right_end_y = self.fov_ends(sensor)
        ax.plot([sensor.x, left_end_x],
                 [sensor.y, left_end_y], 'b--', linewidth='2')
        ax.plot([sensor.x, right_end_x],
                 [sensor.y, right_end_y], 'b--', linewidth='2')

    # calculate end coords of lines indicating field of view
    def fov_ends(self, sensor):
         left_end_x = sensor.x + np.cos(sensor.theta + sensor.field_of_view/2)
         left_end_y = sensor.y + np.sin(sensor.theta + sensor.field_of_view/2)
         right_end_x = sensor.x + np.cos(sensor.theta - sensor.field_of_view/2)
         right_end_y = sensor.y + np.sin(sensor.theta - sensor.field_of_view/2)
         return left_end_x, left_end_y, right_end_x, right_end_y

    # draw robot in a pygame display
    def pygame_draw(self, screen, scale, shiftx, shifty):
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color='darkblue', radius=scale*self.radius)

        self.left_sensor.pygame_draw(screen, scale, shiftx, shifty)
        self.right_sensor.pygame_draw(screen, scale, shiftx, shifty)

        self.pygame_draw_fov(self.left_sensor, screen, scale, shiftx, shifty)
        self.pygame_draw_fov(self.right_sensor, screen, scale, shiftx, shifty)

    # draw lines indicating field of view in pygame display
    def pygame_draw_fov(self, sensor, screen, scale, shiftx, shifty):
        left_end_x, left_end_y, right_end_x, right_end_y = self.fov_ends(sensor)
        pygame.draw.line(screen, color='green',
                         start_pos=(scale * sensor.x + shiftx, scale * sensor.y + shifty),
                         end_pos=(scale * left_end_x + shiftx, scale * left_end_y + shifty), width=2)
        pygame.draw.line(screen, color='green',
                         start_pos=(scale * sensor.x + shiftx, scale * sensor.y + shifty),
                         end_pos=(scale * right_end_x + shiftx, scale * right_end_y + shifty), width=2)
