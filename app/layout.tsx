claude/terranature-scroll-gradients-1gikr
import type { Metadata } from 'next';
import { Inter, Montserrat } from 'next/font/google';
import './globals.css';

// Self-hosted via next/font — no external Google CDN request at runtime,
// fonts are preloaded and the CSS variables are wired into globals.css.
const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-inter',
  display: 'swap',
});
const montserrat = Montserrat({
  subsets: ['latin'],
  weight: ['700', '800', '900'],
  variable: '--font-montserrat',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Terra Nature — Deep-Tech für Klima & Industrie',
  description:
    'Terra Nature wandelt industrielle Abwärme in Strom, nutzbare Wärme und digitale Nachweise. Infrastruktur für Industrie, Stadtwerke und emissionsintensive Standorte.',
};

import type { ReactNode } from 'react';

const TERRABRAND_STYLES = `
  @font-face {
    font-family: "TerraBrand Sans";
    src: local("Inter"), local("Arial"), local("Helvetica");
    font-display: swap;
  }

  @font-face {
    font-family: "TerraBrand Serif";
    src: local("Georgia"), local("Times New Roman"), serif;
    font-display: swap;
  }

  :root {
    --terra-brand-font-sans: "TerraBrand Sans", "Inter", "system-ui", sans-serif;
    --terra-brand-font-serif: "TerraBrand Serif", "Georgia", "Times New Roman", serif;
  }

  body {
    font-family: var(--terra-brand-font-sans);
    margin: 0;
    background-color: #f6f7f9;
    color: #111827;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-family: var(--terra-brand-font-sans);
  }
`;
main

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
claude/terranature-scroll-gradients-1gikr
    <html lang="de" className={`${inter.variable} ${montserrat.variable}`}>

    <html lang="en">
      <head>
        <style dangerouslySetInnerHTML={{ __html: TERRABRAND_STYLES }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
