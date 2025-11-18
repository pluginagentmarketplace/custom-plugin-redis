---
name: backend-development
description: Build scalable backend systems with Node.js, Python, Java, and Spring Boot. Master API design, authentication, async programming, and microservices architecture for production applications.
---

# Backend Development Skill

Master backend development across Node.js, Python, Java, and Spring Boot. Learn API design, authentication, async patterns, and enterprise architectures.

## Quick Start

### Node.js with Express (80 hours)
```typescript
// TypeScript Express server
import express, { Request, Response } from 'express';

const app = express();
app.use(express.json());

// Middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

// Routes with error handling
app.get('/users/:id', async (req: Request, res: Response) => {
  try {
    const user = await fetchUser(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'User not found' });
  }
});

app.post('/users', async (req: Request, res: Response) => {
  const { name, email } = req.body;
  const user = await createUser({ name, email });
  res.status(201).json(user);
});

app.listen(3000, () => console.log('Server ready'));
```

### Python FastAPI (80 hours)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

@app.post('/users')
async def create_user(user: UserCreate, db: Session):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    return db_user

@app.get('/users/{user_id}')
async def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
```

### Java Spring Boot (100 hours)
```java
@RestController
@RequestMapping('/api/users')
public class UserController {

  @Autowired
  private UserService userService;

  @PostMapping
  public ResponseEntity<User> createUser(@RequestBody UserRequest request) {
    User user = userService.create(request);
    return ResponseEntity.status(HttpStatus.CREATED).body(user);
  }

  @GetMapping('/{id}')
  public ResponseEntity<User> getUser(@PathVariable Long id) {
    return userService.findById(id)
      .map(ResponseEntity::ok)
      .orElse(ResponseEntity.notFound().build());
  }
}

@Service
public class UserService {
  @Autowired
  private UserRepository repository;

  public User create(UserRequest request) {
    User user = new User();
    user.setName(request.getName());
    user.setEmail(request.getEmail());
    return repository.save(user);
  }
}
```

### Async/Await Programming
```typescript
// Proper async patterns
async function fetchUserWithPosts(userId: string) {
  try {
    // Parallel requests
    const [user, posts] = await Promise.all([
      fetchUser(userId),
      fetchPosts(userId)
    ]);

    return { ...user, posts };
  } catch (error) {
    logger.error('Failed to fetch user data', error);
    throw new AppError('User not found', 404);
  }
}

// Rate limiting
async function apiCall(url: string) {
  await rateLimiter.acquire();
  try {
    return await fetch(url);
  } finally {
    rateLimiter.release();
  }
}
```

## API Design

### REST Conventions
```
GET    /api/users           - List users
POST   /api/users           - Create user
GET    /api/users/:id       - Get user
PUT    /api/users/:id       - Update user
DELETE /api/users/:id       - Delete user

GET    /api/users/:id/posts - User's posts
```

### Error Handling
```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string
  ) {
    super(message);
  }
}

app.use((err: Error, req: Request, res: Response) => {
  if (err instanceof ApiError) {
    return res.status(err.statusCode).json({
      error: err.message,
      code: err.code
    });
  }
  res.status(500).json({ error: 'Internal server error' });
});
```

### Authentication (JWT)
```typescript
const jwt = require('jsonwebtoken');

function generateToken(user: User) {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
}

const authenticate = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

## Database Integration

### Prisma ORM
```typescript
const prisma = new PrismaClient();

// Create with relations
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John',
    posts: {
      create: [
        { title: 'First Post', content: '...' }
      ]
    }
  },
  include: { posts: true }
});

// Query with filtering
const posts = await prisma.post.findMany({
  where: {
    published: true,
    author: { email: 'user@example.com' }
  },
  include: { author: true }
});
```

### SQL Query Optimization
```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE
SELECT u.*, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id;

-- Index strategy
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published, created_at);
```

## Testing

### Unit Testing
```typescript
describe('UserService', () => {
  let service: UserService;
  let repo: MockRepository<User>;

  beforeEach(() => {
    repo = new MockRepository();
    service = new UserService(repo);
  });

  it('should create a user', async () => {
    const user = await service.create({ name: 'John', email: 'john@example.com' });
    expect(user.id).toBeDefined();
    expect(repo.save).toHaveBeenCalled();
  });
});
```

### Integration Testing
```typescript
describe('UserController', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      controllers: [UserController],
      providers: [UserService, UserRepository]
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();
  });

  it('POST /users should create a user', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(201);
  });
});
```

## Microservices Architecture

### Service Communication
```typescript
// RPC with service discovery
const userService = await serviceRegistry.getService('users');
const user = await userService.call('getUser', { id: 123 });

// Event-driven
const eventBus = new EventBus();
eventBus.emit('user.created', { userId: 123 });
eventBus.on('user.created', (event) => {
  notificationService.sendWelcomeEmail(event.userId);
});
```

## Performance Optimization

### Caching Strategy
```typescript
// Redis cache
const redis = new Redis();

async function getUserWithCache(id: string) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await db.findUser(id);
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  return user;
}
```

### Connection Pooling
```javascript
// Node.js database connection pool
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

const query = (text, params) => pool.query(text, params);
```

## Best Practices

- [ ] Use environment variables for configuration
- [ ] Implement proper logging (Winston, Pino)
- [ ] Add health check endpoints
- [ ] Use API versioning
- [ ] Implement rate limiting
- [ ] Add request/response validation
- [ ] Use compression middleware
- [ ] Implement CORS properly
- [ ] Add security headers
- [ ] Monitor performance and errors

## Tools & Libraries

- **Frameworks**: Express, FastAPI, Spring Boot
- **Databases**: PostgreSQL, MongoDB, Redis
- **ORMs**: Prisma, SQLAlchemy, Hibernate
- **Testing**: Jest, pytest, JUnit
- **Monitoring**: Datadog, New Relic, Prometheus

## When to Invoke This Skill

Invoke when:
- Building REST APIs
- Designing database schemas
- Implementing authentication
- Optimizing query performance
- Setting up microservices
- Testing backend code
- Scaling backend systems
- Error handling strategies
