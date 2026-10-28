"use client";

import React, { useEffect, useState } from "react";
import { useI18n } from "@/lib/i18n";
import { TehsilGeoJSON } from "@/lib/api";
import { 
  BarChart3, 
  Map as MapIcon, 
  TrendingUp, 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  Layers 
} from "lucide-react";

interface SidebarProps {
  tehsils: TehsilGeoJSON | null;
  selectedTehsil: number | null;
  onSelectTehsil: (id: number | null) => void;
  activeSection: string;
  onNavigateSection: (secId: string) => void;
  asOfDate?: string;
}

export function Sidebar({
  tehsils,
  selectedTehsil,
  onSelectTehsil,
  activeSection,
  onNavigateSection,
  asOfDate,
}: SidebarProps) {
  const { t, isMarathi } = useI18n();
  const [isOnline, setIsOnline] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncedText, setLastSyncedText] = useState("आताच / Just now");

  useEffect(() => {
    setIsOnline(navigator.onLine);
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      await new Promise((r) => setTimeout(r, 600));
      setLastSyncedText(new Date().toLocaleTimeString(isMarathi ? "mr-IN" : "en-IN"));
    } finally {
      setIsSyncing(false);
    }
  };

  const navItems = [
    { id: "district-overview", label: t("nav.overview"), icon: BarChart3 },
    { id: "taluka-deep-dive", label: t("nav.deep_dive"), icon: MapIcon },
    { id: "crop-correlation", label: t("nav.correlation"), icon: TrendingUp },
  ];

  return (
    <aside className="w-full lg:w-80 shrink-0 flex flex-col gap-5">
      {/* Mini Tehsil Map Overview Tile */}
      <div className="bg-white rounded-[24px] p-5 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-bold text-[#2B2B26] flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-[#2F5D3A]" />
            <span>{isMarathi ? "नागपूर तालुका नकाशा" : "Nagpur Tehsil Map"}</span>
          </h2>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-[#B5532F]/10 text-[#B5532F] font-semibold">
            १४ तालुके
          </span>
        </div>

        {/* 14 Tehsil Visual Grid */}
        <div className="grid grid-cols-2 gap-2 my-3">
          {tehsils?.features.map((f) => {
            const isSelected = selectedTehsil === f.properties.tehsil_id;
            return (
              <button
                key={f.properties.tehsil_id}
                onClick={() =>
                  onSelectTehsil(isSelected ? null : f.properties.tehsil_id)
                }
                className={`p-2 rounded-xl text-left border transition-all text-xs flex flex-col justify-between ${
                  isSelected
                    ? "bg-[#2F5D3A] text-white border-[#2F5D3A] shadow-sm"
                    : "bg-[#FAF5E9]/50 hover:bg-[#FAF5E9] border-gray-200 text-[#2B2B26]"
                }`}
              >
                <span className="font-semibold truncate">
                  {isMarathi ? f.properties.name_mr : f.properties.name_en}
                </span>
                <span
                  className={`text-[10px] mt-1 ${
                    isSelected ? "text-white/80" : "text-[#B5532F]"
                  }`}
                >
                  {isMarathi ? "दुष्काळग्रस्त" : "Drought"}
                </span>
              </button>
            );
          })}
        </div>

        {/* Legend */}
        <div className="pt-3 border-t border-gray-100 flex items-center justify-between text-[11px] text-[#2B2B26]/70">
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#2F5D3A]" />
            <span>{isMarathi ? "सरासरी" : "Normal"}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#D9A441]" />
            <span>{isMarathi ? "तूट" : "Deficit"}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#B5532F]" />
            <span>{isMarathi ? "गंभीर" : "Severe"}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-[#2F7F86]" />
            <span>{isMarathi ? "अधिक" : "Surplus"}</span>
          </div>
        </div>
      </div>

      {/* Drill-down Navigation */}
      <nav className="bg-white rounded-[24px] p-3 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)] flex flex-col gap-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeSection === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigateSection(item.id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-semibold transition-all ${
                isActive
                  ? "bg-[#2F5D3A] text-white shadow-sm"
                  : "text-[#2B2B26] hover:bg-[#FAF5E9]"
              }`}
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* System Status Card */}
      <div className="bg-white rounded-[24px] p-4 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)] flex flex-col gap-2.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {isOnline ? (
              <Wifi className="w-4 h-4 text-emerald-600" />
            ) : (
              <WifiOff className="w-4 h-4 text-[#B5532F]" />
            )}
            <span className="text-xs font-bold text-[#2B2B26]">
              {isOnline ? t("system.online") : t("system.offline")}
            </span>
          </div>
          <button
            onClick={handleSync}
            disabled={isSyncing}
            className="p-1.5 rounded-lg hover:bg-gray-100 text-gray-600 transition-transform active:rotate-180"
            title={t("system.sync_now")}
            aria-label={t("system.sync_now")}
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? "animate-spin" : ""}`} />
          </button>
        </div>

        <div className="text-[11px] text-[#2B2B26]/60 flex justify-between items-center">
          <span>{t("system.last_synced")}:</span>
          <span className="font-medium text-[#2B2B26]">{lastSyncedText}</span>
        </div>

        {asOfDate && (
          <div className="text-[10px] text-[#2B2B26]/50 pt-2 border-t border-gray-100 truncate">
            {t("kpi.as_of")}
          </div>
        )}
      </div>
    </aside>
  );
}
