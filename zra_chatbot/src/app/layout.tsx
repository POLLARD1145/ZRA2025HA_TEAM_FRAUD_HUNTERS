import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ZRA Fraud Detection Chatbot',
  description: 'AI-powered chatbot for fraud detection assistance',
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
