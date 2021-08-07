import hashlib
from textwrap import dedent
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request



class Blockchain(object):





	def __init__(self):
		self.chain = []
		self.current_transactions = []
		# @dev Creates genesis block
		self.new_block(previous_hash=1, proof=100)

	def new_block(self, proof, previous_hash = None):
		# creates new block in the BLockchain
		'''
		:param proof: <int> The proof given by the Proof of Work Algorithm
		:param previous_hash: <str> Hash of previous block
		'''

		block = {
			'index':len(self.chain) +1,
			'timestamp':time(),
			'transaction':self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
		}

		self.current_transactions = []

		self/chain.append(block)
		return block
		

	def new_transaction(self, sender, recipient, amount):
		# add a new transaction to the chain(as per creation)
		'''
		@dev Creates a new transaction to g o into the next minted block
		: param sender: <str> Address of the Sender
		: param recipient: <str> Address of the recipient(reciever)
		: param amount: <str> Amount to be transferred
		: return: <int> the index of the vblock that will hold this transaction
		'''

		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount,
			})

		return self.last_block['index'] +1

	@property
	def last_block(self):
		return self.chain[-1]

	@staticmethod
	def hash(block):
		# hashes the Block, Block as in the block of timed transactions for 
		# continued encryption

		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()
		
	def proof_of_work(self, last_proof):

		proof= 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1


			return proof

	@staticmethod
	def valid_proof(last_proof, proof):
		guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"




# @dev Block must contain/is a set of index, timestamp
#      (in unix time) and list of transactions and the hash
# 		of the previous bloc
app = Flask(__name__)
node_identifier = str(uuid()).replace('-','')

blockchain  = Blockchain()


@app.route('/mine', method=['GET'])
def mine():
	last_block = blockchain.last_block
	last_proof = last_block['proof']
	proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200 

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that the required fields are in the POST'd data
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
    	return 'Missing values',400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to the Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

    if __name__ == '__main__':
    	app.run(host='0.0.0.0',port:5000)