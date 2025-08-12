export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { jsonl } from '@/lib/mock';
import type { ExportFormat } from '@/lib/types';

/**
 * GET /api/export - Export historical data in CSV or JSONL format
 * Query params:
 * - format: 'csv' | 'jsonl'
 * - minutes: number (clamped to 1-1440)
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const format = searchParams.get('format') as ExportFormat;
    const minutesParam = searchParams.get('minutes');
    
    // Validate format
    if (!format || !['csv', 'jsonl'].includes(format)) {
      return NextResponse.json(
        { error: 'Invalid format. Must be "csv" or "jsonl"' },
        { status: 400 }
      );
    }
    
    // Parse and clamp minutes to [1, 1440] (24 hours max)
    let minutes = parseInt(minutesParam || '30', 10);
    if (isNaN(minutes) || minutes < 1) {
      minutes = 1;
    }
    if (minutes > 1440) {
      minutes = 1440;
    }
    
    // Generate historical data
    const records = [];
    for (let i = 0; i < minutes; i++) {
      records.push(jsonl(i));
    }
    
    // Sort by timestamp ascending (oldest first)
    records.sort((a, b) => a.ts.localeCompare(b.ts));
    
    if (format === 'csv') {
      // Generate CSV with header
      const csvHeader = 'timestamp,device,energy_kWh,heat_kWh,proof_id';
      const csvRows = records.map(record => 
        `${record.ts},${record.device},${record.energy_kWh},${record.heat_kWh},${record.proof_id}`
      );
      const csvContent = [csvHeader, ...csvRows].join('\n') + '\n';
      
      return new NextResponse(csvContent, {
        status: 200,
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': `attachment; filename="terra-nature-metrics-${minutes}min.csv"`,
          'Cache-Control': 'no-store'
        }
      });
    } else {
      // Generate JSONL (NDJSON)
      const jsonlContent = records.map(record => JSON.stringify(record)).join('\n') + '\n';
      
      return new NextResponse(jsonlContent, {
        status: 200,
        headers: {
          'Content-Type': 'application/jsonl',
          'Content-Disposition': `attachment; filename="terra-nature-metrics-${minutes}min.jsonl"`,
          'Cache-Control': 'no-store'
        }
      });
    }
  } catch (error) {
    console.error('Error generating export:', error);
    return NextResponse.json(
      { error: 'Failed to generate export' },
      { status: 500 }
    );
  }
}