"use client";

import React, { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { api, SourceItem } from "@/lib/api";
import { ShieldCheck, ExternalLink } from "lucide-react";

export function SourceChips() {
  const { t, isMarathi } = useI18n();
  const [sources, setSources] = useState<SourceItem[]>([]);

  useEffect(() => {
    let isMounted = true;
    api.getSources(isMarathi ? "mr" : "en")
      .then((data) => {
        if (isMounted) setSources(data.sources || []);
      })
      .catch((err) => console.error("Failed to load sources:", err));
    return () => {
      isMounted = false;
    };
  }, [isMarathi]);

  return (
    <footer className="mt-8 pt-6 pb-24 border-t border-[#2F5D3A]/10 text-xs text-[#2B2B26]/70">
      <div className="flex items-center gap-2 mb-3">
        <ShieldCheck className="w-4 h-4 text-[#2F5D3A]" />
        <span className="font-bold text-[#2B2B26]">
          {isMarathi ? "अधिकृत डेटा स्रोत व पारदर्शकता" : "Official Data Provenance & Trust Tiers"}
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {sources.map((s) => (
          <a
            key={s.source_id}
            href={s.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-gray-200 hover:border-[#2F5D3A] transition-colors shadow-2xs group"
          >
            <span className="font-semibold text-[#2F5D3A] group-hover:underline">
              {s.name}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 text-gray-600">
              {s.trust_tier}
            </span>
            <ExternalLink className="w-3 h-3 text-gray-400 group-hover:text-[#2F5D3A]" />
          </a>
        ))}
      </div>

      <div className="mt-4 text-[11px] text-gray-500">
        {isMarathi
          ? "नागपूर कृषी डेटा प्रणाली • सर्व हक्क राखीव २०२६ • शून्य कृत्रिम डेटा धोरण (Strictly Real Data Only)"
          : "Nagpur Krishi Data System • 2026 • Strict Zero Synthetic Data Architecture"}
      </div>
    </footer>
  );
}

