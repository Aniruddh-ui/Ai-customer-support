from uagents import crypto

# Generate a private key (seed)
private_key = crypto.generate_seed()

# Get public address from seed
address = crypto.address_from_seed(private_key)

# Print both
print("Main Agent Address:", address)
print("Main Agent Seed:", private_key)
