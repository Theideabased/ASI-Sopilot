# ASI-Sopilot: Autonomous Solana DeFi Agents

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

![Live demo](https://img.shields.io/badge/demo-live-brightgreen)

**Powered by Fetch.ai uAgents & ASI Alliance**

An autonomous multi-agent system that simplifies Solana DeFi operations through natural language. Three specialized agents collaborate in real-time to analyze tokens, execute trades, and provide market insights—all accessible via ASI:One.

---

## 🤖 Autonomous Agents

### Solpilot (Coordinator)
- **Address**: `agent1q...` *(generated on first run)*
- **Port**: 8000
- **Role**: Main orchestrator for Solana operations
- **Functions**: Balance checks, swaps, staking, transfers, governance

### Sonia (Token Analyst)
- **Address**: `agent1q...` *(generated on first run)*
- **Port**: 8001
- **Role**: Deep token analysis and research
- **Functions**: Liquidity analysis, tokenomics, risk assessment, recommendations

### Venice (Market Research)
- **Address**: `agent1q...` *(generated on first run)*
- **Port**: 8002
- **Role**: Solana ecosystem intelligence
- **Functions**: News aggregation, protocol updates, DeFi trends, security alerts

---

## 🎯 ASI Alliance Tech Stack

- **uAgents Framework**: Core agent infrastructure with Chat Protocol
- **Agentverse**: Agent registry with mailbox for discovery
- **ASI:One**: User-facing chat interface
- **Chat Protocol**: ChatMessage, ChatAcknowledgement, session management
- **Multi-Agent Communication**: Real-time agent-to-agent coordination

---

## 📺 Demo Video

**[Insert 3-5 minute demo video link here]**

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd agents
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env: Add OPENROUTER_API_KEY and unique agent seeds
```

### 3. Run Agents
```bash
chmod +x run_agents.sh
./run_agents.sh
```

### 4. Register on Agentverse
- Click inspector URLs from terminal
- Enable "Mailbox" for each agent
- Note agent addresses for README

### 5. Test on ASI:One
- Visit https://asi.one
- Search for agents by name
- Start chat: "Check my SOL balance" or "Analyze BONK token"

## 📋 Agent Addresses

Update after first run:
- **Solpilot**: `agent1q...` 
- **Sonia**: `agent1q...`
- **Venice**: `agent1q...`

---

## 💡 How It Works

```
User → ASI:One → Solpilot (analyzes intent)
                     ↓
         ┌───────────┴───────────┐
         ↓                       ↓
    Sonia Agent          Venice Agent
  (Token Analysis)    (Market Research)
         ↓                       ↓
         └───────────┬───────────┘
                     ↓
         Solpilot (synthesizes response)
                     ↓
                  User
```

**Example Interactions**:
- "What's my SOL balance?" → Solpilot checks wallet
- "Analyze BONK token" → Sonia provides risk assessment
- "Latest Solana news?" → Venice aggregates updates

---

## 🛠️ Required Resources

- **Python 3.8+**
- **OpenRouter API Key**: [Get here](https://openrouter.ai)
- **Environment Variables**: See `agents/.env.example`

```env
SOLPILOT_AGENT_SEED=your-unique-seed-1
SONIA_AGENT_SEED=your-unique-seed-2
VENICE_AGENT_SEED=your-unique-seed-3
OPENROUTER_API_KEY=your-api-key
MODEL=anthropic/claude-3.5-sonnet
```

## 📁 Project Structure

```
agents/
├── solpilot_agent.py  # Coordinator agent
├── sonia_agent.py     # Token analyst agent
├── venice_agent.py    # Market research agent
├── requirements.txt   # Dependencies
└── run_agents.sh      # Launch script
```

---

## 🔍 Real-World Impact

- **Simplifies DeFi**: Natural language instead of complex interfaces
- **Informed Decisions**: AI-powered token analysis and risk assessment
- **Time-Saving**: Automated news aggregation and research
- **Accessible**: No technical expertise required for blockchain operations

## 🏆 Competition Compliance

- ✅ Fetch.ai uAgents Framework
- ✅ Chat Protocol for ASI:One
- ✅ Agentverse registration with mailbox
- ✅ Multi-agent real-time communication
- ✅ Innovation Lab categorization
- ✅ Public GitHub repository
- ✅ Comprehensive documentation

---

**Built for ASI Alliance Competition | Powered by Fetch.ai uAgents**

---

## 🐛 Troubleshooting

### "Agent won't start"
- Check Python 3.8+ installed: `python --version`
- Verify ports 8000-8002 available
- Check all env variables set in `agents/.env`

### "Can't register on Agentverse"
- Verify internet connection
- Ensure agent is running (check terminal)
- Try refreshing inspector URL

### "AI not responding"
- Verify OPENROUTER_API_KEY is valid
- Check API quota/limits
- Try switching MODEL in .env

---

## 🚧 Future Enhancements

### Phase 1 (Competition Submission)
- ✅ Three uAgents with Chat Protocol
- ✅ Agentverse registration
- ✅ ASI:One compatibility
- ✅ Multi-agent collaboration

### Phase 2 (Post-Competition)
- 🔄 MeTTa Knowledge Graph integration
- 🔄 Advanced token analytics
- 🔄 Automated trading strategies
- 🔄 Cross-chain support

---

## 📚 Additional Resources

- 📖 [Fetch.ai uAgents Docs](https://docs.fetch.ai/uAgents)
- 🏗️ [Innovation Lab Examples](https://github.com/fetchai/innovation-lab-examples)
- 🌐 [Agentverse Platform](https://agentverse.ai)
- 💬 [ASI:One Interface](https://asi1.ai)
- 🤖 [Competition Details](https://earn.superteam.fun/listing/asi-agents-track)

---

## 📄 License

See the project `LICENSE` file for full terms.

## Run locally

```bash
git clone https://github.com/Theideabased/ASI-Sopilot.git
cd ASI-Sopilot
# Web UI (optional)
npm install
npm run dev

# Agents (uAgents)
cd agents
pip install -r requirements.txt
cp .env.example .env
./run_agents.sh
```

Set required environment variables in `agents/.env` (OpenRouter API key, agent seeds). See `agents/.env.example`.

## Live demo

The production frontend is deployed on Vercel: https://solpilot-ai.vercel.app/

For deployment, Vercel or any Next.js-compatible host works; the agents should be deployed separately (see `agents/`).

## Project Structure

- `/app`: Main application code
  - `/api`: API routes for backend functionality
  - `/components`: React components
  - `/providers`: Context providers
  - `/services`: Service functions for API calls
- `/lib`: Utility libraries
- `/public`: Static assets
- `/ai`: AI-related functionality
- `/wallet`: Wallet integration code

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

This means you are free to:

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.

See the LICENSE file for more details.

---

## 🎯 Competition Submission Checklist

- ✅ **Code**: Public GitHub repository with all agent code
- ✅ **README.md**: Comprehensive documentation with agent names and addresses
- ✅ **Innovation Lab Badges**: Both badges included at the top
- ✅ **uAgents Framework**: All three agents built with Fetch.ai uAgents
- ✅ **Chat Protocol**: ASI:One compatible ChatMessage implementation
- ✅ **Agentverse Registration**: Agents configured for mailbox registration
- ✅ **Multi-Agent Communication**: Agents communicate via uAgents protocol
- ✅ **Real-World Use Case**: Solana DeFi operations and portfolio management
- ✅ **Demo Video**: 3-5 minute demonstration (link to be added)
- ✅ **Extra Resources**: OpenRouter API key requirement documented

---

## 🙏 Acknowledgments

Built for the **ASI Alliance Hackathon** using:
- **Fetch.ai uAgents Framework** for autonomous agent infrastructure
- **Agentverse** for agent registry and discovery
- **ASI:One** for user-facing chat interface
- **Solana** blockchain for DeFi operations
- **OpenRouter** for multi-model AI capabilities

---

## 📞 Contact & Support

- **GitHub Repository**: [Theideabased/ASI-Sopilot](https://github.com/Theideabased/ASI-Sopilot)
- **Competition**: [ASI Alliance Agents Track](https://earn.superteam.fun/listing/asi-agents-track)
- **Documentation**: Complete setup guides in this README
- **Demo Video**: [To be added - 3-5 minutes]

---

**Built with ❤️ for the ASI Alliance Competition by [Your Name/Team]**
