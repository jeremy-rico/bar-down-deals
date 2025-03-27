//import Image from "next/image";
import DealsPage from "@/components/DealsPage.tsx";

export default function Home() {
  const queryParams = {
    sort: "Best Selling",
    tags: ["Goalie", "Knee Protectors"],
  };

  return (
    <div className="mx-auto max-w-2xl pt-2 md:max-w-7xl px-2 2xl:px-0">
      <DealsPage title="Goalie Knee Protectors" queryParams={queryParams} />
    </div>
  );
}
