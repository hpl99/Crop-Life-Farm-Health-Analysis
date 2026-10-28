"use client";

import React from "react";
import { useI18n } from "@/lib/i18n";
import { Home, Map, Sprout, Store, MoreHorizontal } from "lucide-react";

interface TabBarProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
}

export function TabBar({ activeTab, onTabChange }: TabBarProps) {
  const { t } = useI18n();

  const tabs = [
    { id: "home", label: t("nav.home"), icon: Home },
    { id: "map", label: t("nav.map"), icon: Map },
    { id: "crops", label: t("nav.crops"), icon: Sprout },
    { id: "market", label: t("nav.market"), icon: Store },
    { id: "insights", label: t("nav.insights"), icon: MoreHorizontal },
  ];

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-50 h-[72px] bg-white/95 backdrop-blur-md border-t border-[#2F5D3A]/15 px-2 flex items-center justify-around shadow-[0_-4px_16px_rgba(0,0,0,0.06)]"
      role="navigation"
      aria-label="Bottom Navigation"
    >
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex flex-col items-center justify-center flex-1 h-full min-w-[48px] min-h-[48px] py-1 transition-all ${
              isActive
                ? "text-[#2F5D3A] font-bold scale-105"
                : "text-[#2B2B26]/60 hover:text-[#2B2B26] font-medium"
            }`}
          >
            <Icon
              className={`w-5 h-5 mb-1 transition-transform ${
                isActive ? "stroke-[2.5px]" : "stroke-[1.8px]"
              }`}
            />
            <span className="text-[11px] truncate">{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
