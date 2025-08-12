export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { sample } from '@/lib/mock';

/**
 * GET /api/metrics - Returns current metric snapshot
 */
export async function GET() {
  try {
    const metricSample = sample();
    
    return NextResponse.json(metricSample, {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store, max-age=0'
      }
    });
  } catch (error) {
    console.error('Error generating metric sample:', error);
    return NextResponse.json(
      { error: 'Failed to generate metrics' },
      { status: 500 }
    );
  }
}