# EdgeToEquity 🚀

> AI-powered trading automation platform that empowers retail traders to design, optimize, and execute strategies without relying on emotion or deep technical knowledge.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Pending-yellow.svg)]()

## 🎯 Vision

A centralized platform for real traders to design, test, explain, automate, and improve their strategies using AI-powered tools, personalized insights, and psychology-aware feedback loops.

## ✨ Features

### Phase 1 (MVP) - In Development
- 🧠 **Strategy Explainer Agent** - Parse and explain Pine Script/NinjaScript strategies
- 📊 **Performance Analyst Agent** - Analyze trade history with comprehensive metrics
- 🤖 **Master AI Agent** - Central routing system for all trading tools

### Phase 2 (Coming Soon)
- ⚡ **Strategy Optimizer** - Backtest and optimize trading parameters
- 🔧 **Bot Builder** - Convert strategies to executable code
- 🧘 **Psychology Coach** - Behavioral pattern detection and coaching

## 🏗️ Tech Stack

- **Frontend**: Streamlit → React (Progressive enhancement)
- **Backend**: FastAPI + Python 3.9+
- **AI/ML**: OpenAI GPT-4, Anthropic Claude, Langchain
- **Database**: PostgreSQL + Redis
- **Deployment**: Docker, AWS
- **Trading**: NinjaTrader, TradingView Pine Script

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/EdgeToEquity.git
cd EdgeToEquity

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env

# Run the development server
streamlit run src/frontend/app.py
