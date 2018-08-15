from uuid import uuid4

from flask import Flask, jsonify

from blockchain import Blockchain

app = Flask(__name__)

# generate a globally unique node id
node_identifier = str(uuid4()).replace('-','')

# instantiate the blockchain

blockchain = Blockchain()



@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block"


@app.route('transactions/new', methods=['POST'])
def new_transation():
    return "We'll add a new transaction"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)