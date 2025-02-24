import { headerLinks, navigation } from "@/constants/index.tsx";
import HeaderLinks from "@/components/HeaderLinks.tsx";
import { DisclosureButton } from "@headlessui/react";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

export default function MobileMenu() {
  return (
    <div className="border-t-2 border-blue-600">
      <div className="flex justify-evenly py-4 text-white">
        <HeaderLinks />
      </div>

      <div className="flex-col px-4 text-white">
        {navigation.map((item) => (
          <DisclosureButton
            key={item.title}
            as="a"
            href={item.href}
            className="flex justify-between items-center py-4 "
          >
            {item.title}
            <ChevronRightIcon className="block mx-2 text-white size-9" />
          </DisclosureButton>
        ))}
      </div>
    </div>
  );
}
