"use client";

import React from "react";
import { useI18n } from "@/lib/i18n";
import { SeasonSummary } from "@/lib/api";

interface NormalVsActualChartProps {
  summary: SeasonSummary | null;
}

export function NormalVsActualChart({ summary }: NormalVsActualChartProps) {
  const { t, isMarathi } = useI18n();

  const toDevanagari = (num: number | string): string => {
    if (!isMarathi) return num.toString();
    const digits: Record<string, string> = {
      "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
      "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ".": "."
    };
    return num.toString().replace(/[0-9]/g, (d) => digits[d] || d);
  };

  const normal = summary?.normal_rf_mm ?? 936.1;
  const actual = summary?.actual_rf_mm ?? 617.8;
  const deficitPct = summary ? Math.abs(summary.deficit_pct) : 34.0;

  // Visual percentages scaled relative to normal (max 100%)
  const maxVal = Math.max(normal, actual) * 1.1;
  const normalWidth = (normal / maxVal) * 100;
  const actualWidth = (actual / maxVal) * 100;

  return (
    <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <h2 className="text-base font-bold text-[#2B2B26]">
            {t("chart.normal_vs_actual")}
          </h2>
          <p className="text-xs text-[#2B2B26]/60">
            {isMarathi
              ? "दीर्घकालीन सरासरी (१९८८-२०२०) विरुद्ध २०२६ मान्सून"
              : "Long-term normal (1988-2020) vs 2026 Monsoon Actuals"}
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-[#B5532F]/10 text-[#B5532F] text-xs font-bold">
          -{toDevanagari(deficitPct)}% {isMarathi ? "तूट" : "Deficit"}
        </span>
      </div>

      <div className="space-y-4 pt-2">
        {/* Normal Bar */}
        <div>
          <div className="flex justify-between text-xs font-semibold mb-1 text-[#2B2B26]">
            <span className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-md bg-[#2F5D3A]" />
              <span>{isMarathi ? "दीर्घकालीन सरासरी (ICAR-CRIDA)" : "Long-Term Normal (ICAR-CRIDA)"}</span>
            </span>
            <span className="font-bold text-[#2F5D3A]">
              {toDevanagari(normal)} {isMarathi ? "मिमी" : "mm"}
            </span>
          </div>
          <div className="h-6 w-full bg-gray-100 rounded-xl overflow-hidden p-0.5">
            <div
              className="h-full bg-[#2F5D3A] rounded-lg transition-all duration-700"
              style={{ width: `${normalWidth}%` }}
              role="progressbar"
              aria-valuenow={normal}
              aria-valuemin={0}
              aria-valuemax={maxVal}
            />
          </div>
        </div>

        {/* Actual 2026 Bar */}
        <div>
          <div className="flex justify-between text-xs font-semibold mb-1 text-[#2B2B26]">
            <span className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-md bg-[#B5532F]" />
              <span>{isMarathi ? "२०२६ प्रत्यक्ष पाऊस (IMD)" : "2026 Actual Recorded (IMD)"}</span>
            </span>
            <span className="font-bold text-[#B5532F]">
              {toDevanagari(actual)} {isMarathi ? "मिमी" : "mm"}
            </span>
          </div>
          <div className="h-6 w-full bg-gray-100 rounded-xl overflow-hidden p-0.5">
            <div
              className="h-full bg-[#B5532F] rounded-lg transition-all duration-700"
              style={{ width: `${actualWidth}%` }}
              role="progressbar"
              aria-valuenow={actual}
              aria-valuemin={0}
              aria-valuemax={maxVal}
            />
          </div>
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-[11px] text-[#2B2B26]/60">
        <span>{t("kpi.source_label")}</span>
        <span className="font-semibold text-[#6B4A2F]">
          {isMarathi ? "तूट: ३१८.३ मिमी कमी पाऊस" : "Gap: 318.3 mm rain deficit"}
        </span>
      </div>
    </div>
  );
}

