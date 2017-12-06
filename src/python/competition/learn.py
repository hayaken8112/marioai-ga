import os.path
import pickle
import sys
import csv

from agents.myagent import *
from agents.astaragent import *
from experiments.episodicexperiment import EpisodicExperiment
from ga.controller import Controller
from tasks.mariotask import MarioTask

log_list = []

class IndividualReward:
    def __init__(self, individual, reward):
        self.individual = individual
        self.reward = reward

    def __str__(self):
        return str(self.reward)


def make_next_generation(experiment, individuals, numOfGeneration):
    n_individuals = len(individuals)

    rewards = []
    for individual in individuals:
        experiment.agent.individual = individual
        experiment.doEpisodes(1)
        rewards.append(IndividualReward(individual, experiment.task.reward))
        print("reward: {0}".format(experiment.task.reward))
    reward_sum = 0
    for re in rewards:
        reward_sum += re.reward
    average = round(reward_sum/n_individuals,1)
    numberOfElites = 2
    sorted_rewards = sorted(rewards, key=lambda individual_reward: individual_reward.reward, reverse=True)
    print("best reward: {0}".format(sorted_rewards[0].reward))
    elite_individuals = list(map(lambda e: e.individual, sorted_rewards[:numberOfElites]))
    next_individuals = elite_individuals
    log_list.append([numOfGeneration,average,sorted_rewards[0].reward])
    while len(next_individuals) < n_individuals:
        father, mother = Controller.select(list(map(lambda individual_reward: individual_reward.individual, rewards)),
                                           list(map(lambda individual_reward: individual_reward.reward, rewards)))
        child1, child2 = Controller.two_points_cross(father, mother)
        next_individuals.append(child1)
        next_individuals.append(child2)
    next_individuals = next_individuals[:n_individuals]
    Controller.mutate(next_individuals, mutation_rate=0.5)
    return next_individuals


def main():
    agent = MyAgent(None)
    #agent = AstarAgent()
    task = MarioTask(agent.name)
    task.env.initMarioMode = 2
    task.env.levelDifficulty = int(sys.argv[1]) if len(sys.argv) == 2 else 0
    experiment = EpisodicExperiment(task, agent)

    n_individuals = 10
    filename = "learned_individuals_{0}".format(task.env.levelDifficulty)
    if os.path.exists(filename):
        initial_individuals = load(filename)
    else:
        initial_individuals = [Individual(random=True) for i in range(n_individuals)]
    current_individuals = initial_individuals
    n_generations = 50
    for generation in range(n_generations):
        print("generation #{0} playing...".format(generation))
        #task.env.visualization = generation % 10 == 0
        task.env.visualization = generation % 50 == 0
        current_individuals = make_next_generation(experiment, current_individuals,generation)
        save(current_individuals, filename)
        savelog(log_list)
    


def save(individuals, filename):
    l = list(map(lambda x: x.to_list(), individuals))
    with open(filename, "wb") as f:
        pickle.dump(l, f)


def load(filename):
    with open(filename, "rb") as f:
        l = pickle.load(f)
        return list(map(lambda x: Individual.from_list(x), l))

def savelog(log):
    with open('data8.csv', "w") as w_file:
        writer = csv.writer(w_file, lineterminator='\n')
        writer.writerows(log)


if __name__ == "__main__":
    main()
else:
    print("This is module to be run rather than imported.")
