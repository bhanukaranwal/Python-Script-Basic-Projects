import os
import hashlib
import time
import random
import json
from ecdsa import SigningKey, SECP256k1

# --- Utility Functions ---

def sha256(x):
    return hashlib.sha256(x.encode() if isinstance(x, str) else x).hexdigest()

def get_new_keypair():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk

def pubkey_to_address(vk):
    pk_bytes = vk.to_string()
    hashed = sha256(pk_bytes)
    # fake address: first 8 chars, hex
    return hashed[:8]

def sign_data(sk, data):
    h = sha256(data)
    sig = sk.sign(h.encode())
    return sig.hex()

def verify_data(vk, data, signature):
    try:
        h = sha256(data)
        return vk.verify(bytes.fromhex(signature), h.encode())
    except Exception:
        return False

# --- Wallet ---
class Wallet:
    def __init__(self):
        self.sk, self.vk = get_new_keypair()
        self.address = pubkey_to_address(self.vk)
        print(f"New wallet created: address {self.address}")

    def sign(self, data):
        return sign_data(self.sk, data)

    def as_pubkey(self):
        return self.vk.to_string().hex()

# --- Blockchain ---
# A minimal blockchain; not decentralized, proof-of-authority for demo

class Tx:
    def __init__(self, sender, receiver, amount, sender_pub, signature):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.sender_pub = sender_pub
        self.signature = signature
        self.timestamp = time.time()
        self.txid = sha256(f"{self.sender}{self.receiver}{self.amount}{self.timestamp}")

    def verify(self):
        vk_bytes = bytes.fromhex(self.sender_pub)
        vk = SigningKey.from_string(vk_bytes, curve=SECP256k1).get_verifying_key()
        data = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return verify_data(vk, data, self.signature)

    def to_dict(self):
        return self.__dict__

class Block:
    def __init__(self, prev_hash, tx_list, nonce=0):
        self.prev_hash = prev_hash
        self.tx_list = tx_list  # list of Tx
        self.nonce = nonce
        self.timestamp = time.time()
        self.hash = self.compute_hash()

    def compute_hash(self):
        txs_data = json.dumps([tx.to_dict() for tx in self.tx_list], sort_keys=True)
        return sha256(f"{self.prev_hash}{txs_data}{self.nonce}{self.timestamp}")

# --- Blockchain node ---
class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.create_genesis()

    def create_genesis(self):
        genesis = Block("0" * 64, [])
        self.chain.append(genesis)

    def add_tx(self, tx):
        # For demo: no signature enforcement in pool
        self.mempool.append(tx)

    def mine_block(self):
        prev_hash = self.chain[-1].hash
        txs = self.mempool[:]
        block = Block(prev_hash, txs, nonce=random.randint(0, 100000))
        self.chain.append(block)
        self.mempool = []

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.tx_list:
                if tx.receiver == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
        return balance

    def print_chain(self):
        print("--- Blockchain ---")
        for i, block in enumerate(self.chain):
            print(f"Block {i} | Hash: {block.hash[:10]}... | txs: {len(block.tx_list)}")
        print("------------------")

# --- Interactive Demo ---
def main():
    wallet1 = Wallet()
    wallet2 = Wallet()
    bc = SimpleBlockchain()

    # Give wallet1 some coins in genesis
    genesis_tx = Tx("SYSTEM", wallet1.address, 100, "", "")
    bc.chain[0].tx_list.append(genesis_tx)
    
    while True:
        print("\nMenu: 1) Send 2) Check Balance 3) Mine 4) Print Chain 5) Quit")
        cmd = input("Your choice: ").strip()
        if cmd == '1':
            to_addr = wallet2.address
            amt = float(input(f"Amount to send to {to_addr}: "))
            data = f"{wallet1.address}{to_addr}{amt}{time.time()}"
            sig = wallet1.sign(data)
            tx = Tx(wallet1.address, to_addr, amt, wallet1.as_pubkey(), sig)
            bc.add_tx(tx)
            print("Transaction created and added to mempool.")
        elif cmd == '2':
            a1 = bc.get_balance(wallet1.address)
            a2 = bc.get_balance(wallet2.address)
            print(f"Balance for wallet1 ({wallet1.address}): {a1}")
            print(f"Balance for wallet2 ({wallet2.address}): {a2}")
        elif cmd == '3':
            bc.mine_block()
            print("Block mined!")
        elif cmd == '4':
            bc.print_chain()
        elif cmd == '5':
            break
        else:
            print("Invalid.")

if __name__ == "__main__":
    try:
        from ecdsa import SigningKey
    except ImportError:
        print("Please install ecdsa: pip install ecdsa")
        exit()
    main()
