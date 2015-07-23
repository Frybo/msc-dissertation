"""
Author: Andrew van den Hoeven
Contributors: Stuart Squires
Date: May 2015

Simulates multiple agents in an iterative prisoners dilemma, with evolving
strategies.

Some notes from Andrew:
    Required libraries:
        json, random, http_server
        networkx : for the graphs
        matplotlib : for charts
        seaborn : for pretty charts
        
    required files:
        http_server.py
        graph009template.html
    
    Most parameters are in the main function, though the mutation logic is 
    contained in reproduce()

    1 is defect, 0 is cooperate throughout the code
    
    If something doesn't make sense please tell me!
    
    maxstates =1 and noise= False with the snowdrift game produces a mixed 
    population of hawks and doves that oscillates around an equilibrium ratio as
    seen in the literature

Note from Stuart:
    If for some reason the web page doesn't launch automatically for you when
    the server starts, you can access it at http://localhost:8000/graph009.html

TODO:
    -make the sim end with a full gen played but skip the last reproduction so 
     that all the strategies can be ranked and ordered
    -interactive charts?
    -log a history?
    -add family trees across time?
    -add random element to state actions and transitions
    -add noise X (semi complete)
    -turn stats tuple into a named tuple
    -add cost for complexity?
"""

import sys; sys.path.insert(0, 'IPD_functions') 
from game_logic import play_game,tally_score
from generation_logic import play_round,run_generation
from generate_agents import generate_agents
from IPD_utilities import pretty_print
from class_definitions import Agent
from IPD_config import *
import http_server  #to host the results locally

import random as r
import json                     # for d3 drawing
import collections              # for data tracking
import networkx as nx           # for making graphs
from networkx.readwrite import json_graph #more d3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


DEBUG = False
    
def main():
    """Main loop.
    1. Initializes variables.
    2. Runs simulation.
    """
    
    run_all_simulations(game = GAME_MATRIX,
                        evol = EVOLUTION_SETTINGS,
                        number_of_simulations = SIMULATIONS,
                        count = NUMBER_OF_AGENTS, 
                        rounds = ROUNDS, w = W,
                        generations = GENERATIONS, 
                        start_states = START_STATES, 
                        max_states = MAX_STATES, all_max = ALL_MAX, 
                        noise = NOISE)

    return "complete"
    

def run_all_simulations(game, evol, number_of_simulations, count=64, rounds=100, 
                        w=0.9, generations=100, start_states=2, max_states=8, 
                        all_max=False, noise=False):  
    if number_of_simulations==1:
        (result, ranks, stats) = run_simulation(game = game, evol = evol, 
                                                count = count, rounds = rounds, 
                                                w = w, 
                                                generations = generations, 
                                                start_states = start_states, 
                                                max_states = max_states, 
                                                all_max = all_max, 
                                                noise = noise, verbose = True)

        simulation_results = zip(result, ranks, stats[1])

        topAgent = result[0]
        
        draw_to_browser(result,stats)
        return "complete"
    
    
    avg_score_logs=[],
    avg_coop_logs=[],
    avg_defect_logs=[]
    stats=[[],
            [],
            [],      
        ]
    
    final_agents={}
    
    for i in range(number_of_simulations):
        (result, ranks, simulation_stats) = run_simulation( game = game,
                             evol = evol,
                             count = count, 
                             rounds = rounds, w = w,
                             generations = generations, 
                             start_states = start_states, 
                             max_states = max_states, all_max = all_max, 
                             noise = noise)
        if (i+1)%5 ==0: print "simulation ", i+1
        stats[0].append(simulation_stats[0]) #avg turn score
        stats[1].append(simulation_stats[5]) #avg_pop_coop
        stats[2].append(simulation_stats[6]) #avg_pop_defect
        final_agents[i]=[x.behaviour for x in result[:20]] # param save the top 20 agents' behaviour
        
    log_data(stats,number_of_simulations,generations,final_agents)
    draw_overall_charts(stats)
    write_overall_data(stats)
    
def draw_overall_charts(stats):
    #draws charts for data from multiple simulations
    #print stats[0]
    #chart 1 : average score per turn
    sns.set(style = "darkgrid", palette = "muted")
    fig = plt.subplots(1, 1, figsize = (4, 2.5))
    b, g, r, p = sns.color_palette("muted", 4)
    ax = sns.tsplot(stats[0], color=g)
    ax.set(ylabel = "Average score per turn")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/historical_overall.png") 
    
    
    plt.clf()
    plt.cla()
    
    #chart 3: cooperation and defection
    sns.set(style="darkgrid", palette="muted")
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    data = np.dstack([[j for j in stats[i]] for i in [1,2]]) 
    ax = sns.tsplot(data, color = [ b, r])
    ax.set(ylabel = "percent coop/defect")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/cooppct_overall.png") 
    
    return

