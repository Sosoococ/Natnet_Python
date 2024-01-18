import time
from threading import Thread

# from NatNetClient import NatNetClient
# from util import quaternion_to_euler


from optitrack.NatNetClient import NatNetClient
from optitrack.util import quaternion_to_euler
from optitrack.optitrack_main import Optitrack



class OptitrackThread(Thread):
    def __init__(self, client_address="127.0.0.1", server_address="127.0.0.1", frequency=60, robot_ids=[1], show=False, optitrack_queue=None):
        super(OptitrackThread, self).__init__()
        self.optitrack = Optitrack(client_address, server_address, frequency, optitrack_queue)
        self.robot_id = robot_ids
        self.show = show

    def run(self):
        self.optitrack.start_streaming_attitude(self.robot_id, self.show) 
    
    def stop(self):
        self.optitrack.is_running = False
        self.optitrack.stop_streaming()
        

# if __name__ == "__main__":
#     client_address = "127.0.0.1"
#     optitrack_server_address = "127.0.0.1"
#     robot_id = 1  # target rigidbody number
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
