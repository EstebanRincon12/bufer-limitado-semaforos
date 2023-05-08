from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread, Semaphore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

s = Semaphore(1)
buf = []
producer_idx = 0
consumer_idx = 0
counter = 0
producers = list()
consumers = list()
running = True
buf_size = len(buf)
buffer_values = []

class MySemaphore:
    """The class implements the "Producers and Consumers" problem using semaphores. 
    There is a shared region called buffer, which can store a limited number of 
    elements. There are several producers that produce elements and place them 
    in the buffer, and there are several consumers that consume elements from the buffer.
    
    Author:
        Catalina Fajardo    tania.fajardo01@uptc.edu.co
        Esteban Rincon      esteban.rincon@uptc.edu.co
        Gina Castillo       gina.castillo01@uptc.edu.co
        Zulma Samaca        zulma.samaca@uptc.edu.co
    """
    def __init__(self):
        """constructor of a class representing a window in a graphical user interface (GUI) 
        implemented with the Python tkinter library. This function initializes and configures 
        various elements of the window, including labels, inputs, buttons and canvas.
        """
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.geometry('800x500')
        self.window.configure(bg="")
        self.window.title('Productores y Consumidores con semáforos')

        # Create labels for the GUI
        self.labelTitle = tk.Label(self.window, text='Productores y Consumidores  (Semáforos)', font=("Roboto",20,'bold'), fg="#42843B", bg="white")
        self.labelNumberConsumer = ttk.Label(self.window, text='Cantidad de Consumidores',  font=("Roboto",12), background="white")
        self.labelNumberProductors = ttk.Label(self.window, text='Cantidad de Productores',  font=("Roboto",12) ,background="white")
        self.labelSizeBuffer = ttk.Label(self.window, text='Tamaño Buffer', font=("Roboto",12), background="white")
        self.labelBuffer = ttk.Label(self.window, text='Buffer', font=("Roboto",12), background="white")

        # Configure input validation to accept only numbers
        validate_cmd = (self.window.register(self.validate_numbers), '%P')

        # Create entries for the GUI
        self.entryProductos = ttk.Entry(self.window,font=("Roboto",12),validate="key", validatecommand=validate_cmd)
        self.entryConsumers = ttk.Entry(self.window,font=("Roboto",12),validate="key", validatecommand=validate_cmd)
        self.entrySizeBuffer = ttk.Entry(self.window,font=("Roboto",12),validate="key", validatecommand=validate_cmd)

        self.buttonStart = ttk.Button(self.window, text='Iniciar', command=self.startSimulation)
        self.buttonStop = ttk.Button(self.window, text='Detener', command=self.stopSimulation)
        # Create a canvas for the GUI
        self.canvas = tk.Canvas(master=self.window, width=700, height=100)
        # Configure the rows and columns of the GUI layout
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=1)
        self.window.rowconfigure(5, weight=1)
        self.window.rowconfigure(6, weight=1)
        self.window.rowconfigure(7, weight=1)
        self.window.rowconfigure(8, weight=1)
        self.window.rowconfigure(9, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=1)
        self.window.columnconfigure(5, weight=1)
        self.window.columnconfigure(6, weight=1)
       
        # Add the GUI elements to the window
        self.labelTitle.grid(row=0, column=0, columnspan=7)
        self.labelNumberProductors.grid(row=1, column=1)
        self.labelNumberConsumer.grid(row=2, column=1)
        self.labelSizeBuffer.grid(row=3, column=1)
        self.entryProductos.grid(row=1, column=2)
        self.entryConsumers.grid(row=2, column=2)
        self.entrySizeBuffer.grid(row=3, column=2)
        self.buttonStart.grid(row=4, column=2)
        self.buttonStop.grid(row=5, column=2)

        # #
        # self.frame = tk.Frame(self.window)
        # self.frame.grid(row=6, column=0, columnspan=5,sticky=tk.NSEW)
        # self.frame.grid_rowconfigure(0, weight=1)
        # self.frame.grid_columnconfigure(0, weight=1)
        # self.fig = plt.figure()
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        # self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # plt.xlabel('Tiempo')
        # plt.ylabel('Cantidad de productos en el buffer')

        self.labelBuffer.grid(row=7, column=0, columnspan=5, rowspan=4)

    def validate_numbers(self, value):
        """Validates whether a value is a positive integer

        Args:
            value (any): value which can be a number or a letter 

        Returns:
            boolean: If the value is a positive integer, it returns True, 
            which means that the input will be allowed. If the value is an empty string, 
            it also returns True, which means that an empty input will be allowed. 
            In any other case, it returns False, which means that the input will not be allowed.
        """
        if value.isdigit():
            return True
        elif value == "":
            return True
        else:
            return False


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

        buffer_values.append(numberProductors)


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
                self.labelBuffer.config(text="{} => produced '{}' at index='{}'".format(buf, buf[consumer_idx], consumer_idx))
                counter += 1
            sleep(3)

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
                self.labelBuffer.config(text="{} => consumed '{}' at index='{}'".format(buf, buf[consumer_idx], consumer_idx))
                counter -= 1
            sleep(3)
        
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
        """This method closes the simulation by setting the running flag to False and destroying the main window of the simulation (self.window).
        """
        global running
        running = False
        self.window.destroy()

view = MySemaphore()
view.window.protocol("WM_DELETE_WINDOW", view.closeSimulation)
view.window.mainloop()