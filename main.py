from tkinter import *
from tkinter.ttk import Style
from PIL import Image, ImageTk
from ctypes import windll
import threading
import time

SET_SECONDS = 3


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Text Disappearing App')
        self.minsize(1000, 650)
        self.canvas_create()
        self.frame_create()  # need to create frame so that i can place widget on canvas using grid method.
        self.create_widgets()
        self.stop_minutes = None
        self.stop_seconds = None
        self.not_stop = None  # this is to initiate the while loop in relaxation_time()
        self.color = ['#80393C', '#E6676B', '#FF7377']

    def canvas_create(self):
        self.canva = Canvas(self)
        self.canva.pack(fill=BOTH, expand=True)
        img = Image.open('background.jpg')
        self.image = ImageTk.PhotoImage(img)
        # Display the image on the canvas
        self.canva.create_image(0, 0, anchor=NW, image=self.image)

    def frame_create(self):
        self.frame = Frame(self.canva, bg='#88b7a7')
        self.frame.pack(pady=150)

    def create_widgets(self):
        self.seconds = SET_SECONDS

        self.heading = Label(self.frame, text='Disappearing Text App', bg='#88b7a7', font=('arial', 30, 'bold'),
                             fg='#3e363f')
        self.heading.grid(row=0, column=1, pady=10)

        self.timer = Label(self.frame, text='Timer: 3:00', bg='#88b7a7', font=('arial', 15, 'bold'), fg='#3e363f')
        self.timer.grid(row=1, column=0, pady=5)

        self.time_label = Label(self.frame, text='Choose Time and start Typing:', bg='#88b7a7',
                                font=('arial', 15, 'bold'), fg='#3e363f')
        self.time_label.grid(row=1, column=1, pady=5, sticky=E)

        option = [3, 5]
        self.selected_time = IntVar()
        self.selected_time.set(option[0])
        self.choose_time = OptionMenu(self.frame, self.selected_time, *option, command=self.start_action)
        self.choose_time.grid(row=1, column=2)

        self.text_area = Text(self.frame, wrap='word', padx=15, pady=15)
        self.text_area.grid(row=2, column=0, columnspan=3)
        self.text_area.bind('<Key>', self.detect_call_function)  #################

        self.high_score = Label(self.frame, text=f'Highscore:{self.get_highscore(self.selected_time)}', bg='#88b7a7',
                                font=('arial', 10, 'bold'))
        self.high_score.grid(row=3, column=0, pady=10)

        self.time_stop = Label(self.frame, text=f'Seconds: {self.seconds}', bg='#88b7a7', font=('arial', 10, 'bold'))
        self.time_stop.grid(row=3, column=1, pady=10)

        self.words_written = Label(self.frame, text='Words Typed:--', bg='#88b7a7', font=('arial', 10, 'bold'))
        self.words_written.grid(row=3, column=2, pady=10)

    def start_action(self, selected_time):
        # if user decides 5 mins this will show highscore for that 5 mins
        if selected_time == 5:
            self.high_score.config(text=f'Highscore:{self.get_highscore(self.selected_time)}')
        else:
            self.high_score.config(text=f'Highscore:{self.get_highscore(self.selected_time)}')

        self.not_stop = True  # this is to initiate the while loop in relaxation_time()
        self.text_area.config(bg='white')
        self.text_area.focus()
        self.time_stop.config(text=f'Seconds: {self.seconds}')
        self.minutes_remaing(selected_time, 60)
        self.choose_time.config(state='disabled')
        self.thread = threading.Thread(target=self.relaxation_counter, daemon=True)
        self.thread.start()

    def minutes_remaing(self, min, sec):
        if min == 0 and sec == 0:
            with open('draft.txt', 'w') as f:
                f.write(self.text_area.get('1.0', END))
            self.timer.config(text=f'Timer: 0:00')
            self.after_cancel(self.stop_minutes)
            self.choose_time.config(state='normal')
            self.word_typed()
            self.not_stop = False
            return 'break'
        elif sec == 0 or sec == 60:
            sec = 60
            self.timer.config(text=f'Timer: {min}:00')
            min -= 1
        elif sec < 10:
            self.timer.config(text=f'Timer: {min}:0{sec}')
        else:
            self.timer.config(text=f'Timer: {min}:{sec}')
        self.stop_minutes = self.after(1000, self.minutes_remaing, min, sec - 1)

    def seconds_remaining(self, time):
        if time < 0:
            time = 0
            self.time_stop.config(text=f'Seconds: {time}')
            self.after_cancel(self.stop_seconds)
            self.after_cancel(self.stop_minutes)
            self.choose_time.config(state='normal')
            self.text_area.config(bg=self.color[0])
            self.timer.config(text='Time is over!!!!!!')
            self.heading.focus_set()
            self.word_typed()
            self.text_area.delete('1.0', END)
            self.not_stop = False
        else:
            try:
                self.text_area.config(bg=self.color[time])
            except IndexError:
                pass
            self.time_stop.config(text=f'Seconds: {time}')
            self.stop_seconds = self.after(1000, self.seconds_remaining, time - 1)

    #######################Keyboard user catching action######################################################
    def relaxation_counter(self):
        while (self.not_stop):
            if self.detect_key(False) and self.time_stop.cget('text') != 'Seconds: 0':
                self.seconds_remaining(self.seconds)
            time.sleep(3)

    def detect_call_function(self, event):
        empty = (self.text_area.get('1.0', END).split())
        if not empty and self.timer.cget('text') == 'Timer: 3:00':
            self.start_action(3)
        else:
            self.detect_key(event.send_event)

    def detect_key(self, typed):
        if typed:
            try:
                self.after_cancel(self.stop_seconds)
                self.text_area.config(bg='white')
            except:
                pass
            else:
                self.time_stop.config(text=f'Seconds: {self.seconds}')
                return False
        else:
            return True

    #######################################################################################################

    def get_highscore(self, option):
        to_get_variable = option.get()
        if to_get_variable == 3:
            file = 'highscore_for_3mins.txt'
        else:
            file = 'highscore_for_5mins.txt'
        with open(file, 'r') as f:
            high_score = f.read()
            return high_score

    def word_typed(self):
        words = self.text_area.get('1.0', END).split()
        score = len(words)
        self.check_highscore(score, self.selected_time)
        self.words_written.config(text=f'Words Typed:{score}')

    def check_highscore(self, score, option):
        to_get_variable = option.get()
        if to_get_variable == 3:
            chosen_file = 'highscore_for_3mins.txt'
        else:
            chosen_file = 'highscore_for_5mins.txt'
        with open(chosen_file, 'r') as f:
            high_score = f.read()
            if score > int(high_score.split()[0]):
                with open(chosen_file, 'w') as file:
                    file.write(f'{score} words')


if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    app = App()
    theme = Style()
    theme.theme_use('classic')

    # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    app.mainloop()
