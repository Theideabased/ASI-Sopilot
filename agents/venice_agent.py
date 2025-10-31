"""
Venice Agent - Research and News Analyst
An autonomous AI agent for Solana ecosystem research and news gathering.
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

# OpenAI/OpenRouter client
client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = os.getenv("MODEL", "anthropic/claude-3.5-sonnet")

# Create Venice Agent
agent = Agent(
    name="Venice",
    seed=os.getenv("VENICE_AGENT_SEED", "venice-research-agent-seed-2025"),
    port=int(os.getenv("VENICE_PORT", "8002")),
    mailbox=True,  # Enable Agentverse mailbox
)

# Initialize chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# System prompt for Venice
SYSTEM_PROMPT = """
You are Venice, an AI agent specialized in Solana ecosystem research and news analysis.

🔹 **Your Expertise:**
- Latest Solana ecosystem news and developments
- Protocol updates and launches
- DeFi trends and analytics
- NFT market insights
- Developer ecosystem updates
- Governance proposals and DAO activities
- Partnership announcements
- Security incidents and audits

🔹 **Your Research Capabilities:**
- Web search powered by Venice API
- Real-time news aggregation
- Trend analysis and pattern recognition
- Event tracking and monitoring
- Social sentiment analysis
- Technical documentation research

🔹 **Your Communication Style:**
- Informative and up-to-date
- Cite sources when available
- Highlight important developments
- Provide context and analysis
- Distinguish between verified news and rumors
- Focus on actionable insights

🔹 **Your Goal:**
Provide timely, accurate, and relevant information about the Solana ecosystem to help users stay informed and make better decisions.
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
    ctx.logger.info(f"🚀 Venice Research Agent starting...")
    ctx.logger.info(f"📍 Agent address: {agent.address}")
    ctx.logger.info(f"📰 Specialization: Solana News & Research")
    ctx.logger.info(f"✅ Mailbox enabled for Agentverse discovery")


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming research and news requests"""
    ctx.logger.info(f"📨 Received research request from {sender}")
    
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
            ctx.logger.info(f"🔵 Research session started with {sender}")
        elif isinstance(item, TextContent):
            user_text += item.text
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"🔴 Research session ended with {sender}")
    
    if not user_text:
        return
    
    ctx.logger.info(f"🔍 Researching: {user_text}")
    
    try:
        # Process research request with AI
        # In production, this would integrate with Venice API for web search
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Research and provide insights on: {user_text}"}
            ],
            max_tokens=2048,
            temperature=0.6,
        )
        
        response_text = completion.choices[0].message.content or "Unable to find relevant information."
        ctx.logger.info(f"✅ Research complete")
        
        # Send research response
        response_msg = create_text_chat(response_text)
        await ctx.send(sender, response_msg)
        
    except Exception as e:
        ctx.logger.error(f"❌ Error in research: {str(e)}")
        error_msg = create_text_chat(
            f"I encountered an error during research: {str(e)}"
        )
        await ctx.send(sender, error_msg)


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle message acknowledgements"""
    ctx.logger.info(f"✓ Acknowledgement received from {sender}")


# Include the chat protocol and publish manifest
agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    print("=" * 60)
    print("📰 Starting Venice Research Agent")
    print("=" * 60)
    print(f"📍 Agent Address: {agent.address}")
    print(f"🔧 Port: {agent.port}")
    print(f"📬 Mailbox: Enabled")
    print(f"🎯 Specialization: Solana News & Research")
    print("=" * 60)
    
    agent.run()
