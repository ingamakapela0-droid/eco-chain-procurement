# --- CONFIGURATION FOR ECO-CHAIN PROCUREMENT SOLUTIONS ---

CONTRACT_ADDRESS = "0x27cfAB5e3a4283E96046691b41Dc2Fb9cC4839d4"
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

APP_NAME = "Eco-Chain Procurement"
TAGLINE = "The Digital Bridge for Medical Supply Continuity"
DESCRIPTION = "An automated procurement system ensuring clinics never run out of essential medication."

ORDER_STATUS_LABELS = {
    0: "Order Created",
    1: "Payment in Escrow",
    2: "Delivery Verified",
    3: "Order Completed"
}

# Python-formatted ABI (Booleans are capitalized)
CONTRACT_ABI = [
	{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint256","name":"_initialStock","type":"uint256"},{"internalType":"uint256","name":"_threshold","type":"uint256"},{"internalType":"uint256","name":"_reorderQty","type":"uint256"},{"internalType":"uint256","name":"_price","type":"uint256"},{"internalType":"address","name":"_supplier","type":"address"}],"name":"addMedication","outputs":[],"stateMutability":"nonpayable","type":"function"},
	{"inputs":[{"internalType":"uint256","name":"_orderId","type":"uint256"}],"name":"depositEscrow","outputs":[],"stateMutability":"payable","type":"function"},
	{"inputs":[{"internalType":"address","name":"_finance","type":"address"},{"internalType":"address","name":"_staff","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},
	{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"},{"indexed":False,"internalType":"string","name":"medName","type":"string"}],"name":"DeliveryVerified","type":"event"},
	{"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"issueMedication","outputs":[],"stateMutability":"nonpayable","type":"function"},
	{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"medName","type":"string"},{"indexed":False,"internalType":"uint256","name":"remainingStock","type":"uint256"}],"name":"MedicationIssued","type":"event"},
	{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"},{"indexed":False,"internalType":"string","name":"medName","type":"string"},{"indexed":False,"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"OrderGenerated","type":"event"},
	{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"orderId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PaymentEscrowed","type":"event"},
	{"inputs":[{"internalType":"uint256","name":"_orderId","type":"uint256"}],"name":"verifyDelivery","outputs":[],"stateMutability":"nonpayable","type":"function"},
	{"inputs":[],"name":"ceo","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
	{"inputs":[],"name":"financialOfficer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
	{"inputs":[],"name":"getContractBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
	{"inputs":[],"name":"hospitalStaff","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
	{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"inventory","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"currentStock","type":"uint256"},{"internalType":"uint256","name":"minThreshold","type":"uint256"},{"internalType":"uint256","name":"reorderQuantity","type":"uint256"},{"internalType":"uint256","name":"unitPrice","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"bool","name":"isActive","type":"bool"}],"stateMutability":"view","type":"function"},
	{"inputs":[],"name":"orderCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
	{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"orders","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"medName","type":"string"},{"internalType":"uint256","name":"quantity","type":"uint256"},{"internalType":"uint256","name":"totalCost","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"enum EcoChainProcurement.OrderStatus","name":"status","type":"uint8"},{"internalType":"bool","name":"isPaid","type":"bool"}],"stateMutability":"view","type":"function"}
]