/**
 * Kappa Configuration (Node.js side)
 */

export const kappaConfig = {
  apiUrl: process.env.NEXT_PUBLIC_KAPPA_API_URL || "http://localhost:8000",
  enabled: process.env.NEXT_PUBLIC_KAPPA_ENABLED !== "false",
  debug: process.env.NODE_ENV === "development",
};
