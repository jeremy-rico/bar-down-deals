"use client";

import PriceRange from "@/components/PriceRange.tsx";
import Accordian from "@/components/Accordian.tsx";

export default function FilterOptions({
  filterOptions,
  selectedFilters,
  onFilterChange,
  onMinPriceChange,
  maxAvailPrice,
  onMaxPriceChange,
  setCurrentPage,
}) {
  const toggleFilter = (query, option) => {
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
        maxPrice={maxAvailPrice}
        onMaxPriceChange={onMaxPriceChange}
      />
    </div>
  );
}
