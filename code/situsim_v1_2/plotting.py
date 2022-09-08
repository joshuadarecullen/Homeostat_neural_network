from . import *
from . import timeColouredPlots as tcp
import matplotlib.pyplot as plt

# a function to plot a single robot's trajectory
def plot_robot_path(robot, ts, font_size=12):

    # params for plots: I had to make the font bold and bigger than usual for my fullscreen png saves
    # - (saving as eps or svg gave too large files)
    plt.rcParams["font.weight"] = "bold"
    font_size = 18

    fig, axs = plt.subplots(1, 2)

    # plot robot trajectory
    fig.suptitle('Robot trajectories', fontsize=font_size, fontweight='bold')
    axs[0].plot(robot.xs, robot.ys)
    axs[0].plot(robot.xs[-1], robot.ys[-1], 'r*')
    # fix plot axis proportions to equal
    axs[0].set_aspect('equal')

    # only draw colorbar once
    tcp.doColourVaryingPlot2d(robot.xs, robot.ys, ts, fig, axs[1], map='plasma')
    # make lines and text bold, for full-screen png save to get high resolution
    cbar = axs[1].collections[-1].colorbar
    cbar.set_label(label='time', fontsize=font_size, weight='bold')
    cbar.outline.set_linewidth(3)
    cbar.ax.tick_params(direction='out', length=6, width=3)
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(font_size)

    # used to find min and max coordinate values for setting axis limits
    x_min = 1e6
    x_max = -1e6
    y_min = 1e6
    y_max = -1e6

    # find min and max coordinate values for setting axis limits
    if min(robot.xs) < x_min:
        x_min = min(robot.xs)
    if max(robot.xs) > x_max:
        x_max = max(robot.xs)
    if min(robot.ys) < y_min:
        y_min = min(robot.ys)
    if max(robot.ys) > y_max:
        y_max = max(robot.ys)

    # fix limits and proportions of trajectories plots
    for axes in axs:
        # fix axis limits
        axes.set_xlim([x_min-2, x_max+2])
        axes.set_ylim([y_min-2, y_max+2])
        # fix axis proportions to equal
        axes.set_aspect('equal')

        axes.tick_params(axis='both', which='major', labelsize=font_size)
        axes.tick_params(axis='both', which='minor', labelsize=font_size)
        axes.tick_params(direction='out', length=6, width=3)
        for border in ['top', 'bottom', 'left', 'right']:
            axes.spines[border].set_linewidth(3)

        robot.draw(axes)

# plot a robot's motor commands and actual speeds in vertically arranged subplots
def plot_robot_motors(ts, robot):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(ts, robot.controller.left_speed_commands, label='controller speed setting')
    ax[1].plot(ts, robot.controller.right_speed_commands, label='controller speed setting')
    ax[0].plot(ts, robot.left_motor.speeds, label='actual speed', linewidth='2')
    ax[1].plot(ts, robot.right_motor.speeds, label='actual speed', linewidth='2')
    ax[0].legend()
    ax[1].legend()
    ax[0].set_xlabel('Time')
    ax[1].set_xlabel('Time')
    ax[0].set_ylabel('Speed')
    ax[1].set_ylabel('Speed')
    ax[0].set_title('Left motor')
    ax[1].set_title('Right motor')
    fig.tight_layout()

# plot a robot's sensor outputs in vertically arranged subplots
def plot_robot_sensors(ts, robot):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(ts, robot.left_sensor.activations, label='activation')
    ax[1].plot(ts, robot.right_sensor.activations, label='activation')
    ax[0].legend()
    ax[1].legend()
    ax[0].set_xlabel('Time')
    ax[1].set_xlabel('Time')
    ax[0].set_ylabel('Activation')
    ax[1].set_ylabel('Activation')
    ax[0].set_title('Left sensor')
    ax[1].set_title('Right sensor')
    fig.tight_layout()

# plot a robot's controller outputs
def plot_robot_controller(ts, robot):
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(ts, robot.controller.left_speed_commands, label='controller output')
    ax[1].plot(ts, robot.controller.right_speed_commands, label='controller output')
    ax[0].legend()
    ax[1].legend()
    ax[0].set_xlabel('Time')
    ax[1].set_xlabel('Time')
    ax[0].set_ylabel('Speed command')
    ax[1].set_ylabel('Speed Command')
    ax[0].set_title('Left motor controller output')
    ax[1].set_title('Right motor controller output')
    fig.tight_layout()
