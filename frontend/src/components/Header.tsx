"use client";
import { useState } from "react";
import SearchBar from "@/components/SearchBar.tsx";
import HeaderLinks from "@/components/HeaderLinks.tsx";
import MobileMenu from "@/components/MobileMenu.tsx";
import NavBar from "@/components/NavBar.tsx";

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <header className="bg-black">
      <div className="flex items-center max-w-7xl py-4 px-5 mx-auto">
        <a className="text-white text-3xl md:text-5xl" href="localhost:3000">
          LOGO
        </a>
        <SearchBar />
        <div className="hidden md:block">
          <HeaderLinks />
        </div>
        <div className="md:hidden">
          <MobileMenu isOpen={false} onShow={() => setIsOpen(!isOpen)} />
        </div>
      </div>

      <NavBar />
    </header>
  );
}
