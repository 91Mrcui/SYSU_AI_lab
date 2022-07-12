# coding: utf-8
"""Defines some frozen lake maps."""
import gym
from gym.envs.toy_text import frozen_lake, discrete
from gym.envs.registration import register

# De-register environments if there is a collision
env_dict = gym.envs.registration.registry.env_specs.copy()
for env in env_dict:
	if 'Deterministic-4x4-FrozenLake-v0' in env:
		del gym.envs.registration.registry.env_specs[env]

	elif 'Deterministic-8x8-FrozenLake-v0' in env:
		del gym.envs.registration.registry.env_specs[env]

	elif 'Stochastic-4x4-FrozenLake-v0' in env:
		del gym.envs.registration.registry.env_specs[env]


register(
    id='Deterministic-4x4-FrozenLake-v0',
    entry_point='gym.envs.toy_text.frozen_lake:FrozenLakeEnv',
    kwargs={'map_name': '4x4',
            'is_slippery': False})

register(
    id='Deterministic-8x8-FrozenLake-v0',
    entry_point='gym.envs.toy_text.frozen_lake:FrozenLakeEnv',
    kwargs={'map_name': '8x8',
            'is_slippery': False})

register(
    id='Stochastic-4x4-FrozenLake-v0',
    entry_point='gym.envs.toy_text.frozen_lake:FrozenLakeEnv',
    kwargs={'map_name': '4x4',
            'is_slippery': True})