"""
Solpilot Main Agent - ASI Alliance Competition Submission
An autonomous AI agent specialized in Solana blockchain operations.
"""

from datetime import datetime, timezone
from uuid import uuid4
import os
from dotenv import load_dotenv
from openai import OpenAI
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Load environment variables
load_dotenv()

# OpenAI/OpenRouter client for AI processing
client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = os.getenv("MODEL", "anthropic/claude-3.5-sonnet")

# Create Solpilot Agent
agent = Agent(
    name="Solpilot",
    seed=os.getenv("SOLPILOT_AGENT_SEED", "solpilot-main-agent-seed-2025"),
    port=int(os.getenv("SOLPILOT_PORT", "8000")),
    mailbox=True,  # Enable Agentverse mailbox for ASI:One discovery
)

# Initialize chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# System prompt
SYSTEM_PROMPT = """
You are SOLPILOT, an AI assistant specialized in the Solana Blockchain and decentralized finance (DeFi) on Solana. 
You're a Multi Agentic AI Copilot.

🔹 **Your Other Agents & Their Responsibilities:**
- Sonia: She's a token analyst on Solana Blockchain. She can give a brief information about any token on Solana.
- Venice: He's a research analyst on Solana Blockchain. He's powered by Venice API for intelligent web search engine capability to Solpilot.

🔹 **Your Role & Responsibilities:**
- You are strictly limited to **Solana-related** topics, including token swaps, staking, governance, liquidity pools, auctions, transactions, and news.
- You have specific tools to help users with Solana-related tasks.
- You **must not generate or assist with programming, code, or scripts.**
- You **must not discuss stock markets, traditional finance, or non-Solana blockchain ecosystems.**

🔹 **Your Available Tools:**
1. **Balance Check**: Show SOL and SPL token balances
2. **Token Swap**: Swap tokens using Jupiter aggregator
3. **Staking**: Stake SOL with validators
4. **Unstaking**: Unstake SOL from validators
5. **Transfer**: Send SOL or SPL tokens to other addresses
6. **Transaction Search**: Search and analyze transactions by signature
7. **Token Analysis**: Get detailed token analysis via Sonia agent
8. **News Search**: Get latest Solana ecosystem news via Venice
9. **Portfolio Analysis**: Analyze wallet portfolio and holdings
10. **Governance**: Check and interact with governance proposals
11. **Auction Tools**: Participate in Solana burn auctions

🔹 **Your Goal:**  
Always keep discussions **100% focused on Solana**. Keep responses concise and helpful.
"""


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    """Create a ChatMessage with TextContent"""
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=content,
    )


@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent on startup"""
    ctx.logger.info(f"🚀 Solpilot Agent starting...")
    ctx.logger.info(f"📍 Agent address: {agent.address}")
    ctx.logger.info(f"🌐 Agent name: {agent.name}")
    ctx.logger.info(f"✅ Mailbox enabled for Agentverse discovery")


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    ctx.logger.info(f"📨 Received message from {sender}")
    
    # Send acknowledgement
    ack = ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id
    )
    await ctx.send(sender, ack)
    
    # Extract text from message
    user_text = ""
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"🔵 Session started with {sender}")
        elif isinstance(item, TextContent):
            user_text += item.text
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"🔴 Session ended with {sender}")
    
    if not user_text:
        return
    
    ctx.logger.info(f"💬 User query: {user_text}")
    
    try:
        # Process with AI
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        
        response_text = completion.choices[0].message.content or "I'm not sure how to respond to that."
        ctx.logger.info(f"✅ Generated response")
        
        # Send response
        response_msg = create_text_chat(response_text)
        await ctx.send(sender, response_msg)
        
    except Exception as e:
        ctx.logger.error(f"❌ Error processing message: {str(e)}")
        error_msg = create_text_chat(
            f"I encountered an error processing your request: {str(e)}"
        )
        await ctx.send(sender, error_msg)


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle message acknowledgements"""
    ctx.logger.info(f"✓ Acknowledgement received from {sender} for message {msg.acknowledged_msg_id}")


# Include the chat protocol and publish manifest for Agentverse
agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Starting Solpilot Agent for ASI Alliance")
    print("=" * 60)
    print(f"📍 Agent Address: {agent.address}")
    print(f"🔧 Port: {agent.port}")
    print(f"📬 Mailbox: Enabled")
    print(f"🌐 Agentverse: Will auto-register")
    print("=" * 60)
    
    agent.run()
