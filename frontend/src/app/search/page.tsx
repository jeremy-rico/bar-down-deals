// app/search/page.tsx (Server Component by default)
import { Suspense } from "react";
import SearchClient from "@/app/search/SearchClient";

export default function SearchPage() {
  return (
    <Suspense fallback={<div>Loading search results...</div>}>
      <SearchClient />
    </Suspense>
  );
}
