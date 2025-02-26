import Image from "next/image";
const s3_prefix =
  "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/";
export default function DealCard({ deal }) {
  return (
    <div className="group relative">
      {/* Product Image */}
      <Image
        src={s3_prefix + deal.product.image_url}
        width={200}
        height={200}
        alt="product image"
        placeholder="empty" // "empty" | "blur" | "data:image/..."
        className="aspect-square w-full rounded-md bg-gray-200 object-cover group-hover:opacity-75 "
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
          <div className="flex items-center gap-x-3">
            <p className="text-md font-extralight line-through text-gray-500">
              ${deal.original_price}
            </p>
            <p className="hidden md:block whitespace-nowrap text-md font-bold text-red-500">
              You save {deal.discount}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
