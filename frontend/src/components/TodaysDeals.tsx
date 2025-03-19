import { ChevronRightIcon } from "@heroicons/react/24/outline";
import { api } from "@/constants/index.tsx";
import Carousel from "@/components/Carousel.tsx";

export default async function TodaysDeal() {
  const data = await fetch(
    api + "/deals/?sort_by=discount&added_since=month&page=1&limit=20",
  );
  const deals = await data.json();

  return (
    <div id="todays deals">
      <a href="/deals/today" className="flex items-center mb-6">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900 hover:underline">
          Today's Deals
        </h2>
        <ChevronRightIcon className="size-6 mx-2" />
      </a>
      <Carousel deals={deals} />
    </div>
  );
}
