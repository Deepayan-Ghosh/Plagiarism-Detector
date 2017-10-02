import GUI.View as View
import Model.Model as Model
from Tkinter import *
import tkFileDialog as filedialog
import tkMessageBox as msgbx
import os.path


class Controller:
    def __init__(self,master):
        self.master = master
        self.file1,self.file2 = '',''
        self.file1_cont,self.file2_cont = '',''
        self.view = View.View(master,self)
        self.model = Model.Reader()

    def browse_files(self,text):
        if text.endswith('1'):
            self.file1 = filedialog.askopenfilename()
            self.view.file_one_entry.delete(0,END)
            self.view.file_one_entry.insert(0,os.path.split(self.file1)[1])
        else:
            self.file2 = filedialog.askopenfilename()
            self.view.file_two_entry.delete(0, END)
            self.view.file_two_entry.insert(0, os.path.split(self.file2)[1])

    def execution(self,event=None):
        #self.model.set_filename(self.file1,self.file2)
        #self.model.read()
        final_index_list,src_index_list = [],[]
        if not self.view.v.get():
            if len(self.file1)==0 or len(self.file2)==0:
                msgbx.showerror(title='Error',message='Please select two files')
                return
            self.model.set_filename(self.file1,self.file2)
            src_index_list,final_index_list,percent1,percent2 = self.model.read()
        else:
            self.file1_cont = self.view.text_one.get('1.0','end-1c')
            self.file2_cont = self.view.text_two.get('1.0','end-1c')
            if len(self.file1_cont)==0 or len(self.file2_cont)==0:
                msgbx.showerror(title='Error',message='Please select two files')
                return
            src_index_list,final_index_list,percent1,percent2 = self.model.set_content(self.file1_cont,self.file2_cont)

        self.view.add_result_window(self.master)
        self.view.label_final_percent1['text'] = 'File 1 is '+"{:.2f}".format(percent1)+'% plagarised'
        self.view.label_final_percent2['text'] = 'File 2 is '+"{:.2f}".format(percent2)+'% plagarised'

        self.view.result_text_one.delete("1.0","end")
        self.view.result_text_one.insert("end",self.model.src_content)
        self.view.result_text_two.delete("1.0","end")
        self.view.result_text_two.insert("end",self.model.doc_content)
        for each in final_index_list:
            self.view.result_text_two.tag_add("highlight","end -%dc" % (len(self.model.doc_content)+1-each[0]),
                                              "end -%dc" % (len(self.model.doc_content)-each[1]))
        for each in src_index_list:
            self.view.result_text_one.tag_add("highlight","end -%dc" % (len(self.model.src_content)+1-each[0]),
                                              "end -%dc" % (len(self.model.src_content)-each[1]))
        self.view.result_text_two.tag_config("highlight",background='red')
        self.view.result_text_one.tag_config("highlight", background='red')

    def handle_input_method(self):
        #print self.view.v.get()
        if self.view.v.get():
            self.view.file_one_entry['state'],self.view.file_one_button['state'] = DISABLED,DISABLED
            self.view.file_two_entry['state'],self.view.file_two_button['state'] = DISABLED,DISABLED
            self.view.text_one['state'],self.view.text_two['state']=NORMAL,NORMAL
            self.view.text_one['bg'], self.view.text_two['bg'] = 'white','white'
        else:
            self.view.file_one_entry['state'], self.view.file_one_button['state'] = NORMAL,NORMAL
            self.view.file_two_entry['state'], self.view.file_two_button['state'] = NORMAL,NORMAL
            self.view.text_one['state'], self.view.text_two['state'] = DISABLED,DISABLED
            self.view.text_one['bg'], self.view.text_two['bg'] = 'lightgray','lightgray'
        return 'break'

root = Tk()
root.minsize(width = 650, height= 600)
root.resizable(False,False)
root.config(background='white')
controller = Controller(root)
root.mainloop()
