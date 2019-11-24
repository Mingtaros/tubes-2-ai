from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import DetectShape
import ImageProc
from PIL import Image, ImageTk
import numpy as np
import cv2

DEFAULT_PICTURE_IMAGE = 'images/image-pick.png'
DEFAULT_PICTURE_SHAPE = 'images/shape-pick.png'
BACKGROUND_IMAGE = 'images/background-black.jpg'
IMAGE_SIZE = 350
BUTTON_WIDTH = 30
TREE_WIDTH = 270
TREE_HEIGHT = 18

facts_list = 'tes'
rules_list = 'tes'
images_res = ''

class imageClass:
    def __init__(self, master, image_path, image_size):
        self.master = master
        self.img = ''
        self.image_path = image_path
        self.image_size = image_size
        self.loadImage(image_path)
    
    def loadImage(self, image_path):
        try:
            load = Image.open(image_path)
            if (self.img != ''):
                self.img.destroy()
            self.image_path = image_path
            width, height = load.size[:2]
            render = self.resize(height, width, load)
            self.img = Label(self.master, image=render)
            self.img.image = render
            self.img.grid(row = 0, column = 0)
        except:
            print('File tidak valid')

    def resize(self, height, width, load):
        if height > width:
            baseheight = self.image_size
            hpercent = (baseheight/float(load.size[1]))
            wsize = int((float(load.size[0])*float(hpercent)))
            return ImageTk.PhotoImage(load.resize((wsize, baseheight)))
        else:
            basewidth = self.image_size
            wpercent = (basewidth/float(load.size[0]))
            hsize = int((float(load.size[1])*float(wpercent)))
            return ImageTk.PhotoImage(load.resize((basewidth, hsize)))

    def changeImage(self):
        filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if (filename):
            self.loadImage(filename)

    def loadImageFromPILFormat(self, image_pil):
        self.img.destroy()
        width, height = image_pil.size[:2]
        render = self.resize(height, width, image_pil)
        self.img = Label(self.master, image=render)
        self.img.image = render
        self.img.grid(row = 0, column = 0)

class textClass:
    def __init__(self, master):
        self.master = master
        self.text = Text(master, height=TREE_HEIGHT, width=41)
        self.text.pack(side = 'left')
        self.text.configure(state = 'disabled')
        self.text.bind("<1>", lambda event: self.text.focus_set())

    def changeText(self, text):
        self.text.configure(state = 'normal')
        self.text.delete('1.0', END)
        self.text.insert(END, text)
        self.text.configure(state = 'disabled')

def changeShape(event):
    global rules_list
    global image_source
    global image_pattern
    if (image_source.image_path != DEFAULT_PICTURE_IMAGE):
        item = tree.identify('item', event.x, event.y)
        # Call engine
        shape_idx, rules_list, cv_image = DetectShape.findShapes(image_source.image_path, tree.item(item, "text"))
        for i in shape_idx:
            cv_image = ImageProc.gambarContour(cv_image, i)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        image_pattern.loadImageFromPILFormat(pil_image)

def showRules():
    global rules_list
    rules_container.changeText(rules_list)

def showFacts():
    facts_container.changeText(rules_list)

root = Tk()
root.geometry("1000x700")
root.resizable(0, 0)
root.title('Image Detection')

# Row Container
row1 = Frame(root)
row1.pack(side = 'top')
row2 = Frame(root)
row2.pack(side = 'top')

# Source image
labelframe_input = LabelFrame(row1, text="Source Image", width=300, height=300)
labelframe_input.pack(side = 'left')

image_background = imageClass(labelframe_input, BACKGROUND_IMAGE, IMAGE_SIZE)
image_source = imageClass(labelframe_input, DEFAULT_PICTURE_IMAGE, IMAGE_SIZE)

# Pattern image
labelframe_pattern = LabelFrame(row1, text="Detection Image")
labelframe_pattern.pack(side = 'left')

