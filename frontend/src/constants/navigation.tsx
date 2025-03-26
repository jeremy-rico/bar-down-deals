export const navigation = [
  // Deals Section
  {
    title: "Deals",
    href: "#",
    children: [
      {
        title: "Hottest Deals",
        href: "/deals/hot",
        children: [
          { title: "Biggest Discounts", href: "/deals/discount" },
          { title: "Lowest Prices", href: "/deals/lowest" },
        ],
      },
      {
        title: "Under $5",
        href: "/deals/under-5",
      },
      { title: "Shop All Deals", href: "/deals" },
      {
        title: "Shop By New",
        href: "/deals?sort=Newest",
        children: [
          { title: "Sticks", href: "/deals?sort=Newest&tags=Sticks" },
          { title: "Skates", href: "/deals?sort=Newest&tags=Skates" },
          { title: "Protective", href: "/deals?sort=Newest&tags=Protective" },
          { title: "Accessories", href: "/deals?sort=Newest&tags=Accessories" },
          { title: "Apparel", href: "/deals?sort=Newest&tags=Apparel" },
          { title: "Gamewear", href: "/deals?sort=Newest&tags=Gamewear" },
          { title: "Goalie", href: "/deals?sort=Newest&tags=Goalie" },
          { title: "Roller", href: "/deals?sort=Newest&tags=Roller" },
        ],
      },
      {
        title: "Shop By Size",
        href: "#",
        children: [
          { title: "Senior", href: "/deals?tags=Senior" },
          { title: "Intermediate", href: "/deals?tags=Intermediate" },
          { title: "Junior", href: "/deals?tags=Junior" },
          { title: "Youth", href: "/deals?tags=Youth" },
        ],
      },
    ],
  },
  {
    title: "Hockey Equipment",
    href: "#",
    children: [
      {
        title: "Sticks",
        href: "/deals/sticks",
        children: [
          {
            title: "Player Sticks",
            href: "/deals/sticks/player",
            children: [],
          },
          { title: "Goalie Sticks", href: "/deals/goalie/sticks" },
          { title: "Street Hockey Sticks", href: "/deals/sticks/street" },
          { title: "Wood Hockey Sticks", href: "/deals/sticks/wood" },
        ],
      },
      {
        title: "Skates",
        href: "/deals/skates",
        children: [
          {
            title: "Ice Hockey Skates",
            href: "/deals/skates",
            children: [],
          },
          {
            title: "Goalie Skates",
            href: "/deals/inline_skates",
            children: [],
          },
          {
            title: "Inline Hockey Skates",
            href: "/deals/inline_skates",
            children: [],
          },
          { title: "Skate Accessories", href: "/deals/accessories/skates" },
          { title: "Inline Skate Wheels", href: "/deals/inline_wheels" },
        ],
      },
      {
        title: "Protective",
        href: "/deals/protective",
        children: [
          {
            title: "Helmets",
            href: "/deals/protective/helmets",
            children: [],
          },
          {
            title: "Cages & Shields",
            href: "/deals/protective/cages_and_shields",
            children: [],
          },
          {
            title: "Gloves",
            href: "/deals/protective/gloves",
            children: [],
          },
          {
            title: "Shoulder Pads",
            href: "/deals/protective/shoulder_pads",
            children: [],
          },
          {
            title: "Shin Guards",
            href: "/deals/protective/shin_guards",
            children: [],
          },
          {
            title: "Elbow Pads",
            href: "/deals/protective/elbow_pads",
            children: [],
          },
          {
            title: "Pants",
            href: "/deals/protective/pants",
            children: [],
          },
          {
            title: "Pant Shells",
            href: "/deals/protective/pant_shells",
            children: [],
          },
        ],
      },
      {
        title: "Baselayer",
        href: "/deals/protective/baselayer",
        children: [
          { title: "Jocks", href: "/deals/protective/baselayer/jocks" },
          { title: "Shirts", href: "/deals/protective/baselayer/shirts" },
          { title: "Bottoms", href: "/deals/protective/baselayer/bottoms" },
          { title: "Socks", href: "/deals/protective/baselayer/socks" },
        ],
      },
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
    ],
  },
  // Accessories Section
  {
    title: "Accessories",
    href: "/deals/accessories",
    children: [
      {
        title: "Gamewear",
        href: "/deals/gamewear",
        children: [
          { title: "Jerseys", href: "/deals/gamewear/jerseys" },
          { title: "Socks", href: "/deals/gamewear/socks" },
        ],
      },
      { title: "Bags", href: "/deals/bags" },
      {
        title: "Apparel",
        href: "/deals/apparel",
        children: [
          { title: "Adult Apparel", href: "/deals/apparel/mens" },
          { title: "Womens Apparel", href: "/deals/apparel/womens" },
          { title: "Youth Apparel", href: "/deals/apparel/youth" },
          { title: "Headwear", href: "/deals/apparel/Headwear" },
        ],
      },
      { title: "Shop All Accessories", href: "/deals/accessories" },
    ],
  },
  {
    title: "Websites",
    href: "#",
    children: [
      {
        title: "Shop By Site",
        href: "#",
        children: [
          { title: "Hockey Monkey", href: "deals/sites/hockey_monkey" },
          { title: "Pure Hockey", href: "deals/sites/pure_hockey" },
          { title: "Ice Warehouse", href: "deals/sites/ice_warehouse" },
          { title: "CCM", href: "deals/sites/ccm" },
          { title: "Bauer", href: "deals/sites/bauer" },
          { title: "True", href: "deals/sites/true" },
          { title: "Sherwood", href: "deals/sites/sherwood" },
        ],
      },
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

export const sort_options = [
  { id: 1, title: "Best Selling", sort: "best", order: "desc" },
  { id: 2, title: "Alphabetical", sort: "alphabetical", order: "asc" },
  { id: 3, title: "Price, highest", sort: "price", order: "desc" },
  { id: 4, title: "Price, lowest", sort: "price", order: "asc" },
  { id: 5, title: "Discount", sort: "discount", order: "desc" },
  { id: 6, title: "Newest", sort: "date", order: "desc" },
  { id: 7, title: "Oldest", sort: "date", order: "asc" },
];

export const api = "http://13.52.178.97:8000";
