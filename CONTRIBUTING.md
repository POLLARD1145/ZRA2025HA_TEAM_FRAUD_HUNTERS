# Contributing to ZRA Fraud Hunters Project

Thank you for contributing to the ZRA 2025 Hackathon project! This document provides guidelines and standards for contributing to this repository.

## Table of Contents
- [Branching Strategy](#branching-strategy)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Communication](#communication)

## Branching Strategy

### Branch Structure

We use a **personal branch workflow** to ensure code quality and facilitate team collaboration:

- **`main` branch**: The production-ready branch. **DO NOT commit directly to main**.
- **Personal branches**: Each team member has their own branch (e.g., `john`, `alice`, `bob`).
- **Feature branches** (optional): For specific features, created from your personal branch.

### Important Rules

1. ✅ **Always work on your personal branch**
2. ✅ **Test your changes thoroughly before creating a pull request**
3. ✅ **Never commit directly to the `main` branch**
4. ✅ **Keep your branch updated with `main` regularly**
5. ✅ **All changes must go through pull request review**

## Development Workflow

### 1. Start Working on Your Branch

```bash
# Clone the repository (first time only)
git clone https://github.com/POLLARD1145/ZRA2025HA_TEAM_FRAUD_HUNTERS.git
cd ZRA2025HA_TEAM_FRAUD_HUNTERS

# Switch to your personal branch
git checkout your-name

# Pull latest changes
git pull origin your-name
```

### 2. Keep Your Branch Updated

Regularly sync your branch with `main` to avoid conflicts:

```bash
# Fetch latest changes from main
git fetch origin main

# Merge main into your branch
git merge origin/main

# Resolve any conflicts if they occur
# After resolving, commit the merge
git add .
git commit -m "Merge main into [your-name]"
```

### 3. Make Your Changes

```bash
# Create a new feature (optional, or work directly on your branch)
git checkout -b your-name/feature-description

# Make your changes
# ... edit files ...

# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add fraud detection algorithm"

# Push to your branch
git push origin your-name
```

### 4. Test Your Changes

Before creating a pull request, **thoroughly test your changes**:

#### For SDK (Python):
```bash
cd zra_sdk

# Run tests
pytest

# Check code formatting
black .

# Check linting
flake8 .
```

#### For Chatbot (Next.js):
```bash
cd zra_chatbot

# Run tests
npm run test

# Check formatting
npm run format:check

# Run linting
npm run lint

# Test the build
npm run build
```

### 5. Create a Pull Request

Once you've tested your changes:

1. **Push your changes** to your branch:
   ```bash
   git push origin your-name
   ```

2. **Go to GitHub** and navigate to the repository

3. **Click "New Pull Request"**

4. **Select your branch** as the source and `main` as the target

5. **Fill out the PR template** (see below)

6. **Request reviews** from team members

## Pull Request Process

### PR Template

When creating a pull request, use this template:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing
- [ ] Code formatted and linted

## Screenshots (if applicable)
Add screenshots for UI changes.

## Related Issues
Fixes #(issue number)

## Checklist
- [ ] My code follows the project's code standards
- [ ] I have tested my changes thoroughly
- [ ] I have updated documentation if needed
- [ ] My branch is up to date with main
- [ ] No console.log or debug statements left in code
```

### Review Process

1. **Submit PR**: Create your pull request with a clear description
2. **Team Review**: At least **2 team members** should review the PR
3. **Address Feedback**: Make requested changes if needed
4. **Approval**: Once approved, the PR can be merged
5. **Merge**: A designated team member will merge the PR into `main`

### Review Guidelines

When reviewing a PR, check for:

- ✅ Code quality and readability
- ✅ Adherence to coding standards
- ✅ Proper error handling
- ✅ Test coverage
- ✅ Documentation updates
- ✅ No breaking changes
- ✅ Performance considerations

## Code Standards

### General Standards

1. **Write clean, readable code**
   - Use meaningful variable and function names
   - Keep functions small and focused
   - Add comments for complex logic

2. **Follow language-specific conventions**
   - Python: PEP 8
   - TypeScript/JavaScript: ESLint + Prettier

3. **No dead code**
   - Remove commented-out code
   - Remove unused imports and variables

4. **Error handling**
   - Always handle errors appropriately
   - Use proper try-catch blocks
   - Provide meaningful error messages

### Python (SDK) Standards

```python
# Good
def calculate_fraud_score(transaction: dict) -> float:
    """
    Calculate fraud risk score for a transaction.
    
    Args:
        transaction: Dictionary containing transaction details
        
    Returns:
        Float value between 0 and 1 representing fraud risk
        
    Raises:
        ValueError: If transaction data is invalid
    """
    if not transaction:
        raise ValueError("Transaction cannot be empty")
    
    # Calculation logic here
    return 0.0

# Bad
def calc(t):
    return t['amount'] * 0.5  # No type hints, unclear logic
```

### TypeScript/React (Chatbot) Standards

```typescript
// Good
interface TransactionProps {
  id: string;
  amount: number;
  timestamp: Date;
}

export const Transaction: FC<TransactionProps> = ({ id, amount, timestamp }) => {
  return (
    <div className="transaction">
      <span>{id}</span>
      <span>${amount}</span>
    </div>
  );
};

// Bad
export const Transaction = (props: any) => {
  return <div>{props.id}</div>;  // Using 'any', incomplete implementation
};
```

## Testing Requirements

### Minimum Testing Standards

- **Unit Tests**: All new functions must have unit tests
- **Integration Tests**: Test API endpoints and integrations
- **Manual Testing**: Test UI changes manually before submitting PR

### Test Coverage Goals

- **SDK**: Aim for 80%+ code coverage
- **Chatbot**: Test critical user flows and components

### Writing Good Tests

```python
# Python test example
def test_fraud_detection_with_high_amount():
    """Test that high amounts trigger fraud detection."""
    transaction = {
        'id': 'TXN123',
        'amount': 100000.00,
        'user_id': 'USER456'
    }
    
    result = detect_fraud(transaction)
    
    assert result.is_flagged == True
    assert result.risk_score > 0.7
```

```typescript
// TypeScript test example
describe('ChatInput', () => {
  it('should send message on submit', async () => {
    const mockOnSend = jest.fn();
    render(<ChatInput onSend={mockOnSend} />);
    
    const input = screen.getByRole('textbox');
    const button = screen.getByRole('button');
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(button);
    
    expect(mockOnSend).toHaveBeenCalledWith('Test message');
  });
});
```

## Commit Message Guidelines

Use clear, descriptive commit messages following this format:

```
<type>: <subject>

<body (optional)>
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good
git commit -m "feat: add transaction validation in SDK"
git commit -m "fix: resolve chatbot message rendering issue"
git commit -m "docs: update installation instructions"

# Bad
git commit -m "updates"
git commit -m "fixed stuff"
git commit -m "changes"
```

## Folder Structure Standards

Maintain the established folder structure:

### SDK Structure
```
zra_sdk/
├── core/          # Core functionality only
├── models/        # Data models only
├── utils/         # Utility functions only
├── api/           # API endpoints only
└── tests/         # All tests here
```

### Chatbot Structure
```
zra_chatbot/
└── src/
    ├── app/       # Next.js pages and routes
    ├── components/ # Reusable React components
    └── lib/       # Utility functions and configs
```

## Communication

### Channels

- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code discussions
- **Team Meetings**: For major decisions and planning

### Best Practices

1. **Be respectful** in all communications
2. **Be clear and concise** in descriptions
3. **Ask for help** when stuck
4. **Share knowledge** with the team
5. **Document decisions** in issues or PR comments

## Conflict Resolution

If you encounter merge conflicts:

```bash
# 1. Make sure you're on your branch
git checkout your-name

# 2. Fetch and merge latest main
git fetch origin main
git merge origin/main

# 3. Resolve conflicts in your editor
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# 4. After resolving, stage and commit
git add .
git commit -m "Resolve merge conflicts with main"

# 5. Push to your branch
git push origin your-name
```

## Getting Help

If you need help:

1. **Check documentation** in the README files
2. **Search existing issues** on GitHub
3. **Ask the team** in your communication channel
4. **Create an issue** if it's a bug or feature request

## Summary

1. ✅ Work on your personal branch
2. ✅ Test thoroughly before creating PR
3. ✅ Follow code standards
4. ✅ Write clear commit messages
5. ✅ Get code reviewed before merging
6. ✅ Keep your branch updated with main
7. ✅ Never commit directly to main

---

**Thank you for contributing to the ZRA Fraud Hunters project!**

**Last Updated**: 2025-10-10  
**Maintained by**: Team Fraud Hunters
