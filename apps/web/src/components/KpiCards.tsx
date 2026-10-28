"use client";

import React from "react";
import { useI18n } from "@/lib/i18n";
import { SeasonSummary } from "@/lib/api";
import { CloudRain, TrendingDown, Droplets, AlertOctagon } from "lucide-react";

interface KpiCardsProps {
  summary: SeasonSummary | null;
}

export function KpiCards({ summary }: KpiCardsProps) {
  const { t, isMarathi } = useI18n();

  const toDevanagari = (num: number | string): string => {
    if (!isMarathi) return num.toString();
    const digits: Record<string, string> = {
      "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
      "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ".": "."
    };
    return num.toString().replace(/[0-9]/g, (d) => digits[d] || d);
  };

  const actualMm = summary ? summary.actual_rf_mm : "—";
  const deficitPct = summary ? Math.abs(summary.deficit_pct) : "—";
  const missingMm = summary ? summary.missing_rf_mm : "—";
  const droughtTalukas = summary
    ? `${summary.drought_talukas_count}/${summary.total_talukas_count}`
    : "—";

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
      {/* 1. Total Rainfall Card */}
      <div className="bg-white rounded-[24px] p-4 lg:p-5 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)] flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-[#2B2B26]/70">
            {t("kpi.total_rainfall")}
          </span>
          <div className="w-8 h-8 rounded-xl bg-[#2F5D3A]/10 text-[#2F5D3A] flex items-center justify-center">
            <CloudRain className="w-4 h-4" />
          </div>
        </div>
        <div>
          <div className="text-2xl lg:text-3xl font-extrabold text-[#2F5D3A]">
            {toDevanagari(actualMm)}{" "}
            <span className="text-sm font-semibold">{isMarathi ? "मिमी" : "mm"}</span>
          </div>
          <div className="text-[11px] text-[#2B2B26]/60 mt-1">
            {t("kpi.normal_rf")}: {toDevanagari(summary?.normal_rf_mm ?? "—")}{" "}
            {isMarathi ? "मिमी" : "mm"}
          </div>
        </div>
      </div>

      {/* 2. Deficit Card */}
      <div className="bg-white rounded-[24px] p-4 lg:p-5 border border-[#B5532F]/15 shadow-[0_4px_12px_rgba(0,0,0,0.05)] flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-[#2B2B26]/70">
            {t("kpi.deficit")}
          </span>
          <div className="w-8 h-8 rounded-xl bg-[#B5532F]/10 text-[#B5532F] flex items-center justify-center">
            <TrendingDown className="w-4 h-4" />
          </div>
        </div>
        <div>
          <div className="text-2xl lg:text-3xl font-extrabold text-[#B5532F]">
            -{toDevanagari(deficitPct)}%
          </div>
          <div className="text-[11px] text-[#B5532F] font-semibold mt-1">
            {isMarathi ? "गंभीर तूट श्रेणी" : "Severe Deficit Category"}
          </div>
        </div>
      </div>

      {/* 3. Missing Rain Card */}
      <div className="bg-white rounded-[24px] p-4 lg:p-5 border border-[#D9A441]/20 shadow-[0_4px_12px_rgba(0,0,0,0.05)] flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-[#2B2B26]/70">
            {t("kpi.missing_rain")}
          </span>
          <div className="w-8 h-8 rounded-xl bg-[#D9A441]/15 text-[#D9A441] flex items-center justify-center">
            <Droplets className="w-4 h-4" />
          </div>
        </div>
        <div>
          <div className="text-2xl lg:text-3xl font-extrabold text-[#6B4A2F]">
            {toDevanagari(missingMm)}{" "}
            <span className="text-sm font-semibold">{isMarathi ? "मिमी" : "mm"}</span>
          </div>
          <div className="text-[11px] text-[#2B2B26]/60 mt-1">
            {isMarathi ? "सरासरीपेक्षा कमी" : "Below Long-Term Normal"}
          </div>
        </div>
      </div>

      {/* 4. Drought Talukas Card */}
      <div className="bg-white rounded-[24px] p-4 lg:p-5 border border-[#B5532F]/20 shadow-[0_4px_12px_rgba(0,0,0,0.05)] flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-[#2B2B26]/70">
            {t("kpi.drought_talukas")}
          </span>
          <div className="w-8 h-8 rounded-xl bg-[#B5532F]/15 text-[#B5532F] flex items-center justify-center">
            <AlertOctagon className="w-4 h-4" />
          </div>
        </div>
        <div>
          <div className="text-2xl lg:text-3xl font-extrabold text-[#B5532F]">
            {toDevanagari(droughtTalukas)}
          </div>
          <div className="text-[11px] text-[#2B2B26]/60 mt-1 truncate">
            {t("app.drought_source")}
          </div>
        </div>
      </div>
    </div>
  );
}

