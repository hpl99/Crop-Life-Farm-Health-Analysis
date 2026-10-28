"use client";

import React, { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { api } from "@/lib/api";
import { FlaskConical, Download, CheckCircle, FileSpreadsheet } from "lucide-react";

export function AnalysisLab() {
  const { t, isMarathi } = useI18n();
  const [stats, setStats] = useState<any[]>([]);
  const [corr, setCorr] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    Promise.all([
      api.getLabDescribe("soybean", isMarathi ? "mr" : "en"),
      api.getLabCorrelation("soybean", isMarathi ? "mr" : "en"),
    ])
      .then(([descData, corrData]) => {
        if (!isMounted) return;
        setStats(descData.metrics || []);
        setCorr(corrData.analysis || null);
      })
      .catch((err) => {
        console.error("Failed to load lab data:", err);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [isMarathi]);

  const handleDownloadCsv = () => {
    window.open("/api/v1/export.csv", "_blank");
  };

  return (
    <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)] space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-gray-100">
        <div>
          <h2 className="text-base font-bold text-[#2B2B26] flex items-center gap-2">
            <FlaskConical className="w-4 h-4 text-[#2F5D3A]" />
            <span>{t("lab.title")}</span>
          </h2>
          <p className="text-xs text-[#2B2B26]/60">
            {isMarathi
              ? "विद्यार्थी, कृषी अभ्यासक व धोरणकर्त्यांसाठी पारदर्शक सांख्यिकी प्रयोगशाळा"
              : "Educational statistical diagnostics & verified historical data exports"}
          </p>
        </div>

        {/* Download Full CSV Dataset Button */}
        <button
          onClick={handleDownloadCsv}
          className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-[#2F5D3A] hover:bg-[#2F5D3A]/90 text-white font-semibold text-xs transition-all shadow-sm"
        >
          <Download className="w-4 h-4" />
          <span>{t("lab.btn_download")}</span>
        </button>
      </div>

      {/* Descriptive Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {stats.map((s, idx) => (
          <div
            key={idx}
            className="p-4 rounded-2xl bg-[#FAF5E9]/50 border border-gray-200/70 text-xs space-y-2"
          >
            <div className="font-bold text-[#2F5D3A] border-b pb-1.5 flex items-center justify-between">
              <span>{s.label}</span>
              <span className="text-[11px] text-gray-500 font-normal">
                N = {s.count}
              </span>
            </div>
            <div className="grid grid-cols-3 gap-2 text-[11px]">
              <div>
                <span className="text-gray-500 block">
                  {isMarathi ? "सरासरी (Mean)" : "Mean"}:
                </span>
                <span className="font-semibold">{s.mean}</span>
              </div>
              <div>
                <span className="text-gray-500 block">
                  {isMarathi ? "मध्यक (Median)" : "Median"}:
                </span>
                <span className="font-semibold">{s.median}</span>
              </div>
              <div>
                <span className="text-gray-500 block">
                  {isMarathi ? "प्रमाण विचलन (StdDev)" : "StdDev"}:
                </span>
                <span className="font-semibold">{s.std_dev}</span>
              </div>
              <div>
                <span className="text-gray-500 block">
                  {isMarathi ? "किमान (Min)" : "Min"}:
                </span>
                <span className="font-semibold">{s.min}</span>
              </div>
              <div>
                <span className="text-gray-500 block">
                  {isMarathi ? "कमाल (Max)" : "Max"}:
                </span>
                <span className="font-semibold">{s.max}</span>
              </div>
              <div>
                <span className="text-gray-500 block">
                  {isMarathi ? "विषमता (Skew)" : "Skewness"}:
                </span>
                <span className="font-semibold">{s.skewness}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Key Analytical Findings */}
      {corr && (
        <div className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200 text-xs text-emerald-950 space-y-2">
          <div className="font-bold flex items-center gap-1.5">
            <CheckCircle className="w-4 h-4 text-emerald-700" />
            <span>
              {isMarathi
                ? "सांख्यिकी निष्कर्ष व पडताळणी"
                : "Statistical Diagnostics Summary"}
            </span>
          </div>
          <p className="leading-relaxed text-[11px]">
            {isMarathi
              ? corr.plain_takeaway_mr
              : corr.plain_takeaway_en}
          </p>
          <div className="flex gap-4 text-[10px] text-emerald-800 pt-1 border-t border-emerald-200/60">
            <span>Pearson r: {corr.pearson_r.toFixed(3)} (p = {corr.pearson_p_value.toFixed(4)})</span>
            <span>Spearman rho: {corr.spearman_rho.toFixed(3)} (p = {corr.spearman_p_value.toFixed(4)})</span>
          </div>
        </div>
      )}
    </div>
  );
}

