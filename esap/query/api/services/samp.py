
# SAMP example
# 1) run this program
# 2) create a table in TOPCAT and hit the 'Transmit table to all applications using SAMP' button
import time
from astropy.samp import SAMPIntegratedClient
from astropy.table import Table

 # Instantiate the client and connect to the hub
client=SAMPIntegratedClient()
client.connect()

# Set up a receiver class
class Receiver(object):
    def __init__(self, client):
        self.client = client
        self.received = False
    def receive_call(self, private_key, sender_id, msg_id, mtype, params, extra):
        self.params = params
        self.received = True
        self.client.reply(msg_id, {"samp.status": "samp.ok", "samp.result": {}})
    def receive_notification(self, private_key, sender_id, mtype, params, extra):
        self.params = params
        self.received = True

# Instantiate the receiver
r = Receiver(client)

# Listen for any instructions to load a table
client.bind_receive_call("table.load.votable", r.receive_call)
client.bind_receive_notification("table.load.votable", r.receive_notification)

# We now run the loop to wait for the message in a try/finally block so that if
# the program is interrupted e.g. by control-C, the client terminates
# gracefully.

try:

    # We test every 0.1s to see if the hub has sent a message
    while True:
        time.sleep(0.1)
        if r.received:
            t = Table.read(r.params['url'])
            break

finally:

    client.disconnect()

# Print out table
print(t)