# Intergalactic

Yet another P2P blockchain.

> Intergalactic, planetary, planetary, intergalactic  
> Another dimension, another dimension

[https://www.youtube.com/watch?v=qORYO0atB6g](https://www.youtube.com/watch?v=qORYO0atB6g)

## Requirements

### Virtualenv

Check your Python version (we recommend to use Python 3.7)

```
$ python3 --version
```

Make a virtualenv and activate it

```
$ python3 -m venv .
$ source bin/activate
```

### Python packages

Install Python packages

```
$ pip3 install -r requirements.txt
$ pip3 install -e .
```

## Usage

Run the `intergalactic` blockchain

```
$ intergalactic run
```

## Runing a peer-to-peer simulation netwerk

Bring the netwerk up

```
$ docker-compose up
Starting intergalactic_node1_1 ... done
Starting intergalactic_node2_1 ... done
Starting intergalactic_node3_1 ... done
Starting intergalactic_node4_1 ... done
Starting intergalactic_node5_1 ... done
Starting intergalactic_node6_1 ... done
```

Now start interacting with one of the nodes, e.g.:

```
$ curl -X POST http://localhost:8001/mine_block 
{
  "block": {
    "index": 1,
    "previous_hash": "8bc2694bfa070ab3e94bf6f8e0703f3505e99b67efe4b9e750c0e79a6b7413c1",
    "timestamp": 1545335749075,
    "hash": "55105c1bbe19afb436c075b72edd0ce5a8dbec83f5216d716c0cd3374bd1d713"
  }
}
```
