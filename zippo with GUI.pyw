from zipfile import *
from codecs import *
from tkinter import *
import time
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox, Checkbutton, Progressbar
import threading
from math import *

##############НАСТРОЙКИ###################
last_pwd = '' #последний подобранный пароль
log = True #запись лога (имя архива, время перебора, пароль, и т.п.)
debugger = False #выводит перебираемые пароли в консоль (уменьшает скорость)
##########################################
'''
    проблемы:
-если у файлов в архиве разные пароли, то этот алгорити не сработает. Для реше-
ния этой проблемы:
1)создайте копию архива
2)удалите файлы из него, оставив всего 1 файл внутри архива
3)начинайте взлом
4)после успеха, повторите пункты с другими файлами

'''


class Chars():
    def __init__(self):
        '''
        создаю переменную alphabet, содержащую всевозможные символы для подбора
        пароля.
        '''
        self.alphabet = []
        self.symbols = symbols
        for i in self.symbols:
            self.alphabet.append(i)
        self.counter = 0

    def get_char(self):
        '''
        метод возвращает символ из алфавита с индексом счётчика
        '''
        return self.alphabet[self.counter]

    def next_char(self):
        '''
        метод увеличивает счётчик на 1. Если счётчик больше длины алфавита,
        то сбрасывается в 0
        '''
        self.counter += 1
        if self.counter >= len(self.alphabet):
            self.counter = 0
        self.get_char()

    def set_char(self, char):
        '''
        метод устанавливает объекту указанный символ (нужен для продолжения 
        подбора пароля с последнего перебранного)
        '''
        self.counter = self.symbols.index(char)

class Generator():
    def __init__(self):
        self.chars = []
        self.genuinue_pwd = [] #подходящие пароли

    def add_char(self, char=''):
        #метод добавляет символ
        self.chars.append(Chars())
        if char == '':
            pass
        else:
            self.chars[-1].set_char(char)


    def change_char(self, index):
        #метод увеличивает символ на +1
        self.chars[index].next_char()

    def generate(self):
        '''
        метод осуществляет перебор символов
        '''
        if log == True:
            start = time.time()
            file = open('main.log', 'a')
            file.write('\n\nАрхив: '+zip_name+'\n')
            if len(self.chars) > 1:
                file.write('перебор начат с символов '+str(gen)+'\n')
            file.close()
        while True:
            for i in range(0, len(self.chars)):
                if self.check_password() == True:
                    file = open('main.log', 'a')
                    file.write('Пароль подошел: '+str(self.genuinue_pwd))
                    file.write('\nНа подбор ушло '+str(time.time()-start)+
                        ' секунд')
                    return
                if self.chars[i].get_char() != Chars().alphabet[-1]:
                    self.chars[i].next_char()
                    break
                else:
                    if self.chars[-1].get_char() == Chars().alphabet[-1]:
                        self.chars[-1].next_char()

                        #запись времени перебора в лог
                        if log == True:
                            file = open('main.log', 'a')
                            file.write(str(len(self.chars))+
                                ' символьные комбинации из '+
                                str(len(Chars().alphabet))+
                                ' символов перебрано за '+
                                str(time.time()-start)+' секунд\n')
                            file.close()

                        self.chars.append(Chars())
                    self.chars[i].next_char()
            if debugger == True:
                print(gen)

    def check_password(self):
        '''
        метод пытается открыть архив очередным побобранным паролем
        '''
        password = ''
        for char in self.chars: 
            password += char.get_char()
        try:
            zf.extractall(pwd=password.encode('utf-8'))
        except:
            pass
        else:
            self.genuinue_pwd.append(password)
            return True

    def __str__(self):
        '''
        метод вывода строкового представления пароля
        '''
        string = ''
        for char in self.chars: 
            string += char.get_char()
        return string

def choose_zip():
    #предлагает указать zip-файл для взлома
    global zf, zip_name
    zip_name = filedialog.askopenfilename(filetypes={"архив zip"})
    zf = PyZipFile(zip_name)
    zip_name = zip_name.split('/')[-1]
    buttons[8].configure(text='архив '+zip_name)

