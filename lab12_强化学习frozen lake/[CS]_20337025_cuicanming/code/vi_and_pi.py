### MDP Value Iteration and Policy Iteration
import argparse
import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)

parser = argparse.ArgumentParser(description='A program to run assignment 1 implementations.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--env", 
					help="The name of the environment to run your algorithm on.", 
					choices=["Deterministic-4x4-FrozenLake-v0","Stochastic-4x4-FrozenLake-v0"],
					default="Deterministic-4x4-FrozenLake-v0")

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

"""Evaluate the value function from a given policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
"""

#策略评价
def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3):
	value_function = np.zeros(nS)
	############################
	# YOUR IMPLEMENTATION HERE #
	while True:
		#更新前的价值函数
		update_value_fun=np.copy(value_function)
		#遍历每一个状态
		for state in range(nS):
			#选取动作
			action=policy[state]
			#更新
			value_function[state]=sum([trans_prob*(reward+gamma*update_value_fun[next_state])
										for trans_prob, next_state, reward, done in P[state][action]])
    	#判断价值函数是否收敛
		if (np.sum((np.fabs(update_value_fun-value_function))) <=tol):
			break
	############################
	return value_function


#策略提升函数
def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
	new_policy = np.zeros(nS, dtype='int')
	############################
	# YOUR IMPLEMENTATION HERE #
	#遍历每一个状态
	for state in range(nS):
		#计算Q值
		Q_table=np.zeros(nA)
		for action in  range(nA):
			for next_sr in P[state][action]:
				trans_prob, next_state, reward, done = next_sr
                # 更新动作对应的Q值
				Q_table[action]+=(trans_prob *(reward+gamma*value_from_policy[next_state]))
		#选取Q值最大的策略
		new_policy[state]=np.argmax(Q_table)
	############################
	return new_policy

#策略迭代算法
def policy_iteration(P, nS, nA, gamma=0.9, tol=10e-3):

	value_function = np.zeros(nS)
	#随机策略全部为0（往左）
	policy = np.zeros(nS, dtype=int)

	############################
	#迭代次数
	number_iteration=200000
	for i in range(number_iteration):
		#新的价值函数
		new_val_fun=policy_evaluation(P,nS,nA,policy)
		#新的策略
		new_policy=policy_improvement(P,nS,nA,new_val_fun,policy)

		#策略收敛是退出
		if (np.all(policy==new_policy)):
			print("no change between policy\n")
			break
		policy=new_policy
		value_function=new_val_fun

	
	############################
	return value_function, policy


#值迭代
def value_iteration(P, nS, nA, gamma=0.9, tol=1e-3):


	value_function = np.zeros(nS)
	#随机策略全部为0（往左）
	policy = np.zeros(nS, dtype=int)
	############################
	#迭代次数
	number_iteration=100000
	for i in range(number_iteration):
		#更新前的价值函数
		update_val_fun=np.copy(value_function)
		#遍历每一个状态
		for state in range(nS):
			Q_value=[]
			for action in range(nA):
				next_sta_reward=[]
				for next_sr in P[state][action]:
					# done判断是否为终止状态
					trans_prob,next_state, reward, done = next_sr
                    # 计算next_states_reward
					next_sta_reward.append(
                        (trans_prob*(reward+gamma*update_val_fun[next_state])))
                    # 计算Q值
					Q_value.append(np.sum(next_sta_reward))
                    # 取最大Q值更新V表，即更新当前状态的V值
					value_function[state] = max(Q_value)
		#判断是否收敛
		if(np.sum(np.fabs(update_val_fun-value_function)) <= tol):
			print("no change between value function\n")
			break
	############################
	policy=policy_improvement(P,nS,nA,value_function,policy)
	#返回价值函数、策略
	return value_function, policy


def render_single(env, policy, max_steps=100):
	"""
	This function does not need to be modified
	Renders policy once on environment. Watch your agent play!

	Parameters
	----------
	env: gym.core.Environment
		Environment to play on. Must have nS, nA, and P as attributes.
	Policy: np.array of shape [env.nS]
		The action to take at a given state
	"""
	episode_reward = 0
	ob = env.reset()
	done = False
	for t in range(max_steps):
		env.render()
		time.sleep(0.25)
		a = policy[ob]
		ob, rew, done, _ = env.step(a)
		episode_reward += rew
		if done:
			break
	env.render()
	if not done:
		print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
	else:
		print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":
	# read in script argument
	args = parser.parse_args()
	
	# Make gym environment
	env = gym.make(args.env)

	print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)

	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_pi, 100)

	print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)

	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_vi, 100)


