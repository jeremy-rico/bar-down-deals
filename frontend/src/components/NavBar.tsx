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
              className="flex items-center text-white text-md gap-x-1 px-4 py-2 rounded hover:outline outline-1 outline-gray-200"
            >
              {item.title}
              <ChevronDownIcon className="size-4 text-gray-200" />
            </PopoverButton>
            <PopoverBackdrop className="fixed bg-black/50" />
            <PopoverPanel
              anchor="bottom"
              className="absolute h-80 w-full pt-4 pb-2 bg-gray-200 rounded shadow"
            >
              <div className="h-full flex flex-col flex-wrap max-w-7xl mx-auto gap-y-4">
                {item.children &&
                  item.children.map((child) => (
                    <div key={child.title} className="flex flex-col">
                      <Link
                        href={child.href}
                        className="text-gray-700 text-lg font-bold hover:underline"
                      >
                        {child.title}
                      </Link>
                      {child.children &&
                        child.children.map((gchild) => (
                          <div key={gchild.title}>
                            <Link
                              href={gchild.href}
                              className="text-gray-600 text-md hover:underline"
                            >
                              {gchild.title}
                            </Link>
                          </div>
                        ))}
                    </div>
                  ))}
              </div>
            </PopoverPanel>
          </Popover>
        ))}
      </ul>
    </nav>
  );
}
