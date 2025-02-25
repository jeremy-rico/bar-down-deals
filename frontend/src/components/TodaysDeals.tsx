const deals = [
  {
    id: 1,
    product: {
      id: 1,
      name: "Bauer Nexus Senior Hockey Stick",
      brand: "Bauer",
      image_url: "/bauer-hockey-stick-nexus-sync-sr_1.webp",
      description: "A very cool hockey stick",
    },
    website: {
      id: 1,
      name: "Hockey Site",
      url: "https://www.hockesite.com",
    },
    price: 198.99,
    original_price: 205.89,
    discount: 23.0,
    href: "https://www.hockeymonkey.com/bauer-hockey-stick-nexus-sync-sr.html",
    last_scraped: 1212412,
  },
  {
    id: 2,
    product: {
      id: 1,
      name: "Bauer Nexus Senior Hockey Stick",
      brand: "Bauer",
      image_url: "/bauer-hockey-stick-nexus-sync-sr_1.webp",
      description: "A very cool hockey stick",
    },
    website: {
      id: 1,
      name: "Hockey Site",
      url: "https://www.hockesite.com",
    },
    price: 198.99,
    original_price: 205.89,
    discount: 23.08,
    href: "https://www.hockeymonkey.com/bauer-hockey-stick-nexus-sync-sr.html",
    last_scraped: 1212412,
  },
];

import DealCard from "@/components/DealCard.tsx";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

export default function TodayDeal() {
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
