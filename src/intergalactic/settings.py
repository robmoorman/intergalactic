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

import os
from os import environ as env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

BLOCKCHAIN_DB_PATH = os.path.join(BASE_DIR, '.db')

BOOTSTRAP_PEERS = env.get("BOOTSTRAP_PEERS", "")

MAX_PEER_CONNECTIONS = env.get("MAX_PEER_CONNECTIONS", "8")

SERVER_HOST = env.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT = env.get("SERVER_PORT", "5001")
