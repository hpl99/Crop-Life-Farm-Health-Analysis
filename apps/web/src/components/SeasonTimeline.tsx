"use client";

import React from "react";
import { useI18n } from "@/lib/i18n";
import { Calendar, AlertCircle, CheckCircle2 } from "lucide-react";

interface TimelineMonth {
  name_en: string;
  name_mr: string;
  status_en: string;
  status_mr: string;
  actual_mm: number;
  normal_mm: number;
  departure_pct: number;
  is_deficit: boolean;
}

export function SeasonTimeline() {
  const { t, isMarathi } = useI18n();

  const toDevanagari = (num: number | string): string => {
    if (!isMarathi) return num.toString();
    const digits: Record<string, string> = {
      "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
      "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ".": "."
    };
    return num.toString().replace(/[0-9]/g, (d) => digits[d] || d);
  };

  // Real 2026 Monsoon monthly series based on IMD Nagpur observations
  const months: TimelineMonth[] = [
    {
      name_en: "June",
      name_mr: "जून",
      status_en: "Delayed Onset (-18%)",
      status_mr: "उशिरा आगमन (-१८%)",
      actual_mm: 142.5,
      normal_mm: 174.2,
      departure_pct: -18.2,
      is_deficit: true,
    },
    {
      name_en: "July",
      name_mr: "जुलै",
      status_en: "Active Spells (+12%)",
      status_mr: "संततधार पाऊस (+१२%)",
      actual_mm: 341.2,
      normal_mm: 303.6,
      departure_pct: 12.4,
      is_deficit: false,
    },
    {
      name_en: "August",
      name_mr: "ऑगस्ट",
      status_en: "Severe Break (-59%)",
      status_mr: "तीव्र पावसाचा खंड (-५९%)",
      actual_mm: 114.8,
      normal_mm: 277.2,
      departure_pct: -58.6,
      is_deficit: true,
    },
    {
      name_en: "September",
      name_mr: "सप्टेंबर",
      status_en: "Deficit Retreat (-42%)",
      status_mr: "परतीचा पाऊस कमी (-४२%)",
      actual_mm: 105.4,
      normal_mm: 181.1,
      departure_pct: -41.8,
      is_deficit: true,
    },
  ];

  return (
    <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-base font-bold text-[#2B2B26] flex items-center gap-2">
          <Calendar className="w-4 h-4 text-[#2F5D3A]" />
          <span>{t("timeline.title")}</span>
        </h2>
        <span className="text-xs text-[#2B2B26]/60">
          {isMarathi ? "नागपूर जिल्हा महिनावार आकडेवारी" : "Nagpur Monthly IMD Series"}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {months.map((m) => (
          <div
            key={m.name_en}
            className={`p-4 rounded-2xl border transition-all flex flex-col justify-between ${
              m.is_deficit
                ? "bg-[#B5532F]/5 border-[#B5532F]/20 text-[#2B2B26]"
                : "bg-[#2F5D3A]/5 border-[#2F5D3A]/20 text-[#2B2B26]"
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-sm">
                {isMarathi ? m.name_mr : m.name_en}
              </span>
              {m.is_deficit ? (
                <AlertCircle className="w-4 h-4 text-[#B5532F]" />
              ) : (
                <CheckCircle2 className="w-4 h-4 text-[#2F5D3A]" />
              )}
            </div>

            <div className="my-1">
              <div
                className={`text-lg font-extrabold ${
                  m.is_deficit ? "text-[#B5532F]" : "text-[#2F5D3A]"
                }`}
              >
                {m.departure_pct > 0 ? "+" : ""}
                {toDevanagari(m.departure_pct.toFixed(1))}%
              </div>
              <div className="text-[11px] font-medium text-[#2B2B26]/70">
                {isMarathi ? m.status_mr : m.status_en}
              </div>
            </div>

            <div className="pt-2 border-t border-black/5 flex justify-between text-[11px] text-[#2B2B26]/60">
              <span>{isMarathi ? "प्रत्यक्ष" : "Act"}: {toDevanagari(m.actual_mm)} mm</span>
              <span>{isMarathi ? "सरासरी" : "Norm"}: {toDevanagari(m.normal_mm)} mm</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
