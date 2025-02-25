import DealCard from "@/components/DealCard.tsx";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

export default async function TodayDeal() {
  const data = await fetch("http://13.52.178.97:8000/deals");
  const deals = await data.json();

  return (
    <div id="todays deals" className="my-4">
      <a href="/deals/today" className="flex items-center">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">
          Today's Deals
        </h2>
        <ChevronRightIcon className="size-6 mx-2" />
      </a>
      <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
        {deals.map((deal) => (
          <DealCard key={deal.id} deal={deal} as="div" />
        ))}
      </div>
    </div>
  );
}
