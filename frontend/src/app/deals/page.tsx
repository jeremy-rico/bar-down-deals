//import Image from "next/image";
import DealsPage from "@/components/DealsPage.tsx";
import { sort_options } from "@/constants/index.tsx";

export default function Home() {
  return (
    <div className="mx-auto max-w-2xl pt-2 md:max-w-7xl px-2 2xl:px-0">
      <DealsPage title="All Deals" sort={sort_options[0]} />
    </div>
  );
}
