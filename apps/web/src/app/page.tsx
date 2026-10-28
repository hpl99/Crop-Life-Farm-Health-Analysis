"use client";

import React, { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { api, SeasonSummary, DroughtStatus, TehsilGeoJSON } from "@/lib/api";
import { Header } from "@/components/Header";
import { Sidebar } from "@/components/Sidebar";
import { KpiCards } from "@/components/KpiCards";
import { NormalVsActualChart } from "@/components/NormalVsActualChart";
import { SeasonTimeline } from "@/components/SeasonTimeline";
import { TalukaDeepDive } from "@/components/TalukaDeepDive";
import { CorrelationSection } from "@/components/CorrelationSection";
import { AnalysisLab } from "@/components/AnalysisLab";
import { SourceChips } from "@/components/SourceChips";
import { TabBar } from "@/components/TabBar";
import { HomeTab } from "@/components/HomeTab";
import { MapTab } from "@/components/MapTab";
import { MarketTab } from "@/components/MarketTab";

export default function HomePage() {
  const { t, isMarathi } = useI18n();
  const [activeTab, setActiveTab] = useState("insights");
  const [activeSection, setActiveSection] = useState("district-overview");
  const [selectedTehsil, setSelectedTehsil] = useState<number | null>(null);

  const [summary, setSummary] = useState<SeasonSummary | null>(null);
  const [droughtStatus, setDroughtStatus] = useState<DroughtStatus | null>(null);
  const [tehsils, setTehsils] = useState<TehsilGeoJSON | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    Promise.all([
      api.getSeasonSummary(isMarathi ? "mr" : "en"),
      api.getDroughtStatus(isMarathi ? "mr" : "en"),
      api.getTehsils(isMarathi ? "mr" : "en"),
    ])
      .then(([sumData, droughtData, tehsilData]) => {
        if (!isMounted) return;
        setSummary(sumData);
        setDroughtStatus(droughtData);
        setTehsils(tehsilData);
      })
      .catch((err) => {
        console.error("Failed to load initial season data:", err);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [isMarathi]);

  const handleReadAloud = () => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      alert(isMarathi ? "तुमच्या ब्राउझरमध्ये आवाज सुविधा उपलब्ध नाही." : "Text-to-speech is not supported in this browser.");
      return;
    }

    const text = isMarathi
      ? `नागपूर जिल्हा मान्सून २०२६ अहवाल. एकूण पाऊस ६१७.८ मिमी, सरासरीच्या तुलनेत ३४ टक्के तूट. सर्व १४ तालुक्यांमध्ये दुष्काळ जाहीर करण्यात आला आहे.`
      : `Nagpur District Monsoon 2026 Report. Total recorded rainfall 617.8 mm, 34 percent deficit against normal. All 14 tehsils are declared drought-affected.`;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = isMarathi ? "mr-IN" : "en-IN";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  const handleNavigateSection = (secId: string) => {
    setActiveSection(secId);
    const elem = document.getElementById(secId);
    if (elem) {
      elem.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#FAF5E9]">
      {/* 1. Fixed Header (120px desktop, 64px mobile) */}
      <Header
        droughtStatus={droughtStatus}
        tehsils={tehsils}
        selectedTehsil={selectedTehsil}
        onSelectTehsil={setSelectedTehsil}
        onReadAloud={handleReadAloud}
      />

      {/* 2. Main Content Container */}
      <main className="flex-1 max-w-[1440px] w-full mx-auto px-4 lg:px-8 py-6">
        {activeTab === "home" && (
          <div className="space-y-8">
            <HomeTab summary={summary} onNavigateTab={setActiveTab} />
            <SourceChips />
          </div>
        )}

        {activeTab === "map" && (
          <div className="space-y-8">
            <MapTab
              tehsils={tehsils}
              selectedTehsil={selectedTehsil}
              onSelectTehsil={setSelectedTehsil}
            />
            <SourceChips />
          </div>
        )}

        {activeTab === "crops" && (
          <div className="space-y-8">
            <TalukaDeepDive
              tehsils={tehsils}
              selectedTehsil={selectedTehsil}
              onSelectTehsil={setSelectedTehsil}
            />
            <CorrelationSection crop="soybean" />
            <SourceChips />
          </div>
        )}

        {activeTab === "market" && (
          <div className="space-y-8">
            <MarketTab />
            <SourceChips />
          </div>
        )}

        {activeTab === "insights" && (
          <div className="flex flex-col lg:flex-row gap-6">
            {/* Left Sidebar (320px on desktop) */}
            <Sidebar
              tehsils={tehsils}
              selectedTehsil={selectedTehsil}
              onSelectTehsil={setSelectedTehsil}
              activeSection={activeSection}
              onNavigateSection={handleNavigateSection}
              asOfDate={summary?.meta.as_of}
            />

            {/* Right Main Content Stream */}
            <div className="flex-1 min-w-0 space-y-8">
              {/* Level 1: District Overview */}
              <section id="district-overview" className="space-y-6 scroll-mt-24">
                <div className="flex items-center justify-between pb-2 border-b border-[#2F5D3A]/15">
                  <h2 className="text-xl font-extrabold text-[#2F5D3A]">
                    {t("nav.overview")}
                  </h2>
                  <span className="text-xs text-[#2B2B26]/60">
                    {isMarathi ? "हंगाम: जून - सप्टेंबर २०२६" : "Season: Jun - Sep 2026"}
                  </span>
                </div>

                {/* 4 KPI Cards */}
                <KpiCards summary={summary} />

                {/* Normal vs Actual Chart */}
                <NormalVsActualChart summary={summary} />

                {/* Season Journey Timeline */}
                <SeasonTimeline />
              </section>

              {/* Level 2: Taluka Deep-Dive */}
              <section id="taluka-deep-dive" className="scroll-mt-24">
                <TalukaDeepDive
                  tehsils={tehsils}
                  selectedTehsil={selectedTehsil}
                  onSelectTehsil={setSelectedTehsil}
                />
              </section>

              {/* Level 3: Crop Correlation & Analysis Lab */}
              <section id="crop-correlation" className="space-y-6 scroll-mt-24">
                <CorrelationSection crop="soybean" />
                <AnalysisLab />
              </section>

              {/* Footer Provenance Chips */}
              <SourceChips />
            </div>
          </div>
        )}
      </main>

      {/* 3. Fixed Bottom Tab Bar (72px) */}
      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
}
