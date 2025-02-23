"use client";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

export default function Search() {
  return (
    <form
      className="flex w-full h-9 mx-5 justify-end size-full rounded bg-white"
      method="get"
    >
      <input
        className="size-full mx-3 focus:outline-none"
        maxLength="128"
        placeholder="Search"
      ></input>
      <button className="mx-4" type="submit">
        <MagnifyingGlassIcon className="size-5 text-black" />
        <span className="sr-only">Search</span>
      </button>
    </form>
  );
}
