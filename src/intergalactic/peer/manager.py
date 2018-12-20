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

from intergalactic.utils import logging

logger = logging.get_logger(__name__)


class PeerManager:
    def __init__(self):
        self.peers = []
        self.sockets = []

    def add_peer(self, url):
        if not url in self.peers:
            logger.info(f"Add peer {url}")
            self.peers.append(url)

    def add_socket(self, ws):
        if not ws in self.sockets:
            logger.info(f"Add socket {ws}")
            self.sockets.append(ws)

    def remove_peer(self, url):
        logger.info(f"Remove peer {url}")
        self.peers.remove(ws)

    def remove_socket(self, ws):
        logger.info(f"Remove socket {ws}")
        self.sockets.remove(ws)

    def get_peers(self):
        return self.peers

    def get_sockets(self):
        return self.sockets


manager = PeerManager()
