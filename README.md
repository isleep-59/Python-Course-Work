## Design

In the choice of topic, I chose Connect4 as my coursework topic. Then I will show how I implemented this game by using Python's Tkinter module.

1. In the design of the chessboard, I used two two-dimensional arrays as data structures:

   1. The value in `gird[i][j]` is the color in the current grid, which is a string.

   2. The value in `ovals[i][j]` is a circle drawn using the function `create_oval` of the `Canvas` component.

      This design allows me to more conveniently obtain the color of the chess pieces in a specific grid during the game, or modify them.

2. Regarding how to interact with the chess pieces falling, I decided to add a button above each column of the chessboard (a total of 7 buttons). When the button is pressed, the color of the chessboard grid below it will change, as if there are chess pieces It's like falling down.

3. The last thing is to check which player won the game. Since the end of the game will only happen when the chess pieces fall, that is to say, it is only necessary to check whether the currently fallen chess pieces will lead to the end of the game, that is, whether the latest fallen chess pieces are connected to four in a certain direction.

4. After designing the implementation of the Connect4 rules, I began to think about how to make the game run more reasonably:

   1. Before the game starts, players can choose their favorite color for their pieces.

   2. The game needs a start button, when the start button is pressed, the player can start playing chess.

   3. Players need to know whose turn the next move should be, so there needs to be a color prompt at the top of the game interface to tell them.

   4. The game is multi-round, and each time the player wins the next round, his points will be accumulated. Points will be displayed on both sides of the screen in the form of `Label`.

   5. The game needs an end button, when the end button is pressed:

      1. The system will judge who is the final winner based on the points of both players, and prompt in the form of a message box.

      2. Reset the points of both parties to zero to initialize for the next game.

         

## Implement

In this part, I will implement the code according to the above design ideas.

1. Implementation of the `gird` array:

   ```python
   for i in range(0, 7):
       grid.append([])
       for j in range(0, 6):
           grid[i].append(grid_color)
   ```

   Fill the color in `gird[i][j]` with `gird_color`.

2. Canvas layout:

   ```python
   canvas = Canvas(root,width=490,height=420,bg='blue')
   ```

   Set the color of the checkerboard to blue.

3. Implementation of the `ovals` array:

   ```python
   ovals = []
   for i in range(0, 7):
       ovals.append([])
       for j in range(0, 6):
           ovals[i].append(canvas.create_oval(1 + i * 70 + 5, 1 + j * 70 + 5,
                                              1 + (i + 1) * 70 - 5, 1 + (j + 1) * 70 - 5, fill=grid_color))
   
   ```

   Starting from the upper left corner of the chessboard, each row generates circles (7) according to the measured distance, and generates 6 rows.

4. The implementation of the player leaderboard:

   ```python
   l_a = Label(root,text='A\n:\n%d'%a_score,width=3,height=8,bg=a_color,font=('Source code pro', 20))
   l_b = Label(root,text='B\n:\n%d'%b_score,width=3,height=8,bg=b_color,font=('Source code pro', 20))
   ```

   The `Label` component is used, which changes the background color according to the player changing the color of the pieces, and the points in the text will also change according to the progress of the game.

5. Implementation of the top prompt bar:

   ```python
   l_turn = Label(root,text='Waiting...',width=20,height=2,bg='white',font=('Source code pro', 20))
   ```

   The top prompt bar is used to prompt the player whose turn it is currently, and the background color of this component will change according to the color of the chess pieces selected by the player.

6. Initialization of the chessboard:

   ```python
   def init_grid():
       global turn
       turn = -1
       for i in range(0, 7):
           for j in range(0, 6):
               grid[i][j] = grid_color
   
       for i in range(0, 7):
           for j in range(0, 6):
               canvas.itemconfig(ovals[i][j],fill=grid_color)
   
       for i in range(0, 7):
           grid_column[i] = 5
   ```

   This includes the color initialization of `grid` and `ovals`, as well as the initialization of `grid_column`.

   Worth mentioning is the `grid_column` array, which provides helper functionality. During the game, I need to know how many free grids in each column of the current chessboard can store chess pieces to prevent the placement of chess pieces beyond the range of the chessboard. This is the value recorded by the `grid_column` array.

