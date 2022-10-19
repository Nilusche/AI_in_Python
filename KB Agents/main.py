import random
import gym
import fh_ac_ai_gym
from Task.Propositions import *

env = gym.make('Wumpus-v0')
env.reset()


REVERSE_ACTION_DICT= {0: "WALK", 1:"TURNLEFT", 2:"TURNRIGHT", 3:"GRAB", 4: "SHOOT", 5:"CLIMB"}
POSSIBLE_ACTIONS = {v: k for k, v in REVERSE_ACTION_DICT.items()}

KBA = KnowledgebasedAgent("FC")

#Position 1,1 Does KB |= W21 or KB |=W12


observation, reward, done, info= env.step(POSSIBLE_ACTIONS["TURNLEFT"])
env.render()
KBA.TELL(observation)
#print("Knowledgebase: ", KBA.knowledgebase)
KBA.ASK("W21") #FC: False , R: False
 
#Both answers should be wrong since we have no way to know that a wumpus is there definitely
#Now Walk one field up
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
env.render()
KBA.TELL(observation)
#print("Knowledgebase: ", KBA.knowledgebase)
KBA.ASK("W21") #FC: False , R: True

#Using Forward checking we can still not deduct, that in any of those fields there is a wumpus.
#Using Resolution we can deduct that there is a wumpus in W21 just like there should be
#Now move one field up right up to the left of a pit
#Can the agent find the pit now?
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
env.render()
KBA.TELL(observation)
#print("Knowledgebase: ", KBA.knowledgebase)
KBA.ASK("P23") #FC: False , R: True


#Now circle the Pit and return back

observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["TURNRIGHT"])
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["TURNRIGHT"])
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["TURNRIGHT"])
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])
#env.render()
KBA.TELL(observation)
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["TURNRIGHT"])
observation, reward, done, info= env.step(POSSIBLE_ACTIONS["WALK"])

env.render()
#print("Knowledgebase: ", KBA.knowledgebase)

KBA.ASK("P23") #FC: True , R: True















"""
Autonomous walk attempt

for i in range(1000):
    print("Iteration: ", i)
    
    action = random.choice(possible_action)
    print("Agent uses action: ", ACTION_MAP[action])
    observation, reward, done, info= env.step(action)
    print(observation)
    if done:
        if reward[0] == -1000:
            print("AGENT DIED")
        elif reward[0] == 1000:
            print("AGENT GETS THE GOLD AND RETURNED SAFE")
        else: 
            print(reward)
        print("\nFINAL RESULT: ")
        env.render()
        observation = env.reset()
        break;

    print()

"""