from threading import Thread
from queue import Queue, Empty
from optitrack import OptitrackThread
import time

class PrintThread(Thread):
    def __init__(self, optitrack_queue, frequency):
        super(PrintThread, self).__init__()
        self.optitrack_queue = optitrack_queue
        self.is_working = False
        self.frequency = frequency
        
    def run(self):
        self.is_working = True
        while self.is_working:
            try:
                # Retrieve data from the optitrack_queue
                data = self.optitrack_queue.get(timeout=(1/(self.frequency)))  # Use timeout to periodically check for the stop event
                print("optitrack_rigidboy_list:", data)
            except Empty:
                pass  # Ignore empty queue and check for the stop event
                
    def stop(self):
        self.is_working = False  
            

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
    
    robot_ids = [1,2,3,4]  #target streaming rigidbody ids (lookup in motive app)
    frequency = 60 #streaming frequency
    
    optitrack_queue = Queue()
    
    optitrack_thread = OptitrackThread(client_address, optitrack_server_address, frequency, robot_ids, show=True, optitrack_queue=optitrack_queue)
    print_thread = PrintThread(optitrack_queue, frequency)
    try:
        optitrack_thread.start()
        print_thread.start()
        # Do other main thread tasks if needed
        while True:
            pass
            # Add your main thread tasks here

    except KeyboardInterrupt:
        print("Keyboard interrupt detected in the main thread. Stopping the Optitrack streaming thread.")
        optitrack_thread.stop()
        print_thread.stop()
    finally:
        optitrack_thread.join()
        print_thread.join()