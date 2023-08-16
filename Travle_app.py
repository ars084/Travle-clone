import tkinter as tk
from PIL import Image, ImageTk
import os
from random import choice
import numpy as np
import copy
from time import sleep

import Travle_backend as Travle_backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def play():
	app.clear_map = True
	newgame = Travle_backend.game()
	app.newpath = Travle_backend.path(newgame.starting_state,newgame.ending_state)
	goal_label.config(text=f'{newgame.starting_state} to {newgame.ending_state} in {newgame.available_turns} turns or less')
	app.available_turns = newgame.available_turns
	app.starting_state = newgame.starting_state
	app.ending_state = newgame.ending_state
	app.turns = 0
	app.guesses = [app.starting_state,app.ending_state]

	label.config(text=f'Guess a state {app.turns}/{app.available_turns}: ')
	entry.place(relx=0.5, rely=0.8, anchor='center')
	enter_button.place(relx=0.5,rely=0.85, anchor = 'center')
	previous_guesses.config(text='Previous guesses:')
	answer_label.config(text='')

	print(newgame.starting_state)
	print(newgame.ending_state)
	display_state(newgame.starting_state)
	display_state(newgame.ending_state)

def submit_guess():

	app.turns = app.turns + 1
	label.config(text=f'Guess a state {app.turns}/{app.available_turns}: ')
	g = entry.get()
	if g in app.guesses:
		label.config(text='Already guessed this, try again')
		return

	app.newpath.add_state_to_path(g)
	#Let's check if it's a state
	if not app.newpath.valid_guess:
		label.config(text='Invalid Guess, try again')
		return

	app.guesses.append(g)

	guess_txt = 'Previous guesses:'
	
	for guess in app.guesses:
		if guess not in [app.starting_state,app.ending_state]:
			guess_txt = guess_txt + '\n'+guess
	previous_guesses.config(text=guess_txt)
	
	app.newpath.add_state_to_path(g)

	entry.delete(0,len(g))
	display_state(g)
	
	if app.newpath.chosen_path:
		app.path_found = True
		display_answer()
		return

	if app.turns == app.available_turns:
		print(f'path should have been {app.newpath.best_path}')
		print('You lost... damn, maybe you should look at a map sometime :/')
		app.path_found = False
		display_answer()
		return

def display_answer():
	if app.path_found:
		answer_txt = 'You won! The path works:'
		app.path_to_show = app.newpath.chosen_path
	else:
		answer_txt = 'You lost! The best path was:'
		app.path_to_show = app.newpath.best_path

	app.guesses.append(app.starting_state)
	app.guesses.append(app.ending_state)
	entry.place_forget()
	enter_button.place_forget()
	
	for state in app.path_to_show:
		answer_txt = answer_txt+'\n'+state
	print(answer_txt)
	answer_label.config(text=answer_txt)
	answer_label.place(relx=0.5,rely=0.75, anchor='center')

	show_map_answer()

def display_state(state_to_show):
	canvas.delete("all")

	state = Image.open('/Users/andersonscott/Desktop/Travle_USA/States_pngs/'+state_to_show+'.png')
	#state = Image.open('/Users/andersonscott/Desktop/Travle_USA/Africa_pngs/'+state_to_show+'.png')
	if app.need_to_resize:
		state = state.resize((600,600))
	#new_img = np.sum(np.asarray(state),axis=2)
	if len(np.asarray(state).shape) > 2:
		new_img = np.asarray(state)[:,:,0]
	else:
		new_img = np.asarray(state)[:,:]

	if app.clear_map:
		app.full_img = new_img - USimage
		app.clear_map = False
	else:
		#new_img[(new_img > 615) | (new_img < 610)] = 0
		app.full_img = app.full_img + (new_img - USimage)

	photo_img = ImageTk.PhotoImage(Image.fromarray(app.full_img))
	canvas.imgref = photo_img
	canvas.create_image(img_x,img_y,image = photo_img)
	#canvas.itemconfig(img,image=photo_img)
	#plot1.clear()
	#plot1.imshow(app.full_img)
	#canvas.draw()
