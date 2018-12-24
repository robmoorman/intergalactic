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

import hashlib

from intergalactic import settings


class ProofOfWork:
    def __init__(self, difficulty=settings.DIFFICULTY):
        self.difficulty = difficulty

    def get_proof(self, previous_hash: str, merkle_root: str) -> bool:
        proof = 0
        result = False
        while result is False:
            result = self.is_valid(previous_hash, proof, merkle_root)
            proof += 1
        return proof - 1

    def is_valid(self, previous_hash: str, proof: int, merkle_root: str) -> bool:
        value = (
            str(previous_hash)+str(proof)+str(merkle_root)).encode("utf-8")
        hashed_value = hashlib.sha256(value).hexdigest()
        result = hashed_value[:self.difficulty] == '0'*self.difficulty
        return result
