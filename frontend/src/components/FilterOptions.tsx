"use client";

import { useState, useEffect } from "react";
import { Checkbox, Field, Label } from "@headlessui/react";
import { CheckIcon } from "@heroicons/react/24/outline";

export default function FilterList({ onFilterChange }) {
  const [selectedFilters, setSelectedFilters] = useState({});

  const filters = [
    {
      id: "category",
      label: "Category",
      children: [
        { id: 1, label: "Sticks", enabled: false },
        { id: 2, label: "Skates", enabled: false },
        { id: 3, label: "Goalie", enabled: false },
        { id: 4, label: "Roller", enabled: false },
      ],
    },
    { id: "priceRange", label: "Price Range", children: [] },
    { id: "availability", label: "Availability", children: [] },
  ];

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
      {filters.map((filter) => (
        <div key={filter.id} className="">
          <div>
            <h1 className="bg-black text-white py-2 pl-2">{filter.label}</h1>
          </div>
          <div className="flex flex-col gap-y-2 my-4">
            {filter.children.map((child) => (
              <Field key={child.id} className="flex items-center">
                <Checkbox
                  checked={!!selectedFilters[filter.id]}
                  onChange={(checked) => handleToggleFilter(filter.id, checked)}
                  className="size-5 border border-gray-800 rounded-sm"
                >
                  <CheckIcon className="size-3 stroke-black opacity-0 group-data-[checked]:opacity-100" />
                </Checkbox>
                <Label className="ml-2">{child.label}</Label>
              </Field>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
