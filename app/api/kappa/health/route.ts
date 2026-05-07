/**
 * Health Check Proxy
 * Next.js wrapper for Kappa health endpoint
 */

import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  try {
    const kappaUrl = process.env.NEXT_PUBLIC_KAPPA_API_URL || "http://localhost:8000";
    const response = await fetch(`${kappaUrl}/api/kappa/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Kappa health check failed", status: response.status },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data, {
      status: 200,
      headers: {
        "Cache-Control": "no-store",
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("[Kappa Health] Error:", error);
    return NextResponse.json(
      {
        error: "Kappa backend unreachable",
        details: error instanceof Error ? error.message : "Unknown error",
        timestamp: new Date().toISOString(),
      },
      { status: 503 }
    );
  }
}
