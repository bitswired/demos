import {
	Console,
	Effect,
	type Fiber,
	Layer,
	Logger,
	ManagedRuntime,
	pipe,
	Schedule,
	Supervisor,
} from "effect";
import { DatabaseService } from "./database-service";

const getAllTodosNoTransaction = Effect.gen(function* () {
	const { runQuery, schema } = yield* DatabaseService;

	const res = yield* runQuery((db) => db.select().from(schema.todos));

	yield* Console.log("Todos:", res);
});

const simulateFailureEffect = Effect.fail(new Error("Simulated failure"));

const insertTodosWithErrorAndNoTransaction = Effect.gen(function* () {
	const { runQuery, schema } = yield* DatabaseService;

	yield* runQuery(async (db) =>
		db.insert(schema.todos).values({
			title: "Test failure without transaction 1",
		}),
	);

	yield* runQuery(async (db) =>
		db.insert(schema.todos).values({
			title: "Test failure without transaction 2",
		}),
	);

	yield* Effect.sleep("2 second");

	yield* simulateFailureEffect;

	yield* runQuery(async (db) =>
		db.insert(schema.todos).values({
			title: "Test failure without transaction 3",
		}),
	);
});

const insertTodosWithErrorAndTransaction = Effect.gen(function* () {
	const { runQuery, schema, transaction } = yield* DatabaseService;

	const res = yield* transaction(
		Effect.gen(function* () {
			yield* runQuery(async (db) =>
				db.insert(schema.todos).values({
					title: "Test failure with transaction 1",
				}),
			);

			yield* runQuery(async (db) =>
				db.insert(schema.todos).values({
					title: "Test failure with transaction 2",
				}),
			);

			yield* Effect.sleep("2 second");

			//yield* simulateFailureEffect;

			yield* runQuery(async (db) =>
				db.insert(schema.todos).values({
					title: "Test failure with transaction 3",
				}),
			);
		}),
	);

	yield* Effect.sleep("4 seconds");
	yield* Console.log("Todos:", res);
});

const withLogging = <R, E, A>(effect: Effect.Effect<R, E, A>) =>
	Effect.gen(function* () {
		yield* Effect.log("Effect executing");
		const supervisor = yield* Supervisor.track;

		const policy = Schedule.spaced("500 millis");

		const monitorFibers = (
			supervisor: Supervisor.Supervisor<Array<Fiber.RuntimeFiber<any, any>>>,
		): Effect.Effect<void> =>
			Effect.gen(function* () {
				const fibers = yield* supervisor.value; // Get the current set of fibers
				console.log(`number of fibers: ${fibers.length}`);
			});

		yield* monitorFibers(supervisor).pipe(
			// Repeat the monitoring according to the schedule
			Effect.repeat(policy),
			// Fork the monitoring into its own fiber
			Effect.fork,
		);

		const logState = Effect.gen(function* () {
			const { runQuery, schema } = yield* DatabaseService;
			const todos = yield* runQuery(async (db) =>
				db.select().from(schema.todos),
			);
			yield* Effect.log(
				`Current todos state: \n${JSON.stringify(todos, null, 2)}`,
			);
		});

		const result = yield* Effect.supervised(effect, supervisor).pipe(
			Effect.andThen(() => logState),
			Effect.tapError((error) => Effect.logError(`Effect error: ${error}`)),
			Effect.tapError(() => logState),
			Effect.catchAll(() => Effect.void),
		);

		return result;
	});

const cleanup = Effect.gen(function* () {
	const { runQuery, schema } = yield* DatabaseService;
	yield* runQuery(async (db) => db.delete(schema.todos));
});

const layers = Layer.provideMerge(DatabaseService.Default, Logger.pretty);
const runtime = ManagedRuntime.make(layers);

await runtime.runPromise(cleanup);
//await runtime.runPromise(getAllTodosNoTransaction.pipe(withLogging));
//await runtime.runPromise(
//	insertTodosWithErrorAndNoTransaction.pipe(withLogging),
//);
await runtime.runPromise(insertTodosWithErrorAndTransaction.pipe(withLogging));
