import Link from "next/link";
import { headerLinks } from "@/constants/index.tsx";
import {
  QuestionMarkCircleIcon,
  PhoneIcon,
  UserCircleIcon,
} from "@heroicons/react/24/outline";

export default function HeaderLinks() {
  const links = headerLinks.map((item) => (
    <li key={item.id} className="px-2 py-2 rounded hover:bg-gray-800">
      <Link
        href={item.href}
        className="flex items-center gap-x-2 whitespace-nowrap"
      >
        {item.title}
        {item.title == "About" && <QuestionMarkCircleIcon className="size-7" />}
        {item.title == "Contact" && <PhoneIcon className="size-6" />}
        {item.title == "Sign In" && <UserCircleIcon className="size-7" />}
      </Link>
    </li>
  ));
  return (
    <ul className="flex justify-between gap-x-2 text-white text-lg lg:text-xl">
      {links}
    </ul>
  );
}
