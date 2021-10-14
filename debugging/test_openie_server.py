import netspy

client = netspy.CoreNLPClient(port=8888)
client.start()

# Wait for server to start
client.ensure_alive()

# Get its PID
pid = client.get_pid()
print(f"Process running on: {pid if pid else 'Cant find pid'}")


client.stop()

# Make sure server has shut down
assert not client.server
