"use client";
import SearchResultCard from "@/components/SearchResultCard.tsx";
import SortMenu from "@/components/SortMenu.tsx";
import FilterOptions from "@/components/FilterOptions.tsx";
import Pagination from "@/components/Pagination.tsx";
import { useState, useEffect } from "react";
import { api } from "@/constants/index.tsx";

export default function SearchResults({ title, q }) {
  // Pagination variables
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState();
  const [totalItems, setTotalItems] = useState();

  // Sort and order variables
  const [sortOption, setSortOption] = useState("Newest" || null);

  // Filter variables
  const [filterOptions, setFilterOptions] = useState([]);
  const [selectedFilters, setSelectedFilters] = useState({
    tags: [],
    brands: [],
    stores: [],
  });

  // Price range variables
  const [maxAvailPrice, setMaxAvailPrice] = useState();
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState();

  // Deals holder
  const [deals, setDeals] = useState([]);

  useEffect(() => {
    async function fetchDeals() {
      // Create query params
      const query = new URLSearchParams();
      query.append("page", currentPage);
      query.append("q", q);
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
      const res = await fetch(api + `/search/?${query.toString()}`);
      setTotalPages(res.headers.get("x-total-page-count"));
      setTotalItems(res.headers.get("x-total-item-count"));
      setMaxAvailPrice(res.headers.get("x-max-price"));

      const filters = [];
      if (res.headers.get("x-avail-sizes")) {
        filters.push({
          title: "Size",
          query: "tags",
          options: JSON.parse(res.headers.get("x-avail-sizes")),
        });
      }
      if (res.headers.get("x-avail-brands")) {
        filters.push({
          title: "Brand",
          query: "brands",
          options: JSON.parse(res.headers.get("x-avail-brands")),
        });
      }
      if (res.headers.get("x-avail-stores")) {
        filters.push({
          title: "Store",
          query: "stores",
          options: JSON.parse(res.headers.get("x-avail-stores")),
        });
      }
      if (res.headers.get("x-avail-tags")) {
        filters.push({
          title: "Tags",
          query: "tags",
          options: JSON.parse(res.headers.get("x-avail-tags")),
        });
      }
      setFilterOptions(filters);

      // Get deals from response content
      const data = await res.json();
      if (res.ok) {
        setDeals(data);
      } else {
        setDeals([]);
      }
    }
    fetchDeals();
  }, [q, sortOption, selectedFilters, currentPage, minPrice, maxPrice]);

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
        <div className="flex flex-col w-full gap-y-2">
          <div className="flex justify-between text-gray-500">
            <p> Title</p>
            <div className="flex justify-between max-w-72 w-full mr-5">
              <p>Price</p>
              <p>Discount</p>
            </div>
          </div>
          {deals.length == 0 ? (
            <p className="text-md">No deals found. Try again.</p>
          ) : (
            deals.map((deal) => (
              <SearchResultCard key={deal.id} deal={deal} as="div" />
            ))
          )}
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
