from tkinter import *
file = open('enable1.txt','r').read()
WORDS = file.split('\n')
LETTER_VALUES = {
'a' : 1,
'b' : 4,
'c' : 4,
'd' : 2,
'e' : 1,
'f' : 4,
'g' : 3,
'h' : 3,
'i' : 1,
'j' : 10,
'k' : 5,
'l' : 2,
'm' : 4,
'n' : 2,
'o' : 1,
'p' : 4,
'qu' : 10,
'r' : 1,
's' : 1,
't' : 1,
'u' : 2,
'v' : 5,
'w' : 4,
'x' : 10,
'y' : 3,
'z' : 10,
}

# Frame - takefocus - for GUI
class Word:
    def __init__(self, word, path, solver):
        self.word = word
        self.path = path
        self.solver = solver
        self.value = self.val()

    def val(self):
        # add in dl,dw,tl,tw checks
        v = 0
        for letter in self.word:
            v += LETTER_VALUES[letter]
        return v

    def __str__(self):
        return self.word

class Solver:
    def __init__(self, board, dl=[], dw=[], tl=[], tw=[]):
        self.board = board
        self.words = []
        self.dl = dl
        self.dw = dw
        self.tl = tl
        self.tw = tw
        self.q_fix()
        self.generate_word_list()

    def q_fix(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 'q':
                    self.board[i][j] = 'qu'

    def generate_word_list(self):
        for i in range(0,len(self.board[0])):
            for j in range(0,len(self.board[0])):
                self.rec_words(i,j,[], self.board[i][j], self.potential_words(self.board[i][j], WORDS))
        self.words.sort(key=lambda s: s.value)
        self.words = self.words[::-1]

    def rec_words(self, row, column, visited, letters, potential_words):
        if len(potential_words) == 0:
            return
        visited += [(row,column)]
        if letters in potential_words:
            if letters not in self.words:
                self.words += [Word(letters, visited, self)]
        for neighbor in self.neighbors(row, column, visited):
            self.rec_words(neighbor[0], neighbor[1], visited[:], letters + self.board[neighbor[0]][neighbor[1]],
                                  self.potential_words(letters + self.board[neighbor[0]][neighbor[1]], potential_words))

    def potential_words(self, current, potential_words):
        i = 0
        try:
            while not potential_words[i].startswith(current):
                i += 1
            begin = i
        except:
            return []
        try:
            while potential_words[i].startswith(current):
                i += 1
            end = i
        except:
            return potential_words[begin:]
        return potential_words[begin:end]

    def neighbors(self, row, column, visited):
        neighbors = []
        for i in range(row-1,row+2):
            for j in range(column-1,column+2):
                if -1 < i < len(self.board[0]) and -1 < j < len(self.board[0]):
                    if (i,j) not in visited:
                        neighbors += [(i,j)]
        return neighbors

    def print_words(self):
        for word in self.words:
            print(word)

    def __str__(self):
        string = ''
        for row in self.board:
            string += str(row) + '\n'
        return string


class CustomEntry:
    def __init__(self,entry,row,col):
        self.entry = entry
        self.row = row
        self.col = col

    def place(self):
        self.entry.grid(row=self.row,column=self.col)

    def get_entry(self):
        return self.entry

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_next(self):
        col = (self.col + 1) % 4
        if not col:
            row = (self.row + 1) % 4
        else:
            row = self.row
        return row, col

def run():
    class Window(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.master.title("BoggleCheat")
            self.master.configure(background='slate grey')
            self.frame = Frame(self.master)
            self.word_count = Label(self.master, text='')
            self.buttons = {}
            for i in range(4):
                self.buttons[i] = {}
                for j in range(4):
                    self.buttons[i][j] = CustomEntry(Entry(self.frame),i,j)
                    self.buttons[i][j].place()
            self.frame.grid(row=0,column=0)
            self.text = Text(self.master, width=10)  # font=("helvetica", 32)
            label = Label(self.master,text='Press Enter to generate words. Enter "qu" as "q"')
            label.grid(row=8,column=0)
            self.cur_row = 0
            self.cur_col = 0
            self.buttons[self.cur_row][self.cur_col].get_entry().focus_set()
            self.refresh_button = Button(master, text='Refresh', command=self.refresh)
            self.refresh_button.grid(row=4, column=2)

        def refresh(self):
            self.frame.destroy()
            self.text.destroy()
            self.word_count.destroy()
            self.__init__(self.master)

        def submit(self, event):
            board = [['','','',''],['','','',''],['','','',''],['','','','']]
            for row in self.buttons:
                for entry in self.buttons[row]:
                    board[row][entry] = self.buttons[row][entry].get_entry().get()
            self.solver = Solver(board)
            self.display()

        def display(self):
            for word in self.solver.words:
                self.text.insert(END, word.word + '\n')
            self.text.grid(row=11,column=0)
            self.word_count = Label(self.master,text=str(len(self.solver.words))+' words')
            self.word_count.grid(row=9,column=0)

        def key(self, event):
            if event.keysym == 'KP_Enter' or event.keysym == 'Return':
                pass
            else:
                self.cur_row,self.cur_col=self.buttons[self.cur_row][self.cur_col].get_next()
                self.buttons[self.cur_row][self.cur_col].get_entry().focus_set()

    root = Tk()
    root.geometry("1000x600")
    app = Window(root)
    root.bind('<Return>',app.submit)
    root.bind("<Key>", app.key)
    root.mainloop()

if __name__ == "__main__":
    board = [['s', 'e', 't', 'h'], ['n', 'a', 'e', 'c'], ['b', 'r', 'p', 'o'], ['a', 'u', 'qu', 'y']]

    run()
