# Instant Checkout Link - Algorand Smart Contract Project

A full-stack donation platform powered by Algorand smart contracts. Create one-click donation links that process payments instantly on the blockchain.

## Project Overview

**Instant Checkout Link** is an MVP (Minimum Viable Product) application that allows users to:
- Create shareable donation links with custom amounts
- Process payments through Algorand smart contracts
- Track donations on the immutable blockchain
- View real-time statistics and payment history

### Tech Stack

**Backend:**
- Python 3.12+
- Flask (REST API)
- Algorand SDK (blockchain integration)
- Flask-CORS (cross-origin requests)

**Frontend:**
- HTML5/CSS3/JavaScript (vanilla - no frameworks)
- Responsive design with gradient UI
- QR code generation for easy sharing

**Smart Contracts:**
- Algorand Python (PyTeal)
- AlgoKit (development framework)
- ARC4 standards (smart contract interface)

## Project Structure

```
hello-algorand/
├── backend/                    # Python Flask backend
│   ├── app.py                 # Main Flask application
│   ├── database/
│   │   └── links.py           # JSON-based link storage
│   ├── routes/
│   │   ├── create_link.py     # POST /api/create-link
│   │   ├── pay.py             # GET /api/pay/<link_id>
│   │   └── verify.py          # GET /api/verify
│   └── utils/
│       ├── algorand.py        # Blockchain utilities
│       └── contract_client.py # Smart contract interactions
│
├── frontend/
│   └── index.html             # Single-page app interface
│
├── smart_contracts/           # Algorand smart contracts
│   ├── hello_world/           # Sample "Hello World" contract
│   ├── instant_checkout/      # Main payment contract
│   └── artifacts/             # Compiled contracts (TEAL)
│
├── scripts/
│   └── deploy_contract.py     # Contract deployment script
│
├── .env                       # Environment variables (create this)
├── .algokit.toml             # AlgoKit configuration
├── pyproject.toml            # Python project configuration
├── poetry.lock               # Python dependency lock file
└── README.md                 # This file
```

## Prerequisites

Before running this project, ensure you have installed:

