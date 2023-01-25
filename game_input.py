import pyautogui


class GameInput():
    def __init__(self, length, height):
        # split screen into squares
        self.input = ['a', 'b', 'c', 'd']
        # transform into grid
        self.dim_x = 2
        self.dim_y = 2
        self.grid_length = length/self.dim_x
        self.grid_height = height/self.dim_y

    def coordinate_input(self, coordinate):
        # coordinate is in the form of x, y in int
        chosen_num = 0
        for i in range(self.dim_x): #length
            for j in range(self.dim_y): #width
                grid_x_max = self.grid_length*(i+1)
                grid_x_min = self.grid_length*i
                grid_y_max = self.grid_height*(j+1)
                grid_y_min = self.grid_height*j
                if grid_x_min < coordinate[0] and coordinate[0] < grid_x_max and grid_y_min < coordinate[1] and coordinate[1] < grid_y_max:
                    chosen_num = i*self.dim_x+j
        chosen_key = self.input[chosen_num]
        pyautogui.press(chosen_key)
