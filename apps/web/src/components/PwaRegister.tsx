"use client";

import React, { useEffect, useState } from "react";
import { useI18n } from "@/lib/i18n";
import { WifiOff, X } from "lucide-react";

export function PwaRegister() {
  const { isMarathi } = useI18n();
  const [isOffline, setIsOffline] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    // 1. Register Service Worker
    if ("serviceWorker" in navigator && process.env.NODE_ENV === "production") {
      navigator.serviceWorker
        .register("/sw.js")
        .then((reg) => {
          console.log("PWA Service Worker registered successfully:", reg.scope);
        })
        .catch((err) => {
          console.warn("PWA Service Worker registration failed:", err);
        });
    }

    // 2. Track Online / Offline Status
    setIsOffline(!navigator.onLine);
    const handleOnline = () => {
      setIsOffline(false);
      setDismissed(false);
    };
    const handleOffline = () => {
      setIsOffline(true);
      setDismissed(false);
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!isOffline || dismissed) return null;

  return (
    <aside
      role="status"
      aria-live="polite"
      className="sticky top-0 z-50 bg-[#B5532F] text-white px-4 py-2 text-xs font-semibold flex items-center justify-between shadow-md transition-all"
    >
      <div className="flex items-center gap-2 max-w-[1440px] mx-auto w-full">
        <WifiOff className="w-4 h-4 shrink-0" />
        <span>
          {isMarathi
            ? "तुम्ही ऑफलाइन आहात. कॅश केलेला अधिकृत डेटा दर्शविला जात आहे."
            : "You are currently offline. Displaying cached official data."}
        </span>
        <button
          onClick={() => setDismissed(true)}
          className="ml-auto p-1 rounded hover:bg-white/20 transition-colors"
          aria-label="Dismiss banner"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </aside>
  );
}

