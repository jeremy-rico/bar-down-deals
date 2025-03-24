import HeaderLinks from "@/components/layout/header/HeaderLinks.tsx";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/react";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

export default function MobileMenu({ navigation }) {
  return (
    <DisclosurePanel
      transition
      className="lg:hidden overflow-hidden transition duration-100 ease-out data-[closed]:-translate-y-6 data-[closed]:opacity-0"
    >
      <div className="border-t-2 border-blue-600">
        <div className="flex justify-evenly py-4 text-white">
          <HeaderLinks />
        </div>
        <hr className="bg-white h-[1px] mx-8"></hr>
        <div className="flex-col px-4 text-white">
          {navigation.map((item) => (
            <Disclosure key={item.title}>
              <DisclosureButton
                href={item.href}
                className="flex w-full justify-between items-center py-4 "
              >
                {item.title}
                <ChevronRightIcon className="text-white size-9" />
              </DisclosureButton>
              <DisclosurePanel
                transition
                className="bg-gray-200 transition duration-100 ease-out data-[closed]:-translate-y-6 data-[closed]:opacity-0"
              >
                {item.children.map((child) => (
                  <Disclosure key={child.title}>
                    <DisclosureButton className="flex w-full justify-between items-center px-4 py-2 text-gray-700 border border-b-black">
                      {child.title}
                      <ChevronRightIcon className="size-6" />
                    </DisclosureButton>
                    <DisclosurePanel
                      transition
                      className="bg-gray-100 transition duration-100 ease-in data-[closed]:-translate-y-6 data-[closed]:opacity-0"
                    >
                      {child.children &&
                        child.children.map((gchild) => (
                          <a
                            key={gchild.title + gchild.href}
                            className="flex justify-between w-full text-gray-700 px-4 py-2"
                            href={gchild.href}
                          >
                            {gchild.title}
                            <ChevronRightIcon className="size-6" />
                          </a>
                        ))}
                    </DisclosurePanel>
                  </Disclosure>
                ))}
              </DisclosurePanel>
            </Disclosure>
          ))}
        </div>
      </div>
    </DisclosurePanel>
  );
}
