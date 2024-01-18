from multiprocessing import Process, Queue, Event
from queue import Empty
from optitrack import Optitrack
import time

if __name__ == "__main__":
    #if setup loopback in motive 3.0.1 
    client_address = "127.0.0.1"
    optitrack_server_address = "127.0.0.1"
    
    #if setup using ip in motive 3.0.1
    # client_address = "192.168.0.1"
    # optitrack_server_address = "192.168.0.2"
    
    #if setup using ethernet cable and ip in motive 3.0.1
    # client_address = "169.254.75.254"
    # optitrack_server_address = "169.254.75.253"
    
    robot_ids = [1,2,3,4]  #target streaming rigidbody ids (lookup in motive app)
    frequency = 60 #streaming frequency
    
    robo_pos = Optitrack(client_address, optitrack_server_address, frequency)
    try:
        robo_pos.start_streaming_attitude(robot_ids, show = True)  #print data if show = True
        
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping streaming.")
    finally:
        robo_pos.stop_streaming()