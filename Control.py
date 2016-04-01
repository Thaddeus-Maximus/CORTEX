from Tkinter import *
import tkMessageBox as box
import nxt
import nxt.locator
import nxt.brick
import nxt.error
import math

master=Tk()
master.title("StorageBot Control")
number_labels=[]
name_labels=[]
retrieval_checkboxes_vars=[]
retrieval_checkboxes=[]
frame=""
go_button=""

arm = nxt.locator.find_one_brick(name='TJHNXT1', host='00:16:53:09:A5:7F')
truck = nxt.locator.find_one_brick(name="TJHNXT2", host='00:16:53:12:0D:F7')

def run():
    order_list="!"
    for i in range(15):
        if(retrieval_checkboxes_vars[i].get()):
            order_list+=chr(i+97)
        retrieval_checkboxes[i].deselect()

    if(len(order_list) <= 5):
        print order_list
        arm.message_write(3,order_list)
    else:
        box.showerror("Out of Range","More than 4 items selected.")


def shutdown():
    arm.message_write(7,"-");
    truck.message_write(7,"-");

for i in range(15):
    number_labels.append(Label(master,text=str(i+1)))
    number_labels[i].grid(row=i,column=0)
    name_labels.append(Label(master,text="Item",width=15))
    name_labels[i].grid(row=i,column=1)
    retrieval_checkboxes_vars.append(IntVar())
    retrieval_checkboxes.append(Checkbutton(master,text="", variable=retrieval_checkboxes_vars[i] ))
    retrieval_checkboxes[i].grid(row=i,column=2)

go_button=Button(master,text="FETCH!",command=run)
go_button.grid(row=15,columnspan=3,column=0)

menubar = Menu(master)
menubar.add_command(label="Shutdown", command=shutdown)
master.config(menu=menubar)

def task():
    try:
        inbox, message=arm.message_read(12, 0, True)
        truck.message_write(2,message)
        print "2: "+message;
    except nxt.error.DirProtError, e:
        pass
    try:
        inbox, message=truck.message_read(15, 0, True)
        arm.message_write(5,message)
        print "5: "+    message;
    except nxt.error.DirProtError, e:
        pass

    try:
        inbox, message=arm.message_read(17, 0, True)
        for i in range(15):
            if(message[i]=='y'):
                retrieval_checkboxes[i].config(state=NORMAL)
            else:
                retrieval_checkboxes[i].deselect()
                retrieval_checkboxes[i].config(state=DISABLED)
    except nxt.error.DirProtError, e:
        pass

    master.after(10,task)

master.after(10,task)
master.mainloop()
