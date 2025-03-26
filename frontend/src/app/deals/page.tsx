//import Image from "next/image";
import DealsPage from "@/components/DealsPage.tsx";
import { sort_options } from "@/constants/index.tsx";
import { api } from "@/constants/index.tsx";

export default function Home() {
  const baseQuery = api + "/deals/?";
  return (
    <div className="mx-auto max-w-2xl pt-2 md:max-w-7xl px-2 2xl:px-0">
      <DealsPage
        baseQuery={baseQuery}
        title="All Deals"
        sort={sort_options[0]}
      />
    </div>
  );
}