1. **Python 3.12 or later**
   - [Download Python](https://www.python.org/downloads/)
   - Verify: `python --version`

2. **Docker** (for local Algorand network)
   - [Download Docker](https://www.docker.com/)
   - Verify: `docker --version`

3. **AlgoKit CLI** (v2.0.0 or later)
   ```bash
   # Install with pip (recommended)
   pip install algokit
   
   # Verify installation
   algokit --version
   ```

4. **Poetry** (Python package manager)
   ```bash
   # Install with pip
   pip install poetry
   
   # Verify installation
   poetry --version  # Should be 1.2+
   ```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hello-algorand
```

### 2. Install Dependencies

```bash
# Use Poetry to install all dependencies
poetry install

# This automatically creates a virtual environment in `.venv`
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```env
# Network Configuration
ALGORAND_NETWORK=testnet
ALGORAND_SERVER=https://testnet-api.algonode.cloud

# Flask API Configuration
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
BASE_URL=http://localhost:8000

# Testnet Account (from Pera Wallet or AlgoExplorer)
CREATOR_MNEMONIC=your-testnet-mnemonic-here (25 words)
RECEIVER_MNEMONIC=your-receiver-mnemonic-here (25 words)

# Smart Contract ID (fill after deployment)
APP_ID=0
```

**To get testnet accounts:**
1. Visit [Pera Wallet](https://perawallet.app/) or [AlgoExplorer](https://testnet.algoexplorer.io/)
2. Create a testnet wallet
3. Copy the 25-word mnemonic phrase
4. Request testnet ALGO from the [faucet](https://testnet-dispenser.algoexplorerapi.io/)

### 4. Start the Local Algorand Network

```bash
# Start the local development network (Docker required)
algokit localnet start

# Verify it's running (should show "Started")
```

### 5. Deploy the Smart Contract (Optional)

```bash
# Build the smart contracts
poetry run python -m smart_contracts build

# Deploy to testnet (requires APP_ID in .env)
poetry run python -m smart_contracts deploy

# Update .env with the returned APP_ID
```

### 6. Start the Backend

```bash
# Run the Flask development server
poetry run python -m backend.app

# Should output:
# * Running on http://0.0.0.0:5000
# * Debug mode: on
```

### 7. Open the Frontend

```bash
# Open in your browser
# Option 1: Direct file
open frontend/index.html

# Option 2: Use a local HTTP server (recommended)
cd frontend
python -m http.server 8000

# Then visit: http://localhost:8000
```

## How to Use

### Creating a Donation Link

1. Open the frontend at `http://localhost:8000`
2. Go to **"Create Link"** tab
3. Fill in:
   - **Donation Amount**: Amount in ALGO (e.g., 10)
   - **Receiver Address**: Algorand wallet address (58 characters)
   - **Description**: Optional (e.g., "Help me build my app!")
4. Click **"Create Donation Link"**
5. Copy the link or scan the QR code to share

### Processing a Donation

1. Click the donation link or go to **"Donate"** tab
2. Enter:
   - **Link ID**: From the donation link
   - **Your Wallet Address**: Your Algorand address
3. Click **"Proceed to Payment"**
4. Review the payment details
5. Click **"Open Wallet to Confirm"** (demo mode for MVP)

### Viewing Statistics

Real-time blockchain statistics appear on the right side:
- Total ALGO processed
- Total donations received
- Contract version

## API Endpoints

### Create a Donation Link
```http
POST /api/create-link
Content-Type: application/json

{
  "amount": 1.5,
  "receiver_address": "5U4DPE4D5SRTBR36SV2L3MAFZM7VFGN6KQPHKGK4JM7BVGJKMHIKK65I3Y",
  "description": "optional description"
}

Response:
{
  "success": true,
  "link_id": "abc123xy",
  "amount": 1.5,
  "checkout_url": "http://localhost:8000?link=abc123xy",
  "created": "2025-10-18T22:12:33.440310"
}
```

### Get Payment Details
```http
GET /api/pay/<link_id>?user_address=SENDER_ADDRESS

Response:
{
  "success": true,
  "amount": 1.5,
  "receiver": "5U4D...",
  "sender": "user_address",
  "link_id": "abc123xy",
  "deep_link": "algorand://send?receiver=...&amount=..."
}
```

### Verify Payment
```http
GET /api/verify?txid=ABC123TRANSACTION&link_id=abc123xy

Response:
{
  "success": true,
  "status": "confirmed",
  "amount": 1.5,
  "sender": "5U4D...",
  "receiver": "RECV...",
  "confirmed_round": 12345678
}
```

## Development Workflow

### Running Tests

```bash
# Lint Python code
poetry run pylint backend/

# Run unit tests (when available)
poetry run pytest tests/
```

### Building Contracts

```bash
# Compile smart contracts to TEAL
poetry run python -m smart_contracts build

# Compiled files appear in smart_contracts/artifacts/
```

### Debugging Smart Contracts

The project includes AlgoKit AVM Debugger support:

1. Install VSCode extension: [AlgoKit AVM Debugger](https://marketplace.visualstudio.com/items?itemName=algorandfoundation.algokit-avm-vscode-debugger)
2. Add debug configuration to `.vscode/launch.json`
3. Use `F5` to start debugging with breakpoints

## Troubleshooting

### Problem: "CREATOR_MNEMONIC not set"
**Solution:** Add a valid testnet mnemonic to `.env`

### Problem: "Connection refused" to blockchain
**Solution:** Start the local network with `algokit localnet start`

### Problem: "Module not found" errors
**Solution:** Ensure Poetry virtual environment is active
```bash
poetry shell
# Then run your command
```

### Problem: Frontend not loading
**Solution:** Use a local HTTP server instead of opening HTML directly
```bash
cd frontend
python -m http.server 8000
```

### Problem: CORS errors in browser console
**Solution:** Backend CORS is configured for `localhost:8000`. Update `backend/app.py` if using different port

## File Descriptions

### Backend Files

**`backend/app.py`**
- Main Flask application entry point
- Initializes routes and CORS configuration
- Health check and contract statistics endpoints

**`backend/database/links.py`**
- JSON-based persistence layer
- Functions: create_link, get_link, update_link_status
- Production: Replace with MongoDB or PostgreSQL

**`backend/routes/create_link.py`**
- `POST /api/create-link` endpoint
- Validates amount and receiver address
- Generates unique link ID and QR code URL

**`backend/routes/pay.py`**
- `GET /api/pay/<link_id>` endpoint
- Retrieves payment details
- Tracks link clicks

**`backend/routes/verify.py`**
- `GET /api/verify` endpoint
- Queries Algorand blockchain for transaction status
- Updates database when payment confirmed

**`backend/utils/algorand.py`**
- Algorand SDK wrapper functions
- `is_valid_address()` - Validates Algorand addresses
- `get_network_params()` - Gets blockchain parameters
- `check_address_balance()` - Queries account balance

**`backend/utils/contract_client.py`**
- Smart contract interaction wrapper
- `call_process_payment()` - Executes contract method
- `get_contract_stats()` - Reads contract global state

### Frontend Files

**`frontend/index.html`**
- Single HTML file with embedded CSS and JavaScript
- Two tabs: Create Link and Donate
- Real-time statistics display
- QR code generation using external API

### Smart Contract Files

**`smart_contracts/hello_world/contract.py`**
- Sample "Hello World" ARC4 contract
- Simple method: `hello(name: String) -> String`
- Used as template for new contracts

**`smart_contracts/instant_checkout/contract.py`**
- Main payment processing contract (MVP skeleton)
- Ready for full implementation

**`smart_contracts/artifacts/`**
- Compiled TEAL bytecode
- ARC56 JSON specifications
- Generated TypedClient Python classes

## Production Deployment Checklist

Before deploying to mainnet, ensure:

- [ ] Smart contracts fully tested on testnet
- [ ] Environment variables secured (use secrets manager)
- [ ] Rate limiting implemented on API endpoints
- [ ] Database migrated from JSON to production database
- [ ] Frontend HTTPS enforced
- [ ] CORS restrictions tightened
- [ ] API authentication/authorization added
- [ ] Comprehensive error handling and logging
- [ ] Security audit completed
- [ ] Change Algorand server to mainnet

## Resources

- [Algorand Developer Documentation](https://developer.algorand.org/)
- [Algorand Python SDK](https://github.com/algorand/py-algorand-sdk)
- [AlgoKit CLI Documentation](https://github.com/algorandfoundation/algokit-cli)
- [PyTeal Documentation](https://pyteal.readthedocs.io/)
- [Pera Wallet](https://perawallet.app/)

## Support

For issues or questions:
1. Check the [Algorand Developer Discord](https://discord.gg/algorand)
2. Review [AlgoKit documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs)
3. Check GitHub issues in this repository


## Contributing

[Add contribution guidelines if this is open source]
