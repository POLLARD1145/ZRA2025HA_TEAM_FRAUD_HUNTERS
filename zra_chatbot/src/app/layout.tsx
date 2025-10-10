import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ZRA Assistant Chatbot',
  description: 'AI-powered assistant for Zambia Revenue Authority services',
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
