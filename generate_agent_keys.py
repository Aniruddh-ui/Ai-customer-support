from uagents.setup import generate_new_seed, register_agent

# Generate a seed (private key)
seed = generate_new_seed()

# Register the agent (to get its public address)
address = register_agent(seed)

# Print results
print("Agent Seed:", seed)
print("Agent Address:", address)
