import Link from "next/link";
import { headerLinks } from "@/constants/index.tsx";
import {
  QuestionMarkCircleIcon,
  PhoneIcon,
  UserCircleIcon,
} from "@heroicons/react/24/outline";

export default function HeaderLinks() {
  const links = headerLinks.map((item) => (
    <li key={item.id} className="flex justify-between items-center">
      <Link href={item.href} className="whitespace-nowrap">
        {item.title}
      </Link>
      {item.title == "About" && (
        <QuestionMarkCircleIcon className="mx-3 size-7" />
      )}
      {item.title == "Contact" && <PhoneIcon className="mx-3 size-6" />}
      {item.title == "Sign In" && <UserCircleIcon className="mx-3 size-7" />}
    </li>
  ));
  return (
    <ul className="flex text-white text-lg lg:text-xl gap-x-3">{links}</ul>
  );
}
