import type { Metadata } from 'next';
import './globals.css';

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
    <html lang="de">
      <body>{children}</body>
    </html>
  );
}
