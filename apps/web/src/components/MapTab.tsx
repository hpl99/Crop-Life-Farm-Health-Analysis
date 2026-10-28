"use client";

import React, { useState } from "react";
import { useI18n } from "@/lib/i18n";
import { TehsilGeoJSON } from "@/lib/api";
import { MapPin, AlertTriangle, Layers, Droplets } from "lucide-react";

interface MapTabProps {
  tehsils: TehsilGeoJSON | null;
  selectedTehsil: number | null;
  onSelectTehsil: (id: number | null) => void;
}

export function MapTab({ tehsils, selectedTehsil, onSelectTehsil }: MapTabProps) {
  const { t, isMarathi } = useI18n();
  const [activeFilter, setActiveFilter] = useState("all");

  const toDevanagari = (num: number | string): string => {
    if (!isMarathi) return num.toString();
    const digits: Record<string, string> = {
      "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
      "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ".": "."
    };
    return num.toString().replace(/[0-9]/g, (d) => digits[d] || d);
  };

  const selectedFeature = tehsils?.features.find(
    (f) => f.properties.tehsil_id === selectedTehsil
  );

  return (
    <div className="space-y-6">
      {/* Map Header */}
      <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-bold text-[#2F5D3A] flex items-center gap-2">
              <Layers className="w-5 h-5 text-[#2F5D3A]" />
              <span>{isMarathi ? "नागपूर जिल्हा तालुका नकाशा व पर्जन्यमान" : "Nagpur Tehsil Map & Drought Status"}</span>
            </h1>
            <p className="text-xs text-[#2B2B26]/60">
              {isMarathi
                ? "सर्व १४ तालुक्यांची भौगोलिक रचना, एलजीडी कोड आणि वार्षिक सरासरी पाऊस"
                : "Geographical distribution, LGD codes, and annual normals across all 14 tehsils"}
            </p>
          </div>

          <span className="px-3 py-1.5 rounded-xl bg-[#B5532F]/10 text-[#B5532F] text-xs font-bold flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4" />
            <span>{isMarathi ? "१४/१४ तालुके दुष्काळ घोषित" : "14/14 Drought Declared"}</span>
          </span>
        </div>
      </div>

      {/* Tehsil Grid / Visual Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tehsils?.features.map((f) => {
          const isSelected = selectedTehsil === f.properties.tehsil_id;
          return (
            <div
              key={f.properties.tehsil_id}
              onClick={() =>
                onSelectTehsil(isSelected ? null : f.properties.tehsil_id)
              }
              className={`p-5 rounded-[24px] border cursor-pointer transition-all flex flex-col justify-between ${
                isSelected
                  ? "bg-[#2F5D3A] text-white border-[#2F5D3A] shadow-md scale-[1.02]"
                  : "bg-white hover:bg-[#FAF5E9]/50 border-[#2F5D3A]/15 text-[#2B2B26] shadow-sm"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-extrabold text-base">
                    {isMarathi ? f.properties.name_mr : f.properties.name_en}
                  </span>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                      isSelected
                        ? "bg-white/20 text-white"
                        : "bg-[#B5532F]/10 text-[#B5532F]"
                    }`}
                  >
                    {isMarathi ? "दुष्काळग्रस्त" : "Drought-Hit"}
                  </span>
                </div>

                <div className="space-y-1 text-xs">
                  <div
                    className={isSelected ? "text-white/80" : "text-gray-500"}
                  >
                    {isMarathi ? "LGD कोड" : "LGD Code"}: {f.properties.lgd_code}
                  </div>
                  <div
                    className={isSelected ? "text-white/80" : "text-gray-500"}
                  >
                    {isMarathi ? "अक्षांश / रेखांश" : "Centroid"}:{" "}
                    {f.properties.centroid_lat.toFixed(2)}°N,{" "}
                    {f.properties.centroid_lon.toFixed(2)}°E
                  </div>
                </div>
              </div>

              <div
                className={`mt-4 pt-3 border-t flex items-center justify-between text-xs ${
                  isSelected ? "border-white/20" : "border-gray-100"
                }`}
              >
                <span className="flex items-center gap-1 font-semibold">
                  <Droplets className="w-3.5 h-3.5" />
                  <span>{isMarathi ? "वार्षिक सरासरी" : "Annual Normal"}:</span>
                </span>
                <span className="font-bold">
                  {f.properties.annual_normal_rf_mm
                    ? `${toDevanagari(f.properties.annual_normal_rf_mm)} mm`
                    : "९३६.१ mm"}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
