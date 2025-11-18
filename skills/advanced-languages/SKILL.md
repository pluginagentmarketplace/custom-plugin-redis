---
name: advanced-languages
description: Master advanced programming languages (Golang, Rust, C++, Blockchain) and leadership roles (Product Management, Engineering Management, UX Design, Technical Writing, Community Building).
---

# Advanced Technologies & Leadership Skill

Master advanced languages and transition to leadership roles.

## Golang Fundamentals (80 hours)

```go
package main

import (
  "fmt"
  "sync"
)

// Goroutines for concurrency
func main() {
  var wg sync.WaitGroup

  // Launch goroutines
  for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
      defer wg.Done()
      fmt.Printf("Goroutine %d\n", id)
    }(i)
  }

  wg.Wait()
}

// Channels for communication
func worker(jobs <-chan int, results chan<- int) {
  for job := range jobs {
    results <- job * 2
  }
}

// Interfaces for polymorphism
type Reader interface {
  Read(p []byte) (n int, err error)
}

type Writer interface {
  Write(p []byte) (n int, err error)
}
```

## Rust Advanced Patterns (100 hours)

```rust
// Ownership and borrowing
fn main() {
  let s = String::from("hello");
  // s is moved here
  takes_ownership(s);
  // println!("{}", s); // ERROR: s no longer valid

  let x = 5;
  // x is copied (implements Copy trait)
  makes_copy(x);
  println!("{}", x); // OK: x still valid
}

// Lifetime annotations
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
  if x.len() > y.len() { x } else { y }
}

// Error handling with Result
fn divide(a: f64, b: f64) -> Result<f64, String> {
  if b == 0.0 {
    Err(String::from("Division by zero"))
  } else {
    Ok(a / b)
  }
}

fn main() {
  match divide(10.0, 2.0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => println!("Error: {}", e),
  }
}

// Async/await for concurrency
async fn fetch_data() -> Result<String, Error> {
  let response = reqwest::get("https://api.example.com").await?;
  Ok(response.text().await?)
}
```

## Blockchain & Smart Contracts

```solidity
// Solidity smart contract example
pragma solidity ^0.8.0;

contract SimpleBank {
  mapping(address => uint256) public balances;

  event Deposit(address indexed account, uint256 amount);
  event Withdrawal(address indexed account, uint256 amount);

  function deposit() public payable {
    require(msg.value > 0, "Deposit must be positive");
    balances[msg.sender] += msg.value;
    emit Deposit(msg.sender, msg.value);
  }

  function withdraw(uint256 amount) public {
    require(balances[msg.sender] >= amount, "Insufficient balance");
    balances[msg.sender] -= amount;
    payable(msg.sender).transfer(amount);
    emit Withdrawal(msg.sender, amount);
  }

  function getBalance() public view returns (uint256) {
    return balances[msg.sender];
  }
}
```

## Leadership: Product Management

### Product Strategy Template
```markdown
# Product Strategy Document

## Vision
Clear, compelling vision statement (1-2 sentences)

## Goals (OKRs)
- Objective 1
  - Key Result 1.1
  - Key Result 1.2
- Objective 2
  - Key Result 2.1

## User Research Summary
- Target users identified
- Pain points documented
- Jobs to be Done identified

## Roadmap
- Q1: Foundation (3 months)
  - Feature A
  - Feature B
- Q2: Growth (3 months)
  - Feature C
  - Feature D

## Success Metrics
- Primary: Adoption rate >20%
- Secondary: User retention >70%
- Tertiary: NPS > 50
```

## Leadership: Engineering Management

### 1:1 Meeting Framework
```markdown
## Weekly 1:1 Agenda

### Recognition (5 min)
- Celebrate wins from last week
- Acknowledge great work

### Progress (10 min)
- Review action items from last 1:1
- Discuss current projects

### Growth (10 min)
- Career development goals
- Skill improvements
- Learning opportunities

### Blockers (10 min)
- Any obstacles or concerns
- Support needed

### Feedback (10 min)
- Give/receive honest feedback
- Coaching and mentoring
```

## UX Design Process

```markdown
# Design Sprint Process

## Day 1: Understand
- Define problem statement
- User research review
- Competitive analysis

## Day 2: Ideate
- Brainstorming session
- Sketching ideas
- Vote on promising solutions

## Day 3: Prototype
- Build interactive prototype
- Focus on highest priority flow

## Day 4: Test
- User interviews (5 people)
- Observe user behavior
- Collect feedback

## Day 5: Learn
- Synthesize findings
- Identify improvements
- Next steps
```

## Technical Writing

### API Documentation Template
```markdown
# API Documentation

## Authentication

All API requests require Bearer token authentication:

\`\`\`
Authorization: Bearer YOUR_API_KEY
\`\`\`

## Endpoints

### Get User
\`\`\`
GET /api/v1/users/:id
\`\`\`

**Parameters:**
- `id` (string, required): User ID

**Response (200):**
\`\`\`json
{
  "id": "123",
  "name": "John",
  "email": "john@example.com"
}
\`\`\`

**Errors:**
- `404`: User not found
- `401`: Unauthorized
- `500`: Server error

## Rate Limiting
- 100 requests per minute
- Exceeding limit returns 429 status
```

## Community Building Strategy

### Community Engagement Calendar
```
Weekly:
- Office hours (community Q&A)
- Featured member spotlight
- Weekly digest of discussions

Monthly:
- Live webinar with product updates
- Community voting on features
- Virtual meetup

Quarterly:
- Annual virtual conference
- Community recognition awards
- Strategic roadmap sharing
```

## Best Practices for Leaders

### Decision-Making Framework
- Gather data
- Involve stakeholders
- List options
- Evaluate trade-offs
- Decide and communicate
- Document decision
- Follow up

### Difficult Conversations
- Prepare in advance
- Be specific with examples
- Listen actively
- Focus on behavior, not person
- Discuss solutions
- Follow up in writing

## Tools by Role

**Product Managers:**
- JIRA, ProductBoard, Figma
- Amplitude, Mixpanel (analytics)
- UserTesting, Hotjar (research)

**Engineering Managers:**
- GitHub, GitLab
- JIRA, Trello
- 1Password (secrets)
- DataDog (monitoring)

**UX Designers:**
- Figma, Adobe XD
- Framer, Principle
- Maze, UserTesting
- Hotjar (analytics)

**Technical Writers:**
- Markdown + Git
- Docusaurus, MkDocs
- Vercel, Netlify
- OpenAPI/Swagger

**Community Leaders:**
- Discord, Slack
- GitHub Discussions
- Eventbrite, Meetup
- Analytics dashboards

## When to Invoke This Skill

Invoke when:
- Learning Golang/Rust/C++
- Building smart contracts
- Transitioning to leadership
- Product strategy questions
- Team management challenges
- User experience design
- Documentation projects
- Community initiatives
