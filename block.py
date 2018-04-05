
import time
import hashlib


class BlockClass(object):
    
    
    # Block(record) Constructor Method
    def __init__(self, index, proof, previous_hash, transactions):
        self.index = index                      # (1) index of the block in blockchain
        self.proof = proof                      # (2) number which will be generated during mining, a block will be created using proof
        self.previous_hash = previous_hash      # (3) 
        self.transactions = transactions        # (4) list
        self.timestamp = time.time()            # (5) 
		#        {
		#    		"index": 2,
		#    		"proof": 14,
		#    		"previous_hash": "8fb156e516b52afffb5860b5e3a076b0513c0d2d4489a9c4675c98e7e4a48a0d",
		#    		"transactions": [
		#        		{'sender': 'address_x', 'recipient': 'address_y', 'amount': 1}
		#    		],
		#    		"timestamp": 1514822766.046704
		#		}


    @property
    def get_block_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.proof, self.previous_hash, self.transactions, self.timestamp)
        #print("block_string: %s") %block_string
        return hashlib.sha256(block_string.encode()).hexdigest()


    # Should return a printable representation of the object.
    def __repr__(self):
        return "\n  index:{}\n  proof:{}\n  previous_hash:{}\n  transactions:{}\n  timestamp:{}\n\n".format(
        	self.index,
        	self.proof,
        	self.previous_hash,
        	self.transactions, 
        	self.timestamp)