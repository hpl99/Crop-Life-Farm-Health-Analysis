"use client";

import React, { useState } from "react";
import { useI18n, Language } from "@/lib/i18n";
import { DroughtStatus, TehsilGeoJSON } from "@/lib/api";
import { 
  Languages, 
  AlertTriangle, 
  MapPin, 
  Volume2, 
  SunMedium, 
  Type, 
  ChevronDown 
} from "lucide-react";

interface HeaderProps {
  droughtStatus: DroughtStatus | null;
  tehsils: TehsilGeoJSON | null;
  selectedTehsil: number | null;
  onSelectTehsil: (id: number | null) => void;
  onReadAloud?: () => void;
}

export function Header({
  droughtStatus,
  tehsils,
  selectedTehsil,
  onSelectTehsil,
  onReadAloud,
}: HeaderProps) {
  const { language, setLanguage, t, isMarathi } = useI18n();
  const [highContrast, setHighContrast] = useState(false);
  const [textSize, setTextSize] = useState<"normal" | "large" | "xlarge">("normal");
  const [showTehsilMenu, setShowTehsilMenu] = useState(false);

  const toggleContrast = () => {
    const next = !highContrast;
    setHighContrast(next);
    if (next) {
      document.documentElement.setAttribute("data-theme", "high-contrast");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  };

  const cycleTextSize = () => {
    const next = textSize === "normal" ? "large" : textSize === "large" ? "xlarge" : "normal";
    setTextSize(next);
    if (next === "normal") {
      document.documentElement.removeAttribute("data-text-size");
    } else {
      document.documentElement.setAttribute("data-text-size", next);
    }
  };

  const selectedTehsilObj = tehsils?.features.find(
    (f) => f.properties.tehsil_id === selectedTehsil
  );

  return (
    <header className="sticky top-0 z-50 w-full bg-[#FAF5E9]/95 backdrop-blur-md border-b border-[#2F5D3A]/15 px-4 lg:px-8 py-3 transition-colors">
      <div className="max-w-[1440px] mx-auto flex flex-wrap items-center justify-between gap-3">
        {/* Brand Block */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 lg:w-12 lg:h-12 rounded-2xl bg-[#2F5D3A] flex items-center justify-center text-white font-bold text-xl shadow-md">
            ना
          </div>
          <div>
            <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-[#2F5D3A] leading-tight">
              {t("app.title")}
            </h1>
            <p className="text-xs lg:text-sm text-[#2B2B26]/70 hidden sm:block">
              {t("app.subtitle")}
            </p>
          </div>
        </div>

        {/* Tehsil Picker & Drought Badge */}
        <div className="flex items-center gap-2 lg:gap-3">
          {/* Tehsil Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowTehsilMenu(!showTehsilMenu)}
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white border border-[#2F5D3A]/20 hover:border-[#2F5D3A] text-xs lg:text-sm font-medium text-[#2B2B26] shadow-sm min-h-[44px] transition-all"
              aria-label={t("taluka.select")}
            >
              <MapPin className="w-4 h-4 text-[#2F5D3A]" />
              <span>
                {selectedTehsilObj
                  ? (isMarathi ? selectedTehsilObj.properties.name_mr : selectedTehsilObj.properties.name_en)
                  : t("app.all_talukas")}
              </span>
              <ChevronDown className="w-3.5 h-3.5 text-gray-500" />
            </button>

            {showTehsilMenu && (
              <div className="absolute left-0 mt-1 w-56 max-h-72 overflow-y-auto bg-white rounded-2xl shadow-xl border border-gray-100 p-1 z-50">
                <button
                  onClick={() => {
                    onSelectTehsil(null);
                    setShowTehsilMenu(false);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-xl text-xs lg:text-sm transition-colors ${
                    selectedTehsil === null ? "bg-[#2F5D3A] text-white font-semibold" : "hover:bg-gray-100 text-[#2B2B26]"
                  }`}
                >
                  {t("app.all_talukas")}
                </button>
                {tehsils?.features.map((f) => (
                  <button
                    key={f.properties.tehsil_id}
                    onClick={() => {
                      onSelectTehsil(f.properties.tehsil_id);
                      setShowTehsilMenu(false);
                    }}
                    className={`w-full text-left px-3 py-2 rounded-xl text-xs lg:text-sm transition-colors ${
                      selectedTehsil === f.properties.tehsil_id
                        ? "bg-[#2F5D3A] text-white font-semibold"
                        : "hover:bg-gray-100 text-[#2B2B26]"
                    }`}
                  >
                    {isMarathi ? f.properties.name_mr : f.properties.name_en}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Official Drought Badge */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#B5532F]/10 border border-[#B5532F]/30 text-[#B5532F] text-xs lg:text-sm font-bold min-h-[44px]">
            <AlertTriangle className="w-4 h-4 text-[#B5532F] shrink-0" />
            <span>
              {droughtStatus
                ? (isMarathi ? droughtStatus.status_label_mr : droughtStatus.status_label_en)
                : t("app.drought_badge")}
            </span>
          </div>
        </div>

        {/* Right Tools: Language Toggle & Accessibility */}
        <div className="flex items-center gap-1.5 lg:gap-2">
          {/* Read Aloud Button */}
          {onReadAloud && (
            <button
              onClick={onReadAloud}
              className="p-2 rounded-xl bg-white/80 hover:bg-white border border-[#2F5D3A]/20 text-[#2F5D3A] min-w-[44px] min-h-[44px] flex items-center justify-center transition-all"
              title={t("a11y.read_aloud")}
              aria-label={t("a11y.read_aloud")}
            >
              <Volume2 className="w-4 h-4" />
            </button>
          )}

          {/* Text Size Scale Toggle */}
          <button
            onClick={cycleTextSize}
            className="p-2 rounded-xl bg-white/80 hover:bg-white border border-[#2F5D3A]/20 text-[#2B2B26] min-w-[44px] min-h-[44px] flex items-center justify-center font-bold text-xs transition-all"
            title={t("a11y.text_size")}
            aria-label={t("a11y.text_size")}
          >
            <Type className="w-4 h-4" />
          </button>

          {/* High Contrast Toggle */}
          <button
            onClick={toggleContrast}
            className={`p-2 rounded-xl border min-w-[44px] min-h-[44px] flex items-center justify-center transition-all ${
              highContrast
                ? "bg-black text-yellow-300 border-black"
                : "bg-white/80 hover:bg-white border-[#2F5D3A]/20 text-[#2B2B26]"
            }`}
            title={t("a11y.contrast")}
            aria-label={t("a11y.contrast")}
          >
            <SunMedium className="w-4 h-4" />
          </button>

          {/* Bilingual Language Switcher */}
          <div className="flex items-center bg-white/80 border border-[#2F5D3A]/20 rounded-xl p-0.5 min-h-[44px]">
            <button
              onClick={() => setLanguage("mr")}
              className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                isMarathi
                  ? "bg-[#2F5D3A] text-white shadow-sm"
                  : "text-[#2B2B26]/70 hover:text-[#2B2B26]"
              }`}
            >
              मराठी
            </button>
            <button
              onClick={() => setLanguage("en")}
              className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                !isMarathi
                  ? "bg-[#2F5D3A] text-white shadow-sm"
                  : "text-[#2B2B26]/70 hover:text-[#2B2B26]"
              }`}
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

