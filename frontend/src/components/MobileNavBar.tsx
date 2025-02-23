import { headerLinks, categories } from "@/constants/index.tsx";
import Link from "next/link";

export default function MobileNavBar() {
  const links = headerLinks.map((headerLinks) => (
    <li key={headerLinks.id}>
      <Link href={headerLinks.href}>{headerLinks.title}</Link>
    </li>
  ));

  const items = categories.map((categories) => (
    <li key={categories.id}>
      <Link href={categories.href}>{categories.title}</Link>
    </li>
  ));

  return (
    <nav className="text-white">
      <ul>{links}</ul>
      <ul>{items}</ul>
    </nav>
  );
}
