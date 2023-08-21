global bordering_states
from random import choice
import copy
import os
bordering_states = dict()

# Western Europe
bordering_states['Portugal'] = ['Spain']
bordering_states['Spain'] = ['Portugal','France']
bordering_states['France'] = ['United Kingdom','Belgium','Germany','Luxembourg','Italy','Switzerland','Spain']
bordering_states['Belgium'] = ['Netherlands','Germany','Luxembourg','France']
bordering_states['Netherlands'] = ['Germany','Belgium']
bordering_states['Switzerland'] = ['Germany','France','Italy','Austria']
bordering_states['Italy'] = ['France','Switzerland','Austria','Slovenia']
bordering_states['Luxembourg'] = ['Belgium','Germany','France']
bordering_states['Germany'] = ['Denmark','Netherlands','Belgium','Luxembourg','Switzerland','Austria','Poland','Czechia','France']
bordering_states['Austria'] = ['Czechia','Slovakia','Hungary','Slovenia','Italy','Switzerland','Germany']
bordering_states['United Kingdom'] = ['Ireland','France']
bordering_states['Ireland'] = ['United Kingdom']

# Northern Europe
bordering_states['Finland'] = ['Russia','Sweden','Norway']
bordering_states['Norway'] = ['Sweden','Finland','Russia']
bordering_states['Denmark'] = ['Germany','Sweden']
bordering_states['Sweden'] = ['Denmark','Norway','Finland']

# Slav Europe
bordering_states['Estonia'] = ['Russia','Latvia']
bordering_states['Latvia'] = ['Lithuania','Estonia','Russia', 'Belarus']
bordering_states['Lithuania'] = ['Russia','Latvia','Belarus','Poland']
bordering_states['Belarus'] = ['Russia','Lithuania','Latvia','Ukraine','Poland']
bordering_states['Poland'] = ['Russia','Lithuania','Belarus','Ukraine','Slovakia','Czechia','Germany']
bordering_states['Ukraine'] = ['Russia','Belarus','Poland','Slovakia','Hungary','Romania','Moldova']
bordering_states['Russia'] = ['Ukraine','Belarus','Lithuania','Poland','Latvia','Estonia','Finland','Norway','Georgia','Azerbaijan', 'Kazakhstan','Mongolia','China','North Korea']

#Baltic Europe
bordering_states['Moldova'] = ['Ukraine','Romania']
bordering_states['Romania'] = ['Moldova','Ukraine','Hungary','Serbia','Bulgaria']
bordering_states['Hungary'] = ['Slovakia','Austria','Slovenia','Croatia','Serbia','Romania','Ukraine']
bordering_states['Slovakia'] = ['Poland','Czechia','Austria','Hungary','Ukraine']
bordering_states['Czechia'] = ['Poland','Germany','Austria','Slovakia']
bordering_states['Slovenia'] = ['Croatia','Hungary','Austria','Italy']
bordering_states['Croatia'] = ['Slovenia','Hungary','Serbia','Bosnia', 'Montenegro']
bordering_states['Bosnia'] = ['Croatia','Serbia','Montenegro']
bordering_states['Serbia'] = ['Hungary','Croatia','Bosnia','Montenegro','Kosovo','North Macedonia','Bulgaria','Romania']
bordering_states['Bulgaria'] = ['Romania','Serbia','North Macedonia','Greece','Turkey']
bordering_states['Montenegro'] = ['Bosnia','Croatia','Serbia','Kosovo','Albania']
bordering_states['Kosovo'] = ['Serbia','Montenegro','Albania','North Macedonia']
bordering_states['North Macedonia'] = ['Kosovo','Serbia','Bulgaria','Greece','Albania']
bordering_states['Albania'] = ['Montenegro','Kosovo','North Macedonia','Greece']
bordering_states['Greece'] = ['Albania','North Macedonia','Bulgaria','Turkey']

