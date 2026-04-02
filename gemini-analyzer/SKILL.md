---
name: gemini-analyzer
description: Use Gemini CLI with massive context window to analyze entire codebases, verify feature implementations, detect patterns across files, or handle tasks requiring massive context (100KB+ files, full directory analysis).
tools: Bash
---

# Gemini CLI for Large Codebase Analysis

Use `gemini -p` with `@` syntax to include files and directories in your prompts. All paths are relative to the current working directory.

## Core Syntax

| Target Type | Command Pattern |
|--------------|-----------------|
| Single file | `gemini -p "@src/main.py <your prompt>"` |
| Multiple files | `gemini -p "@file1 @file2 @file3 <your prompt>"` |
| Directory | `gemini -p "@src/ <your prompt>"` |
| Multiple directories | `gemini -p "@src/ @tests/ @lib/ <your prompt>"` |
| Entire project | `gemini -p "@./ <your prompt>"` |
| All files recursively | `gemini --all_files -p "<your prompt>"` |

## Common Analysis Tasks

### Feature Implementation Verification

```bash
# Check if a feature exists
gemini -p "@src/ @lib/ Has dark mode been implemented? Show all relevant files and functions"

# Authentication implementation check
gemini -p "@src/ @middleware/ Is JWT authentication implemented? List all auth-related endpoints and middleware"

# Specific feature verification
gemini -p "@backend/ @middleware/ Is rate limiting implemented for API endpoints? Show the implementation details"
```

### Architecture and Pattern Analysis

```bash
# Search for specific patterns
gemini -p "@src/ List all React hooks that handle WebSocket connections with file paths"

# Code organization analysis
gemini -p "@src/ Analyze the code structure and identify patterns. Show how modules are organized"

# Implementation patterns
gemini -p "@src/ @lib/ @services/ Is Redis caching implemented? List all cache-related functions and where they're used"
```

### Security and Best Practices

```bash
# Security measure verification
gemini -p "@src/ @api/ Are SQL injection protections implemented? Show how user inputs are sanitized"

# Error handling audit
gemini -p "@src/ @api/ Is proper error handling implemented for all API endpoints? Show examples of try-catch blocks"

# Security pattern search
gemini -p "@src/ Are there any hardcoded credentials or sensitive data leaks? Show with file paths and line numbers"
```

### Testing and Quality

```bash
# Test coverage verification
gemini -p "@src/payment/ @tests/ Is the payment processing module fully tested? List all test cases"

# Code quality analysis
gemini -p "@src/ Identify code duplication, unused variables, and potential bugs"
```

## When to Use This Skill

Use the Gemini CLI instead of Claude's native analysis when:
- Analyzing entire codebases or large directories (>50 files)
- Comparing multiple large files simultaneously
- Need project-wide pattern or architecture analysis
- Current context window is insufficient for the task
- Working with files totaling more than 100KB
- Verifying if specific features, patterns, or security measures are implemented
- Checking for the presence of certain coding patterns across the entire codebase
- Performing comprehensive code reviews spanning multiple modules

## Important Notes

- All paths in `@` syntax are relative to the current working directory when invoking `gemini`
- The CLI includes file contents directly in the context
- No `--yolo` flag needed for read-only analysis tasks
- Gemini's context window can handle entire codebases that would exceed Claude's context limits
- When checking implementations, be specific about what you're looking for to get accurate results
- The analysis is read-only and safe to run on production codebases
