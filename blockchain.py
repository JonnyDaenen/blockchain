import hashlib
import json
import requests

from time import time


class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.nodes = set()

        # Create the genesis block for this chain
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create new block in the blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of precious block
        :return: <dict> New block
        """

        # construct the block
        block = {
            'index': len(self.chain) + 1,  # QUESTION: why not calculate using last_block?
            'timestamp': time(),  # epoch time
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),  # fallback to manual hash creation
        }

        # empty the transactions
        self.current_transactions = []

        # append the block to the chain
        self.chain.append(block)

        # return the block
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        # look op the index of the previous block
        # and calculate current index
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: <dict> Block
        :return: <str> Hash of the block
        """

        # serialize dictionary to a string
        # ! we make sure it is ordered to keep consistency!
        # note: byte encoding defaults to UTF-8
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]


    def proof_of_work(self, last_proof):
        """
        Simple proof algorithm:
            - let p be the previous proof and p' be the new proof
            - find a number p' such that hash(pp') contains 4 leading zeroes

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates proof: does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if correct, False if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        # skip first block
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n" + "-"*10 + "\n")

            # validate hash
            if block['previous_hash'] != self.hash(last_block):
                return False

            # validate proof of work
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):
        """
        This is the consensus algorithm; it resolves conflicts
        by replacing our chain with the longest one in the network

        :return: <bool> True if our chain was replaces, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # only look for longer changes
        max_length = len(self.chain)

        # get all the chains
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # QUESTION: what if we have multiple chains of the same length?
                # check length
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain


        if new_chain:
            self.chain = new_chain
            return True

        return False

