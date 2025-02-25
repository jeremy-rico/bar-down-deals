import Image from "next/image";
export default function DealCard({ deal }) {
  return (
    <div className="group relative">
      {/* Product Image */}
      <Image
        src={deal.product.image_url}
        width={500}
        height={500}
        alt="product image"
        placeholder="empty" // "empty" | "blur" | "data:image/..."
        className="aspect-square w-full rounded-md bg-gray-200 object-cover group-hover:opacity-75 lg:aspect-auto lg:h-80"
      />

      {/* Product Info */}
      <div id="deal info" className="mt-4 flex-col justify-between">
        <div>
          <h3 className="text-md text-gray-800">
            <a href={deal.href}>
              <span aria-hidden="true" className="absolute inset-0" />
              {deal.product.name}
            </a>
          </h3>
        </div>

        {/* Price Info */}
        <div id="price info">
          <p className="text-lg font-extrabold text-red-500 ">${deal.price}</p>
          <div className="flex gap-x-3">
            <p className="text-md font-extralight text-gray-500">
              ${deal.original_price}
            </p>
            <p className="text-md font-bold text-red-500">{deal.discount}%</p>
          </div>
        </div>
      </div>
    </div>
  );
}
