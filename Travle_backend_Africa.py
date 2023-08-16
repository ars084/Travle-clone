global bordering_states
from random import choice
import copy
bordering_states = dict()

# North Africa
bordering_states['Morocco'] = ['Algeria','Mauritania']
bordering_states['Algeria'] = ['Tunisia','Libya','Niger','Mali','Mauritania','Morocco']
bordering_states['Libya'] = ['Egypt','Sudan','Chad','Niger','Algeria','Tunisia']
bordering_states['Tunisia'] = ['Libya','Algeria']
bordering_states['Egypt'] = ['Libya','Sudan']
bordering_states['Sudan'] = ['Egypt','Eritrea','Ethiopia','South Sudan','CAR','Chad','Libya']
bordering_states['Chad'] = ['Libya','Sudan','CAR','Cameroon','Niger']
bordering_states['Niger'] = ['Libya','Chad','Nigeria','Benin','Burkina Faso','Mali','Algeria']
bordering_states['Mali'] = ['Algeria','Niger','Burkina Faso',"Cote d'Ivoire",'Guinea','Senegal','Mauritania']
bordering_states['Mauritania'] = ['Morocco','Algeria','Mali','Senegal']

# West Africa
bordering_states['Senegal'] = ['Gambia','Mauritania','Mali','Guinea','Guinea-Bissau']
bordering_states['Gambia'] = ['Senegal']
bordering_states['Guinea-Bissau'] = ['Senegal','Guinea']
bordering_states['Guinea'] = ['Guinea-Bissau','Senegal','Mali',"Cote d'Ivoire",'Liberia','Sierra Leone']
bordering_states['Sierra Leone'] = ['Guinea','Liberia']
bordering_states['Liberia'] = ['Sierra Leone','Guinea',"Cote d'Ivoire"]
bordering_states["Cote d'Ivoire"] = ['Liberia','Guinea','Mali','Burkina Faso','Ghana']
bordering_states['Burkina Faso'] = ['Mali','Niger','Benin','Togo','Ghana',"Cote d'Ivoire"]
bordering_states['Ghana'] = ['Togo','Burkina Faso',"Cote d'Ivoire"]
bordering_states['Togo'] = ['Benin','Burkina Faso','Ghana']
bordering_states['Benin'] = ['Nigeria','Niger','Burkina Faso','Togo']
bordering_states['Nigeria'] = ['Benin','Niger','Cameroon']
bordering_states['Cameroon'] = ['Nigeria','Chad','CAR','Congo','Gabon','Equatorial Guinea']
bordering_states['Equatorial Guinea'] = ['Cameroon','Gabon']
bordering_states['Gabon'] = ['Equatorial Guinea','Cameroon','Congo']

# Central Africa
bordering_states['CAR'] = ['Sudan','South Sudan','DRC','Congo','Cameroon','Chad']
bordering_states['South Sudan'] = ['Sudan','Ethiopia','Kenya','Uganda','DRC','CAR']
bordering_states['Uganda'] = ['South Sudan','Kenya','Tanzania','Rwanda','DRC']
bordering_states['Rwanda'] = ['Uganda','Tanzania','Burundi','DRC']
bordering_states['DRC'] = ['Congo','CAR','South Sudan','Uganda','Rwanda','Burundi','Tanzania','Zambia','Angola']
bordering_states['Congo'] = ['Gabon','Cameroon','CAR','DRC']
bordering_states['Burundi'] = ['Rwanda','Tanzania','DRC']

# East Africa
bordering_states['Eritrea'] = ['Sudan','Djibouti','Ethiopia']
bordering_states['Djibouti'] = ['Eritrea','Ethiopia','Somalia']
bordering_states['Ethiopia'] = ['Eritrea','Djibouti','Somalia','Kenya','South Sudan','Sudan']
bordering_states['Somalia'] = ['Djibouti','Ethiopia','Kenya']
bordering_states['Kenya'] = ['Somalia','Ethiopia','South Sudan','Uganda','Tanzania']
bordering_states['Tanzania'] = ['Kenya','Uganda','Rwanda','Burundi','DRC','Zambia','Malawi','Mozambique']

# South Africa
bordering_states['Malawi'] = ['Tanzania','Mozambique','Zambia']
bordering_states['Mozambique'] = ['Tanzania','Malawi','Zambia','Zimbabwe','South Africa', 'Eswatini']
bordering_states['Zambia'] = ['DRC','Tanzania','Malawi','Mozambique','Zimbabwe','Namibia','Angola']
bordering_states['Angola'] = ['DRC','Zambia','Namibia']
bordering_states['Namibia'] = ['Angola','Botswana','Zambia','South Africa']
bordering_states['Botswana'] = ['Namibia','Zimbabwe','South Africa']
bordering_states['Zimbabwe'] = ['Zambia','Botswana','South Africa','Mozambique']
bordering_states['Eswatini'] = ['South Africa','Mozambique']
bordering_states['Lesotho'] = ['South Africa']
bordering_states['South Africa'] = ['Lesotho','Eswatini','Mozambique','Zimbabwe','Botswana','Namibia']


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
		print(f'Go from {self.starting_state} to {self.ending_state} in {self.available_turns} turns')
		for i in range(self.available_turns):
			g = input(f'Guess a state {i+1}/{self.available_turns}: ')
			#Let's check if it's a state
			while g not in list(bordering_states.keys()):
				print('Invalid Guess, try again')
				g = input(f'Guess a state {i+1}/{self.available_turns}: ')
			newpath.add_state_to_path(g)
			if newpath.chosen_path:
				print('Congratulations! You won!')
				print(newpath.chosen_path)
				return
		print(f'path should have been {newpath.best_path}')
		print('You lost... damn, maybe you should look at a map sometime :/')

if __name__ == '__main__':
    newgame = game()





