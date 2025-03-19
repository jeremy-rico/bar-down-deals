//import Image from "next/image";
import DealsPage from "@/components/DealsPage.tsx";
import { sort_options } from "@/constants/index.tsx";

export default function Home() {
  return (
    <div className="mx-auto max-w-2xl px-3 pt-2 md:py-8 md:max-w-7xl 2xl:px-0">
      <DealsPage title="New Deals" sort={sort_options[5]} />
    </div>
  );
}
