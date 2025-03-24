"use client";

import { useState, useEffect } from "react";
import { Input, Checkbox, Field, Label } from "@headlessui/react";
import { CheckIcon } from "@heroicons/react/24/outline";

export default function FilterList({
  filterOptions,
  selectedFilters,
  onFilterChange,
}) {
  function handleToggleFilter(filterId, value) {
    setSelectedFilters((prevFilters) => ({
      ...prevFilters,
      [filterId]: value,
    }));
  }

  useEffect(() => {
    onFilterChange(selectedFilters);
  }, [selectedFilters, onFilterChange]);

  return (
    <div className="flex-grow max-w-56">
      {filterOptions.map((filter, index) => (
        <div key={index} className="">
          <div>
            <h1 className="bg-black text-white py-2 pl-2">{filter.label}</h1>
          </div>
          <div className="flex flex-col gap-y-2 my-4">
            {filter.children.map((child, child_index) => (
              <Field key={child_index} className="flex items-center">
                <Checkbox
                  checked={child.enabled}
                  onChange={() => handleToggleFilter()}
                  className="group size-5 border border-gray-800 rounded-sm"
                >
                  <CheckIcon className="hidden size-5 group-data-[checked]:block" />
                </Checkbox>
                <Label className="ml-2">{child.label}</Label>
              </Field>
            ))}
          </div>
        </div>
      ))}
      <div className="">
        <h1 className="bg-black text-white py-2 pl-2">Price Range</h1>
        <div className="flex justify-between items-center mt-2">
          <p className="text-sm">$</p>
          <Input
            name="minPrice"
            type="number"
            min="1"
            placeholder="Min"
            className="w-20 rounded-sm py-1 px-1"
          />
          -<p className="text-sm">$</p>
          <Input
            name="maxPrice"
            type="number"
            min="1"
            placeholder="Max"
            className="w-20 rounded-sm py-1 px-1"
          />
        </div>
      </div>
      {selectedFilters.map((selected) => ({ selected }))}
    </div>
  );
}
