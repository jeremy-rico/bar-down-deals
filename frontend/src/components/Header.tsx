"use client";
import { useState } from "react";
import {
  Disclosure,
  DisclosureButton,
  DiscolsurePanel,
  Input,
  Menu,
  MenuButton,
  MenuItems,
  MenuItem,
} from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import Search from "@/components/Search.tsx";

export default function Header() {
  //const [isOpen, setIsOpen] = useState(false);
  return (
    <Disclosure as="nav" className="bg-black">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 items-center justify-between">
          <div className="absolute inset-y-0 right-0 flex items-center sm:hidden">
            {/* Mobile menu button*/}
            <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:outline-hidden focus:ring-inset">
              <span className="absolute -inset-0.5" />
              <span className="sr-only">Open main menu</span>
              <Bars3Icon
                aria-hidden="true"
                className="block size-6 group-data-open:hidden"
              />
              <XMarkIcon
                aria-hidden="true"
                className="hidden size-6 group-data-open:block"
              />
            </DisclosureButton>
          </div>
          {/* Logo Hero */}
          <a className="text-white text-lg">LOGO</a>
          <Search />
          <div>
            <a className="text-white text-lg">About</a>
            <a className="text-white text-lg">Contact</a>
            <a className="text-white text-lg">Sign In</a>
          </div>
        </div>
      </div>
    </Disclosure>
  );
}
