import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../..')
from situsim_v1_2 import *

import pygame
import matplotlib.pyplot as plt
import time

# compute average error over the robot's trajectory
def cost_function(robot):
    dists = np.sqrt(np.square(robot.xs) + np.square(robot.ys)) - 5 # 5 is the target circle radius
    return np.mean(np.abs(dists))

# generate a circular arrangement of light sources
def sources_circle(n=20, r=9):
    sources = []
    for i in range(n):
        a = i * 2*np.pi / n
        sources.append(LightSource(r * np.cos(a), r * np.sin(a)))
    return sources

# A subclass of NoisyController
class OpenLoopCircleController(Controller):

    # init controller with passed in noisemakers and control parameters
    def __init__(self, left_noisemaker, right_noisemaker, speed=1, ratio=0.5):
        # NOTE: THIS CALL TO SUPER MUST BE HERE FOR NOISYCONTROLLERS!
        super().__init__(left_noisemaker, right_noisemaker) # call NoisyController.__init__() to set up noisemakers
        self.speed = speed
        self.ratio = ratio

    # step method. depending on the values of speed and ratio, the robot will drive along a circular path
    #   - but noise will be added to the control outputs, so the robot might not achieve its goal!
    def step(self, inputs, dt):

        # set left motor speed to speed parameter
        self.left_speed_command = self.speed
        # set right motor speed to a larger/smaller value to make the robot turn
        self.right_speed_command = self.speed * self.ratio

        return super().step(inputs, dt)

def setup_pygame_window(screen_width):
    # initialise pygame and set parameters
    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_width])
    # scale factor and offsets for converting simulation coordinates to pygame animation display coordinates
    pygame_scale = 30
    pygame_x_offset = screen_width/2
    pygame_y_offset = screen_width/2

    return screen


# draw SituSim agents in pygame window
def pygame_drawsim(screen, systems, width, paused, delay):

    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                delay -= 1
            elif event.key == pygame.K_DOWN:
                delay += 1

    delay = np.max([delay, 0])

    time.sleep(delay/100)

    screen.fill('black')

    # initial scale factor and offsets for converting simulation coordinates
    # to pygame animation display coordinates
    pygame_x_offset = width/2
    pygame_y_offset = width/2

    # find extremes of system trajectories for resizing animation window
    max_xs = []
    max_ys = []
    for system in systems:
        if system.has_position:
            max_xs.append(max(np.abs(system.xs)))
            max_ys.append(max(np.abs(system.ys)))

    # reset scale according to where systems are and have been
    pygame_scale = width / (2 * max(max(max_xs), max(max_ys)) + 1)

    # draw all systems
    for system in systems:
        system.pygame_draw(screen, scale=pygame_scale, shiftx=pygame_x_offset, shifty=pygame_y_offset)

    # flip the pygame display
    screen.blit(pygame.transform.flip(screen, False, True), (0, 0))
    # update the pygame display
    pygame.display.update()

    return running, paused, delay

# main function, to run simulation and generate plots
def run_simulation(speed, screen_width, animate=False, left_noise=0, right_noise=0):

    # set up light sources
    light_sources = sources_circle(r=5)

    # start with no noise
    left_noisemaker = None
    right_noisemaker = None

    #
    if left_noise > 0:
        left_noisemaker = BrownNoiseSource(left_noise)
    if right_noise > 0:
        right_noisemaker = BrownNoiseSource(right_noise)

    # create a controller object to pass to the robot
    controller = OpenLoopCircleController(left_noisemaker=left_noisemaker,
                                          right_noisemaker=right_noisemaker,
                                          speed=1.5, ratio=0.5)

    # construct the robot
    robot = Robot(x=-5, y=0, theta=np.pi/2,
                  controller=controller,
                  field_of_view=0.9*np.pi,
                  left_light_sources=light_sources,
                  right_light_sources=light_sources,
                  left_motor_inertia=100,
                  right_motor_inertia=100
                  )

    # create list of agents - even though we only have one here, I always code
    # using a list, as it makes it easy to add more agents
    agents = [robot]

    # only run pygame code if animating the simulation
    if animate:
        screen = setup_pygame_window(screen_width)

    # animation variables
    delay = 0 # can be used to slow animation down
    running = True # can be used to exit animation early
    paused = False # can be used to pause simulation/animation

    # prepare simulation time variables
    t = 0
    ts = [t]
    dt = 0.1
    # begin simulation main loop
    while t < 60 and running:

        # only move simulation forwards in time if not paused
        if not paused:
            # step all robots
            for agent in agents:
                agent.step(dt)

            # increment time variable and store in ts list for plotting later
            t += dt
            ts.append(t)

        # only run pygame code if animating the simulation
        if animate:
            running, paused, delay = pygame_drawsim(screen, agents + light_sources, screen_width, paused, delay)
    # simulation has completed

    # only run pygame code if animating the simulation
    if animate:
        # Quit pygame.
        pygame.display.quit()
        pygame.quit()

    # our objective is to minimise this error
    print("Average error over time = " + str(cost_function(robot)))

    '''

     do matplotlib plots of robot's trajectory and variables

    '''

    # parameters for plots
    plt.rcParams["font.weight"] = "bold"
    font_size = 18

    # figure for multiple agent trajectories (potentially, but not in this case)
    fig, ax = plt.subplots(1, 1)

    # for all agents, plot trajectories
    for agent in agents:
        # plot agent trajectory
        tcp.doColourVaryingPlot2d(robot.xs, agent.ys, ts, fig, ax, map='plasma', showBar=True)  # only draw colorbar once
    # draw all sources
    for source in light_sources:
        source.draw(ax)
    # draw all agents
    for agent in agents:
        agent.draw(ax)

    # generate coordinates for drawing circular target path
    angles = np.linspace(start=0, stop=2*np.pi, num=60)
    radius = 5
    circle_xs = radius * np.cos(angles)
    circle_ys = radius * np.sin(angles)
    # draw circular target path
    ax.plot(circle_xs, circle_ys, 'r--')

    # fix plot axis proportions to equal
    ax.set_aspect('equal')
    # set axis limits based on robot's trajectory - this is sometimes necessary
    # because of a bug in my tcp.doColourVaryingPlot2d code
    ax.set_xlim([min(agents[0].xs)-5, max(agents[0].xs)+5])
    ax.set_ylim([min(agents[0].ys)-5, max(agents[0].ys)+5])

    # unlike the plot above, these are for just one robot
    plot_robot_motors(ts, robot)
    plot_robot_controller(ts, robot)
    plot_robot_sensors(ts, robot)

    plt.show()

# run the simulation once, with the given parameters
run_simulation(speed=1,
                screen_width=1800,
                animate=True,
                left_noise=0,
                right_noise=0)