def write_overall_data(stats):
    #TODO
    pass
    
def run_simulation( game, evol, count=64, rounds=100, w=0.9, 
                   generations=100, start_states=2, max_states=8, all_max=False,
                   noise=False, verbose=False):
                   
    """
    Runs the simulation.

    Args:
        agents: the list of agents
        game: the game matrix
        evol: a list of evolution settings (breed, survive, newcomers)
        count: the number of agents
        rounds: ???
        w: the probability of the game going on another turn
        generations: the number of generations
        start_states: ???
        max_states: the maximum number of states
        all_max: whether or not the agents will all have the maximum number of
            states
        noise: whether or not to use Joss-Ann noise

    Returns:
        (agents, top_scores, stats): a tuple containing the final agent list,
            top scores, and statistics
    """

    simulation_stats = [[], [0], [], [], []] # what is this?
    
    # returns a tuple,feeds into main
    
    #initialize agents
    agents = generate_agents(count = count, 
                             max_states = start_states, all_max = False,
                             noise = noise)
    
    
    simulation_stats = [[], [0], [], [], [],[],[]]
    last_gen = False
    for i in range(generations):
        if i % 25 == 24 and verbose: print "Generation " + str(i + 1)
        if i == generations - 1: last_gen=True
        
        (agents, top_scores, generation_stats) = run_generation(agents, game, 
                                                     count = count, 
                                                     rounds = rounds, w = w,
                                                     evol = evol, 
                                                     start_states = start_states,
                                                     max_states = max_states, 
                                                     all_max = all_max, 
                                                     noise = noise,
                                                     last_gen = last_gen)

        simulation_stats[0].append(generation_stats[0]) #avgscore
        simulation_stats[2].append(generation_stats[2]) #avg_sentience
        simulation_stats[3].append(generation_stats[3]) #avg_hard_coop , from joss ann noise
        simulation_stats[4].append(generation_stats[4]) #avg_hard_defect , from joss ann noise
        simulation_stats[5].append(generation_stats[5]) #avg_pop_coop
        simulation_stats[6].append(generation_stats[6]) #avg_pop_defect

    simulation_stats[1] = generation_stats[1] #final gen individual batting avgs for final output
    return (agents, top_scores, simulation_stats)


def write_html(json_list): 
    #print json_list["0"]
    html_template = open("IPD_output/graph009template.html", "r")
    html_template_string = html_template.read()
    html_template.close()
    custom = 'var allData='+''+" {'0': {"+'\n'
    
    '''for (index, (key, value)) in enumerate(json_list['0'].items()):
        custom += "'" + str(key) + "'" + " : "  + str(value) + ',\n'
    custom += "}," + '\n' + "'codes':[ " + '\n'
    for i in range(len(json_list["codes"])):
        custom += str(json_list["codes"][i]) + ',\n'
    custom += " ]}" + ';' + '\n'
    custom += 'console.log(typeof allData);'
    total = html_template_string % {"jsonData": custom}'''
    
    total=html_template_string
    output_file = open("IPD_output/graph009.html", "w")
    output_file.seek(0)
    output_file.truncate() # empties file
    output_file.write(total)
    output_file.close()

def log_data(stats,simulations,generations,final_agents):
    #logs the stats data to json files that can be used later
    avg_turn_score_dict={}
    avg_coop_dict={}    
    avg_defect_dict={}    
    for i in range(simulations):
        avg_turn_score_dict[str(i)]=stats[0][i]
        avg_coop_dict[str(i)]=stats[1][i]
        avg_defect_dict[str(i)]=stats[2][i]
        
    avg_turn_score_df=pd.DataFrame.from_dict(avg_turn_score_dict)
    avg_turn_score_df.to_json("avgscore.json")
    
    avg_coop_df=pd.DataFrame.from_dict(avg_coop_dict)
    avg_coop_df.to_json("avgcoop.json")
    

    avg_defect_df=pd.DataFrame.from_dict(avg_defect_dict)
    avg_defect_df.to_json("avgdefect.json")

    final_agents_df=pd.DataFrame.from_dict(final_agents)
    final_agents_df.to_json("final_agents.json")
    
    return
    
    
