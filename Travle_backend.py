from random import choice
import copy

global bordering_states
bordering_states = dict()
bordering_states['Washington']=['Idaho','Oregon']
bordering_states['Oregon']=['Washington','Idaho','Nevada','California']
bordering_states['California']=['Arizona','Nevada','Oregon']
bordering_states['Nevada']=['Idaho','Utah','Arizona','California','Oregon']
bordering_states['Idaho']=['Washington','Oregon','Nevada','Utah','Wyoming','Montana']
bordering_states['Utah']=['Idaho','Nevada','Arizona','New Mexico','Colorado','Wyoming']
bordering_states['Arizona']=['New Mexico','Colorado','Utah','Nevada','California']
bordering_states['Montana']=['North Dakota','South Dakota','Wyoming','Idaho']
bordering_states['Wyoming']=['South Dakota','Nebraska','Colorado','Utah','Idaho','Montana']
bordering_states['Colorado']=['Nebraska','Kansas','Oklahoma','New Mexico','Arizona','Utah','Wyoming']
bordering_states['New Mexico']=['Texas','Oklahoma','Colorado','Utah','Arizona']
bordering_states['North Dakota']=['Montana','South Dakota','Minnesota']
bordering_states['South Dakota']=['North Dakota','Montana','Wyoming','Nebraska','Iowa','Minnesota']
bordering_states['Nebraska']=['South Dakota','Wyoming','Colorado','Kansas','Iowa','Missouri']
bordering_states['Kansas']=['Oklahoma','Nebraska','Colorado','Missouri']
bordering_states['Oklahoma']=['Kansas','Colorado','New Mexico','Texas','Arkansas','Missouri']
bordering_states['Texas']=['Oklahoma','New Mexico','Arkansas','Louisiana']
bordering_states['Louisiana']=['Texas','Arkansas','Mississippi']
bordering_states['Arkansas']=['Louisiana','Texas','Oklahoma','Missouri','Tennessee','Mississippi']
bordering_states['Missouri']=['Kansas','Arkansas','Oklahoma','Nebraska','Iowa','Illinois','Kentucky','Tennessee']
bordering_states['Iowa']=['Missouri','Illinois','Wisconsin','South Dakota','Nebraska','Minnesota']
bordering_states['Minnesota']=['Wisconsin','Iowa','South Dakota','North Dakota']
bordering_states['Wisconsin']=['Minnesota','Iowa','Illinois','Michigan']
bordering_states['Illinois']=['Wisconsin','Iowa','Missouri','Kentucky','Indiana']
bordering_states['Kentucky']=['Illinois','Indiana','Ohio','West Virginia','Virginia','Tennessee','Missouri']
bordering_states['Tennessee']=['Kentucky','Virginia','North Carolina','Georgia','Alabama','Mississippi','Arkansas','Missouri']
bordering_states['Mississippi']=['Louisiana','Arkansas','Tennessee','Alabama']
bordering_states['Alabama']=['Mississippi','Tennessee','Georgia','Florida']
bordering_states['Florida']=['Alabama','Georgia']
bordering_states['Georgia']=['Florida','Alabama','Tennessee','North Carolina','South Carolina']
bordering_states['South Carolina']=['North Carolina','Georgia']
bordering_states['North Carolina']=['Virginia','Tennessee','Georgia','South Carolina']
bordering_states['Virginia']=['Maryland','West Virginia','Kentucky','Tennessee','North Carolina']
bordering_states['West Virginia']=['Maryland','Pennsylvania','Ohio','Kentucky','Virginia']
bordering_states['Ohio']=['Pennsylvania','West Virginia','Kentucky', 'Indiana','Michigan']
bordering_states['Michigan']=['Wisconsin','Indiana','Ohio']
bordering_states['Indiana']=['Michigan','Ohio','Kentucky','Illinois']
bordering_states['Maryland']=['Virginia','West Virginia','Pennsylvania','Delaware']
bordering_states['Delaware']=['Maryland','Pennsylvania','New Jersey']
bordering_states['Pennsylvania']=['New York','New Jersey','Delaware','West Virginia','Ohio','Maryland']
bordering_states['New Jersey']=['Delaware','Pennsylvania','New York']
bordering_states['New York']=['New Jersey','Pennsylvania','Vermont','Massachusetts','Connecticut']
bordering_states['Connecticut']=['Rhode Island','Massachusetts','New York']
bordering_states['Rhode Island']=['Massachusetts','Connecticut']
bordering_states['Massachusetts']=['New Hampshire','Vermont','New York','Connecticut','Rhode Island']
bordering_states['New Hampshire']=['Maine','Massachusetts','Vermont']
bordering_states['Vermont']=['New Hampshire','Massachusetts','New York']
bordering_states['Maine']=['New Hampshire']


