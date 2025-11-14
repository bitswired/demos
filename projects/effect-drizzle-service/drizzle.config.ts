import { defineConfig } from "drizzle-kit";
import { Config, Effect } from "effect";

const dbUrl = Effect.runSync(Config.string("DB_URL"));

export default defineConfig({
	out: "./drizzle",
	schema: "./src/database-service/schema.ts",
	dialect: "sqlite",
	dbCredentials: {
		url: dbUrl,
	},
});
