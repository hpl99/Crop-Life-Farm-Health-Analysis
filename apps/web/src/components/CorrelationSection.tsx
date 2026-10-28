"use client";

import React, { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { api, RainfallResponseResult, OutlookResponse, AnalogYear } from "@/lib/api";
import { TrendingUp, HelpCircle, History, AlertCircle } from "lucide-react";

interface CorrelationSectionProps {
  crop?: string;
}

export function CorrelationSection({ crop = "soybean" }: CorrelationSectionProps) {
  const { t, isMarathi } = useI18n();
  const [responseResult, setResponseResult] = useState<RainfallResponseResult | null>(null);
  const [outlook, setOutlook] = useState<OutlookResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const toDevanagari = (num: number | string): string => {
    if (!isMarathi) return num.toString();
    const digits: Record<string, string> = {
      "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
      "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ".": "."
    };
    return num.toString().replace(/[0-9]/g, (d) => digits[d] || d);
  };

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    Promise.all([
      api.getRainfallResponse(crop, isMarathi ? "mr" : "en"),
      api.getOutlook(crop, -34.0, isMarathi ? "mr" : "en"),
    ])
      .then(([resp, outl]) => {
        if (!isMounted) return;
        setResponseResult(resp);
        setOutlook(outl);
      })
      .catch((err) => {
        console.error("Failed to load correlation data:", err);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [crop, isMarathi]);

  // Scatter points scaling
  const points = responseResult?.scatter_points || [];
  const trendLine = responseResult?.trend_line || [];
  const minRf = 400;
  const maxRf = 1600;
  const minY = 200;
  const maxY = 1800;

  return (
    <div className="space-y-6">
      {/* 1. Correlation Scatter & Trend Line Card */}
      <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
          <div>
            <h2 className="text-base font-bold text-[#2B2B26] flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-[#2F5D3A]" />
              <span>{t("correlation.title")}</span>
            </h2>
            <p className="text-xs text-[#2B2B26]/60">
              {isMarathi
                ? "५८ वर्षांचा (१९६६-२०२४) अधिकृत मान्सून पाऊस व पीक उत्पादन परस्परसंबंध"
                : "58-Year Official Monsoon Rainfall vs. Yield Scatter & Regression"}
            </p>
          </div>

          {/* Stats Badge */}
          {responseResult && (
            <div className="flex items-center gap-2 bg-[#FAF5E9] px-3 py-1.5 rounded-xl border border-[#2F5D3A]/20 text-xs font-semibold text-[#2F5D3A]">
              <span>R² = {responseResult.r_squared.toFixed(3)}</span>
              <span>•</span>
              <span>p = {responseResult.p_value.toFixed(4)}</span>
              <span>•</span>
              <span>
                {isMarathi ? "नमुने" : "Points"}: {points.length}
              </span>
            </div>
          )}
        </div>

        {/* Scatter Plot SVG Container */}
        <div className="relative w-full h-64 bg-[#FAF5E9]/30 rounded-2xl border border-gray-100 p-4 overflow-hidden">
          <svg className="w-full h-full" viewBox="0 0 600 220" preserveAspectRatio="none">
            {/* Grid lines */}
            <line x1="50" y1="20" x2="580" y2="20" stroke="#e5e7eb" strokeDasharray="4 4" />
            <line x1="50" y1="70" x2="580" y2="70" stroke="#e5e7eb" strokeDasharray="4 4" />
            <line x1="50" y1="120" x2="580" y2="120" stroke="#e5e7eb" strokeDasharray="4 4" />
            <line x1="50" y1="170" x2="580" y2="170" stroke="#e5e7eb" strokeDasharray="4 4" />

            {/* Regression line */}
            {trendLine.length >= 2 && (
              <line
                x1={50 + ((trendLine[0].rainfall_mm - minRf) / (maxRf - minRf)) * 520}
                y1={190 - ((trendLine[0].yield_kg_ha - minY) / (maxY - minY)) * 170}
                x2={50 + ((trendLine[trendLine.length - 1].rainfall_mm - minRf) / (maxRf - minRf)) * 520}
                y2={190 - ((trendLine[trendLine.length - 1].yield_kg_ha - minY) / (maxY - minY)) * 170}
                stroke="#2F5D3A"
                strokeWidth="2.5"
                strokeDasharray="6 3"
              />
            )}

            {/* Scatter dots */}
            {points.map((pt) => {
              const cx = 50 + ((pt.rainfall_mm - minRf) / (maxRf - minRf)) * 520;
              const cy = 190 - ((pt.yield_kg_ha - minY) / (maxY - minY)) * 170;
              if (cx < 50 || cx > 580 || cy < 10 || cy > 190) return null;
              return (
                <circle
                  key={pt.year}
                  cx={cx}
                  cy={cy}
                  r="4.5"
                  fill="#2F7F86"
                  opacity="0.8"
                  className="hover:r-6 hover:fill-[#B5532F] transition-all cursor-pointer"
                >
                  <title>{`${pt.year}: ${pt.rainfall_mm} mm, ${pt.yield_kg_ha} kg/ha`}</title>
                </circle>
              );
            })}
          </svg>

          {/* Axis Labels */}
          <div className="absolute bottom-1 left-12 text-[10px] text-gray-400">
            {toDevanagari(minRf)} {isMarathi ? "मिमी" : "mm"}
          </div>
          <div className="absolute bottom-1 right-4 text-[10px] text-gray-400">
            {toDevanagari(maxRf)} {isMarathi ? "मिमी" : "mm"}
          </div>
          <div className="absolute top-2 left-2 text-[10px] text-gray-400">
            {toDevanagari(maxY)} kg/ha
          </div>
        </div>

        <div className="mt-3 flex items-center justify-between text-[11px] text-[#2B2B26]/60">
          <span>X: {isMarathi ? "मान्सून पाऊस (मिमी)" : "Monsoon Rainfall (mm)"}</span>
          <span>Y: {isMarathi ? "पीक उत्पादन (किलो/हेक्टर)" : "Harvest Yield (kg/ha)"}</span>
          <span>{t("kpi.source_label")}</span>
        </div>
      </div>

      {/* 2. Plain English / Marathi View Card */}
      {outlook && (
        <div className="bg-[#FAF5E9] rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/20 shadow-sm flex flex-col gap-3">
          <div className="flex items-center gap-2 text-[#2F5D3A] font-bold text-sm">
            <HelpCircle className="w-5 h-5 shrink-0" />
            <span>{t("plain_view.title")}</span>
          </div>
          <p className="text-sm lg:text-base text-[#2B2B26] leading-relaxed">
            {responseResult?.interpretation ||
              (isMarathi
                ? "मागील ऐतिहासिक पर्जन्यमान व उत्पादनाच्या विश्लेषणावर आधारित वास्तववादी निष्कर्ष."
                : "Empirical findings based on long-term historical crop yield and monsoon data.")}
          </p>
          <div className="pt-2 border-t border-[#2F5D3A]/10 flex flex-wrap items-center justify-between text-xs text-[#2B2B26]/70 gap-2">
            <span className="font-semibold text-[#B5532F]">
              {isMarathi
                ? "२०२६ संभाव्य उत्पादन श्रेणी: "
                : "2026 Expected Yield Range: "}
              {outlook?.range_80_kg_ha
                ? `${toDevanagari(Math.round(outlook.range_80_kg_ha[0]))} - ${toDevanagari(Math.round(outlook.range_80_kg_ha[1]))}`
                : "—"}{" "}
              kg/ha
            </span>
            <span>
              {outlook?.confidence_disclaimer}
            </span>
          </div>
        </div>
      )}

      {/* 3. Similar Years Table (Analog Seasons) */}
      <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-[#2B2B26] flex items-center gap-2">
              <History className="w-4 h-4 text-[#2F5D3A]" />
              <span>{t("analog.title")}</span>
            </h2>
            <p className="text-xs text-[#2B2B26]/60">
              {isMarathi
                ? "चालू २०२६ मधील -३४% तुटीशी सर्वाधिक साम्य असणारी मागील वर्षे"
                : "Past historical seasons closest to current -34% rainfall deficit"}
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-xl bg-orange-50 text-[#B5532F] border border-[#B5532F]/20">
            {isMarathi ? "सादृश्य वर्षे (Analogs)" : "Top Analog Years"}
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-[#2B2B26]">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500 uppercase tracking-wider text-[10px]">
                <th className="py-2.5 px-3 font-semibold">{t("analog.col_year")}</th>
                <th className="py-2.5 px-3 font-semibold">{t("analog.col_rf")}</th>
                <th className="py-2.5 px-3 font-semibold">{t("analog.col_deficit")}</th>
                <th className="py-2.5 px-3 font-semibold">{t("analog.col_yield")}</th>
                <th className="py-2.5 px-3 font-semibold">{t("analog.col_event")}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {outlook?.analog_years.map((row) => (
                <tr key={row.year} className="hover:bg-gray-50/70 transition-colors">
                  <td className="py-3 px-3 font-bold text-[#2F5D3A]">
                    {toDevanagari(row.year)}
                  </td>
                  <td className="py-3 px-3">
                    {toDevanagari(row.monsoon_rf_mm.toFixed(1))}
                  </td>
                  <td className="py-3 px-3 font-semibold text-[#B5532F]">
                    {toDevanagari(row.deficit_pct.toFixed(1))}%
                  </td>
                  <td className="py-3 px-3 font-bold">
                    {toDevanagari(Math.round(row.yield_kg_ha))}
                  </td>
                  <td className="py-3 px-3 text-[#2B2B26]/80">
                    {row.summary}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

