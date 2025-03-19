"use client";
import {
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/outline";
import { sort_options } from "@/constants/index.tsx";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";

export default function SortMenu({ sort, onSortChange }) {
  return (
    <div className="flex justify-between border-t border-t-black border-b border-b-black py-2 mb-5">
      <div className="flex items-center gap-x-3">
        <AdjustmentsHorizontalIcon className="size-7 text-gray-800" />
        <p className="text-lg text-gray-800">Filter</p>
      </div>
      <div className="flex items-center">
        <p className="text-lg text-gray-800 mx-4">Sort by:</p>
        <Menu>
          <MenuButton className="flex items-center text-lg rounded">
            {sort.title}
            <ChevronDownIcon className="mx-1 size-4" />
          </MenuButton>
          <MenuItems
            className="flex flex-col bg-gray-50 p-1 rounded shadow [--anchor-gap:4px]"
            anchor="bottom"
          >
            {sort_options.map((option) => (
              <MenuItem key={option.id}>
                <button
                  onClick={() => onSortChange(option)}
                  className="text-left text-lg px-2 py-1 rounded data-[focus]:bg-gray-300"
                >
                  {option.title}
                </button>
              </MenuItem>
            ))}
          </MenuItems>
        </Menu>
      </div>
    </div>
  );
}
