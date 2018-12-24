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

from intergalactic.blockchain.pow import ProofOfWork


class BlockchainValidator:
    def __init__(self):
        pass

    def validate(self, chain):
        sibling_block = chain[0]
        index = 1
        pow = ProofOfWork()

        while index < len(chain):
            block = chain[index]

            # Validate chain block order
            if block.previous_hash != sibling_block.hash:
                return False

            # Validate proof of work
            if not pow.is_valid(block.previous_hash, block.proof, block.merkle_root):
                return False

            sibling_block = block
            index += 1
        return True
