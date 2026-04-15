// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract EcoChainMaster is AccessControl {
    // --- 1. Role Definitions ---
    bytes32 public constant COO_ROLE = keccak256("COO_ROLE");
    bytes32 public constant CFO_ROLE = keccak256("CFO_ROLE");
    bytes32 public constant DEV_ROLE = keccak256("DEV_ROLE");
    bytes32 public constant MARKETING_ROLE = keccak256("MARKETING_ROLE");

    // --- 2. Business Data Structures ---
    struct Medication {
        string name;
        uint256 currentStock;
        uint256 threshold;
        address supplier;
        bool active;
    }

    struct Participant {
        bool isVerified;
        string rejectionReason;
    }

    mapping(uint256 => Medication) public inventory;
    mapping(address => Participant) public registry;
    uint256 public medCount;

    // --- 3. Events for Transparency ---
    event StockAlert(uint256 medId, string name, uint256 currentStock);
    event RejectionLogged(address account, string reason);

    // --- 4. Constructor: Setting up the Team ---
    constructor(address coo, address cfo, address dev, address marketing) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender); // You are the CEO/Admin
        _grantRole(COO_ROLE, coo);
        _grantRole(CFO_ROLE, cfo);
        _grantRole(DEV_ROLE, dev);
        _grantRole(MARKETING_ROLE, marketing);
    }

    // --- 5. Functional Logic with Role Restrictions ---

    // ONLY COO: Verifies a clinic or supplier
    function verifyParticipant(address _account) external onlyRole(COO_ROLE) {
        registry[_account].isVerified = true;
    }

    // ONLY COO: Rejects with a mandatory reason
    function rejectParticipant(address _account, string calldata _reason) external onlyRole(COO_ROLE) {
        require(bytes(_reason).length > 0, "Reason is mandatory");
        registry[_account].isVerified = false;
        registry[_account].rejectionReason = _reason;
        emit RejectionLogged(_account, _reason);
    }

    // ONLY DEV: Can add new medication types to the system
    function addMedicationType(string memory _name, uint256 _startStock, uint256 _warnAt, address _sup) 
        external onlyRole(DEV_ROLE) 
    {
        medCount++;
        inventory[medCount] = Medication(_name, _startStock, _warnAt, _sup, true);
    }

    // CLINIC ACTION: This is what the scanner app calls
    function dispenseMedication(uint256 _id, uint256 _qty) external {
        require(registry[msg.sender].isVerified, "Clinic not verified");
        require(inventory[_id].currentStock >= _qty, "Insufficient stock");

        inventory[_id].currentStock -= _qty;

        if (inventory[_id].currentStock <= inventory[_id].threshold) {
            emit StockAlert(_id, inventory[_id].name, inventory[_id].currentStock);
            // Logic for CFO to then handle payment/order triggers
        }
    }

    // ONLY MARKETING: Can pull stock reports for impact studies
    function getImpactData(uint256 _id) external view onlyRole(MARKETING_ROLE) returns (uint256) {
        return inventory[_id].currentStock;
    }
}
    
        

  



   
