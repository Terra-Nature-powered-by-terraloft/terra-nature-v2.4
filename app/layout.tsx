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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="de" className={`${inter.variable} ${montserrat.variable}`}>
      <body>{children}</body>
    </html>
  );
}
