
# BlockChain

# Block  =   contains transactions, timestamp, index, hash , ...
# 	Genesis Block = first Block
# 	Current Block = Last Block
# 	Orphan Block = Valid block which is not part of the main chain yet
#
# Mining  =   Method of creating new block
# 
# Proof Of Woork  =  is a data difficult to generate but easy to verify.
# 	will be used to create a block
# 
# Node  =  server
#
# Consensus  =  agreement, when we have more than one node in our blockchain network, to sunch nodes






import time
import hashlib
from block import BlockClass


class BlockChainClass(object):
    
    def __init__(self):                                      # blockChain(chain) Constructor Method
        self.chain = []                                      # Will hold all blocks
        self.current_node_transactions = []                  # Transactions which will be inserted 
        self.nodes = set()
        self.create_genesis_block()           


    def create_new_block(self, proof, previous_hash):
        new_block = BlockClass(
            index = len(self.chain),                         # index = last_index + 1 = length of the chain[]
            proof = proof,                                   # Should be passed by caller
            previous_hash = previous_hash,                   # Should be passed by caller
            transactions = self.current_node_transactions    # List of the transactions which are not part of any block on the node
        )
        self.current_node_transactions = []                  # Reset the transaction list
        self.chain.append(new_block)                         # Appending newly created block to the chain[]
        return new_block                                     # Returning newly created block object


    @property
    def get_serialized_chain(self):
        return [vars(block) for block in self.chain]

    def create_genesis_block(self):
	    self.create_new_block(proof=0, previous_hash=0)      # Genesis (first, special) block



    @staticmethod
    def is_valid_block(block, previous_block):
        if previous_block.index + 1 != block.index:
            return False
        elif previous_block.get_block_hash != block.previous_hash:
            return False
        elif not BlockChain.is_valid_proof(block.proof, previous_block.proof):
            return False
        elif block.timestamp <= previous_block.timestamp:
            return False
        return True



    def create_new_transaction(self, sender, recipient, amount):
        self.current_node_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })                                                    # When this block is mined, this list will be assigned to that block
        return self.get_last_block.index + 1                  # Returning new block's index where this transaction will be stored



    @staticmethod
    def is_valid_transaction():
        # Not Implemented
        pass


    @staticmethod
    def create_proof_of_work(previous_proof):
    	"""
    	This method is very important to keep blockchain safe from spamming.
    	This method will use an algorithm to generate a number that will be used to create a new mined block.
    	You can use your own algorithm and set a difficulty level so that people can't mine block easily.
    	Bitcoin uses the Hashcash proof of work system.

    	Generate "Proof Of Work"
    	A very simple `Proof of Work` Algorithm -
    	-> Find a number such that, Sum of the number and previous POW number is divisible by 7
    	"""
    	proof = previous_proof + 1
    	while (proof + previous_proof) % 7 != 0:
        	proof += 1
    	return proof



    @staticmethod
    def is_valid_proof(proof, previous_proof):
        return (proof + previous_proof) % 7 == 0
   
    @property
    def get_last_block(self):
        return self.chain[-1]                # Last method(get_last_block) is just a helper method to get the last(current block) 
                                             # A negative index accesses elements from the end of the list counting backwards.





    def is_valid_chain(self):
        previous_block = self.chain[0]
        current_index = 1
        while current_index < len(self.chain):
            block = self.chain[current_index]
            if not self.is_valid_block(block, previous_block):
                return False
            previous_block = block
            current_index += 1
        return True



    def mine_block(self, miner_address):
        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
        
        # --- miner rewarding ---
        #self.create_new_transaction(
        #    sender = "0",
        #    recipient = miner_address,
        #    amount = 1,
        #)
        
        last_block = self.get_last_block
        last_proof = last_block.proof
        proof = self.create_proof_of_work(last_proof)
        last_hash = last_block.get_block_hash
        block = self.create_new_block(proof, last_hash)
        return vars(block)  # Return a native Dict type object




    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def get_block_object_from_block_data(block_data):
        return BlockClass(
            block_data['index'],
            block_data['proof'],
            block_data['previous_hash'],
            block_data['transactions']
        )






if __name__ == "__main__":
    blockchain = BlockChainClass()
    #print(blockchain.chain)

    number_of_blocks_to_add = 3
    for i in range (1,number_of_blocks_to_add+1):
        blockchain.create_new_transaction(
            sender = "0",
            recipient = "address_x",
            amount = i,
        )
        last_block = blockchain.get_last_block
        last_proof = last_block.proof
        proof = blockchain.create_proof_of_work(last_proof)
        last_hash = last_block.get_block_hash
        block = blockchain.create_new_block(proof, last_hash)

    print(blockchain.chain)
 































