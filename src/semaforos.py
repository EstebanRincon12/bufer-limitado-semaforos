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
        # Initialize the attributes of the class
        self.ventana = tk.Tk() # Create a new window
        self.ventana.geometry('800x500') # Set the window size
        self.ventana.title('Productores y Consumidores con semáforos') # Set the window title

        # Create labels for the GUI
        self.labelTitle = tk.Label(self.ventana, text='Productores y Consumidores con semáforos')
        self.labelNumberConsumer = ttk.Label(self.ventana, text='N° Consumidores')
        self.labelNumberProductors = ttk.Label(self.ventana, text='N° Productores')
        self.labelSizeBuffer = ttk.Label(self.ventana, text='Tamaño Buffer')
        self.labelBuffer = ttk.Label(self.ventana, text='Buffer')

        # Create entries for the GUI
        self.entryProductos = ttk.Entry(self.ventana)
        self.entryConsumers = ttk.Entry(self.ventana)
        self.entrySizeBuffer = ttk.Entry(self.ventana)

    
        # Create buttons for the GUI
        self.buttonStart = ttk.Button(self.ventana, text='Iniciar', command=self.startSimulation)
        self.buttonStop = ttk.Button(self.ventana, text='Detener', command=self.stopSimulation)
        # Create a canvas for the GUI
        self.canvas = tk.Canvas(master=self.ventana, width=700, height=100)
        # Configure the rows and columns of the GUI layout
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
        # Add the GUI elements to the window
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
        """This method sets up and starts the simulation of a producer-consumer problem with a buffer of a given size.
            It initializes some global variables, such as running, producer_idx, consumer_idx, counter, buf, and buf_size.
        """
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
        """This method represents the producer behavior of the producer-consumer problem. 
        It tries to add an item to the shared buffer until the buffer is full. 
        The producer_idx and counter variables are used to keep track of the position 
        where the item is added in the buffer and the number of items in the buffer, respectively.
        """
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
        """represents the behavior of a consumer in the simulation. 
        It is executed in a loop while the simulation is running. 
        Inside the loop, the method acquires the semaphore s and checks if there is any item to consume in the buffer.    
        """
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
        """This method creates a specified number of producer threads by calling the produce method that adds items to the buffer. 
            Each producer thread is started and added to the producers list.
        """
        for i in range(0,quantity):
            producer = Thread(target=self.produce)
            producer.start()
            producers.append(producer)
        
    def createConsumers(self, quantity):
        """This method creates a specified number of consumer threads and starts them. Each consumer thread runs the self.consume() method, which consumes an item from the buffer if it is not empty. 
            The quantity parameter specifies the number of consumers to create. 
            The created consumers are added to a list called consumers.
        """
        for i in range(0, quantity):
            consumer = Thread(target=self.consume)
            consumer.start()
            consumers.append(consumer)
        
    def stopSimulation(self):
        """The stopSimulation method stops the simulation by setting the running flag to False and clearing the producers and consumers lists. 
            This effectively stops all threads that were created during the simulation.
        """
        global running, producers, consumers
        producers = []
        consumers = []
        running = False

        
    def closeSimulation(self):
        """This method closes the simulation by setting the running flag to False and destroying the main window of the simulation (self.ventana).
        """
        global running
        running = False
        self.ventana.destroy()

view = Semaphore()
view.ventana.protocol("WM_DELETE_WINDOW", view.closeSimulation)
view.ventana.mainloop()