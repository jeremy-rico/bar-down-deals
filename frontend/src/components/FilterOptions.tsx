"use client";

import PriceRange from "@/components/PriceRange.tsx";
import Accordian from "@/components/Accordian.tsx";
import React from "react";

type FilterOption = {
  title: string;
  query: string;
  options: string[];
};
interface SelectedFilters {
  [key: string]: string[];
}
type Props = {
  filterOptions: FilterOption[];
  selectedFilters: SelectedFilters;
  onFilterChange: React.Dispatch<
    React.SetStateAction<{
      tags: string[];
      brands: string[];
      stores: string[];
      [key: string]: string[];
    }>
  >;
  onMinPriceChange: React.Dispatch<React.SetStateAction<number>>;
  maxAvailPrice?: number;
  onMaxPriceChange: React.Dispatch<React.SetStateAction<number | undefined>>;
  setCurrentPage: React.Dispatch<React.SetStateAction<number>>;
};
export default function FilterOptions({
  filterOptions,
  selectedFilters,
  onFilterChange,
  onMinPriceChange,
  maxAvailPrice,
  onMaxPriceChange,
  setCurrentPage,
}: Props) {
  const toggleFilter = (query: string, option: string): void => {
    setCurrentPage(1);
    onFilterChange((prev) => ({
      ...prev, // Keep the rest of the filters
      [query]: prev[query]?.includes(option)
        ? prev[query].filter((item) => item !== option) // Remove if exists
        : [...(prev[query] || []), option], // Add if not exists
    }));
  };

  return (
    <div className="flex-grow max-w-56">
      {filterOptions.map((filter, index) => (
        <div key={index} className="">
          <Accordian
            filter={filter}
            selectedFilters={selectedFilters}
            toggleFilter={toggleFilter}
          />
        </div>
      ))}
      <PriceRange
        onMinPriceChange={onMinPriceChange}
        maxAvailPrice={maxAvailPrice}
        onMaxPriceChange={onMaxPriceChange}
      />
    </div>
  );
}
