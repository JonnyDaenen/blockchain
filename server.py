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
    return "We'll mine a new block"


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