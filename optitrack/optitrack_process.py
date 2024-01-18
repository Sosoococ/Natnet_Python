
# from NatNetClient import NatNetClient
# from util import quaternion_to_euler
import time
from optitrack.NatNetClient import NatNetClient
from optitrack.util import quaternion_to_euler
from optitrack.optitrack_main import Optitrack
from multiprocessing import Process, Queue, Event


class OptitrackProcess(Process):
    def __init__(self, client_address="127.0.0.1", server_address="127.0.0.1", frequency=60, robot_ids=[1], show=False, optitrack_queue=None, stop_event=None):
        super(OptitrackProcess, self).__init__()
        self.optitrack_queue = optitrack_queue
        self.client_address = client_address
        self.server_address = server_address
        self.frequency = frequency
        self.robot_ids = robot_ids
        self.show = show
        self.stop_event = stop_event
        self.stop_stream = False
        
        

    def run(self):
        optitrack = Optitrack(self.client_address, self.server_address, self.frequency, self.optitrack_queue)
        try:
            while not self.stop_event.is_set():
                if self.stop_stream:
                    optitrack.is_running = False
                    optitrack.stop_streaming()
                    break  # Exit the loop when streaming is stopped
                optitrack.start_streaming_attitude_multi(self.robot_ids, self.show)
        finally:
            # Additional cleanup code if needed
            optitrack.is_running = False
            optitrack.stop_streaming()
          
        
    def stop(self):
        self.stop_stream = True
        self.stop_event.set()
        
        

# if __name__ == "__main__":
#     client_address = "127.0.0.1"
#     optitrack_server_address = "127.0.0.1"
#     robot_id = 1  # 你框的rigidbody
#     frequency = 60

#     optitrack_thread = OptitrackThread(client_address, optitrack_server_address, frequency, robot_id, show=True)

#     try:
#         optitrack_thread.start()

#         # Do other main thread tasks if needed
#         while True:
#             time.sleep(1)
#             # Add your main thread tasks here

#     except KeyboardInterrupt:
#         print("Keyboard interrupt detected in the main thread. Stopping the Optitrack streaming thread.")
#     finally:
#         optitrack_thread.join()
