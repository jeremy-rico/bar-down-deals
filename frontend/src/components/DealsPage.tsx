"use client";
import DealCard from "@/components/DealCard.tsx";
import SortMenu from "@/components/SortMenu.tsx";
import {} from "@heroicons/react/24/outline";
import { api } from "@/constants/index.tsx";
import { useState, useEffect } from "react";

export default function DealsPage({ title, sort }) {
  const [deals, setDeals] = useState([]);
  const [sortOption, setSortOption] = useState(sort);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    fetchDeals();
  }, [sortOption]);

  async function fetchDeals() {
    const query = new URLSearchParams(); // TODO: let instead of const?
    if (sortOption.sort) query.append("sort", sortOption.sort);
    if (sortOption.order) query.append("order", sortOption.order);
    Object.entries(filters).forEach(([key, value]) => {
      if (value) query.append(key, value);
    });

    const response = await fetch(api + `/deals/?${query.toString()}`);
    const data = await response.json();
    setDeals(data);
  }

  return (
    <div className="my-4">
      <h1 className="text-3xl font-bold mb-2"> {title} </h1>
      <SortMenu sort={sortOption} onSortChange={setSortOption} />
      <div className="flex">
        <div className="">
          <h1> filter </h1>
          <p>option1</p>
          <p>option1</p>
          <p>option1</p>
          <p>option1</p>
        </div>
        <div className="grid grid-rows-1 grid-cols-2 gap-x-6 gap-y-10 md:grid-cols-3 lg:grid-cols-4 xl:gap-x-8">
          {deals.map((deal) => (
            <DealCard key={deal.id} deal={deal} as="div" />
          ))}
        </div>
      </div>
      <div className="">next page here</div>
    </div>
  );
}
