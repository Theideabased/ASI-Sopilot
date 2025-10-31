"""
Sonia Agent - Token Analysis Specialist
An autonomous AI agent specialized in Solana token analysis.
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

# Create Sonia Agent
agent = Agent(
    name="Sonia",
    seed=os.getenv("SONIA_AGENT_SEED", "sonia-token-analyst-agent-seed-2025"),
    port=int(os.getenv("SONIA_PORT", "8001")),
    mailbox=True,  # Enable Agentverse mailbox
)

# Initialize chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# System prompt for Sonia
SYSTEM_PROMPT = """
You are Sonia, an AI agent specialized in Solana-based token analysis. 

🔹 **Your Expertise:**
- Analyzing token liquidity and market depth
- Identifying top token holders and distribution
- Evaluating tokenomics and fundamentals
- Assessing investment potential and risks
- Analyzing burn mechanisms and deflationary metrics
- Evaluating liquidity pools and trading volumes

🔹 **Your Analysis Framework:**
When analyzing a token, you provide:
1. **Pros**: Strengths and positive factors
2. **Cons**: Weaknesses and risk factors  
3. **Risk Assessment**: Low/Medium/High centralization risk
4. **Liquidity Analysis**: TVL, pool depth, trading volumes
5. **Holder Distribution**: Top holders, concentration metrics
6. **Final Recommendation**: Investment outlook

🔹 **Your Communication Style:**
- Professional and data-driven
- Balanced analysis showing both positives and negatives
- Clear risk warnings when appropriate
- Concise but comprehensive insights

Always base your analysis on provided data and metrics. Be honest about limitations and uncertainties.
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
    ctx.logger.info(f"🚀 Sonia Token Analyst Agent starting...")
    ctx.logger.info(f"📍 Agent address: {agent.address}")
    ctx.logger.info(f"🔬 Specialization: Solana Token Analysis")
    ctx.logger.info(f"✅ Mailbox enabled for Agentverse discovery")


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages for token analysis"""
    ctx.logger.info(f"📨 Received token analysis request from {sender}")
    
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
            ctx.logger.info(f"🔵 Analysis session started with {sender}")
        elif isinstance(item, TextContent):
            user_text += item.text
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"🔴 Analysis session ended with {sender}")
    
    if not user_text:
        return
    
    ctx.logger.info(f"🔬 Analyzing token: {user_text}")
    
    try:
        # Process token analysis request with AI
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=2048,
            temperature=0.5,  # Lower temperature for more analytical responses
        )
        
        response_text = completion.choices[0].message.content or "Unable to analyze this token."
        ctx.logger.info(f"✅ Analysis complete")
        
        # Send analysis response
        response_msg = create_text_chat(response_text)
        await ctx.send(sender, response_msg)
        
    except Exception as e:
        ctx.logger.error(f"❌ Error analyzing token: {str(e)}")
        error_msg = create_text_chat(
            f"I encountered an error analyzing this token: {str(e)}"
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
    print("🔬 Starting Sonia Token Analyst Agent")
    print("=" * 60)
    print(f"📍 Agent Address: {agent.address}")
    print(f"🔧 Port: {agent.port}")
    print(f"📬 Mailbox: Enabled")
    print(f"🎯 Specialization: Solana Token Analysis")
    print("=" * 60)
    
    agent.run()
