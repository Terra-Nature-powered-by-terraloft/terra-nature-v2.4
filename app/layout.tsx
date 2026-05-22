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

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <style dangerouslySetInnerHTML={{ __html: TERRABRAND_STYLES }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
