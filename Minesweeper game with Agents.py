#!/usr/bin/env python
# coding: utf-8

# In[1]:


from agents import *
from notebook import psource
from random import choice
from time import time
######################### PART 1, QUESTION 1.1 ############################
def part1(r,c,na,nd):
    ############## SUB PART 1.1.1 SIMPLE REFLEX AGENT ###########################
    ######### (1.1.1 START)<RUN PROGRAM FROM HERE - SIMPLE REFLEX AGENT> ###################
    """

    Problem Statement/ Concept:
    The environment is actually an old battleground that contains multiple landmines in it.
    We are sending in an AI robotic agent which scans the land (More on this later), defuses and removes the mines.

    Agent:This is a robot which scans the area and performs the following actions.
    If active mines are found, they are defused and removed from the environment.
    If dead mines are found, they are removed from the environment.
    The robot is very good at defusing the mines, so if it reaches the location,
    it has a probability of 1 of defusing the bomb, hence there are no circumstances where
    the agent may fail to defuse the bomb successfully, triggering an explosion.


    PEAS Description:

    Performance:
    Performance Measures: Cost to perform actions, time taken, Percentage of Mines removed, No of steps taken,
    Cost per mine eradication
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.
    Moving forward costs 1 unit
    Turning left or Turning right costs 0.5 units

    Environment:The environment (Battleground) has mines in which some of them have exploded or are dead,
    but there are materialistic remains, which needs to be cleared.
    Active mines should have to be carefully defused and then removed from the battleground.
    It is a 2D Graphically represented environment.
    >Grey square: Empty position
    >Black square: Position containing the agent
    >Red square: Position containing Active Mine
    >Purple square: Position containing Dead Mine
    *Partially observable: The Battleground is partially observable because the agent can only perceive 
    the environment at the location that it is currently present in
    *Deterministic: The result and outcome of the world are already known
    *Sequential
    *Static: The ActiveMine or DeadMine nor the walls move
    *Discrete
    *One agent: Minesweeper agent only


    Actuators:Turn Left, Move Forward, Turn right, Diffuse, Remove
    Note: The process is mentioned 'Diffuse' shortly, but actually it Diffuses and Removes mines.


    Sensors:
    Active Mine Detector, Dead Mine detector in its current position.
    The percepts are stored in a list.

    """



    #importing required libraries and required modules from aima-python-master
