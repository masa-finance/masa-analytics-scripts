import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_mint_events(base_url, contract_address, api_key, topic0):
    page = 1
    offset = 1000
    total_logs = 0

    while True:
        # Get logs of Mint function calls
        response = requests.get(base_url, params={
            "module": "logs",
            "action": "getLogs",
            "fromBlock": "0",
            "toBlock": "latest",
            "address": contract_address,
            "topic0": topic0,
            "page": str(page),
            "offset": str(offset),
            "apikey": api_key
        })

        # Check if the response is not empty and status code is 200
        if response.status_code == 200 and response.text.strip():
            logs = response.json().get('result', [])
            num_logs = len(logs)

            if num_logs == 0:
                # If no more logs, stop requesting
                break

            total_logs += num_logs
        else:
            # Add error handling here. For example, print an error message and break the loop
            print(f"Error: Received invalid response from {base_url}")
            break

        page += 1

    return total_logs

# Define network data
networks = {
    "etherscan": {
        "url": "https://api.etherscan.io/api",
        "contract_address_env": "ETHERSCAN_CONTRACT_ADDRESS",
        "api_key_env": "ETHERSCAN_API_KEY",
    },
    "bscscan": {
        "url": "https://api.bscscan.com/api",
        "contract_address_env": "BSCSCAN_CONTRACT_ADDRESS",
        "api_key_env": "BSCSCAN_API_KEY",
    },
    "polygonscan": {
        "url": "https://api.polygonscan.com/api",
        "contract_address_env": "POLYGONSCAN_CONTRACT_ADDRESS",
        "api_key_env": "POLYGONSCAN_API_KEY",
    },
    "celoscan": {
        "url": "https://api.celoscan.io/api",
        "contract_address_env": "CELOSCAN_CONTRACT_ADDRESS",
        "api_key_env": "CELOSCAN_API_KEY",
    }
}

topic0 = "0x7650948236619e679e44bf502d527ec950d1d58336e6babf229f483c57d04672"  # Updated topic0

total_mint_events = 0

for network in networks.values():
    base_url = network['url']
    contract_address = os.getenv(network['contract_address_env'])
    api_key = os.getenv(network['api_key_env'])
    num_mint_events = get_mint_events(base_url, contract_address, api_key, topic0)
    total_mint_events += num_mint_events
    print(f"Number of mint events for {network}: {num_mint_events}")

print(f"Total number of mint events: {total_mint_events}")
