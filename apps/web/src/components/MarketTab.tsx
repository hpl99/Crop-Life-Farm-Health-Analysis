"use client";

import React, { useState, useEffect } from "react";
import { useI18n } from "@/lib/i18n";
import { Store, TrendingUp, Search, Calendar, ChevronRight } from "lucide-react";

interface MandiPrice {
  market_id: string;
  apmc_name_en: string;
  apmc_name_mr: string;
  crop_id: string;
  price_date: string;
  arrivals_qtl?: number;
  min_price?: number;
  max_price?: number;
  modal_price?: number;
}

export function MarketTab() {
  const { t, isMarathi } = useI18n();
  const [prices, setPrices] = useState<MandiPrice[]>([]);
  const [selectedCrop, setSelectedCrop] = useState<string>("all");
  const [searchMarket, setSearchMarket] = useState("");
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

    const query = selectedCrop !== "all" ? `?crop=${selectedCrop}&limit=80` : `?limit=80`;
    fetch(`/api/v1/market/prices${query}`, {
      headers: { "Accept-Language": isMarathi ? "mr" : "en" },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!isMounted) return;
        setPrices(data.prices || []);
      })
      .catch((err) => console.error("Error loading mandi prices:", err))
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [selectedCrop, isMarathi]);

  const filteredPrices = prices.filter((p) => {
    const marketName = isMarathi ? p.apmc_name_mr : p.apmc_name_en;
    return marketName.toLowerCase().includes(searchMarket.toLowerCase());
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-[24px] p-5 lg:p-6 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <h1 className="text-xl font-bold text-[#2F5D3A] flex items-center gap-2">
              <Store className="w-5 h-5 text-[#2F5D3A]" />
              <span>{isMarathi ? "नागपूर कृषी उत्पन्न बाजार समित्या (APMC)" : "Nagpur Mandi Market Prices"}</span>
            </h1>
            <p className="text-xs text-[#2B2B26]/60">
              {isMarathi
                ? "Agmarknet व MSAMB द्वारे पडताळलेले अधिकृत बाजारभाव व आवक"
                : "Verified APMC arrivals and modal prices from Agmarknet & MSAMB"}
            </p>
          </div>

          {/* Crop Selector Tabs */}
          <div className="flex bg-[#FAF5E9] p-1 rounded-2xl border border-[#2F5D3A]/15 text-xs font-bold">
            <button
              onClick={() => setSelectedCrop("all")}
              className={`px-3 py-1.5 rounded-xl transition-all ${
                selectedCrop === "all" ? "bg-[#2F5D3A] text-white" : "text-[#2B2B26]/70"
              }`}
            >
              {isMarathi ? "सर्व पिके" : "All Crops"}
            </button>
            <button
              onClick={() => setSelectedCrop("soybean")}
              className={`px-3 py-1.5 rounded-xl transition-all ${
                selectedCrop === "soybean" ? "bg-[#2F5D3A] text-white" : "text-[#2B2B26]/70"
              }`}
            >
              {isMarathi ? "सोयाबीन" : "Soybean"}
            </button>
            <button
              onClick={() => setSelectedCrop("cotton")}
              className={`px-3 py-1.5 rounded-xl transition-all ${
                selectedCrop === "cotton" ? "bg-[#2F5D3A] text-white" : "text-[#2B2B26]/70"
              }`}
            >
              {isMarathi ? "कापूस" : "Cotton"}
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchMarket}
            onChange={(e) => setSearchMarket(e.target.value)}
            placeholder={isMarathi ? "बाजार समिती शोधा (उदा. काटोल, कळमेश्वर, सावनेर...)" : "Search market (e.g. Katol, Kalameshwar, Saoner...)"}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 text-xs text-[#2B2B26] focus:bg-white focus:outline-hidden focus:border-[#2F5D3A] transition-all"
          />
        </div>
      </div>

      {/* Mandi Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredPrices.map((p, idx) => (
          <div
            key={idx}
            className="bg-white rounded-[24px] p-5 border border-[#2F5D3A]/10 shadow-[0_4px_12px_rgba(0,0,0,0.05)] space-y-3 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-sm text-[#2B2B26]">
                  {isMarathi ? p.apmc_name_mr : p.apmc_name_en}
                </span>
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-[#2F5D3A]/10 text-[#2F5D3A] font-bold uppercase">
                  {p.crop_id}
                </span>
              </div>
              <div className="text-[11px] text-gray-500 flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                <span>{p.price_date}</span>
              </div>
            </div>

            <div className="bg-[#FAF5E9]/50 p-3 rounded-2xl border border-gray-100 flex items-center justify-between">
              <div>
                <span className="text-[10px] text-gray-500 block uppercase font-medium">
                  {isMarathi ? "मोडल भाव (Modal Price)" : "Modal Price"}
                </span>
                <span className="text-xl font-extrabold text-[#2F5D3A]">
                  ₹{toDevanagari(p.modal_price ?? "—")}
                </span>
                <span className="text-[10px] text-gray-500 ml-1">
                  /{isMarathi ? "क्विंटल" : "qtl"}
                </span>
              </div>

              {p.arrivals_qtl && (
                <div className="text-right">
                  <span className="text-[10px] text-gray-500 block">
                    {isMarathi ? "एकूण आवक" : "Arrivals"}
                  </span>
                  <span className="text-xs font-bold text-[#6B4A2F]">
                    {toDevanagari(p.arrivals_qtl)} {isMarathi ? "क्विंटल" : "qtl"}
                  </span>
                </div>
              )}
            </div>

            <div className="flex items-center justify-between text-[11px] text-gray-600 pt-1">
              <span>
                {isMarathi ? "किमान" : "Min"}: ₹{toDevanagari(p.min_price ?? "—")}
              </span>
              <span>
                {isMarathi ? "कमाल" : "Max"}: ₹{toDevanagari(p.max_price ?? "—")}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