class path:
    def __init__(self,starting_state,final_state):
        self.starting_state = starting_state
        self.ending_state = final_state
        self.path = []
        self.find_best_path()
        
    def Intersection(self,lst1, lst2):
        return set(lst1).intersection(lst2)    
    
    def add_state_to_path(self,state):

        if state not in list(bordering_states.keys()):
            self.valid_guess = False
            return
        self.valid_guess = True
        self.path.append(state)
        self.chosen_path = self.check_path(self.starting_state, self.ending_state, self.path)
        
        if self.chosen_path:
            self.chosen_path = self.prune_path(self.chosen_path)
            
    def check_path(self,starting_state,ending_state,path_to_check):
        path = copy.copy(path_to_check)
        node1_spires = copy.copy(bordering_states[starting_state])
        node1_states = [starting_state]

        chosen_path = []
        chosen_path.append(starting_state)
        
        #Trivial Case
        if ending_state in node1_spires:
            return chosen_path

        #Search through path for end point
        while self.Intersection(node1_spires, path):
            next_state = list(self.Intersection(node1_spires, path))
            node1_spires = []
            
            if len(next_state) == 1:    
                chosen_path.append(next_state[0])
                node1_spires = bordering_states[next_state[0]]
                path.remove(next_state[0])
            else:
                chosen_path.append(next_state)
                for holder in next_state:
                    path.remove(holder)
                    node1_spires.extend(bordering_states[holder])

            if ending_state in node1_spires:
                chosen_path.append(ending_state)
                return chosen_path
        return []

    def prune_path(self, chosen_path):
        chosen_path.reverse()
        pruned_path = []
        for state in chosen_path:
            if isinstance(state,list):
                available_states = state
                connection_states = bordering_states[pruned_path[-1]]
                pruned_state = list(self.Intersection(connection_states,state))[0]
                pruned_path.append(pruned_state)
            else:
                pruned_path.append(state)
        pruned_path.reverse()
        chosen_path = pruned_path
        return chosen_path
    
    def find_best_path(self):
        state1 = self.starting_state
        state2 = self.ending_state

        all_states = list(bordering_states.keys())
        path_fast = []
        spokes = []
        current_state = [state1]

        while all_states:
            if len(current_state) == 1:
                all_states.remove(current_state[0])
                path_fast.append(current_state[0])
                spokes = bordering_states[current_state[0]]
                if state2 in spokes:
                    path_fast.append(state2)
                    break
                path_fast.append(spokes)
                current_state=spokes

            else:
                for current_state_i in current_state:
                    for bordering_state in bordering_states[current_state_i]:
                        if bordering_state in all_states:
                            spokes.append(bordering_state)
                            all_states.remove(bordering_state)
                current_state = spokes
                if state2 in spokes:
                    path_fast.append(state2)
                    break
                path_fast.append(current_state)
            spokes = []
        self.best_path = self.prune_path(path_fast)

class game:
    def __init__(self):        
        all_possible_states = list(bordering_states.keys())
        self.starting_state = choice(all_possible_states)
        self.find_ending_state()
        
        #self.play()
        
    def find_ending_state(self):
        reference = copy.copy(list(bordering_states.keys()))
        state_distances={self.starting_state:0}
        reference.remove(self.starting_state)
        next_states = []
        state_to_examine = self.starting_state
        states_that_border = bordering_states[state_to_examine]
        counter = 0

        while reference:
            for border in states_that_border:
                if border in reference:
                    state_distances[border] = counter
                    next_states.extend(bordering_states[border])
                    reference.remove(border)  
            states_that_border = next_states
            next_states = []
            counter += 1
                              
        self.ending_state = choice(list(state_distances.keys() ))
        while state_distances[self.ending_state] < 1:
            del state_distances[self.ending_state]
            self.ending_state = choice(list(state_distances.keys() ))
        self.available_turns = max(int(state_distances[self.ending_state]*1.5),state_distances[self.ending_state]+3)
        
    def play(self):
        newpath = path(self.starting_state,self.ending_state)
        for i in range(self.available_turns):
            g = input(f'Guess a state {i+1}/{self.available_turns}: ')
            #Let's check if it's a state
            while g not in list(bordering_states.keys()):
                print('Invalid Guess, try again')
                g = input(f'Guess a state {i+1}/{self.available_turns}: ')
            newpath.add_state_to_path(g)
            if newpath.chosen_path:
                print(newpath.chosen_path)
                return
        print(f'path should have been {newpath.best_path}')
        print('You lost... damn, maybe you should look at a map sometime :/')

if __name__ == '__main__':
    newgame = game()