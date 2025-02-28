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
            <PopoverButton
              href={item.href}
              className="relative px-4 py-2 rounded hover:outline outline-1 outline-gray-200"
            >
              <span className="flex items-center gap-x-1 text-white text-md">
                {item.title}
                <ChevronDownIcon className="size-4 text-gray-200" />
              </span>
            </PopoverButton>
            <PopoverBackdrop className="fixed bg-black/50" />
            <PopoverPanel className="absolute flex bg-gray-200 rounded shadow">
              {item.children &&
                item.children.map((child) => (
                  <div key={child.title} className="flex flex-col">
                    <Link
                      href={child.href}
                      className="text-gray-700 text-md font-bold"
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
