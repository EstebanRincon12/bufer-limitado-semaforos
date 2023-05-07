from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread, Semaphore

ventana = tk.Tk()
ventana.geometry('800x500')
ventana.title('Productores y Consumidores con semáforos')

labelTitle = tk.Label(ventana, text='Productores y Consumidores con semáforos')
labelNumberConsumer = ttk.Label(ventana, text='N° Consumidores')
labelNumberProductors = ttk.Label(ventana, text='N° Productores')
labelSizeBuffer = ttk.Label(ventana, text='Tamaño Buffer')
labelBuffer = ttk.Label(ventana, text='Buffer')

entryProductos = ttk.Entry(ventana)
entryConsumers = ttk.Entry(ventana)
entrySizeBuffer = ttk.Entry(ventana)

def startSimulation():

    global buf, buf_size
    buf_size = int(entrySizeBuffer.get())
    buf =[" "] * buf_size
    numberConsumers = int(entryConsumers.get())
    numberProductors = int(entryProductos.get())
    createConsumers(numberConsumers)
    createProducer(numberProductors)

buttonStart = ttk.Button(ventana, text='Iniciar', command=startSimulation)

canvas = tk.Canvas(master=ventana, width=700, height=100)

ventana.rowconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.rowconfigure(2, weight=1)
ventana.rowconfigure(3, weight=1)
ventana.rowconfigure(4, weight=1)
ventana.rowconfigure(5, weight=1)
ventana.rowconfigure(6, weight=1)
ventana.rowconfigure(7, weight=1)
ventana.rowconfigure(8, weight=1)
ventana.rowconfigure(9, weight=1)
ventana.columnconfigure(2, weight=1)
ventana.columnconfigure(3, weight=1)
ventana.columnconfigure(3, weight=1)
ventana.columnconfigure(4, weight=1)
ventana.columnconfigure(5, weight=1)
ventana.columnconfigure(6, weight=1)

labelTitle.grid(row=0, column=0, columnspan=7)
labelNumberProductors.grid(row=1, column=0)
labelNumberConsumer.grid(row=1, column=2)
labelSizeBuffer.grid(row=1, column=4)
entryProductos.grid(row=1, column=1)
entryConsumers.grid(row=1, column=3)
entrySizeBuffer.grid(row=1, column=5)
buttonStart.grid(row=1, column=6)
labelBuffer.grid(row=2, column=0, columnspan=7, rowspan=7)

s = Semaphore(1)
buf = []
producer_idx = 0
consumer_idx = 0
counter = 0
producers = list()
consumers = list()
running = True
buf_size = len(buf)

def produce():
    global producer_idx, counter, buf
    while running:
        with s:
            if counter == buf_size:  # full
                continue
            buf[producer_idx] = "x"
            producer_idx = (producer_idx + 1) % buf_size
            print("{} <= produced 'x' at index='{}'".format(buf, producer_idx))
            labelBuffer.config(text="{} => consumed '{}' at index='{}'".format(buf, buf[consumer_idx], consumer_idx))
            counter += 1
        sleep(1)

def consume():
    global consumer_idx, counter, buf
    while running:
        with s:
            if counter == 0:  # empty
                continue
            buf[consumer_idx] = " "
            consumer_idx = (consumer_idx + 1) % buf_size
            print("{} => consumed '{}' at index='{}'".format(buf, buf[consumer_idx], consumer_idx))
            counter -= 1
        sleep(1)
 
def createProducer(quantity):
    for i in range(0,quantity):
        producer = Thread(target=produce)
        producer.start()
        producers.append(producer)

def createConsumers(quantity):
    for i in range(0, quantity):
        consumer = Thread(target=consume)
        consumer.start()
        consumers.append(consumer)

def stopSimulation():
    global running
    running = False
    ventana.destroy()


ventana.protocol("WM_DELETE_WINDOW", stopSimulation)

ventana.mainloop()



