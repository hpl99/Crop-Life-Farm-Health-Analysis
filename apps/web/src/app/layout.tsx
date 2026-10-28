import type { Metadata, Viewport } from "next";
import { Mukta, Noto_Sans_Devanagari } from "next/font/google";
import "./globals.css";
import { I18nProvider } from "@/lib/i18n";
import { PwaRegister } from "@/components/PwaRegister";

const mukta = Mukta({
  subsets: ["devanagari", "latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-mukta",
  display: "swap",
});

const notoDevanagari = Noto_Sans_Devanagari({
  subsets: ["devanagari"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-noto-devanagari",
  display: "swap",
});

export const metadata: Metadata = {
  title: "नागपूर शेती आकडे (Nagpur Krishi Data)",
  description: "Official agricultural statistics, rainfall departures, and transparent crop analytics for farmers of Nagpur district.",
  applicationName: "Nagpur Krishi Data",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Nagpur Krishi",
  },
};

export const viewport: Viewport = {
  themeColor: "#2F5D3A",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="mr" className={`${mukta.variable} ${notoDevanagari.variable}`}>
      <body className="min-h-screen bg-[#FAF5E9] text-[#2B2B26] antialiased">
        <I18nProvider>
          <PwaRegister />
          {children}
        </I18nProvider>
      </body>
    </html>
  );
}

