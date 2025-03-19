"use client";
import { ChevronDownIcon } from "@heroicons/react/24/outline";
import { sort_options } from "@/constants/index.tsx";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";

export default function SortMenu({ sort, onSortChange }) {
  return (
    <div className="flex justify-end mb-3">
      <p className="text-gray-800 mx-4">Sort by:</p>
      <Menu>
        <MenuButton className="flex items-center rounded">
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
                onClick={() => onSortChange(option.title)}
                className="text-left px-2 py-1 rounded data-[focus]:bg-gray-300"
              >
                {option.title}
              </button>
            </MenuItem>
          ))}
        </MenuItems>
      </Menu>
    </div>
  );
}