def draw_to_browser(agents, stats):
    # print "# of strings"
    # print len(graphStrings)
    draw_sim_charts(stats)
    data1 = {}
    data2= []
    for i in range(len(agents)):
        #print graphStrings[i]
        
        G = create_graph_of_agent(agents[i])
        d = json_graph.node_link_data(G)
        d["directed"] = 1
        d["multigraph"] = 1
        data1[str(i + 1)] = d
        j1, j2 = round(agents[i].joss_ann[0], 4), round(agents[i].joss_ann[1], 4)
        jay1, jay2 = j1, j2
        if j1 + j2 > 1: jay1, jay2 = (1 - j2, 1 - j1)
        text = str(i + 1)  #+ " - (" + str(jay1) + "," + str(jay2) + ")"
        data2.append({"text": text, "value": str(i + 1)})
            
        # print d

    data = {"0": data1,
            "codes": data2}

    # print json_list
    # print len(json_list)
    json_list = json.dumps(data) # node-link format to serialize
    # print d 
    # write json
    write_html(data)
    json.dump(data, open('IPD_output/data.json', 'w'))
    print('Wrote node-link JSON data to temp.json')
    # open URL in running web browser
    http_server.load_url('IPD_output/graph009.html')
    print('Or copy all files to webserver and load graph.html')

def draw_sim_charts(stats):
    #draws charts from a single simulation and saves files to be shown in html output_file
    
    #chart 1 : average score per turn

    sns.set(style = "darkgrid", palette = "muted")
    fig = plt.subplots(1, 1, figsize = (4, 2.5))
    b, g, r, p = sns.color_palette("muted", 4)
    ax = sns.tsplot(stats[0], color=g)
    ax.set(ylabel = "Average score per turn")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("IPD_output/images/historical.png") 
    
    plt.clf()
    plt.cla()
    
    #chart 2 : joss-Ann "sentience" where sentience is defined as how little
    # noise the strategy has. A more "sentient" strategy follows it's states more closely
    sns.set(style="darkgrid", palette="muted")
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    # 1- to flip the y axis
    data = np.dstack([[1 - j for j in stats[i]] for i in range(2, 5)]) 
    ax = sns.tsplot(data, color = [g, b, r])
    ax.set(ylabel = "Average sentience")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("IPD_output/images/sentience.png") 
    
    plt.clf()
    plt.cla()
    
    #chart 3: cooperation and defection
    sns.set(style="darkgrid", palette="muted")
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    data = np.dstack([[j for j in stats[i]] for i in [5,6]]) 
    ax = sns.tsplot(data, color = [ b, r])
    ax.set(ylabel = "percent coop/defect")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("IPD_output/images/cooppct.png") 
    
    return 

    
def create_graph_of_agent(agent):
    # takes a string as input and outputs a Networkx graph object
    (nodes, edges) = parse(agent)
    G = nx.MultiDiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    active_nodes = [1]
    next_nodes = []
    # print nx.number_of_nodes(G)

    for i in range(nx.number_of_nodes(G)):
        
        active_nodes = list(set(active_nodes + next_nodes))
        next_nodes = []

        for node in active_nodes:          
            next_nodes += G.successors(node) #0 is predecessors, 1 is successors
            #print "next_nodes ",next_nodes
    #print active_nodes
    #active_nodes=list(set(sorted(active_nodes)))
    
    #print active_nodes
    #print nodes
    #print edges
    
    
    extra_nodes = sorted(list(set(range(1, nx.number_of_nodes(G) +1)) 
                       - set(active_nodes)), reverse=True)
    #print extra_nodes
    for i in extra_nodes:
        G.remove_node(i)
        #print nx.number_of_nodes(G)
    
    return G
    

def parse(agent):
    #returns two lists of edges and a list of nodes
    #print graph_list
    number_nodes = len(agent.behaviour)
    edge_list = []
    node_list = []
    for i in range(number_nodes):
        # (start, end, {'attribute': 'value'})
        edge_list.append((i +1, agent.behaviour[i][1], {'type': 'C'})) 
        edge_list.append((i +1, agent.behaviour[i][2], {'type': 'D'}))

        if agent.behaviour[i][0]: node_list.append((i + 1, {'type': 'D'}))
        else: node_list.append((i + 1, {'type': 'C'}))
    
    return (node_list, edge_list)

    
if __name__ =="__main__":
    main()