def benchmark_dict():
    #измеряет производительность системы словарём
    buttons[0].configure(state='disabled')
    buttons[1].configure(state='disabled')
    buttons[2].configure(state='disabled')
    buttons[3].configure(state='disabled')
    buttons[4].configure(state='disabled')
    buttons[5].configure(state='disabled')
    buttons[6].configure(state='disabled')
    buttons[7].configure(state='disabled')
    buttons[10].configure(state='disabled')
    buttons[11].configure(state='disabled')
    buttons[8].configure(text='идёт тест производительности...')
    zf = PyZipFile('test.zip')
    dict_counter = 0
    file = open(dictionary, 'r')
    text = file.read()
    text = text.split()
    file.close()
    start = time.time()
    for pwd in text:
        try:
            dict_counter += 1
            zf.extractall(pwd=pwd.encode('utf-8'))
        except:
            pass
        if (time.time()-start) > 2:
            break
    result = 'за 1 секунду перебирается '+str(dict_counter)+' паролей'
    buttons[8].configure(text='тест производительности окончен')
    messagebox.showinfo('Результаты тестирования', result)
    buttons[0].configure(state='normal')
    buttons[1].configure(state='normal')
    buttons[2].configure(state='normal')
    buttons[3].configure(state='normal')
    buttons[4].configure(state='normal')
    buttons[5].configure(state='normal')
    buttons[6].configure(state='normal')
    buttons[7].configure(state='normal')
    buttons[10].configure(state='normal')
    buttons[11].configure(state='normal')

