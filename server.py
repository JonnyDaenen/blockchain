from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)

# generate a globally unique node id
node_identifier = str(uuid4()).replace('-','')

# instantiate the blockchain

blockchain = Blockchain()



@app.route('/mine', methods=['GET'])
def mine():
    # find the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # create a new coin (sender=0)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # create a new block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # create response
    response = {
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transation():
    """
    Example payload:
    {
     "sender": "my address",
     "recipient": "someone else's address",
     "amount": 5
    }
    :return: http status code and confirmation message
    """
    # extract values from the request
    values = request.get_json()

    # check that all required fields are present
    required_fields = ["sender", "recipient", "amount"]
    if not values or not all(k in values for k in required_fields):
        return 'Missing values', 400

    # add transaction
    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )

    # return confirmation message
    # and creation confirmation (201)

    response = {
        'message': f'Transation will be added to block {index}'
    }
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)