# ZRA2025HA Project Summary

## Project Purpose

This repository contains two main components developed for the 2025 Zambia Revenue Authority Hackathon:

### 1. ZRA SDK (Python)
**Purpose**: A developer SDK for integrating ZRA services into third-party applications

**Key Features**:
- Taxpayer verification using TPIN (Taxpayer Identification Number)
- Tax calculations (VAT, income tax, etc.)
- Compliance checks
- Easy-to-use Python API
- RESTful API endpoints

**Use Cases**:
- Financial applications needing to verify taxpayer status
- Tax management systems
- Business automation tools
- Accounting software integration

### 2. ZRA Chatbot (Next.js)
**Purpose**: A general-purpose AI assistant for Zambia Revenue Authority services

**Key Features**:
- Conversational AI interface
- Help with taxpayer registration
- Tax filing assistance
- Compliance query responses
- Payment information
- General ZRA service inquiries

**Use Cases**:
- Customer service automation
- User guidance through ZRA processes
- FAQ and information dissemination
- 24/7 assistance for ZRA services

## Updated Documentation

All README files have been updated to reflect the correct project scope:

1. **Main README** - Overview of both projects
2. **SDK README** - Developer guide for ZRA service integration
3. **Chatbot README** - Developer guide for the AI assistant
4. **CONTRIBUTING.md** - Contribution guidelines and branching workflow

## Quick Start

### For SDK Development:
```bash
cd zra_sdk
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### For Chatbot Development:
```bash
cd zra_chatbot
npm install
npm run dev
```

## Contribution Workflow

- Work on personal branches
- Test thoroughly before creating pull requests
- Require 2+ team member approvals
- Never commit directly to main

---

**Last Updated**: 2025-10-10  
**Team**: Fraud Hunters
