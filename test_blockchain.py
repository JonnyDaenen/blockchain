import unittest
from unittest import TestCase

from blockchain import Blockchain


class TestBlockchain(TestCase):

    def setUp(self):
        # runs for every test method
        self.blockchain = Blockchain()

    def test_blockchain_init(self):

        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(len(self.blockchain.nodes), 0)
        self.assertEqual(len(self.blockchain.current_transactions), 0)


    def test_new_block(self):
        self.assertEqual(len(self.blockchain.current_transactions), 0)
        self.blockchain.new_block(proof=1)
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(len(self.blockchain.current_transactions), 0)

    def test_new_transaction(self):
        self.assertEqual(len(self.blockchain.current_transactions), 0)

        # transactions are added
        self.blockchain.new_transaction("John", "Mary", 10)
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(len(self.blockchain.current_transactions), 1)

        self.blockchain.new_transaction("John", "Mary", 10)
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(len(self.blockchain.current_transactions), 2)

        self.blockchain.new_transaction("John", "Mary", 10)
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(len(self.blockchain.current_transactions), 3)

        # creating a block removes transactions
        self.blockchain.new_block(proof=1)
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(len(self.blockchain.current_transactions), 0)

        # transaction is present in the chain
        self.assertEqual(self.blockchain.chain[1]['transactions'][0]['sender'], "John")
        self.assertEqual(self.blockchain.chain[1]['transactions'][0]['recipient'], "Mary")
        self.assertEqual(self.blockchain.chain[1]['transactions'][0]['amount'], 10)

        expected = {
            'sender': "John",
            'recipient': "Mary",
            'amount': 10
        }
        self.assertDictEqual(self.blockchain.chain[1]['transactions'][0],expected)


    # def test_hash(self):
    #     self.fail()
    #
    # def test_last_block(self):
    #     self.fail()
    #
    # def test_proof_of_work(self):
    #     self.fail()
    #
    # def test_valid_proof(self):
    #     self.fail()
    #
    # def test_register_node(self):
    #     self.fail()
    #
    # def test_valid_chain(self):
    #     self.fail()
    #
    # def test_resolve_conflicts(self):
    #     self.fail()



if __name__ == '__main__':
    unittest.main()