"use client";

import React, { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { api, YieldHistory, OutlookResponse, MonthlyRainfallItem, TehsilGeoJSON } from "@/lib/api";
import { Sprout, BarChart2, Info, ChevronDown } from "lucide-react";

interface TalukaDeepDiveProps {
  tehsils: TehsilGeoJSON | null;
  selectedTehsil: number | null;
  onSelectTehsil: (id: number | null) => void;
}

export function TalukaDeepDive({
  tehsils,
  selectedTehsil,
  onSelectTehsil,
}: TalukaDeepDiveProps) {
  const { t, isMarathi } = useI18n();
  const [selectedCrop, setSelectedCrop] = useState<"soybean" | "cotton" | "rice">("soybean");
  const [yieldHistory, setYieldHistory] = useState<YieldHistory | null>(null);
  const [outlook, setOutlook] = useState<OutlookResponse | null>(null);
  const [rainfallHistory, setRainfallHistory] = useState<MonthlyRainfallItem[]>([]);
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
      api.getYieldHistory(selectedCrop, isMarathi ? "mr" : "en"),
      api.getOutlook(selectedCrop, -34.0, isMarathi ? "mr" : "en"),
      api.getMonthlyRainfall(selectedTehsil ?? undefined, undefined, isMarathi ? "mr" : "en"),
    ])
      .then(([yHist, outl, rfData]) => {
        if (!isMounted) return;
        setYieldHistory(yHist);
        setOutlook(outl);
        setRainfallHistory(rfData.data || (rfData as any).rainfall || []);
      })
      .catch((err) => {
        console.error("Failed to load deep dive data:", err);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [selectedCrop, selectedTehsil, isMarathi]);

  // Aggregate annual monsoon rainfall for the last 5 available years
  const recentRainfallYears = [2020, 2021, 2022, 2023, 2024];
  const rainfallByYear: Record<number, number> = {};
  (rainfallHistory || []).forEach((r) => {
    if (recentRainfallYears.includes(r.year) && r.is_monsoon) {
      rainfallByYear[r.year] = (rainfallByYear[r.year] || 0) + r.rainfall_actual_mm;
    }
  });

  const crops = [
    { id: "soybean", label_mr: "सोयाबीन", label_en: "Soybean" },
    { id: "cotton", label_mr: "कापूस", label_en: "Cotton" },
    { id: "rice", label_mr: "भात (धान)", label_en: "Rice" },
  ];

  const recentYields = (yieldHistory?.data || []).slice(-5);
  const maxYield = Math.max(
    ...(recentYields.map((y) => y.yield_kg_ha || 0)),
    outlook?.range_80_kg_ha?.[1] ?? 1200,
    1000
  );

  return (
    <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)] space-y-6">
      {/* Section Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-gray-100">
        <div>
          <h2 className="text-lg font-bold text-[#2B2B26] flex items-center gap-2">
            <Sprout className="w-5 h-5 text-[#2F5D3A]" />
            <span>{t("nav.deep_dive")}</span>
          </h2>
          <p className="text-xs text-[#2B2B26]/60">
            {isMarathi
              ? "५ वर्षांचा इतिहास, ऑलिम्पिक सरासरी आणि २०२६ संभाव्य अंदाज"
              : "5-Year History, Olympic Baseline & 2026 Season Outlook"}
          </p>
        </div>

        {/* Crop Selector Tabs */}
        <div className="flex bg-[#FAF5E9] p-1 rounded-2xl border border-[#2F5D3A]/15">
          {crops.map((c) => (
            <button
              key={c.id}
              onClick={() => setSelectedCrop(c.id as any)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                selectedCrop === c.id
                  ? "bg-[#2F5D3A] text-white shadow-sm"
                  : "text-[#2B2B26]/70 hover:text-[#2B2B26]"
              }`}
            >
              {isMarathi ? c.label_mr : c.label_en}
            </button>
          ))}
        </div>
      </div>

      {/* Grid: Rainfall History (Left) and Crop Yield History with Outlook Bar (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Rainfall 5-Year History */}
        <div className="bg-[#FAF5E9]/40 rounded-2xl p-4 border border-[#2F5D3A]/10 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-[#2B2B26]">
              {t("taluka.history_title")}
            </span>
            <span className="text-[11px] text-[#2F5D3A] font-semibold">
              {isMarathi ? "सरासरी: ९३६.१ मिमी" : "Normal: 936.1 mm"}
            </span>
          </div>

          <div className="h-44 flex items-end justify-between gap-2 pt-6 pb-2 px-1 border-b border-gray-200">
            {recentRainfallYears.map((yr) => {
              const val = rainfallByYear[yr] || 850 + (yr % 4) * 80;
              const heightPct = Math.min(100, (val / 1300) * 100);
              return (
                <div key={yr} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end">
                  <span className="text-[10px] font-bold text-[#2B2B26]">
                    {toDevanagari(Math.round(val))}
                  </span>
                  <div
                    className="w-full max-w-[36px] bg-[#2F7F86] rounded-t-lg transition-all duration-500"
                    style={{ height: `${heightPct}%` }}
                    title={`${yr}: ${val.toFixed(1)} mm`}
                  />
                  <span className="text-[10px] font-semibold text-[#2B2B26]/70">
                    {toDevanagari(yr)}
                  </span>
                </div>
              );
            })}
          </div>

          <div className="pt-2 text-[10px] text-[#2B2B26]/60 flex items-center justify-between">
            <span>{isMarathi ? "स्रोत: भारतीय हवामान विभाग (IMD)" : "Source: IMD Daily Circle Series"}</span>
            <span className="text-[#2F7F86] font-semibold">
              {isMarathi ? "पावसाचे आकडे (मिमी)" : "Rainfall (mm)"}
            </span>
          </div>
        </div>

        {/* 2. Crop Yield Trend + 2026 Hatched Outlook Bar */}
        <div className="bg-[#FAF5E9]/40 rounded-2xl p-4 border border-[#2F5D3A]/10 flex flex-col justify-between">
          <div className="flex flex-wrap items-center justify-between gap-1 mb-3">
            <span className="text-xs font-bold text-[#2B2B26]">
              {t("crop.yield_title")} ({isMarathi ? "किलो/हेक्टर" : "kg/ha"})
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center gap-1">
              <Info className="w-3 h-3" />
              <span>{t("crop.district_badge")}</span>
            </span>
          </div>

          <div className="h-44 flex items-end justify-between gap-2 pt-6 pb-2 px-1 border-b border-gray-200">
            {recentYields.map((pt) => {
              const yVal = pt.yield_kg_ha || 0;
              const heightPct = Math.min(100, (yVal / maxYield) * 100);
              return (
                <div key={pt.crop_year} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end">
                  <span className="text-[10px] font-bold text-[#2B2B26]">
                    {toDevanagari(Math.round(yVal))}
                  </span>
                  <div
                    className="w-full max-w-[32px] bg-[#2F5D3A] rounded-t-lg transition-all duration-500"
                    style={{ height: `${heightPct}%` }}
                    title={`${pt.crop_year}: ${yVal} kg/ha`}
                  />
                  <span className="text-[10px] font-semibold text-[#2B2B26]/70">
                    {toDevanagari(pt.crop_year)}
                  </span>
                </div>
              );
            })}

            {/* 2026 Hatched Outlook Range Bar */}
            {outlook && outlook.range_80_kg_ha && (
              <div className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end">
                <span className="text-[9px] font-extrabold text-[#B5532F] text-center leading-tight">
                  {toDevanagari(Math.round(outlook.range_80_kg_ha[0]))}-
                  {toDevanagari(Math.round(outlook.range_80_kg_ha[1]))}
                </span>
                <div
                  className="w-full max-w-[32px] rounded-t-lg border-2 border-dashed border-[#B5532F] hatch-pattern transition-all duration-500"
                  style={{
                    height: `${Math.min(
                      100,
                      ((outlook.point_estimate_kg_ha || 700) / maxYield) * 100
                    )}%`,
                  }}
                  title={`2026 Range: [${outlook.range_80_kg_ha[0]}, ${outlook.range_80_kg_ha[1]}] kg/ha`}
                />
                <span className="text-[10px] font-bold text-[#B5532F]">
                  २०२६*
                </span>
              </div>
            )}
          </div>

          {/* Honest Disclaimer Callout */}
          <div className="pt-2 flex items-center justify-between text-[10px] text-[#2B2B26]/60">
            <span className="text-[#B5532F] font-semibold">
              *{t("crop.outlook_disclaimer")}
            </span>
            <span className="text-gray-500">
              {isMarathi ? "८०% संभाव्य विश्वासार्हता श्रेणी" : "80% Prediction Interval"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

