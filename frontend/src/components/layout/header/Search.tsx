"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import { Field, Input, Button } from "@headlessui/react";

export default function Search() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const submitSearch = () => {
    const query = new URLSearchParams();
    setSearchQuery(searchQuery);
    query.append("q", searchQuery);
    router.push(`/search?${query.toString()}`);
  };
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      submitSearch(); // Trigger submit on Enter key press
    }
  };
  return (
    <Field className="flex w-full h-9 mx-5 justify-end size-full rounded bg-white">
      <Input
        className="size-full mx-3 focus:outline-none"
        minLength={3}
        maxLength={128}
        type="search"
        placeholder="Search deals..."
        onKeyDown={handleKeyDown}
        onChange={(e) => setSearchQuery(e.target.value)}
      ></Input>
      <Button onClick={submitSearch} className="mx-4" type="submit">
        <MagnifyingGlassIcon className="size-5 text-black" />
        <span className="sr-only">Search</span>
      </Button>
    </Field>
  );
}
