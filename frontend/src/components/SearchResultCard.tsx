import Image from "next/image";
export default function DealCard({ deal }) {
  return (
    <div className="group relative w-full h-24 px-2 py-2 bg-white rounded shadow">
      <div className="flex justify-between">
        <div className="flex">
          {/* Product Image */}
          <Image
            src={deal.product.image_url}
            width={200}
            height={200}
            alt={deal.product.name}
            placeholder="empty" // "empty" | "blur" | "data:image/..."
            className="aspect-square w-20 rounded-md bg-gray-200 object-cover group-hover:opacity-75 overflow-hidden"
          />

          {/* Product Info */}
          <div className="ml-4">
            <h3 className="text-md text-gray-800">
              <a href={deal.url}>
                <span aria-hidden="true" className="absolute inset-0" />
                {deal.product.name}
              </a>
            </h3>
            <p className="text-sm text-gray-400">by {deal.website.name}</p>
          </div>
        </div>

        {/* Price Info */}
        <div
          id="price info"
          className="flex w-full max-w-72 justify-between mr-5"
        >
          <div className="">
            <p className="text-lg font-extrabold text-red-500 ">
              ${deal.price}
            </p>
            {deal.original_price && (
              <p className="text-md font-extralight line-through text-gray-500">
                ${deal.original_price}
              </p>
            )}
          </div>
          {deal.original_price && (
            <div>
              <p className="whitespace-nowrap text-2xl font-bold text-red-500">
                {Math.round(deal.discount)}%
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
