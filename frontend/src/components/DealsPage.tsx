"use client";
import DealCard from "@/components/DealCard.tsx";
import SortMenu from "@/components/SortMenu.tsx";
import FilterOptions from "@/components/FilterOptions.tsx";
import Pagination from "@/components/Pagination.tsx";
import { useState, useEffect } from "react";
import { api } from "@/constants/index.tsx";

export default function DealsPage({ title, queryParams }) {
  // Pagination variables
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState();
  const [totalItems, setTotalItems] = useState();
  const [sortOption, setSortOption] = useState(queryParams.sort || null);
  const [maxAvailPrice, setMaxAvailPrice] = useState();
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(queryParams.maxPrice || null);
  const [deals, setDeals] = useState([]);

  // Filter variables
  const [filterOptions, setFilterOptions] = useState([]);
  const [selectedFilters, setSelectedFilters] = useState({
    tags: queryParams.tags || [],
    brands: queryParams.brands || [],
    stores: queryParams.stores || [],
  });

  useEffect(() => {
    async function fetchDeals() {
      // Create query params
      const query = new URLSearchParams();
      query.append("page", currentPage);
      if (sortOption) query.append("sort", sortOption);
      if (minPrice) query.append("min_price", minPrice);
      if (maxPrice) query.append("max_price", maxPrice);

      // Iterate through selected filters
      Object.entries(selectedFilters).forEach(([key, value]) => {
        for (let i = 0; i < value.length; i++) {
          query.append(key, value[i]);
        }
      });

      // Get pagination and filtering info from headers
      const response = await fetch(api + `/deals/?${query.toString()}`);
      setTotalPages(response.headers.get("x-total-page-count"));
      setTotalItems(response.headers.get("x-total-item-count"));
      setMaxAvailPrice(response.headers.get("x-max-price"));

      const filters = [];
      if (response.headers.get("x-avail-sizes")) {
        filters.push({
          title: "Size",
          query: "tags",
          options: JSON.parse(response.headers.get("x-avail-sizes")),
        });
      }
      if (response.headers.get("x-avail-brands")) {
        filters.push({
          title: "Brand",
          query: "brands",
          options: JSON.parse(response.headers.get("x-avail-brands")),
        });
      }
      if (response.headers.get("x-avail-stores")) {
        filters.push({
          title: "Store",
          query: "stores",
          options: JSON.parse(response.headers.get("x-avail-stores")),
        });
      }
      if (response.headers.get("x-avail-tags")) {
        filters.push({
          title: "Tags",
          query: "tags",
          options: JSON.parse(response.headers.get("x-avail-tags")),
        });
      }
      setFilterOptions(filters);

      // Get deals from response content
      const data = await response.json();
      setDeals(data);
    }
    fetchDeals();
  }, [sortOption, selectedFilters, currentPage, minPrice, maxPrice]);

  return (
    <div className="my-4">
      <h1 className="text-3xl font-bold my-7"> {title} </h1>
      <SortMenu sortOption={sortOption} onSortChange={setSortOption} />
      <div className="flex justify-between gap-x-4">
        <FilterOptions
          filterOptions={filterOptions}
          selectedFilters={selectedFilters}
          onFilterChange={setSelectedFilters}
          onMinPriceChange={setMinPrice}
          maxAvailPrice={maxAvailPrice}
          onMaxPriceChange={setMaxPrice}
        />
        <div className="grid grid-rows-1 grid-cols-2 gap-x-6 gap-y-10 md:grid-cols-3 lg:grid-cols-4 xl:gap-x-8">
          {deals.map((deal) => (
            <DealCard key={deal.id} deal={deal} as="div" />
          ))}
        </div>
      </div>
      <div className="flex justify-between items-center">
        <p className="block text-sm text-gray-500 ml-4">
          {totalItems} deals found
        </p>
        <Pagination
          onPageChange={setCurrentPage}
          currentPage={currentPage}
          totalPages={totalPages}
        />
      </div>
    </div>
  );
}
