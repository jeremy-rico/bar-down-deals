"use client";

import { useState } from "react";
import { Input, Field, Button } from "@headlessui/react";

export default function PriceRange({
  onMinPriceChange,
  maxAvailPrice,
  onMaxPriceChange,
}) {
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(maxAvailPrice);
  const submitPriceRange = () => {
    onMinPriceChange(minPrice);
    onMaxPriceChange(maxPrice);
  };
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      submitPriceRange(); // Trigger submit on Enter key press
    }
  };
  return (
    <div className="">
      <h1 className="bg-black text-white py-2 pl-2 rounded">Price Range</h1>
      <Field>
        <div className="flex justify-between items-center mt-2">
          <p className="text-sm">$</p>
          <Input
            name="minPrice"
            type="number"
            min="0"
            max={maxAvailPrice}
            placeholder="Min"
            onKeyDown={handleKeyDown}
            onChange={(e) => setMinPrice(e.target.value)}
            className="w-24 rounded-sm py-1 px-1"
          />
          -<p className="text-sm">$</p>
          <Input
            name="maxPrice"
            type="number"
            min="1"
            max={maxAvailPrice}
            placeholder="Max"
            onKeyDown={handleKeyDown}
            onChange={(e) => setMaxPrice(e.target.value)}
            className="w-24 rounded-sm py-1 px-1"
          />
        </div>
        <div className="flex justify-end items-center mt-2">
          <Button
            onClick={submitPriceRange}
            className="bg-gray-600 text-white rounded px-3 py-1 mx-1"
          >
            GO
          </Button>
        </div>
      </Field>
    </div>
  );
}
