"use client";
import DealCard from "@/components/DealCard.tsx";
import SortMenu from "@/components/SortMenu.tsx";
import FilterOptions from "@/components/FilterOptions.tsx";
import Pagination from "@/components/Pagination.tsx";
import { useState, useEffect } from "react";
import { api } from "@/constants/index.tsx";

type FilterOption = {
  title: string;
  query: string;
  options: string[];
};
type Props = {
  title: string;
  queryParams: {
    sort?: string;
    maxPrice?: number;
    tags?: string[];
    brands?: string[];
    stores?: string[];
  };
};
export default function DealsPage({ title, queryParams }: Props) {
  // Pagination variables
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalItems, setTotalItems] = useState(0);
  const [sortOption, setSortOption] = useState(queryParams.sort || "Popular");
  const [maxAvailPrice, setMaxAvailPrice] = useState<number>();
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(queryParams.maxPrice || undefined);
  const [deals, setDeals] = useState([]);

  // Filter variables
  const [filterOptions, setFilterOptions] = useState<FilterOption[]>([]);
  const [selectedFilters, setSelectedFilters] = useState({
    tags: queryParams.tags || [],
    brands: queryParams.brands || [],
    stores: queryParams.stores || [],
  });

  useEffect(() => {
    async function fetchDeals() {
      // Create query params
      const query = new URLSearchParams();
      query.append("page", currentPage.toString());
      if (sortOption) query.append("sort", sortOption);
      if (minPrice) query.append("min_price", minPrice.toString());
      if (maxPrice) query.append("max_price", maxPrice.toString());

      // Iterate through selected filters
      Object.entries(selectedFilters).forEach(([key, value]) => {
        for (let i = 0; i < value.length; i++) {
          query.append(key, value[i]);
        }
      });

      // Get pagination and filtering info from headers
      const response = await fetch(api + `/deals/?${query.toString()}`);
      setTotalPages(Number(response.headers.get("x-total-page-count")));
      setTotalItems(Number(response.headers.get("x-total-item-count")));
      setMaxAvailPrice(Number(response.headers.get("x-max-price")));

      const filterOptions = [];
      if (response.headers.get("x-avail-sizes")) {
        filterOptions.push({
          title: "Size",
          query: "tags",
          options: JSON.parse(response.headers.get("x-avail-sizes") || ""),
        });
      }
      if (response.headers.get("x-avail-brands")) {
        filterOptions.push({
          title: "Brand",
          query: "brands",
          options: JSON.parse(response.headers.get("x-avail-brands") || ""),
        });
      }
      if (response.headers.get("x-avail-stores")) {
        filterOptions.push({
          title: "Store",
          query: "stores",
          options: JSON.parse(response.headers.get("x-avail-stores") || ""),
        });
      }
      if (response.headers.get("x-avail-tags")) {
        filterOptions.push({
          title: "Tags",
          query: "tags",
          options: JSON.parse(response.headers.get("x-avail-tags") || ""),
        });
      }
      setFilterOptions(filterOptions);

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
          setCurrentPage={setCurrentPage}
        />
        <div className="grid grid-rows-1 grid-cols-2 gap-x-6 gap-y-10 md:grid-cols-3 lg:grid-cols-4 xl:gap-x-8">
          {deals.map((deal: any) => (
            <DealCard key={deal.id} deal={deal} />
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
