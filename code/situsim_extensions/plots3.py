import sys
# path to folder which contains situsim_v1_2
sys.path.insert(1, '..')
from situsim_v1_2 import *
import numpy as np
import pygame
import matplotlib.pyplot as plt

# plot a list of robots' motor noise in vertically arranged subplots
def plot_all_robots_motor_noise(all_ts, robots):
    fig, ax = plt.subplots(2, 1)
    for i, robot in enumerate(robots):
        if robot.left_motor.noisemaker is not None:
            ax[0].plot(all_ts[i], robot.left_motor.noisemaker.noises, label='robot' + str(i), linewidth='2')
        if robot.right_motor.noisemaker is not None:
            ax[1].plot(all_ts[i], robot.right_motor.noisemaker.noises, label='robot' + str(i), linewidth='2')
        ax[0].legend()
        ax[1].legend()
        ax[0].set_xlabel('Time')
        ax[1].set_xlabel('Time')
        ax[0].set_ylabel('Noise')
        ax[1].set_ylabel('Noise')
        ax[0].set_title('Left motor noise')
        ax[1].set_title('Right motor noise')
    fig.tight_layout()

# plot a list of robots' controller noise in vertically arranged subplots
def plot_all_robots_controller_noise(all_ts, robots):
    fig, ax = plt.subplots(2, 1)
    for i, robot in enumerate(robots):
        if robot.controller.left_noisemaker is not None:
            ax[0].plot(all_ts[i], robot.controller.left_noisemaker.noises, label='robot' + str(i), linewidth='2')
        if robot.controller.right_noisemaker is not None:
            ax[1].plot(all_ts[i], robot.controller.right_noisemaker.noises, label='robot' + str(i), linewidth='2')
        ax[0].legend()
        ax[1].legend()
        ax[0].set_xlabel('Time')
        ax[1].set_xlabel('Time')
        ax[0].set_ylabel('Noise')
        ax[1].set_ylabel('Noise')
        ax[0].set_title('Controller left motor command noise')
        ax[1].set_title('Controller right motor command noise')
    fig.tight_layout()

# plot a list of robots' sensor noise in vertically arranged subplots
def plot_all_robots_sensor_noise(all_ts, robots):
    fig, ax = plt.subplots(2, 1)
    for i, robot in enumerate(robots):
        if robot.left_sensor.noisemaker is not None:
            ax[0].plot(all_ts[i], robot.left_sensor.noisemaker.noises, label='robot' + str(i), linewidth='2')
        if robot.right_sensor.noisemaker is not None:
            ax[1].plot(all_ts[i], robot.right_sensor.noisemaker.noises, label='robot' + str(i), linewidth='2')
        ax[0].legend()
        ax[1].legend()
        ax[0].set_xlabel('Time')
        ax[1].set_xlabel('Time')
        ax[0].set_ylabel('Noise')
        ax[1].set_ylabel('Noise')
        ax[0].set_title('Left sensor noise')
        ax[1].set_title('Right sensor noise')
    fig.tight_layout()
