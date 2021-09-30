import os
import cv2
import threading as thread
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import *

#https://www.youtube.com/watch?v=K2Svy59O-KA
#uwu

class WindowHandler:
    def __init__(self):
        self.root = Tk()

    def showWindow(self):
        self.root.title('Diskpiggy')
        self.root.geometry('370x150')
        self.root.resizable(False, False)

        self.pathFrame = Frame(self.root)
        self.pathbox = Entry(self.pathFrame)
        self.pathbox.insert(0, 'No Folder Selected')
        self.pathbox.config(state='disabled')
        self.selectButton = Button(self.pathFrame, text='Select Folder', command=self.selectFolder)

        self.pathbox.pack(side='left', fill='x', expand=1, padx=2, pady=2)
        self.selectButton.pack(side='right', padx=2, pady=2)
        self.pathFrame.pack(side='top', fill='x', padx=2)

        self.submitButton = Button(self.root, text='Submit~', command=lambda: thread.Thread(target=self.enlargeFiles).run())
        self.submitButton.pack(side='top', fill='both', expand=1, padx=4, pady=4)

        self.progress = Progressbar(self.root, orient='horiz', length=1, mode='determinate')
        self.progLabel = Label(self.root, text='Idle')

        self.progress.pack(side='bottom', fill='x', pady=2, padx=2)
        self.progLabel.pack(side='bottom', pady=3)

        self.root.mainloop()

    def selectFolder(self):
        path = filedialog.askdirectory(title='Select Folder')
        self.pathbox.configure(state='normal')
        if(len(path) > 0):
            self.pathbox.delete(0, 'end')
            self.pathbox.insert(0, path)
        self.pathbox.configure(state='disabled')

    def enlargeFiles(self):
        path = self.pathbox.get()
        print(path)
        if(os.path.exists(path)):
            self.submitButton.configure(state='disabled')
            for root, dirs, file in os.walk(path):
                if(len(file) > 0):
                    self.progress['value'] = 0
                    self.progress.config(maximum=len(file))
                    for fileName in file:
                        self.progLabel.config(text=fileName)
                        self.root.update_idletasks()
                        
                        #somewhat arbitrary but helps prevent program from locking up with big files
                        if os.path.getsize(os.path.join(root, fileName)) >= 11804265: 
                            print('skipping oversized file (' + str(os.path.getsize(os.path.join(root, fileName))) + 'b)')
                            continue
                        
                        try:
                            self.scaleFactor = 5
                            self.img = cv2.imread(os.path.join(root, fileName), cv2.IMREAD_UNCHANGED)
                            self.progLabel.config(text=fileName + ' loaded.')
                            self.root.update_idletasks()

                            print('resizing with scale factor of ' + str(self.scaleFactor))
                            self.img_ = cv2.resize(self.img, 
                                            (self.img.shape[1] * self.scaleFactor, 
                                             self.img.shape[0] * self.scaleFactor))
                            self.progLabel.config(text=fileName + ' resized, attempting save.')
                            self.root.update_idletasks()

                            cv2.imwrite(os.path.join(root, fileName), self.img_)
                            self.progLabel.config(text=fileName + ' saved.')
                            self.root.update_idletasks()

                        except Exception as e:
                            print('Caught img error\n' + str(e))

                        self.progress['value'] += 1

            self.progLabel.config(text='Idle')
            self.submitButton.configure(state='normal')
            self.progress['value'] += 0

window = WindowHandler()

window.showWindow()