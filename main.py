from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox

def game_start():
    game_menu.entryconfig(0,state='disable')
    game_menu.entryconfig(1, state='normal')
    menu_bar.entryconfig(2,state='disable')
    buttons_change('↓','normal')
    l_turn.config(bg=a_color,text='%c\'s Turn...'%'A')
    return

def game_finish():
    global a_score, b_score, l_a, l_b

    game_menu.entryconfig(0, state='normal')
    game_menu.entryconfig(1, state='disable')
    menu_bar.entryconfig(2, state='normal')
    buttons_change('x','disable')
    l_turn.config(bg='white',text='Waiting...')

    tmp = ' '
    if a_score > b_score:
        tmp = 'a'
    else:
        if a_score == b_score:
            tmp = 'n'
        else:
            tmp = 'b'

    if tmp != 'n':
        answer = messagebox.askokcancel('Information', '%c Wins the Game!!!' % tmp.capitalize())
    else:
        answer = messagebox.askokcancel('Information', 'Dogfall!!!')

    a_score = 0
    b_score = 0
    l_a.config(text='A\n:\n%d'%a_score)
    l_b.config(text='B\n:\n%d'%b_score)

    return

def choose_color(cl):
    global a_color, b_color
    if(cl == 'a'):
        a_color = colorchooser.askcolor()[1]
        l_a.config(bg=a_color)
    else:
        b_color = colorchooser.askcolor()[1]
        l_b.config(bg=b_color)
    return

def buttons_change(txt,st):
    for i in range(0, 7):
        buttons[i].config(text=txt,state=st)
    return

def check(x, y):
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    for i in range(0, 8):
        sum = 0
        nextx = x
        nexty = y
        for j in range(0, 4):
            nextx = nextx + directions[i][0]
            nexty = nexty + directions[i][1]
            if nextx < 0 or nextx >= 7 or nexty < 0 or nexty >= 6:
                break

            if grid[x][y] == grid[nextx][nexty]:
                sum = sum + 1
            else:
                break
        if sum == 3:
            return True
    return False

def drop(idx):
    global turn, canvas, grid
    if turn == -1:
        canvas.itemconfig(ovals[idx][grid_column[idx]],fill=a_color)
        grid[idx][grid_column[idx]] = a_color
        if check(idx, grid_column[idx]) == True:
            score_add('a')
            return
        else:
            l_turn.config(bg=b_color,text='%c\'s Turn...'%'B')
    else:
        canvas.itemconfig(ovals[idx][grid_column[idx]], fill=b_color)
        grid[idx][grid_column[idx]] = b_color
        if check(idx, grid_column[idx]) == True:
            score_add('b')
            return
        else:
            l_turn.config(bg=a_color, text='%c\'s Turn...' % 'A')
    grid_column[idx] = grid_column[idx] - 1
    turn = turn * -1
    return

def score_add(tmp):
    global a_score, b_score, l_a, l_b, l_turn
    answer = messagebox.askokcancel('Information', '%c Win the Round!!!' % tmp.capitalize())
    init_grid()

    if tmp == 'a':
        a_score = a_score + 1
        l_a.config(text='A\n:\n%d'%a_score)
    else:
        b_score = b_score + 1
        l_b.config(text='B\n:\n%d' % b_score)
    l_turn.config(bg=a_color, text='%c\'s Turn...' % 'A')
    return

def init_grid():
    for i in range(0, 7):
        for j in range(0, 6):
            grid[i][j] = grid_color

    for i in range(0, 7):
        for j in range(0, 6):
            canvas.itemconfig(ovals[i][j],fill=grid_color)

    for i in range(0, 7):
        grid_column[i] = 5

def help_info():
    answer = messagebox.askokcancel('Information', 'Connect4 is a two-player connection game in which the players first choose a colour and then take turns dropping coloured discs from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the next available space within the column. The objective of the game is to connect four of one\'s own discs of the same colour next to each other vertically, horizontally, or diagonally before your opponent.')

x_start = 155
y_start = 180

a_score = 0
b_score = 0

a_color = 'red'
b_color = 'yellow'
turn = -1

grid_color = 'black'
grid_column = [5, 5, 5, 5, 5, 5, 5]
grid = []

root = Tk()
root.geometry('800x600')

menu_bar = Menu(root)

game_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Game',menu=game_menu)
game_menu.add_command(label='Start',command=game_start)
game_menu.add_command(label='Finish',command=game_finish,state='disable')

color_menu = Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Color',menu=color_menu)
color_menu.add_command(label='Change A',command=lambda : choose_color('a'))
color_menu.add_command(label='Change B',command=lambda : choose_color('b'))

more_menu = Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='More',menu=more_menu)
more_menu.add_command(label='Help',command=help_info)

l_a = Label(root,text='A\n:\n%d'%a_score,width=3,height=8,bg=a_color,font=('Source code pro', 20))
l_b = Label(root,text='B\n:\n%d'%b_score,width=3,height=8,bg=b_color,font=('Source code pro', 20))
l_turn = Label(root,text='Waiting...',width=20,height=2,bg='white',font=('Source code pro', 20))
canvas = Canvas(root,width=490,height=420,bg='blue')

ovals = []
for i in range(0, 7):
    ovals.append([])
    for j in range(0, 6):
        ovals[i].append(canvas.create_oval(1 + i * 70 + 5, 1 + j * 70 + 5,
                                           1 + (i + 1) * 70 - 5, 1 + (j + 1) * 70 - 5, fill=grid_color))

for i in range(0, 7):
    grid.append([])
    for j in range(0, 6):
        grid[i].append(grid_color)

buttons = []
for i in range(0, 7):
    buttons.append(Button(text='x',padx=27,pady=10,state='disable',command=lambda i = i : drop(i)))
    buttons[i].place(x=x_start + i * 70,y=130)

init_grid()

l_a.pack(side='left')
l_b.pack(side='right')
l_turn.pack(side='top')
canvas.pack(side='bottom')

root.config(menu=menu_bar)
root.mainloop()