#     from agents import *
#     from notebook import psource
#     from random import choice
#     from time import time

    """
    Creating Things Active Mine and Dead mines to use them as objects in our environment
    Child of Thing class in agents.py
    These mines don't have a specific task to do according to our concept, so they are empty.
    They are just objects in our environment
    """
    class ActiveMine(Thing):
        pass
    class DeadMine(Thing):
        pass



    """
    Creating our Agent, to use in our environment
    Child of Agent class in agents.py
    This MinesweeperRandom is our SIMPLE REFLEX AGENT
    """
    class MineSweeperRandom(Agent):
        #Defining variables to store agent location, agent current direction & occured cost
        location = [0,0]
        direction = Direction("down")
        cost = 0
        moves = 0

        #To make agent move forward
        def moveforward(self, success=True):
            '''moveforward possible only if success (i.e. valid destination location)'''
            if not success:
                return
            if self.direction.direction == Direction.R:
                self.location[0] += 1
            elif self.direction.direction == Direction.L:
                self.location[0] -= 1
            elif self.direction.direction == Direction.D:
                self.location[1] += 1
            elif self.direction.direction == Direction.U:
                self.location[1] -= 1
            self.cost += 1
            self.moves +=1

        #To make the agent turn in the given direction
        def turn(self, d):
            self.direction = self.direction + d
            self.cost += 0.5
            self.moves +=1

        #To Diffuse the found Active mine and remove it(delete from environment)
        def diffuse(self, thing):
            '''returns True upon success or False otherwise'''
            if isinstance(thing, ActiveMine):
                self.cost += 3
                self.moves +=1
                return True
            return False

        #To Remove the found Dead mine(delete from environment)
        def remove(self, thing):
            ''' returns True upon success or False otherwise'''
            if isinstance(thing, DeadMine):
                self.cost += 2
                self.moves +=1
                return True
            return False


    """
    The following Program function is the brain of the Agent.
    It takes decisions to be executed, based on the Percepts it receives.

    Our Simple Reflex agent doesn't have to do much except it moves randomly as follows:
    50% Probability to move forward, costs 1 unit
    25% Probability to turn right, costs 0.5 units
    25% Probability to turn Left, costs 0.5 units

    It can see the things available only in it's location, it can't see ahead or around it.

    If it detects any mine in its current location, it removes it from the environment(There's no chance of failure).
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.

    The agent also stays in the bounds of the environment by checking its coordinates using the Bump concept.
    """

    def program(percepts):
        for p in percepts: #Checks the current percepts
            if isinstance(p, ActiveMine): #Diffuses active mine if found
                return 'diffuse'
            elif isinstance(p, DeadMine): #Removes Dead mine if found
                return 'remove'
            if isinstance(p,Bump): # to check if the agent is at an edge and have to turn
                turn = False
                choice = random.choice((1,2)) # turn left or right
            else:
                choice = random.choice((1,2,3,4)) # 1-right, 2-left, others-forward

        # Perform the corresponding move action
        if choice == 1:
            return 'turnright'
        elif choice == 2:
            return 'turnleft'
        else:
            return 'moveforward'



    """
    Creating the Environment BattleGround.
    It is a child of the GraphicEnvironment class in agents.py
    This is a graphical environment and is really useful to visualize simulations.
    The environment can hold 'Things' class's sub classes as things in the environment.
    The defined things are ActiveMines, DeadMines and Bump if the agent is about to bump into a wall.

    """



    class BattleGround(GraphicEnvironment):
        GraphicEnvironment.color={255,255,255}
        def percept(self, agent):
            '''return a list of things that are in our agent's location'''
            things = self.list_things_at(agent.location)
            loc = copy.deepcopy(agent.location)
            #To Check if agent is about to bump into a wall
            if agent.direction.direction == Direction.R:
                loc[0] += 1
            elif agent.direction.direction == Direction.L:
                loc[0] -= 1
            elif agent.direction.direction == Direction.D:
                loc[1] += 1
            elif agent.direction.direction == Direction.U:
                loc[1] -= 1
            if not self.is_inbounds(loc):
                things.append(Bump())
            return things
        #Function to Execute the decided action from the Program function
        def execute_action(self, agent, action):
            '''changes the state of the environment based on what the agent does.'''
            if action == 'turnright':
                print('Simple Reflex Agent {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.R)
            elif action == 'turnleft':
                print('Simple Reflex Agent {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.L)
            elif action == 'moveforward':
                print('Simple Reflex Agent {} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
                agent.moveforward()
            elif action == "diffuse":
                items = self.list_things_at(agent.location, tclass=ActiveMine)
                if len(items) != 0:
                    if agent.diffuse(items[0]):
                        print('Simple Reflex Agent {} diffused {} at location: {}'.format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])
            elif action == "remove":
                items = self.list_things_at(agent.location, tclass=DeadMine)
                if len(items) != 0:
                    if agent.remove(items[0]):
                        print('Simple Reflex Agent {} removed {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])

        def is_done(self):
            '''By default, it's done when we find a live agent can't be found, or when there are no more mines'''
            no_mines = not any(isinstance(thing, ActiveMine) or isinstance(thing, DeadMine) for thing in self.things)
            dead_agents = not any(agent.is_alive() for agent in self.agents)
            return dead_agents or no_mines

    """
    The Environment is customizable in number or rows and columns by modifying following variables.
    This program also contains code to customize the number of active and dead mines by adjusting the
    following num_activemines and num_deadmines variables.
    It randonly generates mines in different locations within the environment.
    """
    rows,columns,num_activemines,num_deadmines = r,c,na,nd
    """
    Instanciating the Environment, creating(instanciating) and adding agent to environment.
    Instaciating ActiveMine and DeadMine.
    """
    battleground = BattleGround(rows,columns,color={'MineSweeperRandom': (0,0,0), 'DeadMine': (139,0,139), 'ActiveMine': (255, 0, 0)})
    minesweeper = MineSweeperRandom(program)
    activemine = ActiveMine()
    deadmine = DeadMine()
    battleground.add_thing(minesweeper, [0,0])

    """
    The code section below is to create and add the given number of ActiveMines and DeadMines by the user.
    It check if the given number of Mines can be implemented in the environment, if not possible, it'll
    raise an error. If it is possible, then it'll add all the Active and Dead Mines in our environment.
    """

    am = {}  #Dict holding activemines
    dm = {}  #Dict holding deadmines
    log = [] #List that rememberes the occupied positions by mines


    #Code to check if the env has enough space to add the given mines
    if (num_activemines + num_deadmines) > (rows*columns):
        ss = '''There is no more space to add any more mines in the battleground. 
         You can have only a maximum of {} mines for your given area configuration,
         but you have given {} active mines and {} dead mines which adds to a total of {} mines.
         Reduce {} number of mines.'''.format(rows*columns,num_activemines,num_deadmines,
                                              num_activemines+num_deadmines,
                                              num_activemines+num_deadmines-rows*columns)
        raise ValueError(ss)


    #Setting up Seed so that the mines created will be in the same place whenever it's being run(For testing & comparing purposes)
    #We can disable the seed if reqd after the performance tests and comparisons.
    random.seed(12)


    #To create and add given number of active mines in the environment
    for i in range(num_activemines):
        var = "AM"+str(i)   #Creating name for the instance of Active mine
        am[var] = ActiveMine() #instanciating active mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log:  #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(am[var],temp) #Created Mine will be added at the decided position


    #To create and add given number of dead mines in the environment
    for i in range(num_deadmines):
        var = "DM"+str(i) #Creating name for the instance of dead mine
        dm[var] = DeadMine() #instanciating dead mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(dm[var],temp) #Created Mine will be added at the decided position

    start_time = time()   
    battleground.run(4000,0.00001) #Run the Simulation
    time_taken = time() - start_time


    '''TO Print Performance Report'''
    occured_cost = minesweeper.cost
    time_taken
    left_mines = 0
    for i in battleground.things:
        if isinstance(i,ActiveMine):
            left_mines += 1
        if isinstance(i,DeadMine):
            left_mines += 1
    Percentage_mines_removed = (num_activemines+num_deadmines - left_mines)/(num_activemines+num_deadmines)
    no_of_steps_taken = minesweeper.moves
    cost_per_mine_eradication = occured_cost / (num_activemines+num_deadmines - left_mines)
    SRA_PF = "\n\nSIMPLE REFLEX AGENT REPORT:\nOccured Cost: {}\nTime taken: {}s\nNumber of total mines: {}\nNumber of Mines Removed: {}\nNumber of mines left: {}\nPercentage of removed mines: {}\nNo of moves: {}\nCost per mine Eradication: {}\nEnvironment dimension: [{},{}]".format(occured_cost,time_taken,num_activemines+num_deadmines,num_activemines+num_deadmines-left_mines,left_mines,Percentage_mines_removed,no_of_steps_taken,cost_per_mine_eradication,rows,columns)

    #print(SRA_PF)

    ######### (1.1.1 END)<RUN PROGRAM UNTIL HERE - SIMPLE REFLEX AGENT> ###################


    

    ############## SUB PART 1.1.2 MODEL BASED AGENT ###########################
    ######### (1.1.2 START)<RUN PROGRAM FROM HERE - MODEL BASED AGENT> ###################
    """

    Problem Statement/ Concept:
    The environment is actually an old battleground that contains multiple landmines in it.
    We are sending in an AI robotic agent which scans the land (More on this later), defuses and removes the mines.

    Agent:This is a robot which scans the area and performs the following actions.
    If active mines are found, they are defused and removed from the environment.
    If dead mines are found, they are removed from the environment.
    The robot is very good at defusing the mines, so if it reaches the location,
    it has a probability of 1 of defusing the bomb, hence there are no circumstances where
    the agent may fail to defuse the bomb successfully, triggering an explosion.

    In this model based agent, the agent has a memory of the mines it has seen and will go to them to take action.
    If there are no mines in memory, then it will move randomly, scanning for mines.
    It will move towards the mine it has seen the earliest(the first ones in its memory list)

    PEAS Description:

    Performance:
    Performance Measures: Cost to perform actions, time taken, Percentage of Mines removed, No of steps taken,
    Cost per mine eradication
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.
    Moving forward costs 1 unit
    Turning left or Turning right costs 0.5 units

    Environment:The environment (Battleground) has mines in which some of them have exploded or are dead,
    but there are materialistic remains, which needs to be cleared.
    Active mines should have to be carefully defused and then removed from the battleground.
    It is a 2D Graphically represented environment.
    >Grey square: Empty position
    >Black square: Position containing the agent
    >Red square: Position containing Active Mine
    >Purple square: Position containing Dead Mine
    *Partially observable: The Battleground is partially observable because the agent can only perceive 
    the environment at the location that it is currently present in
    *Deterministic: The result and outcome of the world are already known
    *Sequential
    *Static: The ActiveMine or DeadMine nor the walls move
    *Discrete
    *One agent: Minesweeper agent only


    Actuators:Turn Left, Move Forward, Turn right, Diffuse, Remove
    Note: The process is mentioned 'Diffuse' shortly, but actually it Diffuses and Removes mines.


    Sensors:
    Active Mine Detector, Dead Mine detector in its current posititon and can also detect in the next front and the side location.
    The percepts are stored in a list.
    Scanned and found mines are stored in its memory until the required action is taken.
    """



    #importing required libraries and required modules from aima-python-master
#     from agents import *
#     from notebook import psource
#     from random import choice
#     from time import time

    """
    Creating Things Active Mine and Dead mines to use them as objects in our environment
    Child of Thing class in agents.py
    These mines don't have a specific task to do according to our concept, so they are empty.
    They are just objects in our environment
    """
    class ActiveMine(Thing):
        pass
    class DeadMine(Thing):
        pass


    """
    Creating our Agent, to use in our environment
    Child of Agent class in agents.py
    This MinesweeperRandom is our SIMPLE REFLEX AGENT
    """

    class MineSweeperRandom(Agent):
        #Defining variables to store agent location, agent current direction & occured cost
        location = [0,0]
        direction = Direction("down")
        found_mines = [] #Memory of Model Based agent to store the found mines
        cost = 0
        moves = 0

        #To make agent move forward    
        def moveforward(self, success=True):
            '''moveforward possible only if success (i.e. valid destination location)'''
            if not success:
                return
            if self.direction.direction == Direction.R:
                self.location[0] += 1
            elif self.direction.direction == Direction.L:
                self.location[0] -= 1
            elif self.direction.direction == Direction.D:
                self.location[1] += 1
            elif self.direction.direction == Direction.U:
                self.location[1] -= 1
            self.cost += 1
            self.moves +=1

        #To make the agent turn in the given direction    
        def turn(self, d):
            self.direction = self.direction + d
            self.cost += 0.5
            self.moves +=1

        #To Diffuse the found Active mine and remove it(delete from environment)      
        def diffuse(self, thing):
            '''returns True upon success or False otherwise'''
            if isinstance(thing, ActiveMine):
                self.cost += 3
                self.moves +=1
                return True
            return False

        #To Remove the found Dead mine(delete from environment)
        def remove(self, thing):
            ''' returns True upon success or False otherwise'''
            if isinstance(thing, DeadMine):
                self.cost += 2
                self.moves +=1
                return True
            return False



    """
    The following Program function is the brain of the Agent.
    It takes decisions to be executed, based on its memory and the Percepts it receives.

    It can see the things available only in it's location, just front and sides of it.

    It moves towards the earliest mine it has seen from it memory and does the required action after reaching it.

    Our Model Based agent moves randomly as follows(if there are no found mines in memory):
    50% Probability to move forward, costs 1 unit
    25% Probability to turn right, costs 0.5 units
    25% Probability to turn Left, costs 0.5 units

    If it detects any mine in its current location, it removes it from the environment(There's no chance of failure).
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.

    The agent also stays in the bounds of the environment by checking its coordinates using the Bump concept.
    """
    def program(xyz, percepts):#xyz is the agent
        choice = 1
        turn = True
        for p in percepts: #Checks the current percepts
            if isinstance(p, ActiveMine):#Diffuses active mine if found
                return 'diffuse'
            elif isinstance(p, DeadMine):#Removes Dead mine if found
                return 'remove'
            if isinstance(p,Bump): # to check if the agent is at an edge and have to turn
                turn = False
                choice = random.choice((1,2));
            if isinstance(p, list): #Vision of the Minesweeper
                for i in p:
                    if i not in xyz.found_mines:
                        xyz.found_mines.append(i)
        #Delete the mine from the memory if the agent has reached it
        if xyz.location in xyz.found_mines:
            xyz.found_mines.remove(xyz.location)

    ###If there are no found mines, then the agent will travel randomly
        if xyz.found_mines == []:
            if turn:
                choice = random.choice((1,2,3,4)) # 1-right, 2-left, others-forward
            if choice == 1:
                return 'turnright'
            elif choice == 2:
                return 'turnleft'
            else:
                return 'moveforward'
    ###If there are found mines, then the agent will move towards the earliest found mine in the memory
        else:
            to_move = 'move_down'
            x,y = xyz.location
            x1,y1 = xyz.found_mines[0]
            x_dir = x-x1
            y_dir = y-y1

    ###Calculating the next move(moveforward, turnright, turnleft) to take in order to go closer to the mine 
            if not x_dir == 0:
                if x_dir < 0:
                    to_move = 'move_right'
                elif x_dir > 0:
                    to_move = 'move_left'
                else:
                    pass
            else:
                if y_dir < 0:
                    to_move = 'move_down'
                elif y_dir > 0:
                    to_move = 'move_up'
                else:
                    pass        


            if to_move == 'move_right':
                if xyz.direction.direction == 'up':
                    return 'turnright'
                elif xyz.direction.direction == 'right':
                    return 'moveforward'
                elif xyz.direction.direction == 'down':
                    return 'turnleft'
                elif xyz.direction.direction == 'left':
                    return 'turnright'

            elif to_move == 'move_left':
                if xyz.direction.direction == 'up':
                    return 'turnleft'
                elif xyz.direction.direction == 'right':
                    return 'turnleft'
                elif xyz.direction.direction == 'down':
                    return 'turnright'
                elif xyz.direction.direction == 'left':
                    return 'moveforward'

            elif to_move == 'move_up':
                if xyz.direction.direction == 'up':
                    return 'moveforward'
                elif xyz.direction.direction == 'right':
                    return 'turnleft'
                elif xyz.direction.direction == 'down':
                    return 'turnright'
                elif xyz.direction.direction == 'left':
                    return 'turnright'

            elif to_move == 'move_down':
                if xyz.direction.direction == 'up':
                    return 'turnright'
                elif xyz.direction.direction == 'right':
                    return 'turnright'
                elif xyz.direction.direction == 'down':
                    return 'moveforward'
                elif xyz.direction.direction == 'left':
                    return 'turnleft'

    """
    Creating the Environment BattleGround.
    It is a child of the GraphicEnvironment class in agents.py
    This is a graphical environment and is really useful to visualize simulations.
    The environment can hold 'Things' class's sub classes as things in the environment.
    The defined things are ActiveMines, DeadMines and Bump if the agent is about to bump into a wall.
    """



    class BattleGround(GraphicEnvironment):
        GraphicEnvironment.color={255,255,255}


        def step(self): #Overriding the function since we're modifying it as follows
            if not self.is_done():
                actions = []
                for agent in self.agents:
                    if agent.alive:
                        actions.append(agent.program(agent, self.percept(agent)))#To pass agent as parameter in function program along with percepts 
                    else:
                        actions.append("")
                for (agent, action) in zip(self.agents, actions):
                    self.execute_action(agent, action)
                self.exogenous_change()

       #Adds thing to the environment in the given location 
        def add_thing(self, thing, location=None):
            if not isinstance(thing, Thing):
                thing = Agent(thing)
            if thing in self.things:
                print("Can't add the same thing twice")
            else:
                thing.location = location if location is not None else self.default_location(thing)
                self.things.append(thing)#Add thing object to self.things list
                if isinstance(thing, Agent):
                    thing.performance = 0
                    thing.location = location#Add thing object(Agent) to the agent's instance
                    self.agents.append(thing)

        def percept(self, agent):
            '''return a list of things that are in our agent's location.
            Add the found mines objects in front and sides of the Agent to it's memory '''
            things = self.list_things_at(agent.location)
            loc = copy.deepcopy(agent.location) # find out the target location
            #Check if agent is about to bump into a wall
            if agent.direction.direction == Direction.R:
                loc[0] += 1
            elif agent.direction.direction == Direction.L:
                loc[0] -= 1
            elif agent.direction.direction == Direction.D:
                loc[1] += 1
            elif agent.direction.direction == Direction.U:
                loc[1] -= 1
            if not self.is_inbounds(loc):
                things.append(Bump())
            things.append(self.vis(agent))#adds the scanned objects to the things list
            return things


        ###This function Scans just in the front and sides of the agent and returns the list.
        #This function is called by the percepts function.
        def vis(self,agent):
            visi = []
            if self.list_things_at([agent.location[0]+1,agent.location[1]], tclass=ActiveMine) != []:
                visi.append([agent.location[0]+1,agent.location[1]])
            if self.list_things_at([agent.location[0]-1,agent.location[1]], tclass=ActiveMine) != []:
                visi.append([agent.location[0]-1,agent.location[1]])
            if self.list_things_at([agent.location[0],agent.location[1]+1], tclass=ActiveMine) != []:
                visi.append([agent.location[0],agent.location[1]+1])
            if self.list_things_at([agent.location[0],agent.location[1]-1], tclass=ActiveMine) != []:
                visi.append([agent.location[0],agent.location[1]-1])
            if self.list_things_at([agent.location[0]+1,agent.location[1]], tclass=DeadMine) != []:
                visi.append([agent.location[0]+1,agent.location[1]])
            if self.list_things_at([agent.location[0]-1,agent.location[1]], tclass=DeadMine) != []:
                visi.append([agent.location[0]-1,agent.location[1]])
            if self.list_things_at([agent.location[0],agent.location[1]+1], tclass=DeadMine) != []:
                visi.append([agent.location[0],agent.location[1]+1])
            if self.list_things_at([agent.location[0],agent.location[1]-1], tclass=DeadMine) != []:
                visi.append([agent.location[0],agent.location[1]-1])
            return visi




    #Function to Execute the decided action from the Program function 
        def execute_action(self, agent, action):
            '''changes the state of the environment based on what the agent does.'''
            if action == 'turnright':
                print('Model Based Agent {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.R)
            elif action == 'turnleft':
                print('Model Based Agent {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.L)
            elif action == 'moveforward':
                print('Model Based Agent {} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
                agent.moveforward()
            elif action == "diffuse":
                items = self.list_things_at(agent.location, tclass=ActiveMine)
                if len(items) != 0:
                    if agent.diffuse(items[0]):
                        print('Model Based Agent {} diffused {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])

            elif action == "remove":
                items = self.list_things_at(agent.location, tclass=DeadMine)
                if len(items) != 0:
                    if agent.remove(items[0]):
                        print('Model Based Agent {} removed {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])


        def is_done(self):
            '''By default, it's done when we find a live agent can't be found, or when there are no more mines'''
            no_mines = not any(isinstance(thing, ActiveMine) or isinstance(thing, DeadMine) for thing in self.things)
            dead_agents = not any(agent.is_alive() for agent in self.agents)
            return dead_agents or no_mines


    """
    The Environment is customizable in number or rows and columns by modifying following variables.
    This program also contains code to customize the number of active and dead mines by adjusting the
    following num_activemines and num_deadmines variables.
    It randonly generates mines in different locations within the environment.
    """
    rows,columns,num_activemines,num_deadmines = r,c,na,nd
    """
    Instanciating the Environment, creating(instanciating) and adding agent to environment.
    Instaciating ActiveMine and DeadMine.
    """
    battleground = BattleGround(rows,columns,color={'MineSweeperRandom': (0,0,0), 'DeadMine': (139,0,139), 'ActiveMine': (255, 0, 0)})
    minesweeper = MineSweeperRandom(program)
    activemine = ActiveMine()
    deadmine = DeadMine()
    battleground.add_thing(minesweeper, [0,0])
    """
    The code section below is to create and add the given number of ActiveMines and DeadMines by the user.
    It check if the given number of Mines can be implemented in the environment, if not possible, it'll
    raise an error. If it is possible, then it'll add all the Active and Dead Mines in our environment.
    """
    am = {} #Dict holding activemines
    dm = {} #Dict holding deadmines
    log = [] #List that rememberes the occupied positions by mines

    #Code to check if the env has enough space to add the given mines
    if (num_activemines + num_deadmines) > (rows*columns):
        ss = 'There is no more space to add any more mines in the battleground. You can have only a maximum of {} mines for your given area configuration, but you have given {} active mines and {} dead mines which adds to a total of {} mines. Reduce {} number of mines.'.format(rows*columns,num_activemines,num_deadmines,num_activemines+num_deadmines,num_activemines+num_deadmines-rows*columns)
        raise ValueError(ss)


    #Setting up Seed so that the mines created will be in the same place whenever it's being run(For testing & comparing purposes)
    #We can disable the seed if reqd after the performance tests and comparisons.
    random.seed(12)

    #To create and add given number of active mines in the environment
    for i in range(num_activemines):
        var = "AM"+str(i) #Creating name for the instance of Active mine
        am[var] = ActiveMine() #instanciating active mine
        temp = [random.randint(0,rows),random.randint(0,columns)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows),random.randint(0,columns)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(am[var],temp) #Created Mine will be added at the decided position


    #To create and add given number of dead mines in the environment    
    for i in range(num_deadmines):
        var = "DM"+str(i) #Creating name for the instance of dead mine
        dm[var] = DeadMine() #instanciating dead mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(dm[var],temp) #Created Mine will be added at the decided position


    start_time = time()   
    battleground.run(4000,0.00001) #Run the Simulation
    time_taken = time() - start_time

    '''TO Print Performance Report'''
    occured_cost = minesweeper.cost
    time_taken
    left_mines = 0
    for i in battleground.things:
        if isinstance(i,ActiveMine):
            left_mines += 1
        if isinstance(i,DeadMine):
            left_mines += 1
    Percentage_mines_removed = (num_activemines+num_deadmines - left_mines)/(num_activemines+num_deadmines)
    no_of_steps_taken = minesweeper.moves
    cost_per_mine_eradication = occured_cost / (num_activemines+num_deadmines - left_mines)
    MBA_PF = "\n\nMODEL BASED AGENT REPORT:\nOccured Cost: {}\nTime taken: {}s\nNumber of total mines: {}\nNumber of Mines Removed: {}\nNumber of mines left: {}\nPercentage of removed mines: {}\nNo of moves: {}\nCost per mine Eradication: {}\nEnvironment dimension: [{},{}]".format(occured_cost,time_taken,num_activemines+num_deadmines,num_activemines+num_deadmines-left_mines,left_mines,Percentage_mines_removed,no_of_steps_taken,cost_per_mine_eradication,rows,columns)

    #print(MBA_PF)

    ######### (1.1.2 END)<RUN PROGRAM UNTIL HERE - MODEL BASED AGENT> ###################






    ############## SUB PART 1.1.3 GOAL BASED AGENT ###########################
    ######### (1.1.3 START)<RUN PROGRAM FROM HERE - GOAL BASED AGENT> ###################
    """

    Problem Statement/ Concept:
    The environment is actually an old battleground that contains multiple landmines in it.
    We are sending in an AI robotic agent which scans the land (More on this later), defuses and removes the mines.

    Agent:This is a robot which scans the area and performs the following actions.
    If active mines are found, they are defused and removed from the environment.
    If dead mines are found, they are removed from the environment.
    The robot is very good at defusing the mines, so if it reaches the location,
    it has a probability of 1 of defusing the bomb, hence there are no circumstances where
    the agent may fail to defuse the bomb successfully, triggering an explosion.

    In this model based agent, the agent has a memory of the mines it has seen and will go to them to take action.
    If there are no mines in memory, then it will move randomly, scanning for mines.
    It will move towards the mine it has seen the earliest(the first ones in its memory list)

    PEAS Description:

    Performance:
    Performance Measures: Cost to perform actions, time taken, Percentage of Mines removed, No of steps taken,
    Cost per mine eradication
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.
    Moving forward costs 1 unit
    Turning left or Turning right costs 0.5 units

    Environment:The environment (Battleground) has mines in which some of them have exploded or are dead,
    but there are materialistic remains, which needs to be cleared.
    Active mines should have to be carefully defused and then removed from the battleground.
    It is a 2D Graphically represented environment.
    >Grey square: Empty position
    >Black square: Position containing the agent
    >Red square: Position containing Active Mine
    >Purple square: Position containing Dead Mine
    *Partially observable: The Battleground is partially observable because the agent can only perceive 
    the environment at the location that it is currently present in
    *Deterministic: The result and outcome of the world are already known
    *Sequential
    *Static: The ActiveMine or DeadMine nor the walls move
    *Discrete
    *One agent: Minesweeper agent only


    Actuators:Turn Left, Move Forward, Turn right, Diffuse, Remove
    Note: The process is mentioned 'Diffuse' shortly, but actually it Diffuses and Removes mines.


    Sensors:
    Active Mine Detector, Dead Mine detector in its current posititon and can also detect in the next front and the side location.
    The percepts are stored in a list.
    Scanned and found mines are stored in its memory until the required action is taken.
    """



    #importing required libraries and required modules from aima-python-master
#     from agents import *
#     from notebook import psource
#     from random import choice
#     from time import time

    """
    Creating Things Active Mine and Dead mines to use them as objects in our environment
    Child of Thing class in agents.py
    These mines don't have a specific task to do according to our concept, so they are empty.
    They are just objects in our environment
    """
    class ActiveMine(Thing):
        pass

    class DeadMine(Thing):
        pass

    """
    Creating our Agent, to use in our environment
    Child of Agent class in agents.py
    This MinesweeperRandom is our SIMPLE REFLEX AGENT
    """


    class MineSweeperRandom(Agent):
        #Defining variables to store agent location, agent current direction & occured cost
        location = [0,0]
        direction = Direction("down")
        found_mines = [] #Memory of Model Based agent to store the found mines
        target_mine = [] #The traget mine that the agent moves to
        cost = 0
        moves = 0

        #To make agent move forward    
        def moveforward(self, success=True):
            '''moveforward possible only if success (i.e. valid destination location)'''
            if not success:
                return
            if self.direction.direction == Direction.R:
                self.location[0] += 1
            elif self.direction.direction == Direction.L:
                self.location[0] -= 1
            elif self.direction.direction == Direction.D:
                self.location[1] += 1
            elif self.direction.direction == Direction.U:
                self.location[1] -= 1
            self.cost += 1
            self.moves +=1

        #To make the agent turn in the given direction    
        def turn(self, d):
            self.direction = self.direction + d
            self.cost += 0.5
            self.moves +=1

        #To Diffuse the found Active mine and remove it(delete from environment)      
        def diffuse(self, thing):
            '''returns True upon success or False otherwise'''
            if isinstance(thing, ActiveMine):
                self.cost += 3
                self.moves +=1
                return True
            return False

        #To Remove the found Dead mine(delete from environment)
        def remove(self, thing):
            ''' returns True upon success or False otherwise'''
            if isinstance(thing, DeadMine):
                self.cost += 2
                self.moves +=1
                return True
            return False

        #To find the closes mine fromt he found_mines, to set the target    
        def closest_mine(self): # p = agent's found_mines
            closest_distance = 99999
            closest_mine = []
            if self.target_mine != []:
                return self.target_mine
            for i in self.found_mines:
                dist = abs(self.location[0] - i[0]) + abs(self.location[1] - i[1]) #Manhattan distance formulae
                if dist < closest_distance:
                    closest_distance = dist
                    closest_mine = i
            return closest_mine

    """
    The following Program function is the brain of the Agent.
    It takes decisions to be executed, after finding the closest mine from its location,
    and setting it as the target and does the required action after reaching it.

    This time, the battleground was scanned with a detachable drone from the robot,
    it scanned and found all the mines locations, returned to the robot and transferred the data
    about the locations of the mines. This time it has powerful percepts.

    If it detects any mine in its current location, it removes it from the environment(There's no chance of failure).
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.

    The agent also stays in the bounds of the environment by checking its coordinates using the Bump concept.

    The Goal of the Agent is to leave with battleground without any mines.
    """
    def program(xyz, percepts): #xyz is the agent
        choice = 1
        turn = True
        for p in percepts: # first eat or drink - you're a dog
            if isinstance(p, ActiveMine):
                return 'diffuse'
            elif isinstance(p, DeadMine):
                return 'remove'
            if isinstance(p,Bump): # then check if you are at an edge and have to turn
                turn = False
                choice = random.choice((1,2));
            if isinstance(p, list): #Vision of the Minesweeper
                for i in p:
                    if i not in xyz.found_mines:
                        xyz.found_mines.append(i)
        #Delete the mine from the memory if the agent has reached it and reset target
        if xyz.location in xyz.found_mines:
            xyz.found_mines.remove(xyz.location)
        if xyz.location == xyz.target_mine:
            xyz.target_mine = []

    ###If there are no found mines, then the agent will travel randomly(But the program also ends since the goal is achieved)
        if xyz.found_mines == [] and xyz.target_mine == []:
            if turn:
                choice = random.choice((1,2,3,4)) # 1-right, 2-left, others-forward
            if choice == 1:
                return 'turnright'
            elif choice == 2:
                return 'turnleft'
            else:
                return 'moveforward'
    ###If there are found mines, then the agent will move towards the earliest found mine in the memory
        else:
            xyz.target_mine = xyz.closest_mine()
            to_move = 'move_down'
            x,y = xyz.location
            x1,y1 = xyz.target_mine
            x_dir = x-x1
            y_dir = y-y1

    ###Calculating the next move(moveforward, turnright, turnleft) to take in order to go closer to the mine 
            if not x_dir == 0:
                if x_dir < 0:
                    to_move = 'move_right'
                elif x_dir > 0:
                    to_move = 'move_left'
                else:
                    pass
            else:
                if y_dir < 0:
                    to_move = 'move_down'
                elif y_dir > 0:
                    to_move = 'move_up'
                else:
                    pass



            if to_move == 'move_right':
                if xyz.direction.direction == 'up':
                    return 'turnright'
                elif xyz.direction.direction == 'right':
                    return 'moveforward'
                elif xyz.direction.direction == 'down':
                    return 'turnleft'
                elif xyz.direction.direction == 'left':
                    return 'turnright'

            elif to_move == 'move_left':
                if xyz.direction.direction == 'up':
                    return 'turnleft'
                elif xyz.direction.direction == 'right':
                    return 'turnleft'
                elif xyz.direction.direction == 'down':
                    return 'turnright'
                elif xyz.direction.direction == 'left':
                    return 'moveforward'

            elif to_move == 'move_up':
                if xyz.direction.direction == 'up':
                    return 'moveforward'
                elif xyz.direction.direction == 'right':
                    return 'turnleft'
                elif xyz.direction.direction == 'down':
                    return 'turnright'
                elif xyz.direction.direction == 'left':
                    return 'turnright'

            elif to_move == 'move_down':
                if xyz.direction.direction == 'up':
                    return 'turnright'
                elif xyz.direction.direction == 'right':
                    return 'turnright'
                elif xyz.direction.direction == 'down':
                    return 'moveforward'
                elif xyz.direction.direction == 'left':
                    return 'turnleft'

    """
    Creating the Environment BattleGround.
    It is a child of the GraphicEnvironment class in agents.py
    This is a graphical environment and is really useful to visualize simulations.
    The environment can hold 'Things' class's sub classes as things in the environment.
    The defined things are ActiveMines, DeadMines and Bump if the agent is about to bump into a wall.
    """




    class BattleGround(GraphicEnvironment):
        GraphicEnvironment.color={255,255,255}


        def step(self): #Overriding the function since we're modifying it as follows
            if not self.is_done():
                actions = []
                for agent in self.agents:
                    if agent.alive:
                        actions.append(agent.program(agent, self.percept(agent))) #To pass agent as parameter in function program along with percepts 
                    else:
                        actions.append("")
                for (agent, action) in zip(self.agents, actions):
                    self.execute_action(agent, action)
                self.exogenous_change()


       #Adds thing to the environment in the given location     
        def add_thing(self, thing, location=None):
            """Add a thing to the environment, setting its location. For
            convenience, if thing is an agent program we make a new agent
            for it. (Shouldn't need to override this.)"""
            if not isinstance(thing, Thing):
                thing = Agent(thing)#Add thing object to self.things list
            if thing in self.things:
                print("Can't add the same thing twice")
            else:
                thing.location = location if location is not None else self.default_location(thing)
                self.things.append(thing)
                if isinstance(thing, Agent):
                    thing.performance = 0
                    thing.location = location#Add thing object(Agent) to the agent's instance
                    self.agents.append(thing)

        def percept(self, agent):
            '''return a list of things that are in our agent's location.
            Add the found mines objects everywhere in the environment '''
            things = self.list_things_at(agent.location)
            loc = copy.deepcopy(agent.location) # find out the target location
            #Check if agent is about to bump into a wall
            if agent.direction.direction == Direction.R:
                loc[0] += 1
            elif agent.direction.direction == Direction.L:
                loc[0] -= 1
            elif agent.direction.direction == Direction.D:
                loc[1] += 1
            elif agent.direction.direction == Direction.U:
                loc[1] -= 1
            if not self.is_inbounds(loc):
                things.append(Bump())
            things.append(self.vis(agent))#adds the scanned objects to the things list
            return things

        ###This function Scans everywhere in the battleground and marks the mine's locations and it's types.
        ###It is equivalent to the drone which scans the full battleground.
        #This function is called by the percepts function.
        def vis(self,agent):
            visi = []
            for i in self.things:
                if isinstance(i,ActiveMine):
                    visi.append(i.location)
                if isinstance(i,DeadMine):
                    visi.append(i.location)
            return visi




    #Function to Execute the decided action from the Program function    
        def execute_action(self, agent, action):
            '''changes the state of the environment based on what the agent does.'''
            if action == 'turnright':
                print('Goal Based Agent {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.R)
            elif action == 'turnleft':
                print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.L)
            elif action == 'moveforward':
                print('Goal Based Agent {} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
                agent.moveforward()
            elif action == "diffuse":
                items = self.list_things_at(agent.location, tclass=ActiveMine)
                if len(items) != 0:
                    if agent.diffuse(items[0]):
                        print('Goal Based Agent {} diffused {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])

            elif action == "remove":
                items = self.list_things_at(agent.location, tclass=DeadMine)
                if len(items) != 0:
                    if agent.remove(items[0]):
                        print('Goal Based Agent {} removed {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])


        def is_done(self):
            '''By default, it's done when we find a live agent can't be found, or when there are no more mines'''
            no_mines = not any(isinstance(thing, ActiveMine) or isinstance(thing, DeadMine) for thing in self.things)
            dead_agents = not any(agent.is_alive() for agent in self.agents)
            return dead_agents or no_mines


    """
    The Environment is customizable in number or rows and columns by modifying following variables.
    This program also contains code to customize the number of active and dead mines by adjusting the
    following num_activemines and num_deadmines variables.
    It randonly generates mines in different locations within the environment.
    """

    rows,columns,num_activemines,num_deadmines = r,c,na,nd
    """
    Instanciating the Environment, creating(instanciating) and adding agent to environment.
    Instaciating ActiveMine and DeadMine.
    """

    battleground = BattleGround(rows,columns,color={'MineSweeperRandom': (0,0,0), 'DeadMine': (139,0,139), 'ActiveMine': (255, 0, 0)})
    minesweeper = MineSweeperRandom(program)
    activemine = ActiveMine()
    deadmine = DeadMine()
    battleground.add_thing(minesweeper, [0,0])

    """
    The code section below is to create and add the given number of ActiveMines and DeadMines by the user.
    It check if the given number of Mines can be implemented in the environment, if not possible, it'll
    raise an error. If it is possible, then it'll add all the Active and Dead Mines in our environment.
    """
    am = {} #Dict holding activemines
    dm = {} #Dict holding deadmines
    log = [] #List that rememberes the occupied positions by mines

    #Code to check if the env has enough space to add the given mines
    if (num_activemines + num_deadmines) > (rows*columns):
        ss = 'There is no more space to add any more mines in the battleground. You can have only a maximum of {} mines for your given area configuration, but you have given {} active mines and {} dead mines which adds to a total of {} mines. Reduce {} number of mines.'.format(rows*columns,num_activemines,num_deadmines,num_activemines+num_deadmines,num_activemines+num_deadmines-rows*columns)
        raise ValueError(ss)


    #Setting up Seed so that the mines created will be in the same place whenever it's being run(For testing & comparing purposes)
    #We can disable the seed if reqd after the performance tests and comparisons.
    random.seed(12)

    #To create and add given number of active mines in the environment
    for i in range(num_activemines):
        var = "AM"+str(i) #Creating name for the instance of Active mine
        am[var] = ActiveMine() #instanciating active mine
        temp = [random.randint(0,rows),random.randint(0,columns)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows),random.randint(0,columns)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(am[var],temp) #Created Mine will be added at the decided position


    #To create and add given number of dead mines in the environment    
    for i in range(num_deadmines):
        var = "DM"+str(i) #Creating name for the instance of dead mine
        dm[var] = DeadMine() #instanciating dead mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(dm[var],temp) #Created Mine will be added at the decided position


    start_time = time()   
    battleground.run(4000,0.00001) #Run the Simulation
    time_taken = time() - start_time

    '''TO Print Performance Report'''
    occured_cost = minesweeper.cost
    time_taken
    left_mines = 0
    for i in battleground.things:
        if isinstance(i,ActiveMine):
            left_mines += 1
        if isinstance(i,DeadMine):
            left_mines += 1
    Percentage_mines_removed = (num_activemines+num_deadmines - left_mines)/(num_activemines+num_deadmines)
    no_of_steps_taken = minesweeper.moves
    cost_per_mine_eradication = occured_cost / (num_activemines+num_deadmines - left_mines)
    GBA_PF = "\n\nGOAL BASED AGENT REPORT:\nOccured Cost: {}\nTime taken: {}s\nNumber of total mines: {}\nNumber of Mines Removed: {}\nNumber of mines left: {}\nPercentage of removed mines: {}\nNo of moves: {}\nCost per mine Eradication: {}\nEnvironment dimension: [{},{}]".format(occured_cost,time_taken,num_activemines+num_deadmines,num_activemines+num_deadmines-left_mines,left_mines,Percentage_mines_removed,no_of_steps_taken,cost_per_mine_eradication,rows,columns)

    #print(GBA_PF)

    ######### (1.1.3 END)<RUN PROGRAM UNTIL HERE - GOAL BASED AGENT> ###################
    print(SRA_PF)
    print(MBA_PF)
    print(GBA_PF)
    
    to_return = "{}\n{}\n{}".format(SRA_PF,MBA_PF,GBA_PF)
    
    return to_return
    

from agents import *
from search import *
from notebook import psource
from time import *
from random import choice


######################### PART 1 ENDS ############################





######################### PART 2, QUESTION 1.2 ############################


def part2(r,c,am,dm):
    ######################### PART 2, QUESTION 1.2 ############################

    ############## SUB PART 1.2 Search Algorithms ###########################
    ######### (1.2 START)<RUN PROGRAM FROM HERE> ###################
    """

    Problem Statement/ Concept:
    The environment is actually an old battleground that contains multiple landmines in it.
    We are sending in an AI robotic agent which scans the land (More on this later), defuses and removes the mines.

    Agent:This is a robot which scans the area and performs the following actions.
    If active mines are found, they are defused and removed from the environment.
    If dead mines are found, they are removed from the environment.
    The robot is very good at defusing the mines, so if it reaches the location,
    it has a probability of 1 of defusing the bomb, hence there are no circumstances where
    the agent may fail to defuse the bomb successfully, triggering an explosion.


    PEAS Description:

    Performance:
    Performance Measures: Cost to perform actions, time taken, Percentage of Mines removed, No of steps taken,
    Cost per mine eradication
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.
    Moving forward costs 1 unit
    Turning left or Turning right costs 0.5 units

    Environment:The environment (Battleground) has mines in which some of them have exploded or are dead,
    but there are materialistic remains, which needs to be cleared.
    Active mines should have to be carefully defused and then removed from the battleground.
    It is a 2D Graphically represented environment.
    >Grey square: Empty position
    >Black square: Position containing the agent
    >Red square: Position containing Active Mine
    >Purple square: Position containing Dead Mine
    *Partially observable: The Battleground is partially observable because the agent can only perceive 
    the environment at the location that it is currently present in
    *Deterministic: The result and outcome of the world are already known
    *Sequential
    *Static: The ActiveMine or DeadMine nor the walls move
    *Discrete
    *One agent: Minesweeper agent only


    Actuators:Turn Left, Move Forward, Turn right, Diffuse, Remove
    Note: The process is mentioned 'Diffuse' shortly, but actually it Diffuses and Removes mines.


    Sensors:
    Active Mine Detector, Dead Mine detector in its current position.
    The percepts are stored in a list.

    """



    #importing required libraries and required modules from aima-python-master
#     from agents import *
#     from search import *
#     from notebook import psource
#     from time import *
#     from random import choice


    class ActiveMine(Thing):
        pass

    class DeadMine(Thing):
        pass
    """
    Creating Things Active Mine and Dead mines to use them as objects in our environment
    Child of Thing class in agents.py
    These mines don't have a specific task to do according to our concept, so they are empty.
    They are just objects in our environment
    """
    class ActiveMine(Thing):
        pass
    class DeadMine(Thing):
        pass



    """
    Creating our Agent, to use in our environment
    Child of Agent class in agents.py
    This MinesweeperRandom is our SIMPLE REFLEX AGENT
    """

    class MineSweeperRandom(Agent):
        #Defining variables to store agent location, agent current direction & occured cost
        location = [0,0]
        direction = Direction("down")
        found_mines = []

        def moveforward(self, success=True):
            '''moveforward possible only if success (i.e. valid destination location)'''
            if not success:
                return
            if self.direction.direction == Direction.R:
                self.location[0] += 1
            elif self.direction.direction == Direction.L:
                self.location[0] -= 1
            elif self.direction.direction == Direction.D:
                self.location[1] += 1
            elif self.direction.direction == Direction.U:
                self.location[1] -= 1

        #To make the agent turn in the given direction
        def turn(self, d):
            self.direction = self.direction + d

        def diffuse(self, thing):
            '''returns True upon success or False otherwise'''
            if isinstance(thing, ActiveMine):
                return True
            return False
        
        #To Diffuse the found Active mine and remove it(delete from environment)
        def remove(self, thing):
            ''' returns True upon success or False otherwise'''
            if isinstance(thing, DeadMine):
                return True
            return False
        
    """
    The following Program function is the brain of the Agent.
    It takes decisions to be executed, based on the Percepts it receives.

    Our Simple Reflex agent doesn't have to do much except it moves randomly as follows:
    50% Probability to move forward, costs 1 unit
    25% Probability to turn right, costs 0.5 units
    25% Probability to turn Left, costs 0.5 units

    It can see the things available only in it's location, it can't see ahead or around it.

    If it detects any mine in its current location, it removes it from the environment(There's no chance of failure).
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.

    The agent also stays in the bounds of the environment by checking its coordinates using the Bump concept.
    """

    def program(xyz, percepts):
        choice = 1
        turn = True
        for p in percepts: #Checks the current percepts
            if isinstance(p, ActiveMine): #Diffuses active mine if found
                return 'diffuse'
            elif isinstance(p, DeadMine): #Removes Dead mine if found
                return 'remove'
            if isinstance(p,Bump): # to check if the agent is at an edge and have to turn
                turn = False
                choice = random.choice((1,2));
            if isinstance(p, list): #Vision of the Minesweeper
                for i in p:
                    if i not in xyz.found_mines:
                        xyz.found_mines.append(i)

        if xyz.location in xyz.found_mines:
            xyz.found_mines.remove(xyz.location)

    ###If there are no found mines, then the agent will travel randomly
        if xyz.found_mines == []:
            if turn:
                choice = random.choice((1,2,3,4)) # 1-right, 2-left, others-forward
            if choice == 1:
                return 'turnright'
            elif choice == 2:
                return 'turnleft'
            else:
                return 'moveforward'
        else:
            to_move = 'move_down'
            x,y = xyz.location
            x1,y1 = xyz.found_mines[0]
            x_dir = x-x1
            y_dir = y-y1

            if not x_dir == 0:
                if x_dir < 0:
                    to_move = 'move_right'
                elif x_dir > 0:
                    to_move = 'move_left'
                else:
                    pass
            else:
                if y_dir < 0:
                    to_move = 'move_down'
                elif y_dir > 0:
                    to_move = 'move_up'
                else:
                    pass




            if to_move == 'move_right':
                if xyz.direction.direction == 'up':
                    return 'turnright'
                elif xyz.direction.direction == 'right':
                    return 'moveforward'
                elif xyz.direction.direction == 'down':
                    return 'turnleft'
                elif xyz.direction.direction == 'left':
                    return 'turnright'

            elif to_move == 'move_left':
                if xyz.direction.direction == 'up':
                    return 'turnleft'
                elif xyz.direction.direction == 'right':
                    return 'turnleft'
                elif xyz.direction.direction == 'down':
                    return 'turnright'
                elif xyz.direction.direction == 'left':
                    return 'moveforward'

            elif to_move == 'move_up':
                if xyz.direction.direction == 'up':
                    return 'moveforward'
                elif xyz.direction.direction == 'right':
                    return 'turnleft'
                elif xyz.direction.direction == 'down':
                    return 'turnright'
                elif xyz.direction.direction == 'left':
                    return 'turnright'

            elif to_move == 'move_down':
                if xyz.direction.direction == 'up':
                    return 'turnright'
                elif xyz.direction.direction == 'right':
                    return 'turnright'
                elif xyz.direction.direction == 'down':
                    return 'moveforward'
                elif xyz.direction.direction == 'left':
                    return 'turnleft'
                
                
    """
    Creating the Environment BattleGround.
    It is a child of the GraphicEnvironment class in agents.py
    This is a graphical environment and is really useful to visualize simulations.
    The environment can hold 'Things' class's sub classes as things in the environment.
    The defined things are ActiveMines, DeadMines and Bump if the agent is about to bump into a wall.
    """
            
    class BattleGround(GraphicEnvironment):
        GraphicEnvironment.color={255,255,255}


        def step(self): #Overriding the function since we're modifying it as follows
            """Run the environment for one time step. If the
            actions and exogenous changes are independent, this method will
            do. If there are interactions between them, you'll need to
            override this method."""
            if not self.is_done():
                actions = []
                for agent in self.agents:
                    if agent.alive:
                        actions.append(agent.program(agent, self.percept(agent))) #To pass agent as parameter in function program along with percepts 
                    else:
                        actions.append("")
                for (agent, action) in zip(self.agents, actions):
                    self.execute_action(agent, action)
                self.exogenous_change()


       #Adds thing to the environment in the given location 
        def add_thing(self, thing, location=None):
            """Add a thing to the environment, setting its location. For
            convenience, if thing is an agent program we make a new agent
            for it. (Shouldn't need to override this.)"""
            if not isinstance(thing, Thing):
                thing = Agent(thing)
            if thing in self.things:
                print("Can't add the same thing twice")
            else:
                thing.location = location if location is not None else self.default_location(thing)
                self.things.append(thing)#Add thing object to self.things list
                if isinstance(thing, Agent):
                    thing.performance = 0
                    thing.location = location#Add thing object(Agent) to the agent's instance
                    self.agents.append(thing)

        def percept(self, agent):
            '''return a list of things that are in our agent's location.
            Add the found mines objects in front and sides of the Agent to it's memory '''
            things = self.list_things_at(agent.location)
            loc = copy.deepcopy(agent.location) # find out the target location
            #Check if agent is about to bump into a wall
            if agent.direction.direction == Direction.R:
                loc[0] += 1
            elif agent.direction.direction == Direction.L:
                loc[0] -= 1
            elif agent.direction.direction == Direction.D:
                loc[1] += 1
            elif agent.direction.direction == Direction.U:
                loc[1] -= 1
            if not self.is_inbounds(loc):
                things.append(Bump())

            things.append(self.vis(agent))#adds the scanned objects to the things list
            return things


        ###This function Scans just in the front and sides of the agent and returns the list.
        #This function is called by the percepts function.
        def vis(self,agent):
            visi = []
            if self.list_things_at([agent.location[0]+1,agent.location[1]], tclass=ActiveMine) != []:
                visi.append([agent.location[0]+1,agent.location[1]])
            if self.list_things_at([agent.location[0]-1,agent.location[1]], tclass=ActiveMine) != []:
                visi.append([agent.location[0]-1,agent.location[1]])
            if self.list_things_at([agent.location[0],agent.location[1]+1], tclass=ActiveMine) != []:
                visi.append([agent.location[0],agent.location[1]+1])
            if self.list_things_at([agent.location[0],agent.location[1]-1], tclass=ActiveMine) != []:
                visi.append([agent.location[0],agent.location[1]-1])
            if self.list_things_at([agent.location[0]+1,agent.location[1]], tclass=DeadMine) != []:
                visi.append([agent.location[0]+1,agent.location[1]])
            if self.list_things_at([agent.location[0]-1,agent.location[1]], tclass=DeadMine) != []:
                visi.append([agent.location[0]-1,agent.location[1]])
            if self.list_things_at([agent.location[0],agent.location[1]+1], tclass=DeadMine) != []:
                visi.append([agent.location[0],agent.location[1]+1])
            if self.list_things_at([agent.location[0],agent.location[1]-1], tclass=DeadMine) != []:
                visi.append([agent.location[0],agent.location[1]-1])
            return visi




    #Function to Execute the decided action from the Program function 
        def execute_action(self, agent, action):
            '''changes the state of the environment based on what the agent does.'''
            if action == 'turnright':
                print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.R)
            elif action == 'turnleft':
                print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.L)
            elif action == 'moveforward':
                print('{} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
                agent.moveforward()
            elif action == "diffuse":
                items = self.list_things_at(agent.location, tclass=ActiveMine)
                if len(items) != 0:
                    if agent.diffuse(items[0]):
                        print('{} diffused {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])

            elif action == "remove":
                items = self.list_things_at(agent.location, tclass=DeadMine)
                if len(items) != 0:
                    if agent.remove(items[0]):
                        print('{} removed {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])


        def is_done(self):
            '''By default, it's done when we find a live agent can't be found, or when there are no more mines'''
            no_mines = not any(isinstance(thing, ActiveMine) or isinstance(thing, DeadMine) for thing in self.things)
            dead_agents = not any(agent.is_alive() for agent in self.agents)
            return dead_agents or no_mines


    """
    The Environment is customizable in number or rows and columns by modifying following variables.
    This program also contains code to customize the number of active and dead mines by adjusting the
    following num_activemines and num_deadmines variables.
    It randonly generates mines in different locations within the environment.
    """
    rows,columns,num_activemines,num_deadmines = r,c,am,dm
    """
    Instanciating the Environment, creating(instanciating) and adding agent to environment.
    Instaciating ActiveMine and DeadMine.
    """
    battleground = BattleGround(rows,columns,color={'MineSweeperRandom': (0,0,0), 'DeadMine': (139,0,139), 'ActiveMine': (255, 0, 0)})
    minesweeper = MineSweeperRandom(program)
    activemine = ActiveMine()
    deadmine = DeadMine()
    battleground.add_thing(minesweeper, [0,0])
    """
    The code section below is to create and add the given number of ActiveMines and DeadMines by the user.
    It check if the given number of Mines can be implemented in the environment, if not possible, it'll
    raise an error. If it is possible, then it'll add all the Active and Dead Mines in our environment.
    """
    am = {} #Dict holding activemines
    dm = {} #Dict holding deadmines
    log = [] #List that rememberes the occupied positions by mines

    #Code to check if the env has enough space to add the given mines
    if (num_activemines + num_deadmines) > (rows*columns):
        ss = 'There is no more space to add any more mines in the battleground. You can have only a maximum of {} mines for your given area configuration, but you have given {} active mines and {} dead mines which adds to a total of {} mines. Reduce {} number of mines.'.format(rows*columns,num_activemines,num_deadmines,num_activemines+num_deadmines,num_activemines+num_deadmines-rows*columns)
        raise ValueError(ss)


    #Setting up Seed so that the mines created will be in the same place whenever it's being run(For testing & comparing purposes)
    #We can disable the seed if reqd after the performance tests and comparisons.
    random.seed(12)

    #To create and add given number of active mines in the environment
    for i in range(num_activemines):
        var = "AM"+str(i) #Creating name for the instance of Active mine
        am[var] = ActiveMine() #instanciating active mine
        temp = [random.randint(0,rows),random.randint(0,columns)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows),random.randint(0,columns)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(am[var],temp) #Created Mine will be added at the decided position


    #To create and add given number of dead mines in the environment    
    for i in range(num_deadmines):
        var = "DM"+str(i) #Creating name for the instance of dead mine
        dm[var] = DeadMine() #instanciating dead mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(dm[var],temp) #Created Mine will be added at the decided position


    am_loc = [x.location for x in list(am.values())]
    dm_loc = [x.location for x in list(dm.values())]

    #Function to find Manhattan Distance between given 2 points
    def manhatt_distance(point1,point2): # p = agent's found_mines
        dist = abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
        return dist

    #We set the heuristic as the sum of all the Manhattan Distances from the agent to all the mines
    def heuristic(node):
        if not node.state:
            return 0
        things = node.state.things
        mines = []
        heur_value = 0
        for i in things:
            if isinstance(i,ActiveMine):
                mines.append(i.location)
            if isinstance(i,DeadMine):
                mines.append(i.location)
        for i in mines:
            heur_value += manhatt_distance(node.state.ag_loc,i)
        return heur_value

    #We are searching by the States of the program. The below class holds all the states.
    class GameState:
        def __init__(self, env, ag, parent = None):
            self.things = copy.deepcopy(env.things) #Available Things in Environment
            self.ag_loc = copy.deepcopy(ag.location) #Agent's location
            self.ag_dir = ag.direction #Agent's Direction
            self.parent = parent #The parent State(Previous State)

        def __eq__(self, other_state): # Function to check if 2 given states are equal
            if isinstance(other_state, GameState):
                if self.ag_dir.direction == other_state.ag_dir.direction:
                    if all([x == y for x,y in zip(self.ag_loc, other_state.ag_loc)]):
                        if all([all([type(x) == type(y), x.location[0] == y.location[0], x.location[1] == y.location[1]]) for x,y in zip(self.things, other_state.things)]):
                            return True
            return False

        def __lt__(self, other_state): # to check if a given state is less than the other one
            return len(self.things) > len(other_state.things)

        def __repr__(self): #Representation of output print(gamestate)
            return '<< GameState Things: {}, Loc: {}, Dir: {} >>'.format(self.things, self.ag_loc, self.ag_dir.direction)

        
    #Here is our BattleGorundProblem class which inherits Problem from search.py
    class BattleGroundProblem(Problem):
        def __init__(self, initial, goal = None, gameSize = None):
            super().__init__(initial, goal)
            self.gameSize = gameSize
            
        #Returns Possible  actions for a given state
        def actions(self, state):
            if not isinstance(state, GameState):
                return []
            mine_actions = []
            for i in state.things:
                    if state.ag_loc[0] == i.location[0] and state.ag_loc[1] == i.location[1]:
                        if isinstance(i, DeadMine):
                            if not 'remove' in mine_actions:
                                return ['remove']
                        if isinstance(i, ActiveMine):
                            if not 'diffuse' in mine_actions:
                                return ['diffuse']
            if len(mine_actions) > 0:
                return mine_actions
            if state.ag_dir.direction == Direction.R:
                if (0 <= state.ag_loc[0]+1 < self.gameSize[0]) and (0 <= state.ag_loc[1] < self.gameSize[1]):
                    return ['moveforward', 'turnleft', 'turnright']
            elif state.ag_dir.direction == Direction.L:
                if (0 <= state.ag_loc[0]-1 < self.gameSize[0]) and (0 <= state.ag_loc[1] < self.gameSize[1]):
                    return ['moveforward', 'turnleft', 'turnright']
            elif state.ag_dir.direction == Direction.D:
                if (0 <= state.ag_loc[0] < self.gameSize[0]) and (0 <= state.ag_loc[1]+1 < self.gameSize[1]):
                    return ['moveforward', 'turnleft', 'turnright']
            elif state.ag_dir.direction == Direction.U:
                if (0 <= state.ag_loc[0] < self.gameSize[0]) and (0 <= state.ag_loc[1]-1 < self.gameSize[1]):
                    return ['moveforward', 'turnleft', 'turnright']
            return ['turnleft', 'turnright']
        
        #To check if the current state has been in the history of states(Uses linked lists)
        def check(self, child):
            ancestor = child.parent
            while not (ancestor.parent == None):
                if(child == ancestor.parent):
                    return True
                ancestor = ancestor.parent
            return False

        #Determines the resulting state when a particular action is taken in the current state
        def result(self, state, action):
            if not isinstance(state, GameState):
                return None
            new_state = copy.deepcopy(state)
            new_state.parent = state
            if action == 'turnright':
                new_state.ag_dir = new_state.ag_dir + Direction.R
                if not self.check(new_state):
                    return new_state
            if action == 'turnleft':
                new_state.ag_dir = new_state.ag_dir + Direction.L
                if not self.check(new_state):
                    return new_state
            if action == 'moveforward':
                if new_state.ag_dir.direction == Direction.R:
                    new_state.ag_loc[0] += 1
                elif new_state.ag_dir.direction == Direction.L:
                    new_state.ag_loc[0] -= 1
                elif new_state.ag_dir.direction == Direction.D:
                    new_state.ag_loc[1] += 1
                elif new_state.ag_dir.direction == Direction.U:
                    new_state.ag_loc[1] -= 1
                if not self.check(new_state):
                    return new_state
            if action == "diffuse":
                for i in new_state.things:
                    if new_state.ag_loc[0] == i.location[0] and new_state.ag_loc[1] == i.location[1]:
                        if isinstance(i, ActiveMine):
                            new_state.things.remove(i)
                if not self.check(new_state):
                    return new_state
            if action == "remove":
                for i in new_state.things:
                    if new_state.ag_loc[0] == i.location[0] and new_state.ag_loc[1] == i.location[1]:
                        if isinstance(i, DeadMine):
                            new_state.things.remove(i)
                if not self.check(new_state):
                    return new_state

        #To check if goal is achieved.
        #Our goal is that the environment shouldn't contain any activemines or dead mines
        def goal_test(self, state):
            if isinstance(state, GameState):
                return not any([isinstance(i, ActiveMine) or isinstance(i, DeadMine) for i in state.things])

        #Defining and adding costs for each action taken to the total path cost
        def path_cost(self, c, state1, action, state2):
            if action == 'turnright':
                c += 0.5
            elif action == 'turnleft':
                c += 0.5
            elif action == 'moveforward':
                c += 1
            elif action == "diffuse":
                c += 3
            elif action == "remove":
                c += 2
            return c
        
        #Value for Hill Climb search, negative of our heuristic since our Heuristic value keeps decreasing,
        #but hill climbing value should keep increasing
        def value(self, state):
            return -heuristic(Node(state))

    #Initializing the initial state, battlegroundproblem and settingup goal states
    init_state = GameState(battleground,minesweeper)
    goal_state = copy.deepcopy(init_state)
    goal_state.things = [minesweeper]
    bgp = BattleGroundProblem(init_state, goal_state, gameSize = [rows,columns])


    ###########BREADTH FIRST SEARCH###############
    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states
    '''
    def breadth_first_graph_search(problem):
        node = Node(problem.initial)
        if problem.goal_test(node.state):
            return node
        frontier = deque([node])
    #     explored = set()
        iteration = 0
        while frontier:
            iteration += 1
            node = frontier.popleft()
    #         explored.add(node.state)
            for child in node.expand(problem):
                if child.state:# not in explored and child not in frontier:
                    if problem.goal_test(child.state):
                        return child
                    frontier.append(child)
        return None

    start = time()
    res1=breadth_first_graph_search(bgp)
    time_taken = time() - start

    BRFS_PR = """BREADTH FIRST SEARCH:

    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}

    DeadMine Locations: {}

    Solution: {}




    """.format(res1.path_cost,time_taken,rows,columns,res1.depth,am_loc,dm_loc,res1.solution())



    ########DEPTH FIRST SEARCH##############
    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states
    '''
        
    def depth_first_graph_search(problem):
        """
        [Figure 3.7]
        Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Does not get trapped by loops.
        If two paths reach a state, only use the first one.
        """
        frontier = [(Node(problem.initial))]  # Stack

    #     explored = []
        iteration = 0
        while frontier:
            iteration += 1
            node = frontier.pop()
            if problem.goal_test(node.state):
                return node
    #         explored.append(node.state)
            children = node.expand(problem)
            frontier.extend(child for child in children)
        return None

    start = time()
    res2=depth_first_graph_search(bgp)
    time_taken = time() - start

    DFS_PR = """DEPTH FIRST SEARCH:

    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}

    DeadMine Locations: {}

    Solution: {}




    """.format(res2.path_cost,time_taken,rows,columns,res2.depth,am_loc,dm_loc,res2.solution())



    ########UNIFORM COST SEARCH############
    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states
    '''
    def best_first_graph_search(problem, f, display=False):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned."""
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
    #     explored = set()
        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return node
    #         explored.add(node.state)
            for child in node.expand(problem):
                if child.state:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None


    def uniform_cost_search(problem, display=False):
        """[Figure 3.14]"""
        return best_first_graph_search(problem, lambda node: node.path_cost, display)

    start = time()
    res3=uniform_cost_search(bgp)
    time_taken = time() - start

    UCS_PR = """UNIFORM COST SEARCH:

    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}

    DeadMine Locations: {}

    Solution: {}




    """.format(res3.path_cost,time_taken,rows,columns,res3.depth,am_loc,dm_loc,res3.solution())

    #############BEST FIRST SEARCH##############
    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states.
    Own Heuristic defined already
    '''
    def best_first_graph_search(problem, f, display=False):
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
    #     explored = set()
        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return node
    #         explored.add(node.state)
            for child in node.expand(problem):
                if child.state:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None


    start = time()
    res4=best_first_graph_search(bgp, heuristic)
    time_taken = time() - start

    BEFS_PR = """BEST FIRST SEARCH:

    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}

    DeadMine Locations: {}

    Solution: {}




    """.format(res4.path_cost,time_taken,rows,columns,res4.depth,am_loc,dm_loc,res4.solution())


    ############# A* SEARCH##############
    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states.
    Own Heuristic defined already
    '''
    def best_first_graph_search(problem, f, display=False):
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
    #     explored = set()
        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return node
    #         explored.add(node.state)
            for child in node.expand(problem):
                if child.state:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None

    def astar_search(problem, h=None, display=False):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
    #     h = memoize(h or problem.h, 'h')
        return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

    start = time()
    res5=astar_search(bgp, heuristic)
    time_taken = time() - start

    ASTAR_PR = """A* SEARCH:

    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}

    DeadMine Locations: {}

    Solution: {}




    """.format(res5.path_cost,time_taken,rows,columns,res5.depth,am_loc,dm_loc,res5.solution())



    ######### HILL CLIMB SEARCH ###################
    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states.
    Own Value defined already (-Heuristic)
    '''
    def hill_climbing(problem):
        """
        [Figure 4.2]
        From the initial node, keep choosing the neighbor with highest value,
        stopping when no neighbor is better.
        """
        current = Node(problem.initial)
        while True:
            neighbors = current.expand(problem)
            if not neighbors:
                break
            neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node.state))
            if problem.value(neighbor.state) <= problem.value(current.state):
                break
            current = neighbor
        return current

    start = time()
    res6=hill_climbing(bgp)
    time_taken = time() - start

    HCS_PR = """HILL CLIMB SEARCH:

    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}

    DeadMine Locations: {}

    Solution: {}




    """.format(res6.path_cost,time_taken,rows,columns,res6.depth,am_loc,dm_loc,res6.solution())

####################RECURSIVE BEST FIRST SEARCH############################

    '''
    Our objects are non hashable. 
    So we removed the explored function and created our own check function 
    which uses linked lists to check of a given state has previously 
    occured in the history of states.
    Own Heuristic defined already
    '''
    
    def recursive_best_first_search(problem, h=None):
        h = memoize(h or problem.h, 'h')

        def RBFS(problem, node, flimit):
            if problem.goal_test(node.state):
                return node, 0  # (The second value is immaterial)
            successors = node.expand(problem)
            if len(successors) == 0:
                return None, np.inf
            for s in successors:
                s.f = max(s.path_cost + h(s), node.f)
            while True:
                # Order by lowest f value
                successors.sort(key=lambda x: x.f)
                best = successors[0]
                if best.f > flimit:
                    return None, best.f
                if len(successors) > 1:
                    alternative = successors[1].f
                else:
                    alternative = np.inf
                result, best.f = RBFS(problem, best, min(flimit, alternative))
                if result is not None:
                    return result, best.f

        node = Node(problem.initial)
        node.f = h(node)
        result, bestf = RBFS(problem, node, np.inf)
        return result

    start = time()
    res8=recursive_best_first_search(bgp, heuristic)
    time_taken = time() - start

    RBFS_PR = """RECURSIVE BEST FIRST SEARCH:
    Path Cost: {}
    Time taken: {}
    Environment Dimension: [{},{}]
    Depth: {}

    ActiveMine Locations: {}
    DeadMine Locations: {}

    Solution: {}
    """.format(res8.path_cost,time_taken,rows,columns,res8.depth,am_loc,dm_loc,res8.solution())

    part2report = """
    *********UNINFORMED SEARCHES:***********
    
    {}
    {}
    {}
    *********INFORMED SEARCHES:************
    {}
    {}
    {}
    {}
    """.format(BRFS_PR,DFS_PR,UCS_PR,BEFS_PR,ASTAR_PR,RBFS_PR,HCS_PR)
    print("*********UNINFORMED SEARCHES:***********\n\n")
    print(BRFS_PR)
    print(DFS_PR)
    print(UCS_PR)
    print("*********INFORMED SEARCHES:************\n\n")
    print(BEFS_PR)
    print(ASTAR_PR)
    print(RBFS_PR)
    print(HCS_PR)
    
    return part2report

    ######### (1.2 ENDS)<RUN PROGRAM UNTIL HERE - SEARCH ALGORITHMS> ###################
    ######################### PART 2, ENDS ############################





from agents import *
from utils import *
from logic import *
from notebook import psource
from random import choice
from time import time
def part3(r,c,amm,dmm):
    ######################### QUESTION 1.3 ############################

    ############## SUB PART 1.3.1 FORWARD CHAINING ###########################
    ######### (1.3.1 START)<RUN PROGRAM FROM HERE - FORWARD CHAINING> ###################
    """

    Problem Statement/ Concept:
    The environment is actually an old battleground that contains multiple landmines in it.
    We are sending in an AI robotic agent which scans the land (More on this later), defuses and removes the mines.

    Agent:This is a robot which scans the area and performs the following actions.
    If active mines are found, they are defused and removed from the environment.
    If dead mines are found, they are removed from the environment.
    The robot is very good at defusing the mines, so if it reaches the location,
    it has a probability of 1 of defusing the bomb, hence there are no circumstances where
    the agent may fail to defuse the bomb successfully, triggering an explosion.


    PEAS Description:

    Performance:
    Performance Measures: Cost to perform actions, time taken, Percentage of Mines removed, No of steps taken,
    Cost per mine eradication
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.
    Moving forward costs 1 unit
    Turning left or Turning right costs 0.5 units

    Environment:The environment (Battleground) has mines in which some of them have exploded or are dead,
    but there are materialistic remains, which needs to be cleared.
    Active mines should have to be carefully defused and then removed from the battleground.
    It is a 2D Graphically represented environment.
    >Grey square: Empty position
    >Black square: Position containing the agent
    >Red square: Position containing Active Mine
    >Purple square: Position containing Dead Mine
    *Partially observable: The Battleground is partially observable because the agent can only perceive 
    the environment at the location that it is currently present in
    *Deterministic: The result and outcome of the world are already known
    *Sequential
    *Static: The ActiveMine or DeadMine nor the walls move
    *Discrete
    *One agent: Minesweeper agent only


    Actuators:Turn Left, Move Forward, Turn right, Diffuse, Remove
    Note: The process is mentioned 'Diffuse' shortly, but actually it Diffuses and Removes mines.


    Sensors:
    Active Mine Detector, Dead Mine detector in its current position.
    The percepts are stored in a list.

    """


    #importing required libraries and required modules from aima-python-master

#     from agents import *
#     from utils import *
#     from logic import *
#     from notebook import psource
#     from random import choice

    """
    Creating Things Active Mine and Dead mines to use them as objects in our environment
    Child of Thing class in agents.py
    These mines don't have a specific task to do according to our concept, so they are empty.
    They are just objects in our environment
    """

    class ActiveMine(Thing):
        pass

    class DeadMine(Thing):
        pass


    """
    Creating our Agent, to use in our environment
    Child of Agent class in agents.py
    This MinesweeperRandom is our SIMPLE REFLEX AGENT
    """

    class MineSweeperRandom(Agent):
        #Defining variables to store agent location, agent current direction & occured cost
        location = [0,0]
        direction = Direction("down")
        cost = 0
        moves = 0

        def __init__(self, program=None):
            self.alive = True
            self.bump = False
            self.holding = []
            self.performance = 0
            if program is None or not isinstance(program, collections.abc.Callable):
                print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

                def program(percept):
                    return eval(input('Percept={}; action? '.format(percept)))

            self.program = program

            ####### Building Agent's Initial Knowledge Base
            self.clauses = []
            self.clauses.append(expr('ActiveMine(x) ==> Action(Diffuse)')) # If Active Mine x exists, then take Action Diffuse
            self.clauses.append(expr('DeadMine(x) ==> Action(Remove)')) #If dead mine Exists, then take Action Remove
            self.clauses.append(expr('(NoMine(x) & NoBump(b)) ==> Action(Moveforward)')) #If NoMine exists and NoBump exists, then take action Moveforward
            self.clauses.append(expr('NoMine(x) ==> Action(Turnleft)')) #If NoMine Exists, Turnleft
            self.clauses.append(expr('NoMine(x) ==> Action(Turnright)')) #If NoMine Exists, Turnright
            self.kb = FolKB(self.clauses) #Build Knowledge Base

        #To make agent move forward
        def moveforward(self, success=True):
            '''moveforward possible only if success (i.e. valid destination location)'''
            if not success:
                return
            if self.direction.direction == Direction.R:
                self.location[0] += 1
            elif self.direction.direction == Direction.L:
                self.location[0] -= 1
            elif self.direction.direction == Direction.D:
                self.location[1] += 1
            elif self.direction.direction == Direction.U:
                self.location[1] -= 1
            self.cost += 1
            self.moves +=1
        #To make the agent turn in the given direction
        def turn(self, d):
            self.direction = self.direction + d
            self.cost += 0.5
            self.moves +=1

        #To Diffuse the found Active mine and remove it(delete from environment)
        def diffuse(self, thing):
            '''returns True upon success or False otherwise'''
            if isinstance(thing, ActiveMine):
                self.cost += 3
                self.moves +=1
                return True
            return False

        #To Remove the found Dead mine(delete from environment)
        def remove(self, thing):
            ''' returns True upon success or False otherwise'''
            if isinstance(thing, DeadMine):
                self.cost += 2
                self.moves +=1
                return True
            return False

    """
    The following Program function is the brain of the Agent.
    It takes decisions to be executed, based on the Percepts it receives, and from its knowledge base.

    Our Simple Reflex agent doesn't have to do much except it moves randomly as follows:
    50% Probability to move forward, costs 1 unit
    25% Probability to turn right, costs 0.5 units
    25% Probability to turn Left, costs 0.5 units

    It can see the things available only in it's location, it can't see ahead or around it.

    If it detects any mine in its current location, it removes it from the environment(There's no chance of failure).
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.

    ***IT PERFORMS EVERY ACTION BY TELLING & ASKING FROM ITS KNOWLEDGE BASE

    The agent also stays in the bounds of the environment by checking its coordinates using the Bump concept.
    """


    def program(agent,percepts):
        no_mine = True #Memory that holds mine availability information
        no_bump = True #Momory that holds the bump availablity information
        for p in percepts: #Checks the current percepts
            if isinstance(p, ActiveMine):
                agent.kb.tell(expr('ActiveMine(AM)'))#Tells to Knowledge base that an Active mine is found
                no_mine = False
            elif isinstance(p, DeadMine):
                agent.kb.tell(expr('DeadMine(DM)'))#Tells to Knowledge base that a Dead mine is found
                no_mine = False
            if isinstance(p,Bump): # then check if you are at an edge and have to turn
                no_bump = False
        if no_mine:
            agent.kb.tell(expr('NoMine(X)'))#Tells to Knowledge base that there's no mine found
        if no_bump:
            agent.kb.tell(expr('NoBump(B)'))#Tells to Knowledge base that there's no Bump found
        to_do = list(fol_fc_ask(agent.kb, expr('Action(x)'))) #Asks the Knowledge base using forward chaining algorithm on what to do, the list of possible actions for this scenario
        print("List of Possible actions:", to_do)
        print()
        print('clauses:', agent.kb.clauses)

        #Refreshes Knowledge Base, removing unwanted information for next iteration
        if expr('ActiveMine(X)') in agent.kb.clauses:
            agent.kb.retract(expr('ActiveMine(X)'))
        if expr('DeadMine(X)') in agent.kb.clauses:
            agent.kb.retract(expr('DeadMine(X)'))
        if expr('NoMine(X)') in agent.kb.clauses:
            agent.kb.retract(expr('NoMine(X)'))
        if expr('NoBump(B)') in agent.kb.clauses:
            agent.kb.retract(expr('NoBump(B)'))
        agent.kb.clauses = agent.kb.clauses[:5]
        print()
        print("NEW CLAUSES:",agent.clauses)
        print()

        choice = random.choice([str(x).lower() for i in to_do for x in i.values()])
        print("choice:",choice)
        print("Agent Direction:",agent.direction.direction)
        return choice

    """
    Creating the Environment BattleGround.
    It is a child of the GraphicEnvironment class in agents.py
    This is a graphical environment and is really useful to visualize simulations.
    The environment can hold 'Things' class's sub classes as things in the environment.
    The defined things are ActiveMines, DeadMines and Bump if the agent is about to bump into a wall.

    """


    class BattleGround(GraphicEnvironment):
        GraphicEnvironment.color={255,255,255}
        def percept(self, agent):
            '''return a list of things that are in our agent's location'''
            things = self.list_things_at(agent.location)
            loc = copy.deepcopy(agent.location) # find out the target location
            #Check if agent is about to bump into a wall
            if agent.direction.direction == Direction.R:
                loc[0] += 1
            elif agent.direction.direction == Direction.L:
                loc[0] -= 1
            elif agent.direction.direction == Direction.D:
                loc[1] += 1
            elif agent.direction.direction == Direction.U:
                loc[1] -= 1
            if not self.is_inbounds(loc):
                things.append(Bump())
            return things
        #Function to Execute the decided action from the Program function
        def execute_action(self, agent, action):
            '''changes the state of the environment based on what the agent does.'''
            if action == 'turnright':
                print('ForwardChained {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.R)
            elif action == 'turnleft':
                print('ForwardChained {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.L)
            elif action == 'moveforward':
                print('ForwardChained {} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
                agent.moveforward()
            elif action == "diffuse":
                items = self.list_things_at(agent.location, tclass=ActiveMine)
                if len(items) != 0:
                    if agent.diffuse(items[0]):
                        print('ForwardChained {} diffused {} at location: {}'.format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])
            elif action == "remove":
                items = self.list_things_at(agent.location, tclass=DeadMine)
                if len(items) != 0:
                    if agent.remove(items[0]):
                        print('ForwardChained {} removed {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])


        def step(self):
            if not self.is_done():
                actions = []
                for agent in self.agents:
                    if agent.alive:
                        actions.append(agent.program(agent,self.percept(agent)))
                    else:
                        actions.append("")
                for (agent, action) in zip(self.agents, actions):
                    self.execute_action(agent, action)
                self.exogenous_change()

        def is_done(self):
            no_mines = not any(isinstance(thing, ActiveMine) or isinstance(thing, DeadMine) for thing in self.things)
            dead_agents = not any(agent.is_alive() for agent in self.agents)
            return dead_agents or no_mines


    """
    The Environment is customizable in number or rows and columns by modifying following variables.
    This program also contains code to customize the number of active and dead mines by adjusting the
    following num_activemines and num_deadmines variables.
    It randonly generates mines in different locations within the environment.
    """
    rows,columns,num_activemines,num_deadmines = r,c,amm,dmm
    """
    Instanciating the Environment, creating(instanciating) and adding agent to environment.
    Instaciating ActiveMine and DeadMine.
    """
    battleground = BattleGround(rows,columns,color={'MineSweeperRandom': (0,0,0), 'DeadMine': (139,0,139), 'ActiveMine': (255, 0, 0)})
    minesweeper = MineSweeperRandom(program)
    activemine = ActiveMine()
    deadmine = DeadMine()
    battleground.add_thing(minesweeper, [0,0])

    """
    The code section below is to create and add the given number of ActiveMines and DeadMines by the user.
    It check if the given number of Mines can be implemented in the environment, if not possible, it'll
    raise an error. If it is possible, then it'll add all the Active and Dead Mines in our environment.
    """
    am = {}  #Dict holding activemines
    dm = {}  #Dict holding deadmines
    log = [] #List that rememberes the occupied positions by mines


    #Code to check if the env has enough space to add the given mines
    if (num_activemines + num_deadmines) > (rows*columns):
        ss = '''There is no more space to add any more mines in the battleground. 
         You can have only a maximum of {} mines for your given area configuration,
         but you have given {} active mines and {} dead mines which adds to a total of {} mines.
         Reduce {} number of mines.'''.format(rows*columns,num_activemines,num_deadmines,
                                              num_activemines+num_deadmines,
                                              num_activemines+num_deadmines-rows*columns)
        raise ValueError(ss)


    #Setting up Seed so that the mines created will be in the same place whenever it's being run(For testing & comparing purposes)
    #We can disable the seed if reqd after the performance tests and comparisons.
    random.seed(12)


    #To create and add given number of active mines in the environment
    for i in range(num_activemines):
        var = "AM"+str(i)   #Creating name for the instance of Active mine
        am[var] = ActiveMine() #instanciating active mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log:  #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(am[var],temp) #Created Mine will be added at the decided position


    #To create and add given number of dead mines in the environment
    for i in range(num_deadmines):
        var = "DM"+str(i) #Creating name for the instance of dead mine
        dm[var] = DeadMine() #instanciating dead mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(dm[var],temp) #Created Mine will be added at the decided position

    start_time = time()   
    battleground.run(4000,0.00001) #Run the Simulation
    time_taken = time() - start_time


    '''TO Print Performance Report'''
    occured_cost = minesweeper.cost
    time_taken
    left_mines = 0
    for i in battleground.things:
        if isinstance(i,ActiveMine):
            left_mines += 1
        if isinstance(i,DeadMine):
            left_mines += 1
    Percentage_mines_removed = (num_activemines+num_deadmines - left_mines)/(num_activemines+num_deadmines)
    no_of_steps_taken = minesweeper.moves
    cost_per_mine_eradication = occured_cost / (num_activemines+num_deadmines - left_mines)
    FC_PF = "\n\nFORWARDCHAINING:\nOccured Cost: {}\nTime taken: {}s\nNumber of total mines: {}\nNumber of Mines Removed: {}\nNumber of mines left: {}\nPercentage of removed mines: {}\nNo of moves: {}\nCost per mine Eradication: {}".format(occured_cost,time_taken,num_activemines+num_deadmines,num_activemines+num_deadmines-left_mines,left_mines,Percentage_mines_removed,no_of_steps_taken,cost_per_mine_eradication)

    print(FC_PF)

    ######### (1.3.1 END)<RUN PROGRAM UNTIL HERE - FORWARD CHAINING> ###################
    ############## SUB PART 1.3.2 BACKWARD CHAINING ###########################
    ######### (1.3.2 START)<RUN PROGRAM FROM HERE - BACKWARD CHAINING> ###################
    """

    Problem Statement/ Concept:
    The environment is actually an old battleground that contains multiple landmines in it.
    We are sending in an AI robotic agent which scans the land (More on this later), defuses and removes the mines.

    Agent:This is a robot which scans the area and performs the following actions.
    If active mines are found, they are defused and removed from the environment.
    If dead mines are found, they are removed from the environment.
    The robot is very good at defusing the mines, so if it reaches the location,
    it has a probability of 1 of defusing the bomb, hence there are no circumstances where
    the agent may fail to defuse the bomb successfully, triggering an explosion.


    PEAS Description:

    Performance:
    Performance Measures: Cost to perform actions, time taken, Percentage of Mines removed, No of steps taken,
    Cost per mine eradication
    Diffusing an active mine and removing it costs 3 units.
    Removing a dead mine costs 2 units.
    Moving forward costs 1 unit
    Turning left or Turning right costs 0.5 units

    Environment:The environment (Battleground) has mines in which some of them have exploded or are dead,
    but there are materialistic remains, which needs to be cleared.
    Active mines should have to be carefully defused and then removed from the battleground.
    It is a 2D Graphically represented environment.
    >Grey square: Empty position
    >Black square: Position containing the agent
    >Red square: Position containing Active Mine
    >Purple square: Position containing Dead Mine
    *Partially observable: The Battleground is partially observable because the agent can only perceive 
    the environment at the location that it is currently present in
    *Deterministic: The result and outcome of the world are already known
    *Sequential
    *Static: The ActiveMine or DeadMine nor the walls move
    *Discrete
    *One agent: Minesweeper agent only


    Actuators:Turn Left, Move Forward, Turn right, Diffuse, Remove
    Note: The process is mentioned 'Diffuse' shortly, but actually it Diffuses and Removes mines.


    Sensors:
    Active Mine Detector, Dead Mine detector in its current position.
    The percepts are stored in a list.

    """


    #importing required libraries and required modules from aima-python-master

    #     from agents import *
    #     from utils import *
    #     from logic import *
    #     from notebook import psource
    #     from random import choice

    """
    Creating Things Active Mine and Dead mines to use them as objects in our environment
    Child of Thing class in agents.py
    These mines don't have a specific task to do according to our concept, so they are empty.
    They are just objects in our environment
    """

    class ActiveMine(Thing):
        pass

    class DeadMine(Thing):
        pass


    """
    Creating our Agent, to use in our environment
    Child of Agent class in agents.py
    This MinesweeperRandom is our SIMPLE REFLEX AGENT
    """

    class MineSweeperRandom(Agent):
        #Defining variables to store agent location, agent current direction & occured cost
        location = [0,0]
        direction = Direction("down")
#         cost = 0
#         moves = 0

        def __init__(self, program=None):
            self.alive = True
            self.bump = False
            self.holding = []
            self.performance = 0
            if program is None or not isinstance(program, collections.abc.Callable):
                print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

                def program(percept):
                    return eval(input('Percept={}; action? '.format(percept)))

            self.program = program

            ####### Building Agent's Initial Knowledge Base
            self.clauses = []
            self.clauses.append(expr('ActiveMine(x) ==> Action(Diffuse)')) # If Active Mine x exists, then take Action Diffuse
            self.clauses.append(expr('DeadMine(x) ==> Action(Remove)')) #If dead mine Exists, then take Action Remove
            self.clauses.append(expr('(NoMine(x) & NoBump(b)) ==> Action(Moveforward)')) #If NoMine exists and NoBump exists, then take action Moveforward
            self.clauses.append(expr('NoMine(x) ==> Action(Turnleft)')) #If NoMine Exists, Turnleft
            self.clauses.append(expr('NoMine(x) ==> Action(Turnright)')) #If NoMine Exists, Turnright
            self.kb = FolKB(self.clauses) #Build Knowledge Base

        #To make Agent move Forward
        def moveforward(self, success=True):
            '''moveforward possible only if success (i.e. valid destination location)'''
            if not success:
                return
            if self.direction.direction == Direction.R:
                self.location[0] += 1
            elif self.direction.direction == Direction.L:
                self.location[0] -= 1
            elif self.direction.direction == Direction.D:
                self.location[1] += 1
            elif self.direction.direction == Direction.U:
                self.location[1] -= 1
#             cost += 1
#             move += 1

        def turn(self, d):
            self.direction = self.direction + d
#             cost += 0.5
#             move += 1

        def diffuse(self, thing):
            '''returns True upon success or False otherwise'''
            if isinstance(thing, ActiveMine):
#                 cost += 3
#                 move += 1
                return True
            return False

        def remove(self, thing):
            ''' returns True upon success or False otherwise'''
            if isinstance(thing, DeadMine):
#                 cost += 2
#                 move += 1
                return True
            return False




        """
        The following Program function is the brain of the Agent.
        It takes decisions to be executed, based on the Percepts it receives, and from its knowledge base.

        Our Simple Reflex agent doesn't have to do much except it moves randomly as follows:
        50% Probability to move forward, costs 1 unit
        25% Probability to turn right, costs 0.5 units
        25% Probability to turn Left, costs 0.5 units

        It can see the things available only in it's location, it can't see ahead or around it.

        If it detects any mine in its current location, it removes it from the environment(There's no chance of failure).
        Diffusing an active mine and removing it costs 3 units.
        Removing a dead mine costs 2 units.

        ***IT PERFORMS EVERY ACTION BY TELLING & ASKING FROM ITS KNOWLEDGE BASE

        The agent also stays in the bounds of the environment by checking its coordinates using the Bump concept.
        """


    def program(agent,percepts):
        '''Returns an action based on it's percepts'''
        no_mine = True #Memory that holds mine availability information
        no_bump = True #Momory that holds the bump availablity information
        for p in percepts: #Checks the current percepts
            if isinstance(p, ActiveMine):
                agent.kb.tell(expr('ActiveMine(AM)'))#Tells to Knowledge base that an Active mine is found
                no_mine = False
            elif isinstance(p, DeadMine):
                agent.kb.tell(expr('DeadMine(DM)'))#Tells to Knowledge base that a Dead mine is found
                no_mine = False
            if isinstance(p,Bump): # then check if you are at an edge and have to turn
                no_bump = False
        if no_mine:
            agent.kb.tell(expr('NoMine(X)'))#Tells to Knowledge base that there's no mine found
        if no_bump:
            agent.kb.tell(expr('NoBump(B)'))#Tells to Knowledge base that there's no Bump found
        choice = str(agent.kb.ask(expr('Action(x)'))[expr('x')]).lower() ######ASKING BACKWARD CHAINING ALGORITHM
        print()
        print('Clauses:', agent.kb.clauses)
        if expr('ActiveMine(X)') in agent.kb.clauses:
            agent.kb.retract(expr('ActiveMine(X)'))
        if expr('DeadMine(X)') in agent.kb.clauses:
            agent.kb.retract(expr('DeadMine(X)'))
        if expr('NoMine(X)') in agent.kb.clauses:
            agent.kb.retract(expr('NoMine(X)'))
        if expr('NoBump(B)') in agent.kb.clauses:
            agent.kb.retract(expr('NoBump(B)'))
        agent.kb.clauses = agent.kb.clauses[:5]
        print()
        print("List of possible actions:",choice)
        print("New Clauses:",agent.clauses)
        print()
        print("choice:",choice)
        print("Agent Direction:",agent.direction.direction)
        return choice        

    """
    Creating the Environment BattleGround.
    It is a child of the GraphicEnvironment class in agents.py
    This is a graphical environment and is really useful to visualize simulations.
    The environment can hold 'Things' class's sub classes as things in the environment.
    The defined things are ActiveMines, DeadMines and Bump if the agent is about to bump into a wall.

    """
    class BattleGround(GraphicEnvironment):
        GraphicEnvironment.color={255,255,255}
        def percept(self, agent):
            '''return a list of things that are in our agent's location'''
            things = self.list_things_at(agent.location)
            loc = copy.deepcopy(agent.location) # find out the target location
            #Check if agent is about to bump into a wall
            if agent.direction.direction == Direction.R:
                loc[0] += 1
            elif agent.direction.direction == Direction.L:
                loc[0] -= 1
            elif agent.direction.direction == Direction.D:
                loc[1] += 1
            elif agent.direction.direction == Direction.U:
                loc[1] -= 1
            if not self.is_inbounds(loc):
                things.append(Bump())
            return things

            #Function to Execute the decided action from the Program function
        def execute_action(self, agent, action):
            '''changes the state of the environment based on what the agent does.'''
            if action == 'turnright':
                print('BackwardChained {} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.R)
            elif action == 'turnleft':
                print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
                agent.turn(Direction.L)
            elif action == 'moveforward':
                print('BackwardChained {} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
                agent.moveforward()
            elif action == "diffuse":
                items = self.list_things_at(agent.location, tclass=ActiveMine)
                if len(items) != 0:
                    if agent.diffuse(items[0]):
                        print('BackwardChained {} diffused {} at location: {}'.format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])
            elif action == "remove":
                items = self.list_things_at(agent.location, tclass=DeadMine)
                if len(items) != 0:
                    if agent.remove(items[0]):
                        print('BackwardChained {} removed {} at location: {}'
                              .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                        self.delete_thing(items[0])


        def step(self):
            if not self.is_done():
                actions = []
                for agent in self.agents:
                    if agent.alive:
                        actions.append(agent.program(agent,self.percept(agent)))
                    else:
                        actions.append("")
                for (agent, action) in zip(self.agents, actions):
                    self.execute_action(agent, action)
                self.exogenous_change()

        def is_done(self):
            no_mines = not any(isinstance(thing, ActiveMine) or isinstance(thing, DeadMine) for thing in self.things)
            dead_agents = not any(agent.is_alive() for agent in self.agents)
            return dead_agents or no_mines


    """
    The Environment is customizable in number or rows and columns by modifying following variables.
    This program also contains code to customize the number of active and dead mines by adjusting the
    following num_activemines and num_deadmines variables.
    It randonly generates mines in different locations within the environment.
    """

    rows,columns,num_activemines,num_deadmines = r,c,amm,dmm
    """
    Instanciating the Environment, creating(instanciating) and adding agent to environment.
    Instaciating ActiveMine and DeadMine.
    """
    battleground = BattleGround(rows,columns,color={'MineSweeperRandom': (0,0,0), 'DeadMine': (139,0,139), 'ActiveMine': (255, 0, 0)})
    minesweeper = MineSweeperRandom(program)
    activemine = ActiveMine()
    deadmine = DeadMine()
    battleground.add_thing(minesweeper, [0,0])

    """
    The code section below is to create and add the given number of ActiveMines and DeadMines by the user.
    It check if the given number of Mines can be implemented in the environment, if not possible, it'll
    raise an error. If it is possible, then it'll add all the Active and Dead Mines in our environment.
    """
    am = {}  #Dict holding activemines
    dm = {}  #Dict holding deadmines
    log = [] #List that rememberes the occupied positions by mines


    #Code to check if the env has enough space to add the given mines
    if (num_activemines + num_deadmines) > (rows*columns):
        ss = """There is no more space to add any more mines in the battleground. 
         You can have only a maximum of {} mines for your given area configuration,
         but you have given {} active mines and {} dead mines which adds to a total of {} mines.
         Reduce {} number of mines.""".format(rows*columns,num_activemines,num_deadmines,
                                              num_activemines+num_deadmines,
                                              num_activemines+num_deadmines-rows*columns)
        raise ValueError(ss)


    #Setting up Seed so that the mines created will be in the same place whenever it's being run(For testing & comparing purposes)
    #We can disable the seed if reqd after the performance tests and comparisons.
    random.seed(12)


    #To create and add given number of active mines in the environment
    for i in range(num_activemines):
        var = "AM"+str(i)   #Creating name for the instance of Active mine
        am[var] = ActiveMine() #instanciating active mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log:  #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(am[var],temp) #Created Mine will be added at the decided position


    #To create and add given number of dead mines in the environment
    for i in range(num_deadmines):
        var = "DM"+str(i) #Creating name for the instance of dead mine
        dm[var] = DeadMine() #instanciating dead mine
        temp = [random.randint(0,rows-1),random.randint(0,columns-1)] #Suggesting a random location for mine
        while temp in log: #Checks if the suggested position is occupied, otherwise suggests a new locations and checks it until the task is complete
            temp = [random.randint(0,rows-1),random.randint(0,columns-1)]
        log.append(temp) #Position of Mine recorded in history
        battleground.add_thing(dm[var],temp) #Created Mine will be added at the decided position

    start_time = time()   
    battleground.run(4000,0.00001) #Run the Simulation
    time_taken = time() - start_time


    '''TO Print Performance Report'''
    occured_cost = "N/A"
    time_taken
    left_mines = 0
    for i in battleground.things:
        if isinstance(i,ActiveMine):
            left_mines += 1
        if isinstance(i,DeadMine):
            left_mines += 1
    Percentage_mines_removed = (num_activemines+num_deadmines - left_mines)/(num_activemines+num_deadmines)
    no_of_steps_taken = "N/A"
    cost_per_mine_eradication = "N/A"
    BC_PF = "\n\nBACKWARD CHAINING:\nOccured Cost: {}\nTime taken: {}s\nNumber of total mines: {}\nNumber of Mines Removed: {}\nNumber of mines left: {}\nPercentage of removed mines: {}\nNo of moves: {}\nCost per mine Eradication: {}".format(occured_cost,time_taken,num_activemines+num_deadmines,num_activemines+num_deadmines-left_mines,left_mines,Percentage_mines_removed,no_of_steps_taken,cost_per_mine_eradication)

    print(BC_PF)
    to_ret = """
    {}
    {}
    """.format(FC_PF,BC_PF)
    return to_ret

    ######### (1.3.2 END)<RUN PROGRAM UNTIL HERE - BACKWARD CHAINING> ###################

#############################PART 3 ENDS ############################################### 


# In[5]:


part1reports = part1(20,20,35,35) #Rows,Columns,No of Active mines, No of dead mines #Q1
part2reports = part2(3,3,0,1) #Rows,Columns,No of Active mines, No of dead mines #Q2
part3reports = part3(25,25,50,50) #Rows,Columns,No of Active mines, No of dead mines
print("--------------------PART 1------------------------\n")
print(part1reports)
print("\n\n-------------------PART 2-------------------------\n")
print(part2reports)
print("\n\n-------------------PART 3-------------------------\n")
print(part3reports)


# In[ ]:




