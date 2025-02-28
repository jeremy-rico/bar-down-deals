export const navigation = [
  { title: "New", href: "/deals/new", children: [] },
  {
    title: "Sticks",
    href: "/deals/sticks",
    children: [
      {
        title: "Composite",
        href: "/deals/sticks/composite",
        children: [
          { title: "Senior", href: "/deals/sticks/composite/senior" },
          {
            title: "Intermediate",
            href: "/deals/sticks/composite/intermediate",
          },
          { title: "Junior", href: "/deals/sticks/composite/junior" },
          { title: "Youth", href: "/deals/sticks/composite/youth" },
        ],
      },
      { title: "Street Hockey Sticks", href: "/deals/sticks/street" },
      { title: "Wood Hockey Sticks", href: "/deals/sticks/wood" },
    ],
  },
  {
    title: "Skates",
    href: "/deals/skates",
    children: [
      { title: "Senior", href: "/deals/skates/senior" },
      {
        title: "Intermediate",
        href: "/deals/skates/intermediate",
      },
      { title: "Junior", href: "/deals/skates/junior" },
      { title: "Youth", href: "/deals/skates/youth" },
    ],
  },
  {
    title: "Protective",
    href: "/deals/protective",
    children: [
      { title: "Helmets", href: "/deals/protective/helmets" },
      { title: "Cages & Shields", href: "/deals/protective/cages_and_sheilds" },
      { title: "Gloves", href: "/deals/protective/gloves" },
      { title: "Shoulder Pads", href: "/deals/protective/shoulder_pads" },
      { title: "Shin Guards", href: "/deals/protective/shin_guards" },
      { title: "Elbow Pads", href: "/deals/protective/elbow_pads" },
      { title: "Pants", href: "/deals/protective/pants" },
      { title: "Pant Shells", href: "/deals/protective/pant_shells" },
      { title: "Jocks", href: "/deals/protective/jocks" },
    ],
  },
  { title: "Bags", href: "/deals/bags", children: [] },
  { title: "Accessories", href: "/deals/accessories", children: [] },
  { title: "Apparel", href: "/deals/apparel", children: [] },
  { title: "Jerseys", href: "/deals/jerseys", children: [] },
  {
    title: "Goalie",
    href: "/deals/goalie",
    children: [
      { title: "Leg Pads", href: "/deals/goalie/leg_pads" },
      { title: "Masks", href: "/deals/goalie/masks" },
      { title: "Blockers", href: "/deals/goalie/blockers" },
      { title: "Chest & Arm", href: "/deals/goalie/chest_and_arm" },
      { title: "Knee Protectors", href: "/deals/goalie/knee_protectors" },
      { title: "Catchers", href: "/deals/goalie/catchers" },
      { title: "Goalie Sticks", href: "/deals/goalie/sticks" },
      { title: "Goalie Skates", href: "/deals/goalie/skates" },
    ],
  },
  {
    title: "Roller",
    href: "/deals/roller",
    children: [
      { title: "Inline Skates", href: "/deals/roller/inline_skates" },
      { title: "Inline Wheels", href: "/deals/roller/inline_wheel" },
    ],
  },
  { title: "Coupons", href: "/coupons", children: [] },
  { title: "Promos", hred: "/promos", children: [] },
];

export const headerLinks = [
  { id: 1, title: "About", href: "/about" },
  { id: 2, title: "Contact", href: "/contact" },
  { id: 3, title: "Sign In", href: "/signin" },
];

export const api = "http://13.52.178.97:8000/";
