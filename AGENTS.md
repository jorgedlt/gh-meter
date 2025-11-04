# AGENTS.md

## Build/Lint/Test Commands

### Build Commands
- `npm run build` - Build the project for production
- `npm run dev` - Start development server

### Test Commands
- `npm test` - Run all tests
- `npm run test:unit` - Run unit tests only
- `npm run test:integration` - Run integration tests
- `npm run test -- --testNamePattern="specific test name"` - Run a single test

### Lint Commands
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Auto-fix linting issues
- `npm run typecheck` - Run TypeScript type checking

## Code Style Guidelines

### Imports
- Use ES6 imports with named exports preferred
- Group imports: React, third-party libraries, local modules
- Use absolute imports for internal modules

### Formatting
- Use Prettier for consistent formatting
- 2 spaces for indentation
- Single quotes for strings
- Semicolons required

### Types
- Use TypeScript for all new code
- Prefer interfaces over types for object shapes
- Use strict null checks
- Avoid `any` type

### Naming Conventions
- camelCase for variables and functions
- PascalCase for components and classes
- UPPER_SNAKE_CASE for constants
- kebab-case for file names

### Error Handling
- Use try/catch for async operations
- Throw specific error types
- Log errors appropriately
- Handle errors at appropriate levels

### Additional Rules
- No console.log in production code
- Use functional components with hooks
- Follow React best practices
- Write descriptive commit messages