"use client";

import { Checkbox, Field, Label } from "@headlessui/react";
import { CheckIcon } from "@heroicons/react/24/outline";
import PriceRange from "@/components/PriceRange.tsx";

export default function FilterOptions({
  filterOptions,
  selectedFilters,
  onFilterChange,
  onMinPriceChange,
  maxAvailPrice,
  onMaxPriceChange,
}) {
  const toggleFilter = (query, option) => {
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
          <div>
            <h1 className="bg-black text-white py-2 pl-2">{filter.title}</h1>
          </div>
          <div className="flex flex-col gap-y-2 my-4">
            {filter.options.map((option, optionIndex) => (
              <Field key={optionIndex} className="flex items-center">
                <Checkbox
                  checked={selectedFilters[filter.query].includes(option)}
                  onChange={() => toggleFilter(filter.query, option)}
                  className="group size-5 border border-gray-800 rounded-sm"
                >
                  <CheckIcon className="hidden size-5 group-data-[checked]:block" />
                </Checkbox>
                <Label className="ml-2">{option}</Label>
              </Field>
            ))}
          </div>
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
