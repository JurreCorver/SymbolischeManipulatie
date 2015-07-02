import tkinter as tk
import subprocess
import os
import time
from PIL import Image
from expression_template import *

root = tk.Tk() #initialize the window
root.wm_title("Ruben is Trojaanse Manipulator")
root.geometry('800x600')

inpFrame = tk.Frame(root)
inpBox = tk.Text(root,height=1) #make a text box 1 line high at the bottom of the screen
inpBox.pack(side=tk.BOTTOM, fill=tk.X)

#make a checkbutton for LaTeX function toggling
useTex = tk.IntVar() 
useTex.set(1)
texBox = tk.Checkbutton(inpFrame,text='Use LaTeX',variable=useTex)
texBox.grid(column=1,row=0)

#make three radiobuttons for the user to specify what kind of output processing is done
outSettingLabel = tk.Label(inpFrame,text='\tOutput processing: ')
outSettingLabel.grid(column=2,row=0)
outputSetting=tk.StringVar()
outputSetting.set('simplify')
simplifyButton = tk.Radiobutton(inpFrame, text='Simplify',variable=outputSetting,value='simplify')
simplifyButton.grid(column=3,row=0)
evaluateButton = tk.Radiobutton(inpFrame,text='Evaluate',variable=outputSetting,value='evaluate')
evaluateButton.grid(column=4,row=0)
noneButton = tk.Radiobutton(inpFrame,text='None',variable=outputSetting,value='none')
noneButton.grid(column=5,row=0)

inpFrame.pack(side=tk.TOP, fill=tk.X)

def sendCommand(self): #Command used to parse content of inpBox when Return is pressed
    outBox.config(state=tk.NORMAL) #enable the output box so it can be edited
    inpText = inpBox.get("1.0",'end') #get the text
    inpText = inpText.replace('\n','') #remove newline characters from input
    inpText = inpText.replace(' ','') #remove spaces

    global inpRingIndex #add the input to the history and set the index to the end of the list
    inpRing.append(inpText)
    inpRingIndex = len(inpRing)
    if len(inpText)==0: #stop if the user pressed enter on an empty line
        return None
    if len(inpText)>0: #Insert the text
        outBox.insert(tk.END, '>>> '+inpText+'\n')
        inpBox.delete("1.0",tk.END)
        try: #process input based on settings and catch+print any errors
            outSet = outputSetting.get()
            outExpr = frost(inpText)
            if type(outExpr)!=list:
                if outSet == 'simplify':
                    outExpr = sfrost(inpText)
                elif outSet == 'evaluate':
                    outExpr = frost(inpText).evaluate()
                elif outSet == 'none':
                    outExpr = frost(inpText)
        except Exception as err:
            outBox.insert(tk.END,err.__class__.__name__+': '+str(err)+'\n')
        else: #if there were no errors convert the output to tex if the option is enabled
            if useTex.get()==1:
                try: #catch errors that converting to LaTeX may produce
                    if type(outExpr)==list:
                        if len(outExpr)==1:
                            texToImage(outExpr[0].tex())
                        else:
                            texList = [e.tex() for e in outExpr]
                            outTex=''
                            for i in range(len(texList)):
                                if i==0:
                                    outTex+="["+texList[i]+", "
                                elif i!=len(texList)-1:
                                    outTex+=texList[i]+", "
                                else:
                                    outTex+=texList[i]+"]"
                            texToImage(outTex)
                    else:
                        texToImage(outExpr.tex())
                except Exception as err:
                    outBox.insert(tk.END,'Error evaluating LaTeX: '+str(err))
                outBox.insert(tk.END,'\n')
            else:
                if type(outExpr)==list:
                    for exp in outExpr:
                        outBox.insert(tk.END, str(exp)+'\n')
                else:
                    outBox.insert(tk.END, str(outExpr)+'\n')
    outBox.config(state=tk.DISABLED) #disable the output box

#bind sending the input to the enter key    
inpBox.bind("<Return>",sendCommand)

#allow for the user to cycle through input history via the up/down arrow keys
inpRing = []
inpRingIndex=0
def cycleRing(direction):
    global inpRingIndex
    inpBox.delete("1.0",tk.END)
    if len(inpRing)>0:
        inpRingIndex+=direction
        if inpRingIndex == -1:
            inpRingIndex = len(inpRing)
        if inpRingIndex == len(inpRing)+1:
            inpRingIndex = 0
        if inpRingIndex != len(inpRing):
            inpBox.insert(tk.END, inpRing[inpRingIndex])

def cycleRingUp(self):
    cycleRing(-1)
def cycleRingDown(self):
    cycleRing(1)
inpBox.bind("<Up>",cycleRingUp)
inpBox.bind("<Down>",cycleRingDown)
inpFrame = tk.Frame(root)

#add a a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#create the box where the output goes
outBox = tk.Text(root,height=10000,state=tk.DISABLED,yscrollcommand=scrollbar.set)
scrollbar.config(command=outBox.yview)
outBox.pack(side=tk.TOP, fill=tk.BOTH)

#create a list of images to be displayed later
root.images=[]

class latexError(Exception): #create an exception class for LaTeX errors 
    def __init__(self,message):
        self.message = message

    def __str__(self):
        return self.message

def texToImage(string):
    outputTex = open('equation.tex','w')
    outputTex.write('\\documentclass[border=1pt,convert={density=600}]{standalone}\n')#changing density will change the DPI of the image, creating a linearly larger image
    outputTex.write('\\begin{document}\n')
    outputTex.write('\\batchmode\n') #make LaTeX go on even when encountering erros
    outputTex.write('$\\displaystyle\n')
    outputTex.write(string) #this is where the actual math expression goes.
    outputTex.write('\n$\n')
    outputTex.write('\\end{document}')
    outputTex.close()

    #use LaTeX to conver the tex file into a DVI file. The convert option of standalone then works its magic and outputs a png file with the name equation.png
    subprocess.call(['latex','-shell-escape', 'equation.tex'],stdout=open(os.devnull,'w')) #then call LaTeX

    #open the log and check for errors
    texLog = open('equation.log','r')
    texErrors=''
    for line in texLog:
        if line[0]=='!': #the line containing  errors in the log always start with an exclamation mark
            texErrors+=line[1:-1]
    if texErrors!='':
        raise latexError(texErrors)
    texLog.close()

    im = Image.open('equation.png') #open the image for processing
    out=im.resize((int(im.size[0]/5),int(im.size[1]/5)),Image.LANCZOS) #scale down the image. Lanczos is a nice looking (but slow) algorithm to do so
    out.save('equation_conv.png')#save the converted equation and display it to the output
    root.images.append(tk.PhotoImage(file='equation_conv.png'))
    outBox.image_create('end',image=root.images[-1])

    #this process generates a lot of files, which we are going to remove now
    os.remove('equation.aux')
    os.remove('equation.dvi')
    os.remove('equation.log')
    os.remove('equation.png')
    os.remove('equation.ps')
    os.remove('equation.tex')
    os.remove('equation_conv.png')

root.mainloop() #starts the event loop, any code after this will NOT be evaluated unless the window is closed
exit() #make sure the process ends after closing the window
