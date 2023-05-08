from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread, Semaphore


s = Semaphore(1)
buf = []
producer_idx = 0
consumer_idx = 0
counter = 0
producers = list()
consumers = list()
running = True
buf_size = len(buf)

"""
    The class implements the "Producers and Consumers" problem using semaphores. 
    There is a shared region called buffer, which can store a limited number of 
    elements. There are several producers that produce elements and place them 
    in the buffer, and there are several consumers that consume elements from the buffer.
    
    Author:
        Catalina Fajardo    tania.fajardo01@uptc.edu.co
        Esteban Rincon      esteban.rincon@uptc.edu.co
        Gina Castillo       gina.castillo01@uptc.edu.co
        Zulma Samaca        zulma.samaca@uptc.edu.co
"""
class Semaphore:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry('800x500')
        self.ventana.title('Productores y Consumidores con semáforos')

        self.labelTitle = tk.Label(self.ventana, text='Productores y Consumidores con semáforos')
        self.labelNumberConsumer = ttk.Label(self.ventana, text='N° Consumidores')
        self.labelNumberProductors = ttk.Label(self.ventana, text='N° Productores')
        self.labelSizeBuffer = ttk.Label(self.ventana, text='Tamaño Buffer')
        self.labelBuffer = ttk.Label(self.ventana, text='Buffer')

        self.entryProductos = ttk.Entry(self.ventana)
        self.entryConsumers = ttk.Entry(self.ventana)
        self.entrySizeBuffer = ttk.Entry(self.ventana)

    

        self.buttonStart = ttk.Button(self.ventana, text='Iniciar', command=self.startSimulation)
        self.buttonStop = ttk.Button(self.ventana, text='Detener', command=self.stopSimulation)

        self.canvas = tk.Canvas(master=self.ventana, width=700, height=100)

        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)
        self.ventana.rowconfigure(3, weight=1)
        self.ventana.rowconfigure(4, weight=1)
        self.ventana.rowconfigure(5, weight=1)
        self.ventana.rowconfigure(6, weight=1)
        self.ventana.rowconfigure(7, weight=1)
        self.ventana.rowconfigure(8, weight=1)
        self.ventana.rowconfigure(9, weight=1)
        self.ventana.columnconfigure(2, weight=1)
        self.ventana.columnconfigure(3, weight=1)
        self.ventana.columnconfigure(3, weight=1)
        self.ventana.columnconfigure(4, weight=1)
        self.ventana.columnconfigure(5, weight=1)
        self.ventana.columnconfigure(6, weight=1)

        self.labelTitle.grid(row=0, column=0, columnspan=7)
        self.labelNumberProductors.grid(row=1, column=0)
        self.labelNumberConsumer.grid(row=1, column=2)
        self.labelSizeBuffer.grid(row=1, column=4)
        self.entryProductos.grid(row=1, column=1)
        self.entryConsumers.grid(row=1, column=3)
        self.entrySizeBuffer.grid(row=1, column=5)
        self.buttonStart.grid(row=1, column=6)
        self.buttonStop.grid(row=2, column=6)
        self.labelBuffer.grid(row=2, column=0, columnspan=7, rowspan=7)
        


    def startSimulation(self):
        global running, producer_idx, consumer_idx, counter, buf, buf_size
        running = True
        producer_idx = 0
        consumer_idx = 0
        counter = 0
        buf_size = int(self.entrySizeBuffer.get())
        buf =[" "] * buf_size
        numberConsumers = int(self.entryConsumers.get())
        numberProductors = int(self.entryProductos.get())
        self.createConsumers(numberConsumers)
        self.createProducer(numberProductors)

    def produce(self):
        global producer_idx, counter, buf
        while running:
            with s:
                if counter == buf_size:  # full
                    continue
                buf[producer_idx] = "x"
                producer_idx = (producer_idx + 1) % buf_size
                print("{} <= produced 'x' at index='{}'".format(buf, producer_idx))
                self.labelBuffer.config(text="{} => consumed '{}' at index='{}'".format(buf, buf[consumer_idx], consumer_idx))
                counter += 1
            sleep(1)

    def consume(self):
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
 
    def createProducer(self, quantity):
        for i in range(0,quantity):
            producer = Thread(target=self.produce)
            producer.start()
            producers.append(producer)

    def createConsumers(self, quantity):
        for i in range(0, quantity):
            consumer = Thread(target=self.consume)
            consumer.start()
            consumers.append(consumer)

    def stopSimulation(self):
        global running, producers, consumers
        producers = []
        consumers = []
        running = False


    def closeSimulation(self):
        global running
        running = False
        self.ventana.destroy()

view = Semaphore()
view.ventana.protocol("WM_DELETE_WINDOW", view.closeSimulation)
view.ventana.mainloop()