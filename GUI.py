from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

IMAGE_SIZE = 350
BUTTON_WIDTH = 30
TREE_WIDTH = 270
TREE_HEIGHT = 18

class imageClass:
    def __init__(self, master, image_path, image_size):
        self.master = master
        self.img = ''
        self.image_size = image_size
        self.loadImage(image_path)
    
    def loadImage(self, image_path):
        load = Image.open(image_path)
        render = ImageTk.PhotoImage(load.resize((self.image_size, self.image_size)))
        self.img = Label(self.master, image=render)
        self.img.image = render
        self.img.pack(side = 'left')

    def changeImage(self):
        filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.img.destroy()
        self.loadImage(filename)

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
    item = tree.identify('item', event.x, event.y)
    print("you clicked on", tree.item(item, "text"))
    #switch case for tree.item

def pickSource():
    img.destroy()
    filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File", filetypes =
    (("jpeg files","*.jpg"),("all files","*.*")) )
    print(filename)
    load = Image.open(filename)
    render = ImageTk.PhotoImage(load.resize((IMAGE_SIZE, IMAGE_SIZE)))
    img = Label(labelframe_input, image=render)
    img.image = render
    img.pack(side = 'left')



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
labelframe_input = LabelFrame(row1, text="Source Image")
labelframe_input.pack(side = 'left')

image_source = imageClass(labelframe_input, "images/box.jpeg", IMAGE_SIZE)

# Pattern image
labelframe_pattern = LabelFrame(row1, text="Detection Image")
labelframe_pattern.pack(side = 'left')

image_pattern = imageClass(labelframe_pattern, "images/rectangle.jpg", IMAGE_SIZE)

# Button
button_container = Label(row1)
button_container.pack(side = 'left')
 
btn_open_image = Button(button_container, text='Open Image', width = BUTTON_WIDTH, command = image_source.changeImage)
btn_open_image.pack(side = 'top', pady = 4)

btn_open_rule = Button(button_container, text='Open Rule Editor', width = BUTTON_WIDTH)
btn_open_rule.pack(side = 'top', pady = 4)

btn_show_rule = Button(button_container, text='Show Rules', width = BUTTON_WIDTH)
btn_show_rule.pack(side = 'top', pady = 4)

btn_show_facts = Button(button_container, text='Show Facts', width = BUTTON_WIDTH)
btn_show_facts.pack(side = 'top', pady = 4)

# Treeview
tree = ttk.Treeview(button_container)
tree.column("#0", width=TREE_WIDTH, minwidth=TREE_WIDTH, stretch=NO)
tree.heading("#0",text="Shape")

#Level 0
shape = tree.insert('', 'end', text = "All Shapes")
#Level 1
segitiga = tree.insert(shape, 'end', text = "Segitiga")
segiempat = tree.insert(shape, 'end', text = "Segiempat")
segilima = tree.insert(shape, 'end', text = "Segilima")
segienam = tree.insert(shape, 'end', text = "Segienam")
#Level 2
segitiga_lancip = tree.insert(segitiga, 'end', text = "Segitiga Lancip")
segitiga_tumpul = tree.insert(segitiga, 'end', text = "Segitiga Tumpul")
segitiga_siku = tree.insert(segitiga, 'end', text = "Segitiga Siku-siku")
segitiga_kaki = tree.insert(segitiga, 'end', text = "Segitiga Sama Kaki")
segitiga_sisi = tree.insert(segitiga, 'end', text = "Segitiga Sama Sisi")

jajaran_genjang = tree.insert(segiempat, 'end', text = "Jajaran Genjang")
trapesium = tree.insert(segiempat, 'end', text = "Trapesium")

segilima_sisi = tree.insert(segilima, 'end', text = "Segilima Sama Sisi")
segienam_sisi = tree.insert(segienam, 'end', text = "Segienam Sama Sisi")

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

# Result image
labelframe_result = LabelFrame(row2, text="Detection Result")
labelframe_result.pack(side = 'left')

image_result = imageClass(labelframe_result, "images/rectangle.jpg", 300)

# Facts lists
labelframe_facts = LabelFrame(row2, text="Hit Rules")
labelframe_facts.pack(side = 'left')

facts_container = textClass(labelframe_facts)

# Rulse lists
labelframe_rule = LabelFrame(row2, text="Matched Facts")
labelframe_rule.pack(side = 'left')

rules_container = textClass(labelframe_rule)

root.mainloop()