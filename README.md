# ZRA Fraud Hunters - 2025 Hackathon Project

Welcome to the **Team Fraud Hunters** repository for the 2025 Zambia Revenue Authority (ZRA) Hackathon! This project consists of a fraud detection SDK and an AI-powered chatbot for fraud detection assistance.

## 🚀 Project Overview

This repository contains two main components:

1. **ZRA SDK** (`zra_sdk/`) - A Python-based fraud detection SDK
2. **ZRA Chatbot** (`zra_chatbot/`) - A Next.js-based AI chatbot interface

## 📁 Repository Structure

```text
ZRA2025HA_TEAM_FRAUD_HUNTERS/
├── zra_sdk/                    # Python SDK for fraud detection
│   ├── __init__.py
│   ├── core/                   # Core fraud detection logic
│   │   └── __init__.py
│   ├── models/                 # Data models and schemas
│   │   └── __init__.py
│   ├── utils/                  # Utility functions
│   │   └── __init__.py
│   ├── api/                    # API endpoints and handlers
│   │   └── __init__.py
│   ├── tests/                  # Test suite
│   │   └── __init__.py
│   ├── requirements.txt        # Python dependencies
│   ├── setup.py               # Package setup
│   ├── pyproject.toml         # Python project config
│   ├── .env.example           # Environment variables template
│   └── README.md              # SDK documentation
│
├── zra_chatbot/               # Next.js chatbot application
│   ├── src/
│   │   ├── app/               # Next.js app directory
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/        # React components
│   │   └── lib/               # Utilities and configs
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── next.config.js         # Next.js config
│   ├── tailwind.config.ts     # TailwindCSS config
│   ├── postcss.config.js      # PostCSS config
│   ├── .eslintrc.json         # ESLint config
│   ├── .prettierrc            # Prettier config
│   ├── .env.example           # Environment variables template
│   └── README.md              # Chatbot documentation
│
├── .gitignore                 # Git ignore rules
├── CONTRIBUTING.md            # Contribution guidelines
└── README.md                  # This file
```

## 🛠️ Getting Started

### Prerequisites

**For SDK (Python):**
- Python 3.8 or higher
- pip package manager

**For Chatbot (Next.js):**
- Node.js 18.x or higher
- npm, yarn, or pnpm

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/POLLARD1145/ZRA2025HA_TEAM_FRAUD_HUNTERS.git
cd ZRA2025HA_TEAM_FRAUD_HUNTERS
```

#### 2. Set Up the SDK

```bash
cd zra_sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

#### 3. Set Up the Chatbot

```bash
cd zra_chatbot

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to view the chatbot.

## 📚 Documentation

- **[SDK Developer Guide](./zra_sdk/README.md)** - Complete guide for working with the Python SDK
- **[Chatbot Developer Guide](./zra_chatbot/README.md)** - Complete guide for working with the Next.js chatbot
- **[Contributing Guidelines](./CONTRIBUTING.md)** - How to contribute to this project

## 🤝 Contributing

We follow a **branch-based workflow**. Please read our [Contributing Guidelines](./CONTRIBUTING.md) before making any changes.

### Quick Contribution Overview

1. **Work on your personal branch** (never commit directly to `main`)
2. **Test your changes thoroughly**
3. **Create a pull request** for review
4. **Get approval from at least 2 team members**
5. **Merge after approval**

```bash
# Switch to your branch
git checkout your-name

# Make changes and commit
git add .
git commit -m "feat: your feature description"

# Push changes
git push origin your-name

# Create pull request on GitHub
```

## 🧪 Testing

### SDK Testing

```bash
cd zra_sdk

# Run tests
pytest

# Run with coverage
pytest --cov=zra_sdk --cov-report=html
```

### Chatbot Testing

```bash
cd zra_chatbot

# Run tests
npm run test

# Run in watch mode
npm run test:watch
```

## 🏗️ Tech Stack

### SDK
- **Python 3.8+**
- **FastAPI** - API framework
- **Pydantic** - Data validation
- **Pytest** - Testing framework

### Chatbot
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Lucide React** - Icons
- **Jest** - Testing framework

## 👥 Team Members

Team Fraud Hunters - ZRA 2025 Hackathon

## 📄 License

This project is part of the ZRA 2025 Hackathon.

## 🔗 Useful Links

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

## 📞 Support

For questions or issues:
- Create an issue in this repository
- Contact the team lead
- Check the documentation in each project folder

---

**Last Updated**: 2025-10-10  
**Maintained by**: Team Fraud Hunters
