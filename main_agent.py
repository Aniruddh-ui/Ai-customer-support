# main_agent.py

from uagents import Agent, Context
from messages import UserQuery, FAQResponse

# ✅ Use the actual address of your running FAQ agent here
FAQ_AGENT_ADDRESS = "agent1qt0mvrl2440uu3hqv8hcqje6w0z2k6aaazurwm2lr27sehs9xlfygru33xw"

# ✅ Replace with your own main agent’s seed
main_agent = Agent(name="MainAgent", seed="mainagent_secret_seed", endpoint="http://localhost:8001")

@main_agent.on_event("startup")
async def start(ctx: Context):
    query = "Where can I track my order?"
    ctx.logger.info(f"Sending query: {query}")
    await ctx.send(FAQ_AGENT_ADDRESS, UserQuery(text=query))

@main_agent.on_message(model=FAQResponse)
async def receive_faq(ctx: Context, msg: FAQResponse):
    ctx.logger.info(f"Received FAQ Response:\nQ: {msg.question}\nA: {msg.answer}")

if __name__ == "__main__":
    main_agent.run()