def benchmark_bf():
    #измеряет производительность системы брутфорсом
    buttons[0].configure(state='disabled')
    buttons[1].configure(state='disabled')
    buttons[2].configure(state='disabled')
    buttons[3].configure(state='disabled')
    buttons[4].configure(state='disabled')
    buttons[5].configure(state='disabled')
    buttons[6].configure(state='disabled')
    buttons[7].configure(state='disabled')
    buttons[10].configure(state='disabled')
    buttons[11].configure(state='disabled')
    buttons[8].configure(text='идёт тест производительности...')
    global symbols, gen, zf, zip_name
    symbols = ''
    symbols += 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    symbols += '0123456789'
    symbols += ' /*()+-=&^%$@![]{<}>,._'
    zip_name = 'test.zip'
    zf = PyZipFile(zip_name)
    start = time.time()
    gen = Generator() #создаю экземпляр БрутФорса
    gen.add_char() #начинаю генерировать односимвольный пароль
    gen.generate() #запускаю перебор
    finish = time.time()
    bench_time = finish-start #время теста

    result = 'полный перебор 2x символов за '+str(int(bench_time))+' секунд\n'
    if bench_time*len(symbols) > 3600:
        result += 'полный перебор 3x символов за '+str(int(bench_time*len(symbols)//3600))+' часов\n'
    elif bench_time*len(symbols) > 60:
        result += 'полный перебор 3x символов за '+str(int(bench_time*len(symbols)//60))+' минут\n'
    else:
        result += 'полный перебор 3x символов за '+str(int(bench_time*len(symbols)))+' секунд\n'
    if bench_time*(len(symbols)**2) > 3600:   
        result += 'полный перебор 4x символов за '+str(int(bench_time*(len(symbols)**2)//3600))+' часов\n'
    elif bench_time*(len(symbols)**2) > 60:
        result += 'полный перебор 4x символов за '+str(int(bench_time*(len(symbols)**2)//60))+' минут\n'
    else:
        result += 'полный перебор 4x символов за '+str(int(bench_time*(len(symbols)**2)))+' секунд\n'
    if bench_time*(len(symbols)**3) > 86400:
        result += 'полный перебор 5x символов за '+str(int(bench_time*(len(symbols)**3)//86400))+' дней\n'
    elif bench_time*(len(symbols)**3) > 3600:   
        result += 'полный перебор 5x символов за '+str(int(bench_time*(len(symbols)**3)//3600))+' часов\n'
    elif bench_time*(len(symbols)**3) > 60:
        result += 'полный перебор 5x символов за '+str(int(bench_time*(len(symbols)**3)//60))+' минут\n'
    else:
        result += 'полный перебор 5x символов за '+str(int(bench_time*(len(symbols)**3)))+' секунд\n'

    buttons[8].configure(text='тест производительности окончен')
    messagebox.showinfo('Результаты тестирования', result)
    buttons[0].configure(state='normal')
    buttons[1].configure(state='normal')
    buttons[2].configure(state='normal')
    buttons[3].configure(state='normal')
    buttons[4].configure(state='normal')
    buttons[5].configure(state='normal')
    buttons[6].configure(state='normal')
    buttons[7].configure(state='normal')
    buttons[10].configure(state='normal')
    buttons[11].configure(state='normal')

    del gen

def start_bench():
    '''функция запуска бенчмарка в отдельном потоке
        run benchmark in apart thread'''
    if mode == 'bruteforce':
        server = threading.Thread(target=benchmark_bf)
    else:
        server = threading.Thread(target=benchmark_dict)
    server.daemon = True 
    server.start() 

def thread_start():
    '''функция запускает взлом в отдельном потоке'''
    try: #проверка, был ли указан архив для взлома
        if zf == '':
            pass 
    except:
        messagebox.showerror(title='ошибка', message='вы не указали архив!')
        return

    global hack
    buttons[1].configure(state='disabled')
    buttons[2].configure(state='disabled')
    buttons[3].configure(state='disabled')
    buttons[4].configure(state='disabled')
    buttons[5].configure(state='disabled')
    buttons[6].configure(state='disabled')
    buttons[7].configure(state='disabled')
    buttons[10].configure(state='disabled')
    buttons[11].configure(state='disabled')
    hack = threading.Thread(target=pre_start)
    hack.daemon = True 
    hack.start()

def select_mode():
    global mode
    '''
    функция для кнопок RadioButton, для выбора режима взлома
    '''
    if selected_mode.get() == 0:
        '''выбран брутфорс'''
        buttons[3].configure(state='enabled')
        buttons[4].configure(state='enabled')
        buttons[5].configure(state='enabled')
        buttons[9].configure(state='disabled')
        buttons[10].configure(state='normal')
        buttons[11].configure(state='normal')
        mode = 'bruteforce'
    else:
        '''выбран словарь'''
        buttons[3].configure(state='disabled')
        buttons[4].configure(state='disabled')
        buttons[5].configure(state='disabled')
        buttons[9].configure(state='normal')
        buttons[10].configure(state='disabled')
        buttons[11].configure(state='disabled')
        mode = 'dictionary'

def stop():
    global gen, last_pwd, text
    buttons[1].configure(state='normal')
    buttons[2].configure(state='normal')
    buttons[3].configure(state='normal')
    buttons[4].configure(state='normal')
    buttons[5].configure(state='normal')
    buttons[6].configure(state='normal')
    buttons[7].configure(state='normal')
    buttons[10].configure(state='normal')
    buttons[11].configure(state='normal')
    try:
        last_pwd = str(gen) #последний подобранный пароль
    except:
        pass
    if mode == 'bruteforce':
        if log == True:
            file = open('main.log', 'a')
            file.write('Остановлено на: '+last_pwd+'\n')
            file.close()
        buttons[8].configure(text='остановлено на '+last_pwd)
        buttons[0].configure(text='продолжить',fg='green', font='arial',
         command=thread_start)
    else:
        buttons[8].configure(text='остановлено')
        buttons[0].configure(text='начать',fg='green', font='arial',
         command=thread_start)
    
    text = ''
    try:
        del gen
    except:
        pass

def pre_start():
    '''функция преименения выбранных настроек и запуск взлома'''
    global symbols, gen, last_pwd, text
    buttons[8].configure(text='идёт подбор пароля, подождите')
    buttons[0].configure(text='стоп')
    buttons[0].configure(fg='red', font='arial', command=stop)
    if mode == 'bruteforce':
        if log == True:
            try:
                file = open('main.log', 'a')
            except:
                file = open('main.log', 'w')
            finally:
                file.close()
        symbols = ''
        if var3.get() == 1:
            symbols += 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        if var4.get() == 1:
            symbols += '0123456789'
        if var5.get() == 1:
            symbols += ' /*()+-=&^%$@![]{<}>,._'
        gen = Generator() #create instantion Bruteforce
        if buttons[10].get() != '' and last_pwd == '':  
            for i in buttons[10].get(): #продолжаю перебор с последнего места
                gen.add_char(i)
        elif last_pwd != '':
            for i in last_pwd: #продолжаю перебор с последнего места
                gen.add_char(i)
        else: #если же последний пароль не указан
            gen.add_char() #начинаю генерировать односимвольный пароль
        gen.generate() #запускаю перебор
        buttons[8].configure(text='Пароль подошел => '+str(gen))

    else:
        file = open(dictionary, 'r')
        text = file.read()
        text = text.split()
        file.close()
        for pwd in text:
            try:
                zf.extractall(pwd=pwd.encode('utf-8'))
            except:
                pass
            else:
                buttons[8].configure(text='Пароль подошел => '+pwd)
    buttons[1].configure(state='normal')
    buttons[2].configure(state='normal')
    buttons[3].configure(state='normal')
    buttons[4].configure(state='normal')
    buttons[5].configure(state='normal')
    buttons[6].configure(state='normal')
    buttons[7].configure(state='normal')
    buttons[10].configure(state='normal')
    buttons[11].configure(state='normal')
    buttons[0].configure(text='старт', command=thread_start)
    buttons[0].configure(fg='green', font='arial')

def change_dict():
    global dictionary
    dictionary = filedialog.askopenfilename()

    
if __name__ == "__main__":
    dictionary = 'passwords.dic' #built-in dictionary
    mode = 'bruteforce' #hacking mode
    window = Tk()
    window.title("Dragmors ZipHack")
    window.geometry('270x290') #window resolution
    # window.resizable(width=False, height=False) #off resizable mode
    window.wm_iconbitmap("img/icon.ico") #load icon
    buttons = [] #buttons list
    var3 = BooleanVar()
    var3.set(True)
    var4 = BooleanVar()
    var4.set(True)
    var5 = BooleanVar()
    var5.set(True)
    selected_mode = IntVar()
    symbols = '' #chars for bulkhead
    buttons.append(Button(text='старт', command=thread_start))#0
    buttons.append(Button(text='ВЫБРАТЬ АРХИВ', command=choose_zip))#1   
    buttons.append(Button(text='тест производительности',
     command=start_bench))#2 
    buttons.append(Checkbutton(text='A-z', var=var3))#3
    buttons.append(Checkbutton(text='0-9', var=var4))#4
    buttons.append(Checkbutton(text='прочие символы', var=var5))#5
    buttons.append(Radiobutton(text='словарь   ', value=1,
     var=selected_mode, command=select_mode))#6

    buttons.append(Radiobutton(text='брутфорс', value=0,
     var=selected_mode, command=select_mode))#7

    buttons.append(Label(text='выберите архив', font='system',
     bg='lightgray', height=2))#8
    buttons.append(Button(text='выбрать свой словарь', command=change_dict))#9
    buttons.append(Entry()) #10
    buttons.append(Label(text='последний перебранный пароль'))

    buttons[9].configure(state='disabled')

   
    buttons[0].pack(side='bottom',anchor='n', fill='both')
    buttons[2].pack(side='bottom',anchor='n', fill='both')
    buttons[1].pack(side='bottom',anchor='n', fill='both')
    buttons[8].pack(side='bottom',anchor='n', fill='both')
    buttons[9].pack(side='bottom',anchor='n', fill='both')
    buttons[10].pack(side='bottom',anchor='n', fill='both')
    buttons[11].pack(side='bottom',anchor='n', fill='both')
    buttons[3].pack(side='bottom',anchor='n', fill='both')
    buttons[4].pack(side='bottom',anchor='n', fill='both')
    buttons[5].pack(side='bottom',anchor='n', fill='both')
    buttons[7].pack(side='top',anchor='center')
    buttons[6].pack(side='top',anchor='center')
    

    buttons[0].configure(fg='green', font='arial')

    window.mainloop()
'''
version 1.3 10.04.2022
update UI 20.11.2022
'''