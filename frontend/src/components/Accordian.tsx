"use client";

import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Checkbox,
  Field,
  Label,
} from "@headlessui/react";
import { PlusIcon, MinusIcon, CheckIcon } from "@heroicons/react/24/outline";

type SelectedFilters = {
  [key: string]: string[];
};
type Filter = {
  title: string;
  query: string;
  options: string[];
};
type Props = {
  filter: Filter;
  selectedFilters: SelectedFilters;
  toggleFilter: (query: string, option: string) => void;
};
export default function Accordian({
  filter,
  selectedFilters,
  toggleFilter,
}: Props) {
  return (
    <Disclosure>
      <DisclosureButton className="group flex justify-between items-center text-white bg-black w-full py-2 px-2 my-1 rounded">
        <p>{filter.title}</p>
        <PlusIcon className="size-5 group-data-[open]:hidden" />
        <MinusIcon className="hidden size-5 group-data-[open]:block" />
      </DisclosureButton>
      <DisclosurePanel
        transition
        className="flex flex-col gap-y-2 my-4 overflow-hidden transition-[height] duration-500 ease-in-out data-[closed]:h-0"
      >
        {filter.options.map((option, index) => (
          <Field key={index} className="flex items-center">
            <Checkbox
              checked={selectedFilters[filter.query].includes(option)}
              onChange={() => toggleFilter(filter.query, option)}
              className="group size-5 border border-gray-800 rounded-sm"
            >
              <CheckIcon className="hidden size-5 group-data-[checked]:block" />
            </Checkbox>
            <Label className="ml-2">{option}</Label>
          </Field>
        ))}
      </DisclosurePanel>
    </Disclosure>
  );
}
