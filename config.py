# ============================================================
# config.py - ECO CHAIN PROCUREMENT
# ============================================================

APP_NAME = "Eco Chain Procurement"
APP_TAGLINE = "Smart Medication Supply Monitoring"
APP_DESCRIPTION = "A blockchain-powered medication monitoring system for Gauteng clinics."
LOGO_PATH = "logo.png"

# BLOCKCHAIN NETWORK SETTINGS
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CHAIN_ID = 11155111
CHAIN_HEX = "0xaa36a7"
CONTRACT_ADDRESS = "0x104ce265233F23D6C322eC6B868A8a913437DB8b"

# HUMAN READABLE LABELS
ROLE_NAMES = {
    0: "Unregistered",
    1: "Hospital",
    2: "Supplier"
}

CATEGORY_MAPPING = {
    "HIV (Antiretrovirals)": 0,
    "TB (Antibiotics)": 1,
    "Diabetes": 2,
    "Emergency Supply": 3
}

# PRESET MEDICATION DATABASE
MEDICATION_DATABASE = {
    "HIV (Antiretrovirals)": {
        "TLD (Tenofovir/Lamivudine/Dolutegravir)": 150,
        "Abacavir/Lamivudine": 110,
        "Dolutegravir (DTG) 50mg": 90
    },
    "TB (Antibiotics)": {
        "Rifafour (RHZE)": 280,
        "Bedaquiline": 950
    },
    "Diabetes": {
        "Metformin 500mg": 25,
        "Rapid-Acting Insulin": 135
    },
    "Emergency Supply": {
        "Adrenaline": 55,
        "Medical Oxygen": 210
    }
}

# FULL SMART CONTRACT ABI
CONTRACT_ABI = [
	{"inputs": [{"internalType": "address", "name": "_finance", "type": "address"}], "stateMutability": "nonpayable", "type": "constructor"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "string", "name": "medName", "type": "string"}, {"indexed": False, "internalType": "uint256", "name": "remainingStock", "type": "uint256"}], "name": "MedicationIssued", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "string", "name": "medName", "type": "string"}], "name": "OrderGenerated", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "amountPaid", "type": "uint256"}], "name": "OrderSettled", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "enum EcoChainProcurement.Role", "name": "role", "type": "uint8"}], "name": "RegistrationApproved", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "enum EcoChainProcurement.Role", "name": "role", "type": "uint8"}], "name": "RegistrationRequested", "type": "event"},
	{"inputs": [], "name": "admin", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "address", "name": "_user", "type": "address"}], "name": "approveRegistration", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [], "name": "ceo", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}], "name": "checkStock", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
	{"inputs": [], "name": "financialOfficer", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "string", "name": "", "type": "string"}], "name": "inventory", "outputs": [{"internalType": "string", "name": "name", "type": "string"}, {"internalType": "enum EcoChainProcurement.IllnessCategory", "name": "category", "type": "uint8"}, {"internalType": "uint256", "name": "currentStock", "type": "uint256"}, {"internalType": "uint256", "name": "minThreshold", "type": "uint256"}, {"internalType": "uint256", "name": "reorderQuantity", "type": "uint256"}, {"internalType": "uint256", "name": "unitPrice", "type": "uint256"}, {"internalType": "address", "name": "supplier", "type": "address"}, {"internalType": "bool", "name": "isActive", "type": "bool"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}], "name": "issueMedication", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [], "name": "orderCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "orders", "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "string", "name": "medName", "type": "string"}, {"internalType": "uint256", "name": "quantity", "type": "uint256"}, {"internalType": "uint256", "name": "totalCost", "type": "uint256"}, {"internalType": "address", "name": "supplier", "type": "address"}, {"internalType": "enum EcoChainProcurement.OrderStatus", "name": "status", "type": "uint8"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "_orderId", "type": "uint256"}], "name": "payAndReplenish", "outputs": [], "stateMutability": "payable", "type": "function"},
	{"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "pendingRequests", "outputs": [{"internalType": "enum EcoChainProcurement.Role", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "enum EcoChainProcurement.IllnessCategory", "name": "_category", "type": "uint8"}, {"internalType": "uint256", "name": "_initialStock", "type": "uint256"}, {"internalType": "uint256", "name": "_threshold", "type": "uint256"}, {"internalType": "uint256", "name": "_reorderQty", "type": "uint256"}, {"internalType": "uint256", "name": "_priceInWei", "type": "uint256"}, {"internalType": "address", "name": "_supplier", "type": "address"}], "name": "registerMedication", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "registeredRoles", "outputs": [{"internalType": "enum EcoChainProcurement.Role", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "enum EcoChainProcurement.Role", "name": "_role", "type": "uint8"}], "name": "requestRegistration", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]