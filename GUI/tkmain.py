import tkinter as tk
import subprocess
from PIL import Image

root = tk.Tk() #initialize the window
root.wm_title("Project symbolische manipulatie")

# ret = subprocess.call(['latex','-shell-escape', r'C:\Users\Rik\Documents\Python\SymbolischeManipulatie\testfile.tex']) 

im = Image.open('testfile.png')
print(im.size)
out=im.resize((int(im.size[0]/2),int(im.size[1]/2)),Image.LANCZOS)
out.save('testfile2.png')

teximage = tk.PhotoImage(file='testfile2.png')
canvas = tk.Canvas(root, width = 500,height=500)


canvas.create_image(0,0,image=teximage, anchor=tk.NW)
canvas.pack(anchor=tk.CENTER)


root.mainloop() #starts the event loop, any code after this will NOT be evaluated unless the window is closed
exit() #make sure the process ends after closing the window
