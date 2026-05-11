# config.py

# 1. CORE PERSONNEL WALLET ADDRESSES
ADMIN_ADDR = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"
CEO_ADDR = "0xc2ABbFb05C6868Daf749F2ed037a66acC9e6fc07"

# 2. PUBLIC BLOCKCHAIN GATEWAY (Free & Reliable)
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com" 

# Your Deployed Contract Address
CONTRACT_ADDRESS = "0x29382A813A37b35bA9B3273aD8aD888e05944A0e"

# 3. SMART CONTRACT ABI
CONTRACT_ABI = [
	{"inputs": [],"stateMutability": "nonpayable","type": "constructor"},
	{"inputs": [{"internalType": "address","name": "_user","type": "address"}],"name": "approveRegistration","outputs": [],"stateMutability": "nonpayable","type": "function"},
	{"inputs": [{"internalType": "string","name": "_name","type": "string"}],"name": "issueMedication","outputs": [],"stateMutability": "nonpayable","type": "function"},
	{"inputs": [{"internalType": "uint256","name": "_orderId","type": "uint256"}],"name": "payAndReplenish","outputs": [],"stateMutability": "payable","type": "function"},
	{"inputs": [{"internalType": "string","name": "_name","type": "string"},{"internalType": "enum EcoChainProcurement.IllnessCategory","name": "_category","type": "uint8"},{"internalType": "uint256","name": "_initialStock","type": "uint256"},{"internalType": "uint256","name": "_threshold","type": "uint256"},{"internalType": "uint256","name": "_reorderQty","type": "uint256"},{"internalType": "uint256","name": "_priceInWei","type": "uint256"},{"internalType": "address","name": "_supplier","type": "address"}],"name": "registerMedication","outputs": [],"stateMutability": "nonpayable","type": "function"},
	{"inputs": [{"internalType": "enum EcoChainProcurement.Role","name": "_role","type": "uint8"}],"name": "requestRegistration","outputs": [],"stateMutability": "nonpayable","type": "function"},
	{"inputs": [{"internalType": "address","name": "","type": "address"}],"name": "registeredRoles","outputs": [{"internalType": "enum EcoChainProcurement.Role","name": "","type": "uint8"}],"stateMutability": "view","type": "function"},
    {"inputs": [],"name": "orderCount","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},
    {"inputs": [{"internalType": "uint256","name": "","type": "uint256"}],"name": "orders","outputs": [{"internalType": "uint256","name": "id","type": "uint256"},{"internalType": "string","name": "medName","type": "string"},{"internalType": "uint256","name": "quantity","type": "uint256"},{"internalType": "uint256","name": "totalCost","type": "uint256"},{"internalType": "address","name": "supplier","type": "address"},{"internalType": "enum EcoChainProcurement.OrderStatus","name": "status","type": "uint8"}],"stateMutability": "view","type": "function"}
]