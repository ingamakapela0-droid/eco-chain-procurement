# ========================= config.py =========================
# This file stores all the configuration values used by the Streamlit app.
#
# SECTION 1: APP DISPLAY SETTINGS
# These values control the application name, tagline, logo path,
# and short description shown in the interface.
#
# SECTION 2: BLOCKCHAIN CONNECTION SETTINGS
# These values connect the app to the Ethereum Sepolia test network
# and identify the deployed smart contract.
#
# SECTION 3: HUMAN-READABLE LABELS
# Smart contracts often store numbers for roles and statuses.
# This section translates those values into plain English labels
# so the app can display readable text to users.
#
# SECTION 4: CONTRACT ABI
# The ABI tells web3.py how to communicate with the smart contract.
# It includes all readable and writable contract functions.
#
# This file contains configuration only.
# No application logic should be written here.

# ============================================================
# APP DISPLAY SETTINGS
# ============================================================

APP_NAME = "Eco Chain Procurement"
APP_TAGLINE = "Smart Medication Stock Monitoring and Procurement"
APP_DESCRIPTION = (
    "Eco Chain Procurement helps clinics and hospitals automatically monitor medication stock levels and replenish shortages using blockchain technology."
)

# Optional logo path
# Leave empty "" if no logo exists
LOGO_PATH = "logo.png"

# ============================================================
# BLOCKCHAIN CONNECTION SETTINGS
# ============================================================

RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

CONTRACT_ADDRESS = "0x29382A813A37b35bA9B3273aD8aD888e05944A0e"

SEPOLIA_CHAIN_ID = 11155111

ETHERSCAN_TX_URL = "https://sepolia.etherscan.io/tx/"

# ============================================================
# HUMAN-READABLE LABELS
# ============================================================

# Role labels used by the contract
ROLE_LABELS = {
    0: "Unregistered",
    1: "Administrator",
    2: "Clinic Staff",
    3: "Supplier",
    4: "Finance Officer",
    5: "Chief Executive Officer"
}

# Order status labels
ORDER_STATUS_LABELS = {
    0: "Pending",
    1: "Paid",
    2: "Completed",
    3: "Cancelled"
}

# Illness category labels
ILLNESS_CATEGORY_LABELS = {
    0: "General",
    1: "Chronic",
    2: "Emergency",
    3: "Pediatric",
    4: "Infectious Disease"
}

# ============================================================
# CONTRACT ABI
# ============================================================

CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_user",
                "type": "address"
            }
        ],
        "name": "approveRegistration",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            }
        ],
        "name": "issueMedication",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "medName",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "remainingStock",
                "type": "uint256"
            }
        ],
        "name": "MedicationIssued",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "medName",
                "type": "string"
            }
        ],
        "name": "OrderGenerated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountPaid",
                "type": "uint256"
            }
        ],
        "name": "OrderSettled",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_orderId",
                "type": "uint256"
            }
        ],
        "name": "payAndReplenish",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "_category",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "_initialStock",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_threshold",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_reorderQty",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_priceInWei",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_supplier",
                "type": "address"
            }
        ],
        "name": "registerMedication",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "role",
                "type": "uint8"
            }
        ],
        "name": "RegistrationApproved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "role",
                "type": "uint8"
            }
        ],
        "name": "RegistrationRequested",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint8",
                "name": "_role",
                "type": "uint8"
            }
        ],
        "name": "requestRegistration",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_newFinance",
                "type": "address"
            }
        ],
        "name": "setFinanceOfficer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "admin",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "ceo",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "financialOfficer",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getContractBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_orderId",
                "type": "uint256"
            }
        ],
        "name": "getOrderDetails",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "medName",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "quantity",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "totalCost",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "supplier",
                        "type": "address"
                    },
                    {
                        "internalType": "uint8",
                        "name": "status",
                        "type": "uint8"
                    }
                ],
                "internalType": "tuple",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "name": "inventory",
        "outputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "category",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "currentStock",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "minThreshold",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reorderQuantity",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "unitPrice",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "supplier",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "isActive",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "orderCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "orders",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "medName",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "quantity",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "totalCost",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "supplier",
                "type": "address"
            },
            {
                "internalType": "uint8",
                "name": "status",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "pendingRequests",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "registeredRoles",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]