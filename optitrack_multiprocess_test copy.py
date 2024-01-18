from multiprocessing import Process, Queue, Event
from queue import Empty
from optitrack import OptitrackProcess, RealTimePlot3D
import time

class PrintProcess(Process):
    def __init__(self, optitrack_queue, frequency, stop_event):
        super(PrintProcess, self).__init__()
        self.optitrack_queue = optitrack_queue
        self.frequency = frequency
        self.dt = 1/self.frequency
        self.stop_event = stop_event
    def run(self):
        while not self.stop_event.is_set():
            try:
                while not self.optitrack_queue.empty():
                    # Retrieve data from the optitrack_queue
                    data = self.optitrack_queue.get()
                    id,(x,y,z),(roll,pitch,yall),data_time = data
                    #data = [id,(x,y,z),(roll,pitch,yall),data_time]
                    if id == 1 or id == 2 or id == 3 or id == 4:
                        print(data, time.time() - data_time)
                time.sleep(self.dt)
                # print(z)
            except Empty:
                pass  # Ignore empty queue and check for the stop event
                
    def stop(self):
        self.stop_event.set() 


if __name__ == "__main__":
    #if setup loopback in motive 3.0.1 
    client_address = "127.0.0.1"
    optitrack_server_address = "127.0.0.1"
    
    #if setup using ip in motive 3.0.1
    # client_address = "192.168.1.10"
    # optitrack_server_address = "192.168.1.71"
    
    #if setup using ethernet cable and ip in motive 3.0.1
    # client_address = "169.254.75.254"
    # optitrack_server_address = "169.254.75.253"
    
    print(client_address,optitrack_server_address)
    robot_id = [1,2,3,4] #target streaming rigidbody ids (lookup in motive app)
    frequency = 120
    optitrack_queue = Queue(maxsize=len(robot_id)) #set maxsize to clean Queue (Queue was FIFO just clean it to reduce the delay time)
    
    stop_print = Event()
    stop_opti = Event()
    stop_plot = Event()
    
    #OptitrackProcess print the data from natnet client if show = True
    optitrack_process  = OptitrackProcess(client_address, optitrack_server_address, frequency, robot_id, show=False, optitrack_queue=optitrack_queue, stop_event= stop_opti)
    
    print_process = PrintProcess(optitrack_queue, frequency, stop_print)
    # plot_process = RealTimePlot3D(optitrack_queue, frequency, stop_plot)  #not available now
    
    try:
        optitrack_process.start()
        # plot_process.start()
        print_process.start()
        # Do other main thread tasks if needed
        while True:
            # Add your main thread tasks here
            pass

    except KeyboardInterrupt:
        print("Keyboard interrupt detected in the main thread. Stopping all process.")
        optitrack_process.stop()
        print_process.stop()
        # plot_process.stop()
    finally:
        optitrack_process.kill()
        print_process.kill()
        # plot_process.kill()
