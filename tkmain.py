import tkinter as tk
import subprocess
import os
import time
from PIL import Image
from expression_template import *

root = tk.Tk() #initialize the window
root.wm_title("Project symbolische manipulatie")
root.geometry('800x600')


inpBox = tk.Text(root,height=1) #make a text box 1 line high at the bottom of the screen
inpBox.pack(side=tk.BOTTOM, fill=tk.X)


def sendCommand(self): #Command used to parse content of inpBox when Return is pressed
    outBox.config(state=tk.NORMAL) #enable the output box so it can be edited
    inpText = inpBox.get("1.0",'end') #get the text
    inpText = inpText[0:-1] #remove the last character
    if ord(inpText[0])==10: #remove first character of text if its a newline character (which has code 10)
        inpText =inpText[1::]
    if inpText: #Insert the text
        outBox.insert(tk.END, '>>> '+inpText+'\n')
    inpBox.delete("1.0",tk.END)
    outBox.insert(tk.END, str(sfrost(inpText))+'\n')
    outBox.config(state=tk.DISABLED) #disable the output box again
    
inpBox.bind("<Return>",sendCommand)


outBox = tk.Text(root,height=10000,state=tk.DISABLED)
outBox.pack(side=tk.TOP, fill=tk.BOTH)

def texToImage(string):
    outputTex = open('equation.tex','w')
    outputTex.write('\\documentclass[convert={density=600}]{standalone}\n')#changing density will change the DPI of the image, creating a linearly larger image
    outputTex.write('\\begin{document}\n')
    outputTex.write('$\\displaystyle\n')
    outputTex.write(string) #this is where the actual math expression goes.
    #The r'<some string>' is to make it into a raw string so that Python doesn't try to interpret the \'s
    outputTex.write('\n$\n')
    outputTex.write('\\end{document}')
    outputTex.close()

#use LaTeX to conver the tex file into a DVI file. The convert option of standalone then works its magic and outputs a png file with the name equation.png
    with open(os.devnull,'w') as f: #running LaTeX gives a LOT of output to the command line, this is to silence it
        subprocess.call(['latex','-shell-escape', 'equation.tex'],stdout=f) #then call LaTeX 

    im = Image.open('equation.png') #open the image for processing
    out=im.resize((int(im.size[0]/5),int(im.size[1]/5)),Image.LANCZOS) #scale down the image. Lanczos is a nice looking (but slow) algorithm to do so
    out.save('equation_conv.png') #save the converted equation


# tex = r'\sum_{n=1}^\infty \frac1{n^2} = \frac{\pi^2}6'

# t1 = time.time()#time the function. It ran about 700-800ms on my desktop PC
# texToImage(tex*2)
# print(time.time()-t1,'s')


# teximage = tk.PhotoImage(file='equation_conv.png')
# canvas = tk.Canvas(pane, width = 10000,height=500)
# pane.add(canvas)
    
#canvas.create_image(0,0,image=teximage, anchor=tk.NW)
#canvas.pack(anchor=tk.NW)


root.mainloop() #starts the event loop, any code after this will NOT be evaluated unless the window is closed
exit() #make sure the process ends after closing the window
