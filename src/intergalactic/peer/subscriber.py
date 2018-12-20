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

import json
import websockets

from intergalactic import settings
from intergalactic.peer.handlers import message_handler
from intergalactic.peer.manager import manager
from intergalactic.types import MessageType
from intergalactic.utils import logging

logger = logging.get_logger(__name__)


async def subscribe_to_peer(url):
    ws = await websockets.connect(url)

    await init_peer_connection(ws, url=url)


async def init_peer_connection(ws, url=None, trigger_initial_message=True):
    if url is not None:
        manager.add_peer(url)

    manager.add_socket(ws)

    if trigger_initial_message:
        await ws.send(json.dumps({
            "type": MessageType.PING.value
        }))

    while True:
        msg = await ws.recv()
        await message_handler(ws, msg)
