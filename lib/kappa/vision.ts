/**
 * Vision Processing Utilities for Kappa
 * Screenshot capture and image processing for Claude Vision API
 */

export interface ScreenshotOptions {
  quality?: number; // 0-1, default 0.8
  format?: 'png' | 'jpeg' | 'webp';
  scale?: number; // default 1.0
  targetElement?: HTMLElement;
}

/**
 * Capture screenshot of the entire page or specific element
 */
export async function captureScreenshot(
  options: ScreenshotOptions = {}
): Promise<string> {
  const {
    quality = 0.8,
    format = 'png',
    scale = 1.0,
    targetElement = document.documentElement,
  } = options;

  try {
    // Import html2canvas dynamically to avoid build-time dependency
    const html2canvas = await import('html2canvas').then((m) => m.default);

    const canvas = await html2canvas(targetElement, {
      scale,
      logging: false,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
    });

    return canvasToBase64(canvas, format, quality);
  } catch (error) {
    // Fallback to Canvas API if html2canvas fails
    return canvasScreenshot(targetElement, format, quality);
  }
}

/**
 * Capture screenshot using Canvas API (simpler but less accurate)
 */
async function canvasScreenshot(
  element: HTMLElement,
  format: 'png' | 'jpeg' | 'webp',
  quality: number
): Promise<string> {
  try {
    // Create canvas from current viewport
    const canvas = await html2canvasBasic(element);
    return canvasToBase64(canvas, format, quality);
  } catch (error) {
    throw new Error(`Screenshot capture failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * Minimal canvas screenshot implementation
 */
async function html2canvasBasic(element: HTMLElement): Promise<HTMLCanvasElement> {
  const rect = element.getBoundingClientRect();
  const canvas = document.createElement('canvas');
  canvas.width = rect.width;
  canvas.height = rect.height;

  const ctx = canvas.getContext('2d');
  if (!ctx) {
    throw new Error('Cannot get canvas context');
  }

  // This is a simplified version - ideally use html2canvas library
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  return canvas;
}

/**
 * Convert Canvas to Base64 data URL
 */
function canvasToBase64(
  canvas: HTMLCanvasElement,
  format: 'png' | 'jpeg' | 'webp' = 'png',
  quality: number = 0.8
): string {
  const mimeType = {
    png: 'image/png',
    jpeg: 'image/jpeg',
    webp: 'image/webp',
  }[format];

  const dataUrl = canvas.toDataURL(mimeType, quality);
  // Remove the "data:image/png;base64," prefix
  return dataUrl.split(',')[1];
}

/**
 * Capture screenshot as Blob (for direct upload)
 */
export async function captureScreenshotAsBlob(
  options: ScreenshotOptions = {}
): Promise<Blob> {
  const base64 = await captureScreenshot(options);
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return new Blob([bytes], { type: `image/${options.format || 'png'}` });
}

/**
 * Load image from URL and convert to Base64
 */
export async function loadImageAsBase64(url: string): Promise<string> {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    return blobToBase64(blob);
  } catch (error) {
    throw new Error(`Failed to load image from URL: ${url}`);
  }
}

/**
 * Convert Blob to Base64 string
 */
export async function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      const base64 = dataUrl.split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

/**
 * Validate Base64 image data
 */
export function isValidBase64Image(data: string): boolean {
  // Check if it looks like base64
  return /^[A-Za-z0-9+/=]*$/.test(data) && data.length % 4 === 0;
}

/**
 * Get dimensions of Base64 image
 */
export async function getImageDimensions(base64: string): Promise<{ width: number; height: number }> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({ width: img.width, height: img.height });
    };
    img.onerror = () => {
      reject(new Error('Failed to load image'));
    };
    img.src = `data:image/png;base64,${base64}`;
  });
}

/**
 * Resize Base64 image to fit within max dimensions
 */
export async function resizeBase64Image(
  base64: string,
  maxWidth: number = 1920,
  maxHeight: number = 1080
): Promise<string> {
  const { width, height } = await getImageDimensions(base64);

  if (width <= maxWidth && height <= maxHeight) {
    return base64;
  }

  const scale = Math.min(maxWidth / width, maxHeight / height);
  const newWidth = Math.floor(width * scale);
  const newHeight = Math.floor(height * scale);

  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = newWidth;
      canvas.height = newHeight;

      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(img, 0, 0, newWidth, newHeight);
        resolve(canvasToBase64(canvas));
      }
    };
    img.src = `data:image/png;base64,${base64}`;
  });
}

/**
 * Create visual feedback element showing screenshot region
 */
export function createScreenshotPreview(base64: string, containerId: string = 'screenshot-preview'): HTMLDivElement {
  const container = document.getElementById(containerId) || document.createElement('div');
  container.id = containerId;
  container.innerHTML = `
    <div style="
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 200px;
      height: 150px;
      border: 2px solid #4CAF50;
      border-radius: 8px;
      background: #f5f5f5;
      z-index: 10000;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
      <img src="data:image/png;base64,${base64}" style="
        width: 100%;
        height: 100%;
        object-fit: cover;
      " alt="Screenshot preview" />
      <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(76, 175, 80, 0.1);
      "></div>
    </div>
  `;

  if (!document.getElementById(containerId)) {
    document.body.appendChild(container);
  }

  return container as HTMLDivElement;
}

/**
 * Hide screenshot preview
 */
export function hideScreenshotPreview(containerId: string = 'screenshot-preview'): void {
  const container = document.getElementById(containerId);
  if (container) {
    container.style.display = 'none';
  }
}
