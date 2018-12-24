# Copyright 2018 Rob Moorman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from intergalactic.blockchain.transaction import Transaction


class Block:
    def __init__(self, index, previous_hash, timestamp, hash, merkle_root, proof, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = hash
        self.merkle_root = merkle_root
        self.proof = proof
        self.transactions = transactions

    @staticmethod
    def from_dict(data):
        return Block(
            data["index"],
            data["previous_hash"],
            data["timestamp"],
            data["hash"],
            data["merkle_root"],
            data["proof"],
            [Transaction.from_dict(x) for x in data["transactions"]]
        )

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "merkle_root": self.merkle_root,
            "proof": self.proof,
            "transactions": [x.to_dict() for x in self.transactions]
        }
