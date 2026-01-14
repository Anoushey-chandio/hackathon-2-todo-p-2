import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { jwt } from "better-auth/plugins";

// Make sure env variables are loaded
if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is not defined in .env");
}

if (!process.env.BETTER_AUTH_SECRET) {
  throw new Error("BETTER_AUTH_SECRET is not defined in .env");
}

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.DATABASE_URL.includes("neon.tech")
      ? { rejectUnauthorized: false }
      : false,
  }),
  secret: process.env.BETTER_AUTH_SECRET, // <-- secret goes here
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET,
    }),
  ],
});
