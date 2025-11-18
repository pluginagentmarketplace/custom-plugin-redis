---
name: frontend-technologies
description: Master modern web development with HTML5, CSS3, JavaScript, TypeScript, React, Vue, and Angular. Includes responsive design, component architecture, state management, and performance optimization for building production-ready web applications.
---

# Frontend Technologies Skill

Master modern web development across the complete frontend ecosystem. Learn from HTML fundamentals through advanced framework patterns and performance optimization.

## Quick Start

### HTML5 Foundation (20 hours)
```html
<!-- Semantic markup -->
<header>
  <nav aria-label="main navigation">
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Article Title</h1>
    <p>Content here...</p>
  </article>
</main>
<footer>Copyright 2025</footer>
```

### CSS3 Responsive Design (30 hours)
```css
/* Flexbox for layouts */
.container {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

/* Grid for complex layouts */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

/* Mobile-first responsive */
@media (min-width: 768px) {
  .container {
    flex-direction: row;
  }
}
```

### JavaScript ES6+ Fundamentals (100 hours)
```javascript
// Arrow functions and destructuring
const users = [{id: 1, name: 'Alice'}, {id: 2, name: 'Bob'}];
const [firstUser, ...rest] = users;
const names = users.map(({name}) => name);

// Async/await for promises
async function fetchData(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Classes and OOP
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }

  getDisplayName() {
    return `${this.name} <${this.email}>`;
  }
}
```

### TypeScript Type Safety (50 hours)
```typescript
// Interfaces and types
interface User {
  id: number;
  name: string;
  email?: string;
}

type UserRole = 'admin' | 'user' | 'guest';

// Generics for reusable code
function createArray<T>(length: number, value: T): T[] {
  return Array(length).fill(value);
}

// Utility types
type ReadOnlyUser = Readonly<User>;
type UserPreview = Pick<User, 'id' | 'name'>;
```

### React Component Architecture (80 hours)
```typescript
// Functional components with hooks
import { useState, useEffect } from 'react';

interface TodoProps {
  initialTodos?: Todo[];
  onTodoChange: (todos: Todo[]) => void;
}

export function TodoList({ initialTodos = [], onTodoChange }: TodoProps) {
  const [todos, setTodos] = useState<Todo[]>(initialTodos);

  useEffect(() => {
    onTodoChange(todos);
  }, [todos]);

  const addTodo = (text: string) => {
    const newTodo: Todo = {
      id: Date.now(),
      text,
      completed: false
    };
    setTodos([...todos, newTodo]);
  };

  return (
    <ul>
      {todos.map(todo => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </ul>
  );
}
```

### Vue Composition API (70 hours)
```typescript
// Vue 3 Composition API
import { ref, computed, watch } from 'vue';

export function useCounter(initialValue = 0) {
  const count = ref(initialValue);
  const doubled = computed(() => count.value * 2);

  watch(() => count.value, (newValue) => {
    console.log(`Count updated to: ${newValue}`);
  });

  const increment = () => count.value++;

  return { count, doubled, increment };
}
```

### Angular Advanced (120 hours)
```typescript
// Angular Services with Signals
import { Injectable, signal, computed } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class TodoService {
  private todos = signal<Todo[]>([]);
  public todos$ = this.todos.asReadonly();
  public count = computed(() => this.todos().length);

  addTodo(text: string) {
    this.todos.update(todos => [...todos, { id: Date.now(), text }]);
  }
}

// Component with Signals
@Component({
  selector: 'app-todo-list',
  template: `
    <h2>Todos ({{ count() }})</h2>
    @for (todo of todos(); track todo.id) {
      <div>{{ todo.text }}</div>
    }
  `
})
export class TodoListComponent {
  todos = inject(TodoService).todos$;
  count = inject(TodoService).count;
}
```

## Key Topics

### Performance Optimization
- Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Code splitting with dynamic imports
- Lazy loading components and images
- Memoization (React.memo, useMemo)
- Image optimization (WebP, AVIF, responsive)
- Bundle analysis tools

### State Management
- Context API (React)
- Redux and Redux Toolkit
- Zustand for lightweight stores
- Vuex and Pinia (Vue)
- NgRx (Angular)
- Signal-based state (Angular)

### Testing Frameworks
- Unit testing: Jest, Vitest
- Component testing: React Testing Library, Vue Test Utils
- E2E testing: Cypress, Playwright
- Coverage targets: > 80%

### Accessibility (WCAG 2.1 AA)
- Semantic HTML
- ARIA attributes for screen readers
- Keyboard navigation support
- Color contrast ratios (4.5:1 minimum)
- Alt text for images
- Form labels and validation messages

## Real-World Patterns

### Component Composition
```typescript
// Container component (smart)
const UserListContainer = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetchUsers().then(setUsers);
  }, []);

  return <UserListPresenter users={users} />;
};

// Presentational component (dumb)
interface UserListPresenterProps {
  users: User[];
}

const UserListPresenter = ({ users }: UserListPresenterProps) => (
  <ul>
    {users.map(user => <UserItem key={user.id} user={user} />)}
  </ul>
);
```

### Form Handling
```typescript
// React Hook Form with validation
import { useForm } from 'react-hook-form';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

type FormData = z.infer<typeof schema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();

  const onSubmit = async (data: FormData) => {
    await loginUser(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  );
}
```

## Best Practices Checklist

- [ ] Use semantic HTML elements
- [ ] Implement proper error boundaries
- [ ] Write accessible components
- [ ] Use TypeScript for type safety
- [ ] Follow DRY principles
- [ ] Implement proper testing
- [ ] Optimize for Core Web Vitals
- [ ] Use lazy loading for images
- [ ] Implement proper caching
- [ ] Monitor performance in production

## Tools & Resources

- **IDEs**: VS Code, WebStorm
- **Build Tools**: Vite, Webpack, Parcel
- **Testing**: Jest, Cypress, Playwright
- **Linting**: ESLint, Prettier
- **Performance**: Lighthouse, WebPageTest
- **Monitoring**: Sentry, LogRocket

## Learning Resources

1. **Official Docs**: React, Vue, Angular documentation
2. **Interactive Tutorials**: Frontend Masters, egghead.io
3. **Best Practices**: Web.dev by Google
4. **Standards**: MDN Web Docs
5. **Community**: Dev.to, CSS-Tricks

## 2025 Trends

- React Server Components mainstream
- Vue Vapor as alternative rendering
- Angular Signals standard adoption
- TypeScript ubiquity
- Web Components growing adoption
- Edge computing for frontend
- AI-assisted development tools
- Enhanced browser APIs (Signals, Observables)

## When to Invoke This Skill

Invoke this skill when:
- Learning web development fundamentals
- Building components with React/Vue/Angular
- Optimizing web performance
- Implementing accessibility standards
- Working with forms and validation
- Testing components
- Choosing frontend technologies
- Migrating between frameworks
