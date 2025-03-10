"use client";

import { useState } from "react";
import DealCard from "@/components/DealCard";
import {
  ChevronDoubleRightIcon,
  ChevronDoubleLeftIcon,
} from "@heroicons/react/24/outline";

const Carousel = ({ deals }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const dealsPerPage = 5;
  const totalSlides = Math.ceil(deals.length / dealsPerPage);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === totalSlides - 1 ? 0 : prevIndex + 1,
    );
  };

  const prevSlide = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === 0 ? totalSlides - 1 : prevIndex - 1,
    );
  };

  const startIndex = currentIndex * dealsPerPage;
  const visibleDeals = deals.slice(startIndex, startIndex + dealsPerPage);

  return (
    <div className="relative w-full">
      {/* Deals */}
      <div className="flex gap-x-6 overflow-hidden">
        {visibleDeals.map((deal, index) => (
          <DealCard key={index} deal={deal} />
        ))}
      </div>

      {/* Navigation Arrows */}
      <button
        onClick={prevSlide}
        className="absolute top-1/3 left-2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-1 rounded-full"
      >
        <ChevronDoubleLeftIcon className="size-7" />
      </button>
      <button
        onClick={nextSlide}
        className="absolute top-1/3 right-2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-1 rounded-full"
      >
        <ChevronDoubleRightIcon className="size-7" />
      </button>
    </div>
  );
};

export default Carousel;
