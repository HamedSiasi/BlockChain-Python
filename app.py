# Hamed Siasi
# Create a simple decentralized BlockChain Network.

import requests
from uuid import uuid4
from flask import Flask, jsonify, url_for, request
from blockchain import BlockChainClass


app = Flask(__name__)             #We are creating an object of Flask class which will be a WSGI application.
blockchain = BlockChainClass()

# Unique address for current node 
# This address will be used when we have multiple nodes in blockchain network.
node_address = uuid4().hex  # Unique address for current node





#
# (1) --- create_transaction ---
# The first method will be used to process the new transaction 
# It will accept send, recipient and amount information in payload
# curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/create-transaction -d "{\"sender\": \"addr1\", \"recipient\": \"addr2\", \"amount\": 3}"
#
@app.route('/create-transaction', methods=['POST'])
def create_transaction():
	print("hello")
	"""
    Input Payload:
    {
        "sender": "address_1"
        "recipient": "address_2",
        "amount": 3
    }
    """
	transaction_data = request.get_json()     # Accepting Payload from user in JSON content type
	print transaction_data
	index = blockchain.create_new_transaction(**transaction_data)
	response = {
        'message': 'Transaction has been submitted successfully',
        'block_index': index
    }
	return jsonify(response), 201
    






#
# (2) --- mine ---
# The second method will be used to mine a new block and some reward money will be awarded to current node/server.
# curl "http://127.0.0.1:5000/mine"
#
@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_address)
    response = {
        'message': 'Successfully Mined the new Block',
        'block_data': block
    }
    return jsonify(response)








#
# (3) --- Get Full Chain ---
# The third method will be used to get the full chain on this node
# curl "http://127.0.0.1:5000/chain"
#
@app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.get_serialized_chain
    }
    return jsonify(response)









# (4) --- Let's make it decentralized,,, Register a node ---
# This method will register a node to our blockchain node set/list.
"""
In a decentralized network, all nodes/servers have the copy of all transactions/chain etc. 
If someone made any changes in any node(i.e. new transaction or mine a new block), 
we have to somehow inform other nodes and make them sync their chain with the updated data.

So whenever we create a new node in Blockchain network
we have to send our node's address to all other nodes available in the network 
so that they can register our node and in future, all node can sync with each other.

curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/register-node -d "{\"address\": \"http://127.0.0.1:5001\"}"

"""
@app.route('/register-node', methods=['POST'])
def register_node():
    node_data = request.get_json()
    blockchain.create_node(node_data.get('address'))
    response = {
        'message': 'New node has been added',
        'node_count': len(blockchain.nodes),
        'nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201











#
# (5)
# most interesting and important part of Blockchain Network called Consensus.
# This func will sync all nodes with the correct chain
# The longest chain is a valid chain and if
# There is more than one chain of the same length I would consider calling node's chain is correct.
#
#
@app.route('/sync-chain', methods=['GET'])
def consensus():

	def get_neighbour_chains():
		neighbour_chains = []
		for node_address in blockchain.nodes:
			print node_address
			resp = requests.get(node_address + url_for('get_full_chain')).json()
			chain = resp['chain']
			neighbour_chains.append(chain)
		return neighbour_chains

	neighbour_chains = get_neighbour_chains()
	if not neighbour_chains:
		return jsonify({'message': 'No neighbour chain is available'})

	longest_chain = max(neighbour_chains, key=len)  # Get the longest chain

	if len(blockchain.chain) >= len(longest_chain):  # If our chain is longest, then do nothing
		response = {
			'message': 'Chain is already up to date',
			'chain': blockchain.get_serialized_chain
		}
	else:  # If our chain isn't longest, then we store the longest chain
		blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
		response = {
			'message': 'Chain was replaced',
			'chain': blockchain.get_serialized_chain
		}

	return jsonify(response)










if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()

    # run the application server
    app.run(host=args.host, port=args.port, debug=True) 