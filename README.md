# Natnet_Python
 Python Natnet Client for retrieving Optitrack data from Motive 3.0.1.
 It's only available for rigidbody now.

# Setup
In Motive System:
* Turn on the streaming setting in Motive system
* Create the **rigidbody** in motive and setup streaming id

In the script **optitrack_test.py**, **optitrack_multiprocess_test.py** and **optitrack_thread_test.py**:
* Edit the **client_address** and the **optitrack_server_address** in the code. 
* Edit the **robot_ids**, which is a list of streaming ids.
* Edit the **frequency**.
* Run the script:

    ```
    $ python optitrack_test.py
    ```
    or
    ```
    $ python optitrack_multiprocess_test.py
    ```
    or
    ```
    $ python optitrack_thread_test.py
    ```

# Note 
It is now available for Linux or Windows. For other system, please modify the line from 280 to 284 of the **NatNetClient.py**

```
try:
    if platform == "linux" or platform == "linux2":
        result.bind((self.multicast_address, port))
    elif platform == "win32":
        result.bind((self.local_ip_address, port))
```