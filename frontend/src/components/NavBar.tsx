"use client";
import Link from "next/link";
import { categories } from "@/constants/index.tsx";

export default function NavBar() {
  const items = categories.map((categories) => (
    <li key={categories.id}>
      <Link href={categories.href}>{categories.title}</Link>
    </li>
  ));
  return (
    <div className="hidden md:block max-w-screen-2xl mx-auto py-3">
      <nav>
        <ul className="flex justify-evenly w-full text-white text-sm md:text-lg">
          {items}
        </ul>
      </nav>
    </div>
  );
}
