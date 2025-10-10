# ZRA Chatbot - Developer Guide

## Overview
The ZRA Chatbot is a Next.js-based web application that provides an AI-powered conversational interface for fraud detection assistance. Built with modern React, TypeScript, and TailwindCSS, it integrates with the ZRA SDK for fraud detection capabilities.

## Table of Contents
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Deployment](#deployment)

## Project Structure

```
zra_chatbot/
├── src/
│   ├── app/                  # Next.js app directory
│   │   ├── layout.tsx       # Root layout component
│   │   ├── page.tsx         # Home page
│   │   └── globals.css      # Global styles
│   ├── components/          # React components
│   └── lib/                 # Utility functions and libraries
├── public/                  # Static assets
├── package.json             # Node.js dependencies
├── tsconfig.json            # TypeScript configuration
├── next.config.js           # Next.js configuration
├── tailwind.config.ts       # TailwindCSS configuration
├── postcss.config.js        # PostCSS configuration
├── .eslintrc.json          # ESLint configuration
├── .prettierrc             # Prettier configuration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Getting Started

### Prerequisites
- Node.js 18.x or higher
- npm, yarn, or pnpm package manager
- Git

### Installation

1. **Navigate to the chatbot directory**:
   ```bash
   cd zra_chatbot
   ```

2. **Install dependencies**:
   ```bash
   # Using npm
   npm install

   # Using yarn
   yarn install

   # Using pnpm
   pnpm install
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env.local
   
   # Edit .env.local with your actual configuration
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Development Setup

### Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run format:check # Check code formatting

# Testing
npm run test         # Run tests
npm run test:watch   # Run tests in watch mode
```

### Environment Variables

Create a `.env.local` file in the root directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# ZRA SDK Configuration
ZRA_SDK_API_KEY=your-api-key-here
ZRA_SDK_API_SECRET=your-api-secret-here

# OpenAI or AI Provider (if using)
OPENAI_API_KEY=your-openai-key-here
```

## Code Standards

### TypeScript Guidelines

- Use **TypeScript** for all new files
- Define proper types and interfaces
- Avoid using `any` type unless absolutely necessary
- Use type inference where possible

### Example Component Structure

```typescript
// src/components/ChatMessage.tsx
import { FC } from 'react';

interface ChatMessageProps {
  message: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export const ChatMessage: FC<ChatMessageProps> = ({ message, sender, timestamp }) => {
  return (
    <div className={`message ${sender === 'user' ? 'user-message' : 'bot-message'}`}>
      <p>{message}</p>
      <span className="timestamp">{timestamp.toLocaleTimeString()}</span>
    </div>
  );
};
```

### Naming Conventions

- **Components**: `PascalCase` (e.g., `ChatMessage.tsx`)
- **Functions/Variables**: `camelCase` (e.g., `handleSubmit`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)
- **Files**: Match component name or use `kebab-case` for utilities

### Code Formatting

This project uses **Prettier** and **ESLint**:

```bash
# Format all files
npm run format

# Check formatting without making changes
npm run format:check

# Lint code
npm run lint
```

### Component Structure

```typescript
// Recommended order for component structure:
// 1. Imports
import { FC, useState, useEffect } from 'react';
import { MessageSquare } from 'lucide-react';

// 2. Types/Interfaces
interface Props {
  title: string;
}

// 3. Component
export const MyComponent: FC<Props> = ({ title }) => {
  // 3.1. Hooks
  const [state, setState] = useState('');
  
  // 3.2. Effects
  useEffect(() => {
    // Effect logic
  }, []);
  
  // 3.3. Handlers
  const handleClick = () => {
    // Handler logic
  };
  
  // 3.4. Render
  return (
    <div>
      <h1>{title}</h1>
    </div>
  );
};
```

## Styling

### TailwindCSS

This project uses TailwindCSS for styling. Follow these guidelines:

- Use utility classes over custom CSS
- Use semantic class names for complex components
- Leverage Tailwind's responsive utilities (`md:`, `lg:`, etc.)
- Use Tailwind's dark mode utilities when applicable

```typescript
// Good
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
  <h2 className="text-xl font-bold text-gray-800">Title</h2>
</div>

// Avoid inline styles
<div style={{ display: 'flex', padding: '16px' }}>
  <h2 style={{ fontSize: '20px' }}>Title</h2>
</div>
```

## Testing

### Writing Tests

Tests should be written using Jest and React Testing Library:

```typescript
// src/components/__tests__/ChatMessage.test.tsx
import { render, screen } from '@testing-library/react';
import { ChatMessage } from '../ChatMessage';

describe('ChatMessage', () => {
  it('renders user message correctly', () => {
    render(
      <ChatMessage 
        message="Hello" 
        sender="user" 
        timestamp={new Date()} 
      />
    );
    
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

### Running Tests

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test -- --coverage
```

## API Integration

### Connecting to ZRA SDK

```typescript
// src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function detectFraud(transactionData: TransactionData) {
  const response = await fetch(`${API_BASE_URL}/api/detect-fraud`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(transactionData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to detect fraud');
  }
  
  return response.json();
}
```

### Using API Routes

Create API routes in `src/app/api/`:

```typescript
// src/app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  // Process chat request
  const response = {
    message: 'Response from chatbot',
    timestamp: new Date().toISOString(),
  };
  
  return NextResponse.json(response);
}
```

## Building for Production

### Build Process

```bash
# Create production build
npm run build

# Test production build locally
npm run start
```

### Production Checklist

- [ ] All environment variables set in production
- [ ] Remove console.log statements
- [ ] Optimize images and assets
- [ ] Test all critical user flows
- [ ] Check responsive design on multiple devices
- [ ] Verify API integration with production endpoints

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Configure environment variables in Vercel dashboard
4. Deploy

### Manual Deployment

```bash
# Build the application
npm run build

# The output will be in the `.next` directory
# Deploy the `.next` directory and `package.json` to your hosting provider
```

## Performance Optimization

### Best Practices

- Use **Next.js Image** component for images
- Implement **code splitting** with dynamic imports
- Use **React.memo** for expensive components
- Implement **data fetching** on the server side when possible

```typescript
// Dynamic import example
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
});
```

## Troubleshooting

### Common Issues

**Module not found**: Run `npm install` to ensure all dependencies are installed.

**Port already in use**: Change the port by running `PORT=3001 npm run dev`.

**Environment variables not working**: Ensure they are prefixed with `NEXT_PUBLIC_` for client-side access.

**Build errors**: Clear `.next` folder and rebuild: `rm -rf .next && npm run build`.

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Lucide Icons](https://lucide.dev/)

## Support

For questions or issues, please contact the team or create an issue in the GitHub repository.

---

**Last Updated**: 2025-10-10  
**Maintained by**: Team Fraud Hunters
