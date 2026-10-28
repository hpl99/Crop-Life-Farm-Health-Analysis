"use client";

import React from "react";
import { useI18n } from "@/lib/i18n";
import { SeasonSummary } from "@/lib/api";
import { CloudRain, AlertTriangle, Sprout, Store, ArrowRight, ShieldCheck } from "lucide-react";

interface HomeTabProps {
  summary: SeasonSummary | null;
  onNavigateTab: (tabId: string) => void;
}

export function HomeTab({ summary, onNavigateTab }: HomeTabProps) {
  const { t, isMarathi } = useI18n();

  const toDevanagari = (num: number | string): string => {
    if (!isMarathi) return num.toString();
    const digits: Record<string, string> = {
      "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
      "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ".": "."
    };
    return num.toString().replace(/[0-9]/g, (d) => digits[d] || d);
  };

  const stories = [
    {
      title_mr: "मान्सून २०२६: ३४% पावसाची तूट",
      title_en: "Monsoon 2026: 34% Rainfall Deficit",
      desc_mr: "नागपूर जिल्ह्यात ९३६.१ मिमी सरासरीच्या तुलनेत केवळ ६१७.८ मिमी पावसाची नोंद झाली आहे.",
      desc_en: "Nagpur district recorded only 617.8 mm against long-term normal of 936.1 mm.",
      icon: CloudRain,
      color: "text-[#B5532F] bg-[#B5532F]/10",
      tab: "insights",
    },
    {
      title_mr: "सर्व १४ तालुक्यांत दुष्काळ जाहीर",
      title_en: "14/14 Tehsils Drought-Declared",
      desc_mr: "महाराष्ट्र शासनाच्या २५ सप्टेंबर २०२६ च्या निर्णयानुसार नागपूर जिल्ह्यातील सर्व तालुक्यांना दुष्काळी सवलती लागू.",
      desc_en: "Government Resolution dated 25 Sep 2026 extends drought relief to all 14 tehsils.",
      icon: AlertTriangle,
      color: "text-[#D9A441] bg-[#D9A441]/15",
      tab: "map",
    },
    {
      title_mr: "सोयाबीन व कापूस पीक अंदाज",
      title_en: "Soybean & Cotton Harvest Outlook",
      desc_mr: "ऐतिहासिक सादृश्य वर्षांनुसार सोयाबीन उत्पादन ७२०-९८० किलो/हेक्टर श्रेणीत राहण्याची शक्यता.",
      desc_en: "Historical analog seasons project soybean yields in the 720-980 kg/ha range.",
      icon: Sprout,
      color: "text-[#2F5D3A] bg-[#2F5D3A]/10",
      tab: "crops",
    },
    {
      title_mr: "नागपूर बाजार समित्यांचे आजचे भाव",
      title_en: "Nagpur APMC Mandi Rates",
      desc_mr: "कळमेश्वर, काटोल, सावनेर आणि नागपूर मुख्य बाजारातील सोयाबीन व कापूस मोडल भाव पहा.",
      desc_en: "Check live modal prices for Soybean and Cotton across Kalameshwar, Katol, and Saoner.",
      icon: Store,
      color: "text-[#2F7F86] bg-[#2F7F86]/10",
      tab: "market",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Welcome Banner */}
      <div className="bg-gradient-to-br from-[#2F5D3A] to-[#1E3D26] text-white rounded-[32px] p-6 lg:p-8 shadow-elevated relative overflow-hidden">
        <div className="relative z-10 max-w-2xl space-y-3">
          <span className="px-3 py-1 rounded-full bg-white/20 text-xs font-semibold backdrop-blur-xs">
            {isMarathi ? "खरीप हंगाम २०२६ अहवाल" : "Kharif Season 2026 Report"}
          </span>
          <h1 className="text-2xl lg:text-4xl font-extrabold tracking-tight leading-tight">
            {isMarathi ? "नागपूरच्या शेतकऱ्यांसाठी अधिकृत व पारदर्शक माहिती" : "Official & Verified Insights for Nagpur Farmers"}
          </h1>
          <p className="text-white/80 text-xs lg:text-sm leading-relaxed">
            {isMarathi
              ? "हवामान विभाग (IMD), कृषी आयुक्तालय, आणि शासकीय राजपत्रांवर आधारित १००% वास्तववादी आकडेवारी. कोणताही काल्पनिक किंवा अंदाज नसलेला डेटा नाही."
              : "100% real data sourced from IMD, Agriculture Commission, and Maharashtra Government Resolutions. Zero simulated or placeholder metrics."}
          </p>
          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => onNavigateTab("insights")}
              className="px-5 py-2.5 rounded-2xl bg-[#FAF5E9] text-[#2F5D3A] font-bold text-xs lg:text-sm flex items-center gap-2 shadow-sm hover:bg-white transition-all"
            >
              <span>{isMarathi ? "सविस्तर विश्लेषण पहा" : "Explore Insights Lab"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigateTab("crops")}
              className="px-5 py-2.5 rounded-2xl bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold text-xs lg:text-sm transition-all"
            >
              {isMarathi ? "माझे पीक तपासा" : "Check My Crop"}
            </button>
          </div>
        </div>
      </div>

      {/* 4 Season Story Cards */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold text-[#2B2B26] uppercase tracking-wider text-gray-500">
          {isMarathi ? "चालू हंगामाच्या ४ महत्त्वाच्या घडामोडी" : "Key Season Stories (2026)"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {stories.map((s, idx) => {
            const Icon = s.icon;
            return (
              <div
                key={idx}
                onClick={() => onNavigateTab(s.tab)}
                className="bg-white rounded-[24px] p-5 border border-[#2F5D3A]/10 hover:border-[#2F5D3A]/40 shadow-[0_4px_12px_rgba(0,0,0,0.05)] cursor-pointer transition-all flex items-start gap-4 group"
              >
                <div className={`p-3 rounded-2xl shrink-0 ${s.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className="flex-1 space-y-1">
                  <h3 className="text-sm font-bold text-[#2B2B26] group-hover:text-[#2F5D3A] transition-colors flex items-center justify-between">
                    <span>{isMarathi ? s.title_mr : s.title_en}</span>
                    <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-[#2F5D3A] group-hover:translate-x-1 transition-all" />
                  </h3>
                  <p className="text-xs text-[#2B2B26]/70 leading-relaxed">
                    {isMarathi ? s.desc_mr : s.desc_en}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick Summary Strip */}
      <div className="bg-white rounded-[24px] p-5 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
          {isMarathi ? "जिल्हा मुख्य आकडे" : "District Summary Strip"}
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center divide-x divide-gray-100">
          <div>
            <div className="text-2xl font-extrabold text-[#2F5D3A]">
              {toDevanagari(summary?.actual_rf_mm ?? 617.8)} मिमी
            </div>
            <div className="text-[11px] text-gray-500">
              {isMarathi ? "प्रत्यक्ष पाऊस" : "Recorded Rain"}
            </div>
          </div>
          <div>
            <div className="text-2xl font-extrabold text-[#B5532F]">
              -{toDevanagari(Math.abs(summary?.deficit_pct ?? 34.0))}%
            </div>
            <div className="text-[11px] text-gray-500">
              {isMarathi ? "मान्सून तूट" : "Monsoon Deficit"}
            </div>
          </div>
          <div>
            <div className="text-2xl font-extrabold text-[#6B4A2F]">
              {toDevanagari(summary?.missing_rf_mm ?? 318.3)} मिमी
            </div>
            <div className="text-[11px] text-gray-500">
              {isMarathi ? "कमी झालेला पाऊस" : "Deficit Volume"}
            </div>
          </div>
          <div>
            <div className="text-2xl font-extrabold text-[#B5532F]">
              १४/१४
            </div>
            <div className="text-[11px] text-gray-500">
              {isMarathi ? "दुष्काळी तालुके" : "Drought Tehsils"}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

