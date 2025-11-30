import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DecoPlan - HDB Interior Design Visualization',
  description: 'AI-powered furniture placement and visualization for HDB apartments using RAG technology',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
