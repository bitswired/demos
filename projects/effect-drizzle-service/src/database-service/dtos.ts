import type { InferSelectModel } from "drizzle-orm";
import { Schema as S } from "effect";
import type * as schema from "./schema.ts";

function ensureSchema<TType, TSchema extends S.Schema<TType, any, any>>(
	schema: TSchema,
): TSchema {
	return schema;
}

const common = {
	id: S.Number,
	createdAt: S.Date,
	updatedAt: S.Date,
};

type Todo = InferSelectModel<typeof schema.todos>;
const _TodoSchema = S.Struct({
	...common,
	title: S.String,
	completed: S.Boolean,
});
export const TodoSchema = ensureSchema<Todo, typeof _TodoSchema>(_TodoSchema);
