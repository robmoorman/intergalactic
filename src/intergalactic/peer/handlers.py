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

import asyncio
import json

from sanic import Sanic

from intergalactic import settings
from intergalactic.blockchain.block import Block
from intergalactic.blockchain.blockchain import blockchain
from intergalactic.blockchain.transaction import Transaction
from intergalactic.peer.manager import manager
from intergalactic.peer.publisher import broadcast
from intergalactic.node import node
from intergalactic.server import server
from intergalactic.types import MessageType
from intergalactic.utils import logging

logger = logging.get_logger(__name__)


async def peer_to_peer_handler(request, ws):
    from intergalactic.peer.subscriber import init_peer_connection

    try:
        await init_peer_connection(ws, trigger_initial_message=False)
    except:
        manager.remove_socket(ws)

    while True:
        msg = await ws.recv()
        await message_handler(ws, msg)


async def message_handler(ws, msg):
    msg_dict = json.loads(msg)
    msg_type = msg_dict["type"]

    logger.info(f"Received message: {msg_type}")

    handler = {
        MessageType.PING.value: handle_ping,
        MessageType.PONG.value: handle_pong,
        MessageType.NOTIFY_NEW_PEERS.value: handle_notify_new_peers,
        MessageType.NOTIFY_NEW_BLOCKS.value: handle_notify_new_blocks,
        MessageType.NOTIFY_NEW_TRANSACTION.value: handle_notify_new_transaction,
        MessageType.QUERY_CONNECTED_PEERS.value: handle_query_connected_peers,
        MessageType.QUERY_LATEST_BLOCK.value: handle_query_latest_block,
        MessageType.QUERY_ALL_BLOCKS.value: handle_query_all_blocks
    }.get(msg_type, None)

    if handler:
        await handler(ws, msg_dict)
    else:
        logger.error(f"Unknown message type {msg_type}")


async def handle_ping(ws, data):
    await ws.send(json.dumps({
        "type": MessageType.PONG.value,
        "data": {
            "nid": node.nid,
            "block_height": blockchain.get_block_height()
        }
    }))


async def handle_pong(ws, data):
    logger.info(f"Received pong {data}")

    nid = data["data"]["nid"]
    block_height = data["data"]["block_height"]

    if blockchain.get_block_height() < block_height:
        logger.info("Connected peer seems to have a longer blockchain")

        await ws.send(json.dumps({
            "type": MessageType.QUERY_LATEST_BLOCK.value
        }))

    await ws.send(json.dumps({
        "type": MessageType.QUERY_CONNECTED_PEERS.value
    }))


async def handle_notify_new_peers(ws, data):
    from intergalactic.peer.subscriber import subscribe_to_peer

    parent_peers = data["data"]
    current_peers = manager.get_peers()
    new_peers = [x for x in parent_peers if x not in current_peers]

    if len(new_peers):
        logger.info(f"Discovered new peers {new_peers}")

        for peer in new_peers:
            loop = asyncio.get_event_loop()
            loop.create_task(subscribe_to_peer(peer))
    else:
        logger.info("Parent peers already discovered")


async def handle_notify_new_blocks(ws, data):
    blocks = data["data"]
    latest_received_block = Block.from_dict(blocks[-1])
    latest_known_block = blockchain.get_latest_block()

    logger.info(f"Received blocks {blocks}")

    if latest_received_block.index > latest_known_block.index:
        if latest_received_block.previous_hash == latest_known_block.hash:
            logger.info(f"Add block {latest_received_block.hash} to blockchain")

            blockchain.add_block(latest_received_block)

            await broadcast({
                "type": MessageType.NOTIFY_NEW_BLOCKS.value,
                "data": [latest_received_block.to_dict()]
            })
        elif len(blocks) == 1:
            logger.info("Blockchain seems to be out-of-date, we will ask other"
                        " nodes in the network for their blockchains")
            await broadcast({
                "type": MessageType.QUERY_ALL_BLOCKS.value,
                "data": {
                    "nid": node.nid,
                    "block_height": blockchain.get_block_height()
                }
            })
        else:
            logger.info("Replace blockchain with received blocks")
            blockchain.replace_blocks([Block.from_dict(x) for x in blocks])
    else:
        logger.info("Received block is no longer than current latest block, no"
                    " further action required")


async def handle_notify_new_transaction(ws, data):
    transaction = Transaction.from_dict(data["data"])

    verified = blockchain.verify_transaction_signature(
        transaction.sender, transaction, transaction.signature)

    if verified:
        logger.info(f"Received transaction {transaction.hash}")
        blockchain.add_transaction(transaction)
    else:
        logger.warning(f"Received invalid transaction {transaction.hash}")


async def handle_query_connected_peers(ws, data):
    peers = manager.get_peers()

    await ws.send(json.dumps({
        "type": MessageType.NOTIFY_NEW_PEERS.value,
        "data": [str(x) for x in peers]
    }))


async def handle_query_latest_block(ws, data):
    block = blockchain.get_latest_block()

    await ws.send(json.dumps({
        "type": MessageType.NOTIFY_NEW_BLOCKS.value,
        "data": [block.to_dict()]
    }))

async def handle_query_all_blocks(ws, data):
    peer_nid = data["data"]["nid"]

    # Skip checking our own block height
    if node.nid != peer_nid:
        peer_block_height = data["data"]["block_height"]
        node_block_height = blockchain.get_block_height()

        if node_block_height > peer_block_height:
            blocks = blockchain.get_blocks()

            await ws.send(json.dumps({
                "type": MessageType.NOTIFY_NEW_BLOCKS.value,
                "data": [x.to_dict() for x in blocks]
            }))
