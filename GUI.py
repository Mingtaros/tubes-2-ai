from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def changeShape(event):
    item = tree.identify('item', event.x, event.y)
    print("you clicked on", tree.item(item, "text"))
    #switch case for tree.item

root = Tk()
root.geometry("1200x700")
root.resizable(0, 0)
root.title('Image Detection')

labelframe_input = LabelFrame(root, text="This is a LabelFrame")
labelframe_input.grid(column = 0, row = 1)


load = Image.open("images/box.jpeg")
render = ImageTk.PhotoImage(load.resize((400, 400)))
img = Label(labelframe_input, image=render)
img.image = render
img.grid(column = 0, row = 0)

labelframe_pattern = LabelFrame(root, text="This is a LabelFrame")
labelframe_pattern.grid(column = 1, row = 1)

load = Image.open("images/rectangle.jpg")
render = ImageTk.PhotoImage(load.resize((400, 400)))
img = Label(labelframe_pattern, image=render)
img.image = render
img.grid(column = 0, row = 0)

button_container = Label(root)
button_container.grid(column = 2, row = 1)
 
btn_open_image = Button(button_container, text='Open Image', width = 38)
btn_open_image.grid(column = 0, row = 0, pady = 7, padx = 5)

btn_open_rule = Button(button_container, text='Open Rule Editor', width = 38)
btn_open_rule.grid(column = 0, row = 1, pady = 7, padx = 5)

btn_show_rule = Button(button_container, text='Show Rules', width = 38)
btn_show_rule.grid(column = 0, row = 2, pady = 7, padx = 5)

btn_show_facts = Button(button_container, text='Show Facts', width = 38)
btn_show_facts.grid(column = 0, row = 3, pady = 7, padx = 5)

tree = ttk.Treeview(button_container)
tree.column("#0", width=375, minwidth=375, stretch=NO)
tree.heading("#0",text="Shape",anchor=W)

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
tree.grid(column = 0, row = 4, pady = 7, padx = 5)

root.mainloop()