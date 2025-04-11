//import Image from "next/image";
import DealsPage from "@/components/DealsPage.tsx";

export default function Home() {
  const queryParams = {
    sort: "Popular",
    tags: ["Elbow Pads"],
  };

  return (
    <div className="mx-auto max-w-2xl pt-2 md:max-w-7xl px-2 2xl:px-0">
      <DealsPage title="Elbow Pads" queryParams={queryParams} />
    </div>
  );
}
