import tkinter as tk
import subprocess
import os
import time
from PIL import Image

#this should work, but it gives an error (if we place it in /GUI)
#from .gui import * 

root = tk.Tk() #initialize the window
root.wm_title("Project symbolische manipulatie")
root.geometry('800x300')

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


tex = r'\sum_{n=1}^\infty \frac1{n^2} = \frac{\pi^2}6'

t1 = time.time()#time the function. It ran about 700-800ms on my desktop PC
texToImage(tex*4)
print(time.time()-t1,'s')


teximage = tk.PhotoImage(file='equation_conv.png')
canvas = tk.Canvas(root, width = 10000,height=500)
    
canvas.create_image(0,0,image=teximage, anchor=tk.NW)
canvas.pack(anchor=tk.NW)


root.mainloop() #starts the event loop, any code after this will NOT be evaluated unless the window is closed
exit() #make sure the process ends after closing the window
