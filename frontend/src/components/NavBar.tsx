import {
  Popover,
  PopoverButton,
  PopoverPanel,
  PopoverBackdrop,
} from "@headlessui/react";
import { ChevronDownIcon } from "@heroicons/react/24/solid";
import Link from "next/link";

export default function NavBar({ navigation }) {
  return (
    <nav className="hidden lg:block max-w-screen-2xl mx-auto py-1">
      <ul className="flex justify-evenly w-full">
        {navigation.map((item) => (
          <Popover key={item.title} className="relative">
            <span>
              <PopoverButton
                href={item.href}
                className="relative flex items-center text-white text-md gap-x-1 px-4 py-2 rounded hover:outline outline-1 outline-gray-200"
              >
                {item.title}
                <ChevronDownIcon className="size-4 text-gray-200" />
              </PopoverButton>
            </span>
            <PopoverBackdrop className="fixed bg-black/50" />
            <PopoverPanel className="absolute flex flex-wrap max-w-lg gap-4 px-4 py-2 bg-gray-200 rounded shadow">
              {item.children &&
                item.children.map((child) => (
                  <div key={child.title} className="flex flex-col">
                    <Link
                      href={child.href}
                      className="text-gray-700 text-md font-bold whitespace-nowrap"
                    >
                      {child.title}
                    </Link>
                    {child.children &&
                      child.children.map((gchild) => (
                        <div key={gchild.title}>
                          <Link
                            href={gchild.href}
                            className="text-gray-600 text-sm"
                          >
                            {gchild.title}
                          </Link>
                        </div>
                      ))}
                  </div>
                ))}
            </PopoverPanel>
          </Popover>
        ))}
      </ul>
    </nav>
  );
}
