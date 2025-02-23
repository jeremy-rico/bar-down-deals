"use client";
export default function SearchBar() {
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
        <svg
          className="size-5"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 20 20"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
        <span className="sr-only">Search</span>
      </button>
    </form>
  );
}
