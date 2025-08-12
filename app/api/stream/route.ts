export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

import { NextRequest } from 'next/server';
import { sample } from '@/lib/mock';

/**
 * GET /api/stream - Server-Sent Events endpoint for live metrics
 * Emits fresh MetricSample every second with 120s idle timeout
 */
export async function GET(request: NextRequest) {
  // Check if client supports SSE
  const headers = new Headers({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Cache-Control'
  });

  // Create readable stream for SSE
  const encoder = new TextEncoder();
  let isConnected = true;
  let timeoutId: NodeJS.Timeout;

  const stream = new ReadableStream({
    start(controller) {
      // Send initial connection message
      const initialData = `data: ${JSON.stringify({ type: 'connected', timestamp: new Date().toISOString() })}\n\n`;
      controller.enqueue(encoder.encode(initialData));

      // Function to send metric data
      const sendMetric = () => {
        if (!isConnected) return;
        
        try {
          const metric = sample();
          const data = `data: ${JSON.stringify({ type: 'metric', ...metric })}\n\n`;
          controller.enqueue(encoder.encode(data));
        } catch (error) {
          console.error('Error generating metric for SSE:', error);
          const errorData = `data: ${JSON.stringify({ type: 'error', message: 'Failed to generate metric' })}\n\n`;
          controller.enqueue(encoder.encode(errorData));
        }
      };

      // Send metrics every second
      const intervalId = setInterval(sendMetric, 1000);

      // Set idle timeout (120 seconds)
      timeoutId = setTimeout(() => {
        if (isConnected) {
          isConnected = false;
          clearInterval(intervalId);
          
          // Send close message
          const closeData = `data: ${JSON.stringify({ type: 'close', reason: 'idle_timeout' })}\n\n`;
          controller.enqueue(encoder.encode(closeData));
          controller.close();
        }
      }, 120000); // 120 seconds

      // Handle client disconnect
      request.signal.addEventListener('abort', () => {
        isConnected = false;
        clearInterval(intervalId);
        clearTimeout(timeoutId);
        
        try {
          controller.close();
        } catch (e) {
          // Stream might already be closed
        }
      });
    },

    cancel() {
      isConnected = false;
      clearTimeout(timeoutId);
    }
  });

  return new Response(stream, { headers });
}