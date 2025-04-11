import DealCard from "@/components/DealCard.tsx";
import {
  ChevronDoubleRightIcon,
  ChevronRightIcon,
} from "@heroicons/react/24/outline";
import { api } from "@/constants/index.tsx";

export default async function AllDeal() {
  const data = await fetch(api + "/deals/?page=1&limit=20");
  const deals = await data.json();

  return (
    <div id="all deals" className="my-4">
      <a href="/deals" className="flex items-center mb-6">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900 hover:underline">
          All Deals
        </h2>
        <ChevronRightIcon className="size-6 mx-2" />
      </a>
      <div className="grid grid-rows-1 grid-cols-2 gap-x-6 gap-y-10 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 xl:gap-x-8">
        {deals.map((deal: any) => (
          <DealCard key={deal.id} deal={deal} />
        ))}
      </div>
      <div className="flex items-center text-gray-500 mt-5">
        <p className="font-thin text-md">Browse All Deals</p>
        <ChevronDoubleRightIcon className="size-5 mx-1" />
      </div>
    </div>
  );
}
