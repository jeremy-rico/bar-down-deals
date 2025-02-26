"use client";
import Link from "next/link";
import { navigation } from "@/constants/index.tsx";

export default function NavBar() {
  const items = navigation.map((item) => (
    <li key={item.title} className="px-4 py-2 rounded hover:bg-gray-800">
      <Link href={item.href}>{item.title}</Link>
    </li>
  ));
  return (
    <nav className="hidden md:block max-w-screen-2xl mx-auto py-1">
      <ul className="flex justify-evenly w-full text-white text-lg">{items}</ul>
    </nav>
  );
}
