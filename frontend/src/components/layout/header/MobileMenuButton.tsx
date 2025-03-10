import { DisclosureButton } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
export default function MobileMenuButton() {
  return (
    <div className="right-0 flex items-center">
      {/* Mobile menu button*/}
      <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:outline-hidden focus:ring-inset">
        <span className="absolute -inset-0.5" />
        <span className="sr-only">Open main menu</span>
        <Bars3Icon
          aria-hidden="true"
          className="block size-7 group-data-[open]:hidden"
        />
        <XMarkIcon
          aria-hidden="true"
          className="hidden size-7 group-data-[open]:block"
        />
      </DisclosureButton>
    </div>
  );
}
