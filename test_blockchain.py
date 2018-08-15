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

    # def test_new_transaction(self):
    #     self.fail()
    #
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