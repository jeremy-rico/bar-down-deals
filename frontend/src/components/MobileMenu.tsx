import HamburgerIcon from "@/components/icons/HamburgerIcon.tsx";
import XIcon from "@/components/icons/XIcon.tsx";
import MobileNavBar from "@/components/MobileNavBar.tsx";

export default function MobileMenu(isOpen, onOpen) {
  return (
    <nav className="md:hidden">
      <button
        className="relative inline-flex items-center justify-center rounded-md p-2 text-white hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:outline-hidden focus:ring-inset"
        onClick={onOpen}
      >
        {isOpen ? <XIcon /> : <HamburgerIcon />}
      </button>
      {isOpen && <MobileNavBar />}
    </nav>
  );
}