image_background_2 = imageClass(labelframe_pattern, BACKGROUND_IMAGE, IMAGE_SIZE)
image_pattern = imageClass(labelframe_pattern, DEFAULT_PICTURE_SHAPE, IMAGE_SIZE)

# Button
button_container = Label(row1)
button_container.pack(side = 'left')
 
btn_open_image = Button(button_container, text='Open Image', width = BUTTON_WIDTH, command = image_source.changeImage)
btn_open_image.pack(side = 'top', pady = 4)

btn_open_rule = Button(button_container, text='Open Rule Editor', width = BUTTON_WIDTH)
btn_open_rule.pack(side = 'top', pady = 4)

btn_show_rule = Button(button_container, text='Show Rules', width = BUTTON_WIDTH, command = showRules)
btn_show_rule.pack(side = 'top', pady = 4)

btn_show_facts = Button(button_container, text='Show Facts', width = BUTTON_WIDTH, command = showFacts)
btn_show_facts.pack(side = 'top', pady = 4)

# Treeview
tree = ttk.Treeview(button_container)
tree.column("#0", width=TREE_WIDTH, minwidth=TREE_WIDTH, stretch=NO)
tree.heading("#0",text="Shape")

#Level 0
shape = tree.insert('', 'end', text = "All Shapes")
#Level 1
segitiga = tree.insert(shape, 'end', text = "Segitiga")
segiempat = tree.insert(shape, 'end', text = "Segi Empat")
segilima = tree.insert(shape, 'end', text = "Segi Lima")
segienam = tree.insert(shape, 'end', text = "Segi Enam")
segitiga_lancip = tree.insert(segitiga, 'end', text = "Segitiga Lancip")
segitiga_tumpul = tree.insert(segitiga, 'end', text = "Segitiga Tumpul")
segitiga_siku = tree.insert(segitiga, 'end', text = "Segitiga Siku-siku")
segitiga_kaki = tree.insert(segitiga, 'end', text = "Segitiga Sama Kaki")
segitiga_sisi = tree.insert(segitiga, 'end', text = "Segitiga Sama Sisi")

jajaran_genjang = tree.insert(segiempat, 'end', text = "Jajaran Genjang")
trapesium = tree.insert(segiempat, 'end', text = "Trapesium")

segilima_sisi = tree.insert(segilima, 'end', text = "Segi Lima Sama Sisi")
segienam_sisi = tree.insert(segienam, 'end', text = "Segi Enam Sama Sisi")

#Level 3
segitiga_kaki_siku = tree.insert(segitiga_kaki, 'end', text = "Segitiga Sama Kaki dan Siku-siku")
segitiga_kaki_tumpul = tree.insert(segitiga_kaki, 'end', text = "Segitiga Sama Kaki dan Tumpul")
segitiga_kaki_lancip = tree.insert(segitiga_kaki, 'end', text = "Segitiga Sama Kaki dan Lancip")

segiempat_beraturan = tree.insert(jajaran_genjang, 'end', text = "Segiempat Beraturan")
layang_layang = tree.insert(jajaran_genjang, 'end', text = "Segiempat Berbentuk Layang-layang")

trapesium_kaki = tree.insert(trapesium, 'end', text = "Trapesium Sama Kaki")
trapesium_kanan = tree.insert(trapesium, 'end', text = "Trapesium Rata Kanan")
trapesium_kiri = tree.insert(trapesium, 'end', text = "Trapesium Rata Kiri")

tree.bind('<Double-1>', changeShape)
tree.pack(side = 'top')

# Result
labelframe_result = LabelFrame(row2, text="Detection Result")
labelframe_result.pack(side = 'left')

result_text = textClass(labelframe_result)

# Facts lists
labelframe_rule = LabelFrame(row2, text="Hit Rules")
labelframe_rule.pack(side = 'left')

rules_container = textClass(labelframe_rule)

# Rulse lists
labelframe_fact = LabelFrame(row2, text="Matched Facts")
labelframe_fact.pack(side = 'left')

facts_container = textClass(labelframe_fact)

root.mainloop()