import { Disclosure, DisclosurePanel } from "@headlessui/react";
import Search from "@/components/Search.tsx";
import HeaderLinks from "@/components/HeaderLinks.tsx";
import NavBar from "@/components/NavBar.tsx";
import MobileMenu from "@/components/MobileMenu.tsx";
import MobileMenuButton from "@/components/MobileMenuButton.tsx";
import { navigation } from "@/constants/index.tsx";
import Link from "next/link";

export default async function Header() {
  return (
    <Disclosure as="nav" className="bg-black">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="flex h-20 lg:h-16 items-center justify-between">
          {/* Logo Hero */}
          <Link className="text-blue-500 text-2xl" href="/">
            LOGO
          </Link>

          {/* Search Form */}
          <Search />

          {/* Header Links */}
          <div className="hidden lg:flex">
            <HeaderLinks />
          </div>

          {/* Mobile Menu Button */}
          <div className="lg:hidden">
            <MobileMenuButton />
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      <MobileMenu navigation={navigation} />

      {/* Navigation Bar */}
      <NavBar navigation={navigation} />
    </Disclosure>
  );
}
