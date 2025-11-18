---
name: security-quality
description: Master cybersecurity, secure coding practices, QA testing methodologies, test automation, compliance frameworks (GDPR, HIPAA, PCI-DSS), and security incident response.
---

# Security & Quality Assurance Skill

Master cybersecurity, secure development, QA testing, and compliance.

## Quick Start

### OWASP Top 10 Prevention (50 hours)

#### SQL Injection Prevention
```typescript
// WRONG - vulnerable to SQL injection
const query = `SELECT * FROM users WHERE email = '${email}'`;

// CORRECT - using parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);

// ORM approach
const user = await User.findOne({ email });
```

#### Cross-Site Scripting (XSS) Prevention
```typescript
// WRONG - unsafe HTML insertion
const html = `<div>${userInput}</div>`;
element.innerHTML = html;

// CORRECT - text content only
element.textContent = userInput;

// React auto-escapes
<div>{userInput}</div>

// Sanitization library
import DOMPurify from 'dompurify';
const cleanHtml = DOMPurify.sanitize(userInput);
```

#### Cross-Site Request Forgery (CSRF) Prevention
```typescript
// CSRF token middleware
app.use(csrf());

// Include in forms
<form action="/transfer" method="POST">
  <input type="hidden" name="_csrf" value="<%= csrfToken %>" />
  <button>Transfer Money</button>
</form>

// Verify on server
const token = req.body._csrf;
if (!token || !isValidToken(token)) {
  return res.status(403).json({ error: 'Invalid CSRF token' });
}
```

### Authentication & Authorization (40 hours)

#### Secure Password Hashing
```typescript
import bcrypt from 'bcrypt';

// Hash password during registration
const hashedPassword = await bcrypt.hash(password, 10);

// Verify password during login
const isValid = await bcrypt.compare(password, hashedPassword);

// Never store plain passwords
// Always use bcrypt, scrypt, or Argon2
```

#### JWT Implementation
```typescript
import jwt from 'jsonwebtoken';

// Generate secure token
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '24h', algorithm: 'HS256' }
);

// Verify token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  req.user = decoded;
} catch (error) {
  return res.status(401).json({ error: 'Unauthorized' });
}
```

#### RBAC Implementation
```typescript
// Define roles and permissions
const roles = {
  admin: ['read', 'write', 'delete'],
  user: ['read'],
  guest: []
};

// Middleware for authorization
const authorize = (...allowedRoles) => (req, res, next) => {
  if (!allowedRoles.includes(req.user.role)) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
};

// Usage
app.delete('/users/:id', authorize('admin'), deleteUser);
```

### QA Testing Automation (60 hours)

#### Unit Testing with Jest
```typescript
import { sum, subtract } from './math';

describe('Math functions', () => {
  it('should add two numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(sum(-2, -3)).toBe(-5);
  });

  it('should subtract two numbers', () => {
    expect(subtract(5, 3)).toBe(2);
  });
});
```

#### API Testing
```typescript
import request from 'supertest';
import app from './app';

describe('User API', () => {
  it('POST /users should create a user', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        name: 'John',
        email: 'john@example.com'
      });

    expect(response.status).toBe(201);
    expect(response.body.email).toBe('john@example.com');
  });

  it('GET /users/:id should return a user', async () => {
    const response = await request(app)
      .get('/users/1');

    expect(response.status).toBe(200);
    expect(response.body.id).toBe(1);
  });
});
```

#### End-to-End Testing with Cypress
```typescript
describe('User Registration', () => {
  it('should register a new user', () => {
    cy.visit('/register');
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('SecurePassword123!');
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

### Compliance Frameworks (40 hours)

#### GDPR Compliance
```typescript
// Consent management
const hasConsent = (userId) => {
  return db.query('SELECT consent FROM user_consents WHERE user_id = ?', [userId]);
};

// Right to be forgotten
const deleteUserData = async (userId) => {
  await db.query('DELETE FROM users WHERE id = ?', [userId]);
  await db.query('DELETE FROM user_data WHERE user_id = ?', [userId]);
};

// Data export
const exportUserData = async (userId) => {
  const data = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
  return generateJSON(data);
};
```

#### PCI-DSS Compliance
```typescript
// Never log credit card numbers
logger.info('Transaction:', {
  amount: 100,
  card: '****1234'  // Only last 4 digits
});

// Encrypt sensitive data
const encrypted = crypto.encrypt(creditCardNumber);

// Never store passwords
// Use tokenization for payment processing
const token = await paymentGateway.tokenize(creditCard);
```

## Code Review Checklist

- [ ] No hardcoded secrets
- [ ] Input validation on all endpoints
- [ ] Proper error handling
- [ ] Authentication/authorization checks
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] CORS properly configured
- [ ] Logging of security events
- [ ] Encryption of sensitive data
- [ ] Rate limiting implemented
- [ ] No exposed sensitive information in logs

## Security Headers

```typescript
// Security headers middleware
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

## Testing Pyramid

```
       /\
      /  \  E2E Tests (5-10%)
     /____\
    /      \
   /   I    \ Integration Tests (15-20%)
  /_________ \
 /           \
/ Unit Tests  \ (60-70%)
/____________ \
```

## Tools & Frameworks

- **Security**: OWASP ZAP, Snyk, SonarQube
- **Testing**: Jest, Cypress, Playwright
- **Code Review**: SonarQube, CodeClimate
- **Monitoring**: Sentry, New Relic
- **Vulnerability Scan**: Dependabot, Snyk

## Best Practices

- [ ] Use HTTPS everywhere
- [ ] Implement rate limiting
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Implement comprehensive logging
- [ ] Conduct code reviews
- [ ] Penetration testing
- [ ] Incident response plan
- [ ] Security training for team

## When to Invoke This Skill

Invoke when:
- Implementing authentication
- Writing secure code
- Building automated tests
- Compliance auditing
- Vulnerability assessment
- Creating security policies
- Test automation
- Performance testing
