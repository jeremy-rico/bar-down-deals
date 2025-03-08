import { navigation } from "@/constants/index.tsx";
import HeaderLinks from "@/components/HeaderLinks.tsx";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/react";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

export default function MobileMenu() {
  return (
    <div className="border-t-2 border-blue-600">
      <div className="flex justify-evenly py-4 text-white">
        <HeaderLinks />
      </div>

      <div className="flex-col px-4 text-white">
        {navigation.map((item) => (
          <Disclosure key={item.title}>
            <DisclosureButton
              href={item.href}
              className="flex items-center py-4 "
            >
              {item.title}
              <ChevronRightIcon className="absolute right-0 mx-2 text-white size-9" />
            </DisclosureButton>
            <DisclosurePanel className="bg-gray-200">
              {item.children.map((child) => (
                <div
                  key={child.title}
                  className=" flex items-center py-2 mx-2 text-gray-700 border border-b-black"
                >
                  {child.title}
                  <ChevronRightIcon className="absolute right-3 mx-2 size-6" />
                </div>
              ))}
            </DisclosurePanel>
          </Disclosure>
        ))}
      </div>
    </div>
  );
}
