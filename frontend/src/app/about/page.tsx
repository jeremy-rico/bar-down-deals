import Link from "next/link";
export default function About() {
  return (
    <div className="mx-auto max-w-2xl pt-2 md:max-w-7xl px-2 2xl:px-0">
      <h1 className="text-3xl font-bold my-7"> About </h1>
      <h2 id="description" className="text-lg font-bold my-2">
        Description
      </h2>
      <p className="indent-4">
        Bar Down Deals is a web scraping app created by Jeremy Rico for the
        purpose of collecting all the best deals on hockey gear from around the
        internet. Every day, our scrapers extract data from several popular
        online stores (see:{" "}
        <Link href="#List of Stores" className="text-blue-500 hover:underline">
          List Of Stores
        </Link>
        ), and accumulate the deals in our database. This makes it your first
        stop when looking to score a deal on a new stick, gloves, and even
        apparel.
      </p>
      <h2 id="How It Works" className="text-lg font-bold my-2">
        How It Works
      </h2>
      <p className="indent-4">
        Our hockey scrapers grab deals from the clearance section of each site
        listed in the List of Stores section. Sometimes, not all information is
        found so you may run into deals with missing information like the
        original price or a picture. Clicking on the link will take you to the
        product page on the store that the deal was found on.
      </p>
      {/*<p className="indent-4">
        Coupons and promos are submitted by users like you! You can create a new
        coupon or promo post by going to the{" "}
        <Link href="/create" className="text-blue-500 hover:underline">
          Create{" "}
        </Link>
        page and creating a coupon or promo there. We will then check the
        validation of the coupon.
      </p>
      */}
      <h2 id="List Of Stores" className="text-lg font-bold my-2">
        List Of Stores
      </h2>
      <p className="indent-4">
        The following is a list of online stores that are scraped by our
        crawlers:
      </p>
      <ul className="pl-12 list-disc">
        <li>Hockey Monkey</li>
        <li>Pure Hockey</li>
        <li>Ice Warehouse</li>
        <li>CCM</li>
        <li>Bauer</li>
        <li>Sherwood</li>
        <li>True</li>
      </ul>
      <h2 id="Reporting Issues" className="text-lg font-bold my-2">
        Reporting Issues
      </h2>
      <p className="indent-4">
        This site is currently in its beta stage. If you run into any issues or
        404 errors please report your issue via the{" "}
        <Link href="/contact" className="text-blue-500 hover:underline">
          Contact{" "}
        </Link>
        page
      </p>
      <h2 id="Disclaimer" className="text-lg font-bold my-2">
        Disclaimer
      </h2>
      <p className="indent-4">
        Bar Down Deals may recieve payment from brands for deals, including
        promoted items
      </p>
    </div>
  );
}
