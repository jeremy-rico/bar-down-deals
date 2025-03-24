import { Button } from "@headlessui/react";
import {
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/react/24/outline";

export default function Pagination({ onPageChange, currentPage, totalPages }) {
  //const pages = Array.from({ length: totalPages }, (_, index) => index + 1);
  const pages = [];
  if (totalPages <= 7) {
    pages.push(...Array.from({ length: totalPages }, (_, i) => i + 1));
  } else {
    pages.push(1);
    if (currentPage > 3) pages.push("...");

    const start = Math.max(2, currentPage - 2);
    const end = Math.min(totalPages - 1, currentPage + 2);

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    if (currentPage < totalPages - 2) pages.push("...");
    pages.push(totalPages);
  }
  return (
    <div className="flex my-7 gap-x-1 items-center">
      {/* First Page Button */}
      <Button
        onClick={() => onPageChange(1)}
        className="bg-gray-300 px-1 py-2 rounded border border-gray-400 hover:bg-gray-200"
      >
        <ChevronDoubleLeftIcon className="size-4" />
      </Button>

      {/* Previous Page Button */}
      <Button
        onClick={() => onPageChange(currentPage - 1)}
        className="bg-gray-300 px-1 py-2 rounded border border-gray-400 data-[disabled]:bg-gray-200"
        disabled={currentPage == 1}
      >
        <ChevronLeftIcon className="size-4" />
      </Button>

      {/* Numbered Page Buttons */}
      <div className="flex gap-x-1 mx-1">
        {pages.map((pageNumber, index) => (
          <div key={index}>
            {pageNumber == "..." ? (
              <p className="text-gray-400 pt-2">...</p>
            ) : (
              <Button
                className="bg-gray-300 px-2 py-1 rounded border border-gray-400 hover:bg-gray-200 data-[disabled]:bg-gray-200"
                onClick={() => onPageChange(pageNumber)}
                disabled={currentPage == pageNumber}
              >
                {pageNumber}
              </Button>
            )}
          </div>
        ))}
      </div>

      {/* Next Page Button */}
      <Button
        onClick={() => onPageChange(currentPage + 1)}
        className="bg-gray-300 px-1 py-2 rounded border border-gray-400 data-[disabled]:bg-gray-200"
        disabled={currentPage == totalPages}
      >
        <ChevronRightIcon className="size-4" />
      </Button>

      {/* Last Page Button */}
      <Button
        onClick={() => onPageChange(totalPages)}
        className="bg-gray-300 px-1 py-2 rounded border border-gray-400 hover:bg-gray-200"
      >
        <ChevronDoubleRightIcon className="size-4" />
      </Button>
    </div>
  );
}
