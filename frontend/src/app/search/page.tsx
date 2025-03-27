//import Image from "next/image";
"use client";
import SearchResults from "@/components/SearchResults.tsx";
import { useSearchParams } from "next/navigation";

export default function Search() {
  const searchParams = useSearchParams();
  const q = searchParams.get("q");
  return (
    <div className="mx-auto max-w-2xl pt-2 md:max-w-7xl px-2 2xl:px-0">
      <SearchResults title={`Results for "${q}"`} q={q} />
    </div>
  );
}
