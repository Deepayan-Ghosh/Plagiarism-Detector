from Tkinter import *
class View:
    def __init__(self,master,controller):

        self.file_one_entry = Entry(master,width=35,bd=2)
        self.file_one_entry.grid(row=0,padx=20,pady=(45,15))
        self.file_one_button = Button(master,text='Choose file 1',
                                      command=lambda x='Choose file 1' : controller.browse_files(x))
        self.file_one_button.grid(row=1)

        self.file_two_entry = Entry(master, width=35,bd=2)
        self.file_two_entry.grid(row=0, column=1,padx=20, pady=(45,15))
        self.file_two_button = Button(master, text='Choose file 2',
                                      command=lambda x='Choose file 2' : controller.browse_files(x))
        self.file_two_button.grid(row=1,column=1)

        self.v=IntVar()
        self.checkbutton = Checkbutton(master, text="OR", bg='white', font='Arial 16 bold', variable=self.v,
                                       command=controller.handle_input_method)
        self.checkbutton.grid(row=2,columnspan=2,rowspan=2,pady=(50,50))

        self.label_enter_text_one = Label(master,text='Enter text of file 1:',bg='white',font='Arial 12 bold')
        self.label_enter_text_one.grid(row=3,sticky='w',padx=(90,0),pady=(60,0))

        self.label_enter_text_two = Label(master,text='Enter text of file 2:',bg='white',font='Arial 12 bold')
        self.label_enter_text_two.grid(row=3,column=1,sticky='w',padx=(50,0),pady=(60,0))

        self.text_frame1 = Frame(master,width=300,height=320,bg='blue')
        self.text_frame1.grid(row=4)

        self.text_frame2 = Frame(master, width=300, height=320, bg='blue')
        self.text_frame2.grid(row=4,column=1)

        self.text_one = Text(self.text_frame1, wrap='word', width=40,undo=1,bg='lightgray',state=DISABLED)
        self.text_one.bind('<Control-A>',self.select_all)
        self.text_one.bind('<Control-a>', self.select_all)
        self.text_one.bind('<Control-Y>',self.redo)
        self.text_one.bind('<Control-y>', self.redo)
        self.text_one.pack(side=LEFT)

        self.text_two = Text(self.text_frame2, wrap='word', bg='lightgray',width=40,undo=1,state=DISABLED)
        self.text_two.bind('<Control-A>', self.select_all)
        self.text_two.bind('<Control-a>', self.select_all)
        self.text_two.bind('<Control-Y>', self.redo)
        self.text_two.bind('<Control-y>', self.redo)
        self.text_two.pack(side=RIGHT)

        self.compare_button = Button(master,text='Compare',command=controller.execution)
        self.compare_button.grid(row=5,columnspan=2,pady=20)

        '''
            final window for displaying result
        '''

        self.toplevel=None
        self.label_final_percent1 = None
        self.label_final_percent2 = None

        self.result_text_one = None
        self.result_text_two = None


    def select_all(self,event=None):
        print event.keysym
        event.widget.tag_add('sel','1.0','end')
        return 'break'

    def redo(self,event=None):
        event.widget.event_generate('<<Redo>>')
        return 'break'

    def add_result_window(self,master):
        self.toplevel = Toplevel(master,bg='white')
        self.toplevel.minsize(600,500)
        self.toplevel.resizable(False,False)
        self.toplevel.transient(master)
        self.label_final_percent1 = Label(self.toplevel, text="",bg='white',font='Arial 12')
        self.label_final_percent2 = Label(self.toplevel, text="",bg='white',font='Arial 12')
        self.label_final_percent1.grid(row=0,column=0,padx=45,pady=10)
        self.label_final_percent2.grid(row=0,column=1,padx=(60,0),pady=10)

        self.result_text_one = Text(self.toplevel, wrap='word', width=50, undo=1, bg='white')
        self.result_text_one.bind('<Control-A>', self.select_all)
        self.result_text_one.bind('<Control-a>', self.select_all)
        self.result_text_one.bind('<Control-Y>', self.redo)
        self.result_text_one.bind('<Control-y>', self.redo)
        self.result_text_one.grid(row=1)

        self.result_text_two = Text(self.toplevel, wrap='word', bg='white', width=50, undo=1)
        self.result_text_two.bind('<Control-A>', self.select_all)
        self.result_text_two.bind('<Control-a>', self.select_all)
        self.result_text_two.bind('<Control-Y>', self.redo)
        self.result_text_two.bind('<Control-y>', self.redo)
        self.result_text_two.grid(row=1,column=1)

if __name__=="__main__":
    root = Tk()
    root.minsize(width = 650, height= 600)
    root.config(background='white')
    ob = View(root)
    root.mainloop()