# effect-drizzle-service

A production-ready database service layer built with [Effect](https://effect.website/) and [Drizzle ORM](https://orm.drizzle.team/), providing type-safe database operations with automatic transaction management and context-aware query execution.

## 🎥 Video Tutorial

[![Watch the tutorial](https://img.youtube.com/vi/8u3vetGUtMo/maxresdefault.jpg)](https://youtu.be/8u3vetGUtMo)

**[Watch on YouTube →](https://youtu.be/8u3vetGUtMo)**

## Overview

This project demonstrates how to build a robust database service using Effect's dependency injection and resource management capabilities combined with Drizzle ORM's type-safe SQL queries. It showcases:

- **Context-Aware Transactions**: Automatic detection of transaction context for nested operations
- **Type-Safe Operations**: Full TypeScript type safety from database schema to runtime
- **Effect Service Pattern**: Clean service architecture with proper error handling
- **Runtime Configuration**: Environment-based configuration using Effect's Config system

## Features

- 🔐 **Transaction Context Management**: Automatically detects whether code is running inside a transaction
- 🎯 **Type-Safe Schema**: Drizzle ORM schemas with Effect Schema DTOs for runtime validation
- ⚡ **Optimized SQLite**: Pre-configured PRAGMAs for maximum performance
- 🔄 **Automatic Migrations**: Optional migration support via configuration
- 🛡️ **Error Handling**: Comprehensive error types and handling using Effect's error model
- 📦 **Service Layer Pattern**: Clean separation of concerns with Effect Services

## Project Structure

```
effect-drizzle-service/
├── src/
│   ├── database-service/
│   │   ├── index.ts          # Main database service implementation
│   │   ├── schema.ts         # Drizzle ORM schema definitions
│   │   └── dtos.ts           # Effect Schema DTOs for validation
│   └── test.ts               # Example usage and tests
├── drizzle.config.ts         # Drizzle Kit configuration
├── package.json
└── tsconfig.json
```

## Installation

```bash
bun install
```

## Configuration

Set the following environment variables:

```bash
# Required
DB_URL="file:./database.db"

# Optional - enable migrations
DB_SHOULD_MIGRATE="true"
```

## Usage

### Basic Database Service Usage

```typescript
import { Effect, Layer, ManagedRuntime } from "effect";
import { DatabaseService } from "./database-service";

// Create a managed runtime with the database service
const layers = Layer.provideMerge(DatabaseService.Default, Logger.pretty);
const runtime = ManagedRuntime.make(layers);

// Query example
const getAllTodos = Effect.gen(function* () {
  const { runQuery, schema } = yield* DatabaseService;
  
  const todos = yield* runQuery((db) => 
    db.select().from(schema.todos)
  );
  
  return todos;
});

// Execute
await runtime.runPromise(getAllTodos);
```

### Transaction Management

The service automatically handles transaction context:

```typescript
const insertMultipleTodos = Effect.gen(function* () {
  const { runQuery, schema, transaction } = yield* DatabaseService;
  
  // Wrap multiple operations in a transaction
  yield* transaction(
    Effect.gen(function* () {
      yield* runQuery((db) =>
        db.insert(schema.todos).values({ title: "First todo" })
      );
      
      yield* runQuery((db) =>
        db.insert(schema.todos).values({ title: "Second todo" })
      );
      
      // If any operation fails, all are rolled back
    })
  );
});
```

### Schema Definition

Define your database schema using Drizzle ORM:

```typescript
// src/database-service/schema.ts
import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const todos = sqliteTable("todos", {
  id: integer("id").primaryKey(),
  title: text("title").notNull(),
  completed: integer("completed", { mode: "boolean" }).default(false).notNull(),
  createdAt: integer("created_at", { mode: "timestamp_ms" }).notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp_ms" }).notNull(),
});
```

### Type-Safe DTOs with Effect Schema

Create runtime-validated DTOs:

```typescript
// src/database-service/dtos.ts
import { Schema as S } from "effect";
import type { InferSelectModel } from "drizzle-orm";
import type * as schema from "./schema";

type Todo = InferSelectModel<typeof schema.todos>;

export const TodoSchema = S.Struct({
  id: S.Number,
  title: S.String,
  completed: S.Boolean,
  createdAt: S.Date,
  updatedAt: S.Date,
});
```

## Database Migrations

Push schema changes to your database:

```bash
bun run db:push
```

## Key Concepts

### Context-Aware Query Execution

The `runQuery` function automatically detects if it's running inside a transaction:

- **Outside transaction**: Executes directly against the database
- **Inside transaction**: Executes against the transaction client
- **Automatic rollback**: Any error in a transaction rolls back all changes

### Service Layer Architecture

The database service is implemented as an Effect Service, providing:

- **Dependency injection**: Easy testing and composition
- **Resource management**: Automatic cleanup and lifecycle management
- **Error handling**: Type-safe error propagation

### Transaction Context Propagation

Uses Effect's context system to propagate transaction state:

```typescript
const TransactionContext = Context.GenericTag<TransactionContextShape>(
  "TransactionContext"
);
```

This allows nested operations to automatically participate in the parent transaction without explicit parameter passing.

## Example: Transaction with Error Handling

```typescript
const safeInsert = Effect.gen(function* () {
  const { runQuery, schema, transaction } = yield* DatabaseService;
  
  const result = yield* transaction(
    Effect.gen(function* () {
      yield* runQuery((db) =>
        db.insert(schema.todos).values({ title: "Todo 1" })
      );
      
      yield* runQuery((db) =>
        db.insert(schema.todos).values({ title: "Todo 2" })
      );
      
      // Simulate an error - will rollback both inserts
      yield* Effect.fail(new Error("Something went wrong"));
    })
  ).pipe(
    Effect.catchAll((error) => 
      Effect.log(`Transaction failed: ${error}`)
    )
  );
});
```

## Performance Optimizations

The service applies several SQLite PRAGMAs for optimal performance:

- `foreign_keys = ON` - Enforce referential integrity
- `journal_mode = WAL` - Write-Ahead Logging for better concurrency
- `synchronous = NORMAL` - Balance between safety and performance
- `cache_size = 1000000000` - Large cache for better read performance
- `temp_store = memory` - Store temporary tables in memory
- `mmap_size = 268435456` - Memory-mapped I/O for faster access

## Error Handling

The service defines custom error types:

```typescript
class DatabaseError extends Data.TaggedError("DatabaseError")<{
  message?: string;
  readonly cause: unknown;
}> {}
```

All database operations are wrapped in `Effect.tryPromise` for proper error handling.

## Testing

Run the test suite:

```bash
bun run src/test.ts
```

The test file demonstrates:
- Basic queries without transactions
- Transaction rollback on errors
- Fiber monitoring and supervision
- State logging and debugging

## Tech Stack

- **[Effect](https://effect.website/)** - Powerful TypeScript framework for building robust applications
- **[Drizzle ORM](https://orm.drizzle.team/)** - TypeScript ORM with SQL-like syntax
- **[Bun](https://bun.sh/)** - Fast JavaScript runtime and toolkit
- **[@libsql/client](https://github.com/tursodatabase/libsql-client-ts)** - SQLite client for TypeScript
- **SQLite** - Embedded relational database

## Dependencies

```json
{
  "dependencies": {
    "effect": "^3.19.3",
    "@effect/platform": "^0.93.1",
    "@effect/platform-bun": "^0.83.0",
    "drizzle-orm": "^0.44.7",
    "drizzle-kit": "^0.31.6",
    "@libsql/client": "^0.15.15"
  }
}
```

## Learn More

- [Effect Documentation](https://effect.website/docs/introduction)
- [Drizzle ORM Documentation](https://orm.drizzle.team/docs/overview)
- [Effect Service Pattern](https://effect.website/docs/guides/context-management/services)
- [Effect Error Handling](https://effect.website/docs/guides/error-management)