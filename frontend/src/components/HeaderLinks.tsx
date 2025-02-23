import Link from "next/link";
import { headerLinks } from "@/constants/index.tsx";

export default function HeaderLinks() {
  const links = headerLinks.map((headerLinks) => (
    <li key={headerLinks.id}>
      <Link href={headerLinks.href}>{headerLinks.title}</Link>
    </li>
  ));
  return (
    <div className="flex items-center">
      <ul className="hidden md:flex text-white text-sm md:text-lg lg:text-xl whitespace-nowrap gap-x-5 ">
        {links}
      </ul>
    </div>
  );
}
