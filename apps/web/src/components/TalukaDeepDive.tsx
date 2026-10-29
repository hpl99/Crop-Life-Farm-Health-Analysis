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
    const val = r.rainfall_actual_mm ?? r.rainfall_mm ?? 0;
    const isMonsoon = r.is_monsoon ?? (r.month >= 6 && r.month <= 9);
    if (recentRainfallYears.includes(r.year) && isMonsoon) {
      rainfallByYear[r.year] = (rainfallByYear[r.year] || 0) + val;
    }
  });

  const crops = [
    { id: "soybean", label_mr: "सोयाबीन", label_en: "Soybean" },
    { id: "cotton", label_mr: "कापूस", label_en: "Cotton" },
    { id: "rice", label_mr: "भात (धान)", label_en: "Rice" },
  ];

  const selectedFeature = tehsils?.features.find(
    (f) => f.properties.tehsil_id === selectedTehsil
  );
  const selectedTehsilName = selectedFeature
    ? (isMarathi ? selectedFeature.properties.name_mr : selectedFeature.properties.name_en)
    : (isMarathi ? "नागपूर जिल्हा सरासरी" : "Nagpur District Average");
  const normalRf = selectedFeature?.properties.annual_normal_rf_mm ?? 936.1;

  const maxRainfall = Math.max(
    ...recentRainfallYears.map((yr) => rainfallByYear[yr] || 0),
    normalRf,
    1200
  );

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
            <span className="text-xs font-semibold text-[#2F5D3A] bg-[#2F5D3A]/10 px-2.5 py-0.5 rounded-full">
              {selectedTehsilName}
            </span>
          </h2>
          <p className="text-xs text-[#2B2B26]/60">
            {isMarathi
              ? "५ वर्षांचा इतिहास, ऑलिम्पिक सरासरी आणि २०२६ संभाव्य अंदाज"
              : "5-Year History, Olympic Baseline & 2026 Season Outlook"}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Quick Tehsil Selector */}
          <div className="relative">
            <select
              value={selectedTehsil ?? ""}
              onChange={(e) => {
                const val = e.target.value;
                onSelectTehsil(val === "" ? null : Number(val));
              }}
              className="bg-[#FAF5E9] text-xs font-bold text-[#2B2B26] px-3 py-1.5 rounded-xl border border-[#2F5D3A]/20 focus:outline-none focus:ring-2 focus:ring-[#2F5D3A]/30 cursor-pointer"
              aria-label={t("taluka.select")}
            >
              <option value="">{t("app.all_talukas")}</option>
              {tehsils?.features.map((f) => (
                <option key={f.properties.tehsil_id} value={f.properties.tehsil_id}>
                  {isMarathi ? f.properties.name_mr : f.properties.name_en}
                </option>
              ))}
            </select>
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
      </div>

      {/* Grid: Rainfall History (Left) and Crop Yield History with Outlook Bar (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Rainfall 5-Year History */}
        <div className="bg-[#FAF5E9]/40 rounded-2xl p-4 border border-[#2F5D3A]/10 flex flex-col justify-between">
          <div className="flex flex-wrap items-center justify-between gap-1 mb-3">
            <div>
              <span className="text-xs font-bold text-[#2B2B26] block">
                {selectedTehsilName} • {t("taluka.history_title")}
              </span>
              <span className="text-[10px] text-[#2B2B26]/60">
                {isMarathi ? "जून-सप्टेंबर मान्सून प्रत्यक्ष पाऊस" : "Jun-Sep Monsoon Actual Rainfall"}
              </span>
            </div>
            <span className="text-[11px] text-[#2F5D3A] font-bold bg-[#2F5D3A]/10 px-2 py-0.5 rounded-lg">
              {isMarathi ? `दीर्घकालीन सरासरी: ${toDevanagari(normalRf)} मिमी` : `Normal: ${normalRf} mm`}
            </span>
          </div>

          <div className="h-44 flex items-end justify-between gap-2 pt-6 pb-2 px-1 border-b border-gray-200">
            {recentRainfallYears.map((yr) => {
              const val = rainfallByYear[yr] || 0;
              const heightPct = val > 0 ? Math.min(100, (val / (maxRainfall * 1.08)) * 100) : 4;
              return (
                <div key={yr} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end">
                  <span className="text-[10px] font-bold text-[#2B2B26]">
                    {val > 0 ? toDevanagari(Math.round(val)) : "—"}
                  </span>
                  <div
                    className="w-full max-w-[36px] bg-[#2F7F86] rounded-t-lg transition-all duration-500 shadow-sm"
                    style={{ height: `${heightPct}%` }}
                    title={`${selectedTehsilName} (${yr}): ${val > 0 ? val.toFixed(1) : 0} mm`}
                  />
                  <span className="text-[10px] font-semibold text-[#2B2B26]/70">
                    {toDevanagari(yr)}
                  </span>
                </div>
              );
            })}
          </div>

          <div className="pt-2 text-[10px] text-[#2B2B26]/60 flex items-center justify-between">
            <span>
              {isMarathi
                ? (selectedTehsil ? "स्रोत: ERA5 / Open-Meteo (तालुका केंद्र)" : "स्रोत: भारतीय हवामान विभाग (जिल्हा सरासरी)")
                : (selectedTehsil ? "Source: ERA5 Reanalysis (Tehsil Centroid)" : "Source: IMD District Series")}
            </span>
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
          <div className="pt-2 flex flex-col gap-1 text-[10px] text-[#2B2B26]/60">
            <div className="flex items-center justify-between">
              <span className="text-[#B5532F] font-semibold">
                *{t("crop.outlook_disclaimer")}
              </span>
              <span className="text-gray-500">
                {isMarathi ? "८०% संभाव्य विश्वासार्हता श्रेणी" : "80% Prediction Interval"}
              </span>
            </div>
            {selectedTehsil && (
              <p className="text-[9px] text-[#2F5D3A] italic">
                {isMarathi
                  ? `टीप: महाराष्ट्र कृषी विभागाचे पीक कापणी प्रयोग (CCE) केवळ जिल्हा स्तरावर संकलित होतात. त्यामुळे डावीकडील पाऊस ${selectedTehsilName} चा व उजवीकडील पीक आकडेवारी नागपूर जिल्ह्याची आहे.`
                  : `Note: Official Crop Cutting Experiments (CCE) are compiled at district level. Left shows ${selectedTehsilName} rainfall; right shows Nagpur district yield.`}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