7. The implementation of the game menu contains three submenus `Game` menu, `Color` menu and `More` menu:

   ```python
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
   ```

   1. The `Game` menu mainly implements the start and end of the game:

      1. Games Start:

         ```python
         def game_start():
             init_grid()
             game_menu.entryconfig(0,state='disable')
             game_menu.entryconfig(1, state='normal')
             menu_bar.entryconfig(2,state='disable')
             buttons_change('↓','normal')
             l_turn.config(bg=a_color,text='%c\'s Turn...'%'A')
             return
         ```

         1. Before the game starts, the "Game Over" option in the menu is unavailable; after the game starts, the "Color Selection" option in the menu is unavailable.

         2. The "game start" function is related to the `buttons_change` function, which realizes the icon change of the drop button above the board: when the game is not started, the icon displayed by the button is `X`; after the game starts, the icon displayed by the button is ` ↓`. Also, when the button icon is `X`, it cannot be pressed.

            ```python
            def buttons_change(txt,st):
                for i in range(0, 7):
                    buttons[i].config(text=txt,state=st)
                return
            ```

      2. Game Over:

         ```python
         def game_finish():
             global a_score, b_score, l_a, l_b
         
             init_grid()
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
         ```

         1. Before the game ends, the "Game Start" and "Color Selection" options in the menu are unavailable; after the game ends, the prompt information on the top prompt bar returns to `Waiting...`.
         2. The "game over" option also needs to tell the player who the final winner of the game is based on the score of the standings, and there is a corresponding prompt if it is a tie.

   2. The `Color` menu mainly implements the modification of the player's chess piece color:

      ```python
      def choose_color(cl):
          global a_color, b_color
          if(cl == 'a'):
              a_color = colorchooser.askcolor()[1]
              l_a.config(bg=a_color)
          else:
              b_color = colorchooser.askcolor()[1]
              l_b.config(bg=b_color)
          return
      ```

      By default player A is red and player B is yellow.

      When modifying the color, the color of the player points `Label` on both sides of the screen should also be modified.

   3. The `More` menu provides a `help` function to tell the player the rules of the "Connect 4" game.

8. Buttons directly above the board:

   ```python
   buttons = []
   for i in range(0, 7):
       buttons.append(Button(text='x',padx=27,pady=10,state='disable',command=lambda i = i : drop(i)))
       buttons[i].place(x=x_start + i * 70,y=130)
   ```

   The implementation relationship of the button is related to three functions:

   1. `drop` function:

      ```python
      def drop(idx):
          global turn, canvas, grid, grid_column
          if grid_column[idx] < 0:
              messagebox.askokcancel('Information', 'Chess pieces can\'t be put down')
              return
      
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
      ```

      The `drop` function realizes the whereabouts of chess pieces and solves the following problems:

      1. When there is no space to place the pieces, the player is prompted to re-select the position of the pieces.
      2. In the rounds of different players, the colors of the falling pieces are different, so when the same button is pressed, the pieces of the corresponding color need to be dropped. Here I use an auxiliary global variable `turn`: when `turn == 1`, it means that it is currently player A's turn; when `turn == 1`, it means that it is currently player B's turn. Every time the button is clicked `turn = turn * -1`, in order to achieve color conversion.
      3. If the `check` function judges that the game is over, the corresponding player gets one point.

   2. `check` function:

      ```python
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
      ```

      The `check` function is used to judge whether the game is won or lost: the `directions` array stores the coordinates of eight directions. Search four steps in eight directions respectively to see if there is a line that can be connected into four.

   3. `score_add` function:

      ```python
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
      ```

      The `score_add` function prompts different congratulatory messages according to different winning players, and modifies the score of their standings, and modifies the information on the top prompt bar to Player A's round.

      

## Test Result

1. Game initial interface

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219044639337.png" alt="image-20230219044639337" style="zoom:50%;" />

2. Menu

   1. Game

      ![image-20230219044712660](C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219044712660.png)

   2. Color

      ![image-20230219044725669](C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219044725669.png)

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045657945.png" alt="image-20230219045657945" style="zoom:50%;" />

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045713662.png" alt="image-20230219045713662" style="zoom:50%;" />

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045730280.png" alt="image-20230219045730280" style="zoom:50%;" />

      

      

   3. More

      ![image-20230219044737269](C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219044737269.png)

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045752484.png" alt="image-20230219045752484" style="zoom:50%;" />

3. Game Start

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219044757299.png" alt="image-20230219044757299" style="zoom:50%;" />

4. Chess process

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045125259.png" alt="image-20230219045125259" style="zoom:50%;" />

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045132036.png" alt="image-20230219045132036" style="zoom:50%;" />

   

5. Random input

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219044939428.png" alt="image-20230219044939428" style="zoom:50%;" />

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045009867.png" alt="image-20230219045009867" style="zoom:50%;" />

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045050005.png" alt="image-20230219045050005" style="zoom:50%;" />

6. Game Over

   1. Player A Wins the game

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045302353.png" alt="image-20230219045302353" style="zoom:50%;" />

   2. Player B wins the game

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045427281.png" alt="image-20230219045427281" style="zoom:50%;" />

   3. Dogfall

      <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045317031.png" alt="image-20230219045317031" style="zoom:50%;" />

   

7. Out of board range

   <img src="C:\Users\WSSSJ\AppData\Roaming\Typora\typora-user-images\image-20230219045842202.png" alt="image-20230219045842202" style="zoom:50%;" />