import sys
# path folder which contains situsim_v1_2
sys.path.insert(1, '..')
from situsim_v1_2 import *
import numpy as np
import pygame
import matplotlib.pyplot as plt


# unfortunately, this only works correctly if all time series have the same length
# - if different runs have different lengths, then the colors cannot be trusted,
#   as the colorbar only applies to the longest of all the runs
#   - it is not possible to fix this from here (as far as I could discover)
#       - at some later time, doColourVaryingPlot2d will need to be modified
def plot_all_agents_trajectories(all_ts, agents, light_sources, draw_agents=False):
        # figure for multiple agent trajectories (potentially, but not in this case)
        fig, ax = plt.subplots(1, 1)

        longest_len = 0
        longest_ind = 0
        for i, ts in enumerate(all_ts):
            l = len(ts)
            if l > longest_len:
                longest_len = l
                longest_ind = i

        # for all agents, plot trajectories
        for i, agent in enumerate(agents):
            tcp.doColourVaryingPlot2d(agent.xs, agent.ys, all_ts[i], fig, ax, map='plasma', showBar=i==longest_ind)  # only draw colorbar once

        # draw all sources
        for source in light_sources:
            source.draw(ax)
        # draw all agents
        x_min = 1E6
        y_min = 1E6
        x_max = -1E6
        y_max = -1E6
        for agent in agents:
            if draw_agents:
                agent.draw(ax)
            else:
                ax.plot(agent.xs[-1], agent.ys[-1], 'r*')
            agent_min_x = min(agent.xs)
            agent_max_x = max(agent.xs)
            agent_min_y = min(agent.ys)
            agent_max_y = max(agent.ys)
            if agent_min_x < x_min:
                x_min = agent_min_x
            if agent_max_x > x_max:
                x_max = agent_max_x
            if agent_min_y < y_min:
                y_min = agent_min_y
            if agent_max_y > y_max:
                y_max = agent_max_y
        # fix plot axis proportions to equal
        ax.set_aspect('equal')
        # set axis limits based on robots' trajectories - this is sometimes necessary
        # because of a bug in my tcp.doColourVaryingPlot2d code
        ax.set_xlim([x_min-5, x_max+5])
        ax.set_ylim([y_min-5, y_max+5])

# plot a list of robots' sensor outputs - for a robot with only 2 sensors
def plot_all_robots_sensors(all_ts, robots):
    fig, ax = plt.subplots(2, 1)
    for i, robot in enumerate(robots):
        ax[0].plot(all_ts[i], robot.left_sensor.activations, label='robot' + str(i))
        ax[1].plot(all_ts[i], robot.right_sensor.activations, label='robot' + str(i))
        ax[0].legend()
        ax[1].legend()
        ax[0].set_xlabel('Time')
        ax[1].set_xlabel('Time')
        ax[0].set_ylabel('Activation')
        ax[1].set_ylabel('Activation')
        ax[0].set_title('Left sensor')
        ax[1].set_title('Right sensor')
    fig.tight_layout()

# plot a list of robots' controller outputs (i.e. motor input commands)
def plot_all_robots_controllers(all_ts, robots):
    fig, ax = plt.subplots(2, 1)
    for i, robot in enumerate(robots):
        ax[0].plot(all_ts[i], robot.controller.left_speed_commands, label='robot' + str(i))
        ax[1].plot(all_ts[i], robot.controller.right_speed_commands, label='robot' + str(i))
        ax[0].legend()
        ax[1].legend()
        ax[0].set_xlabel('Time')
        ax[1].set_xlabel('Time')
        ax[0].set_ylabel('Speed command')
        ax[1].set_ylabel('Speed Command')
        ax[0].set_title('Left motor controller output')
        ax[1].set_title('Right motor controller output')
    fig.tight_layout()

# plot a list of robots' actual motor speeds in vertically arranged subplots
def plot_all_robots_motors(all_ts, robots):
    fig, ax = plt.subplots(2, 1)
    for i, robot in enumerate(robots):
        # ax[0].plot(all_ts[i], robot.controller.left_speed_commands, label='robot' + str(i))
        # ax[1].plot(all_ts[i], robot.controller.right_speed_commands, label='robot' + str(i))
        ax[0].plot(all_ts[i], robot.left_motor.speeds, label='robot' + str(i), linewidth='2')
        ax[1].plot(all_ts[i], robot.right_motor.speeds, label='robot' + str(i), linewidth='2')
        ax[0].legend()
        ax[1].legend()
        ax[0].set_xlabel('Time')
        ax[1].set_xlabel('Time')
        ax[0].set_ylabel('Speed')
        ax[1].set_ylabel('Speed')
        ax[0].set_title('Left motor')
        ax[1].set_title('Right motor')
    fig.tight_layout()
