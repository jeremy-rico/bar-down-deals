import Image from "next/image";
type Props = {
  deal: any;
};
export default function DealCard({ deal }: Props) {
  return (
    <div className="group relative flex-shrink-0 w-52 lg:w-[238px]">
      {/* Product Image */}
      <Image
        src={deal.product.image_url}
        width={200}
        height={200}
        alt={deal.product.name}
        placeholder="empty" // "empty" | "blur" | "data:image/..."
        className="aspect-square bg-white w-full rounded-md object-contain group-hover:opacity-75 "
      />

      {/* Product Info */}
      <div id="deal info" className="mt-4 flex-col justify-between">
        <div>
          <h3 className="text-md text-gray-800">
            <a href={deal.url}>
              <span aria-hidden="true" className="absolute inset-0" />
              {deal.product.name}
            </a>
          </h3>
          <p className="text-sm text-gray-400">by {deal.website.name}</p>
        </div>

        {/* Price Info */}
        <div id="price info" className="pt-2">
          <p className="text-lg font-extrabold text-red-500 ">${deal.price}</p>
          {deal.original_price && (
            <div className="flex items-center gap-x-3">
              <p className="text-md font-extralight line-through text-gray-500">
                ${deal.original_price}
              </p>
              <p className="hidden md:block whitespace-nowrap text-md font-bold text-red-500">
                You save {Math.round(deal.discount)}%
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
