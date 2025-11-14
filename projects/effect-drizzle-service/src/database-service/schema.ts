import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

const timestamp = (name: string) => integer(name, { mode: "timestamp_ms" });

const common = {
	id: integer("id").primaryKey(),
	createdAt: timestamp("created_at")
		.$default(() => new Date())
		.notNull(),
	updatedAt: timestamp("updated_at")
		.$onUpdate(() => new Date())
		.notNull(),
};

export const todos = sqliteTable("todos", {
	...common,
	title: text("title").notNull(),
	completed: integer("completed", { mode: "boolean" }).default(false).notNull(),
});
