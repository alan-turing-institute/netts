import stanza
from stanza.server import CoreNLPClient

stanza.install_corenlp()

client = CoreNLPClient(port=8888)
client.start()

# Wait for server to start
client.ensure_alive()

# Get its PID
pid = client.server.pid
print(f"Process running on: {pid if pid else 'Cant find pid'}")


# client.stop()
client.stop()

# Make sure server has shut down
assert not client.server
