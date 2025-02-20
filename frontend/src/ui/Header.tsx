"use client";
import Link from "next/link";

export default function Header() {
  return (
    <nav className="bg-blue-600 p-4 shadow-md fixed w-full top-0">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-white text-xl font-bold">MyApp</h1>
        <div className="space-x-4">
          <Link href="/" className="text-white hover:underline">
            Home
          </Link>
          <Link href="/about" className="text-white hover:underline">
            About
          </Link>
          <Link href="/contact" className="text-white hover:underline">
            Contact
          </Link>
        </div>
      </div>
    </nav>
  );
}