def show_map_answer():
	#canvas.delete('all')

	app.full_img = USimage

	photo_img = ImageTk.PhotoImage(Image.fromarray(app.full_img))

	#app.full_img = np.asarray(img)
	canvas.imgref = photo_img
	canvas.create_image(img_x,img_y,image = photo_img)

	for state in app.guesses:
		holder_func(state,modifier = 1.5)
	for state in app.path_to_show:
		holder_func(state)

def holder_func(state_img,modifier = 1):
	state = Image.open('/Users/andersonscott/Desktop/Travle_USA/States_pngs/'+state_img+'.png')
	#state = Image.open('/Users/andersonscott/Desktop/Travle_USA/Africa_pngs/'+state_img+'.png')
	if app.need_to_resize:
		state = state.resize((600,600))
	if len(np.asarray(state).shape) > 2:
		holder = np.asarray(state)[:,:,0]*modifier
	else:
		holder = np.asarray(state)*modifier
	
	#if state_img not in app.path_to_show:
	#	
	#	app.full_img = np.minimum(app.full_img, holder*1.7)
	#else:
	#	app.full_img = np.minimum(app.full_img, holder)
	#app.full_img = np.maximum(app.full_img, holder)
	app.full_img = np.minimum(app.full_img, holder)
	photo_img = ImageTk.PhotoImage(Image.fromarray(app.full_img))
	canvas.imgref = photo_img
	canvas.create_image(img_x,img_y,image=photo_img)

app = tk.Tk()
app.geometry("700x800")


img = Image.open('/Users/andersonscott/Desktop/Travle_USA/States_pngs/US.png')
#img = Image.open('/Users/andersonscott/Desktop/Travle_USA/Africa_pngs/Africa.png')
if max(img.size) > 600:
	img = img.resize((600,600))
	app.need_to_resize = True
else:
	app.need_to_resize = False

photo_img = ImageTk.PhotoImage(img)

if len(np.asarray(img).shape) > 2:
	USimage = copy.copy(np.asarray(img)[:,:,0])
	app.full_img = np.asarray(img)[:,:,0]
else:
	USimage = copy.copy(np.asarray(img))
	app.full_img = np.asarray(img)


app.turns = 0
app.guesses = []

img_x = 300
img_y = 300

frame = tk.Frame(app, width=600, height=600)
frame.pack(padx = 30, pady = 10, fill='both')

#fig = Figure()
#plot1 = fig.add_subplot(111)
#canvas = FigureCanvasTkAgg(fig, master=frame)
#frame = tk.Frame(app,width=600,height=600)
#frame.place(relx = 0.5, rely = 0.5, anchor='center')
answer_label = tk.Label(text='')

canvas = tk.Canvas(frame, width = 600, height = 600)
canvas.pack()
canvas.create_image(img_x,img_y,image=photo_img)

goal_label = tk.Label()
goal_label.place(relx=0.3,rely=0.05)

button = tk.Button(app,text = 'Play a new game',command=play)
button.place(relx=0.5,rely=0.1, anchor='center')

label = tk.Label(app, text = 'Sample')

previous_guesses = tk.Label(app,text='Previous guesses:')
previous_guesses.place(relx=0.7, rely=0.75)

label.place(relx=0.2,rely=0.8, anchor='center')
#fig = Figure()
#plot1 = fig.add_subplot(111)
#canvas = FigureCanvasTkAgg(fig, master=frame)

#plot1.imshow(app.full_img)
#canvas.draw()



entry = tk.Entry(app)
#entry.place(relx=0.5, rely=0.8, anchor='center')
enter_button = tk.Button(app,text='Enter Guess',command=submit_guess)
#enter_button.place(relx=0.5,rely=0.85, anchor = 'center')

app.mainloop()