# Middle East
bordering_states['Georgia'] = ['Armenia','Azerbaijan','Turkey','Russia']
bordering_states['Armenia'] = ['Georgia','Azerbaijan','Turkey','Iran']
bordering_states['Azerbaijan'] = ['Russia','Georgia','Armenia','Iran']
bordering_states['Turkey'] = ['Georgia','Armenia','Iran','Iraq','Syria','Greece','Bulgaria']
bordering_states['Syria'] = ['Iraq','Turkey','Lebanon','Israel','Jordan']
bordering_states['Lebanon'] = ['Syria','Israel']
bordering_states['Palestine'] = ['Jordan','Israel']
bordering_states['Israel'] = ['Palestine','Jordan','Syria','Lebanon']
bordering_states['Jordan'] = ['Palestine','Israel','Syria','Iraq','Saudi Arabia']
bordering_states['Iraq'] = ['Syria','Turkey','Iran','Kuwait','Saudi Arabia','Jordan']
bordering_states['Kuwait'] = ['Saudi Arabia','Iraq']
bordering_states['Saudi Arabia'] = ['Kuwait','Iraq','Jordan','Bahrain','Qatar','UAE','Oman','Yemen']
bordering_states['Yemen'] = ['Saudi Arabia','Oman']
bordering_states['Oman'] = ['UAE','Saudi Arabia','Yemen']
bordering_states['UAE'] = ['Oman','Saudi Arabia']
bordering_states['Qatar'] = ['Saudi Arabia']
bordering_states['Bahrain'] = ['Saudi Arabia']
bordering_states['Iran'] = ['Azerbaijan','Armenia','Turkey','Iraq','Turkmenistan','Afghanistan','Pakistan']

# Central Asia ie the -stans
bordering_states['Bangladesh'] = ['Myanmar','India']
bordering_states['Bhutan'] = ['China','India']
bordering_states['Nepal'] = ['China','India']
bordering_states['India'] = ['Bangladesh','Myanmar','Bhutan','Nepal','Pakistan','China']
bordering_states['Pakistan'] = ['India','China','Afghanistan','Iran']
bordering_states['Afghanistan'] = ['Tajikistan','Uzbekistan','Turkmenistan','Iran','Pakistan','China']
bordering_states['Turkmenistan'] = ['Iran','Afghanistan','Uzbekistan','Kazakhstan']
bordering_states['Uzbekistan'] = ['Kazakhstan','Kyrgyzstan','Tajikistan','Afghanistan','Turkmenistan']
bordering_states['Tajikistan'] = ['Kyrgyzstan','Uzbekistan','Afghanistan','China']
bordering_states['Kyrgyzstan'] = ['China','Kazakhstan','Uzbekistan','Tajikistan']
bordering_states['Kazakhstan'] = ['Turkmenistan','Uzbekistan','Kyrgyzstan','China','Russia']

# East Asia
bordering_states['North Korea'] = ['China','South Korea','Russia']
bordering_states['South Korea'] = ['North Korea']
bordering_states['China'] = ['North Korea','Mongolia','Russia','Kazakhstan','Kyrgyzstan','Tajikistan','Afghanistan','Pakistan','India','Nepal','Bhutan','Myanmar','Laos','Vietnam']
bordering_states['Mongolia'] = ['China','Russia']
bordering_states['Vietnam'] = ['China','Laos','Cambodia']
bordering_states['Laos'] = ['Vietnam','China','Myanmar','Thailand','Cambodia']
bordering_states['Thailand'] = ['Myanmar','Laos','Cambodia','Malaysia']
bordering_states['Myanmar'] = ['Thailand','Laos','China','India','Bangladesh']
bordering_states['Cambodia'] = ['Vietnam','Laos','Thailand']
bordering_states['Malaysia'] = ['Thailand','Indonesia']
bordering_states['Indonesia'] = ['Malaysia']


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



def check_countries_for_connectedness():
	all_countries = list(bordering_states.keys())
	for country in all_countries:
		print(f'Checking {country}')
		neighbors = bordering_states[country]
		if not os.path.isfile(os.path.join('Eurasia_pngs',country+'.png')):
			print(f'{country} map not found')
		for neighbor in neighbors:
			if country not in bordering_states[neighbor]:
				print(f'{country} not found in {neighbor} neighbors')
