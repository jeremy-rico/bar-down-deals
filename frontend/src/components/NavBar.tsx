"use client";
import Link from "next/link";
import { navigation } from "@/constants/index.tsx";

export default function NavBar() {
  const items = navigation.map((item) => (
    <li key={item.id}>
      <Link href={item.href}>{item.title}</Link>
    </li>
  ));
  return (
    <div className="hidden md:block max-w-screen-2xl mx-auto py-3">
      <nav>
        <ul className="flex justify-evenly w-full text-white text-lg">
          {items}
        </ul>
      </nav>
    </div>
  );
}
