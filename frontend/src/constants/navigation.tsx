export const navigation = [
  // Deals Section
  {
    title: "Deals",
    href: "#",
    children: [
      {
        title: "Popular Deals",
        href: "/deals/popular",
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
        href: "/deals/new",
        children: [
          { title: "Sticks", href: "/deals/new/sticks" },
          { title: "Skates", href: "/deals/new/skates" },
          { title: "Protective", href: "/deals/new/protective" },
          { title: "Accessories", href: "/deals/new/accessories" },
          { title: "Apparel", href: "/deals/new/apparel" },
          { title: "Gamewear", href: "/deals/new/gamewear" },
          { title: "Goalie", href: "/deals/new/goalie" },
          { title: "Roller", href: "/deals/new/roller" },
        ],
      },
      {
        title: "Shop By Size",
        href: "#",
        children: [
          { title: "Senior", href: "/deals/senior" },
          { title: "Intermediate", href: "/deals/intermediate" },
          { title: "Junior", href: "/deals/junior" },
          { title: "Youth", href: "/deals/youth" },
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
            href: "/deals/sticks/player", //TODO:
            children: [],
          },
          { title: "Goalie Sticks", href: "/deals/goalie/sticks" },
          { title: "Street Hockey Sticks", href: "/deals/sticks/street" }, //TODO:
          { title: "Wood Hockey Sticks", href: "/deals/sticks/wood" }, //TODO:
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
            href: "/deals/goalie/skates",
            children: [],
          },
          {
            title: "Inline Hockey Skates",
            href: "/deals/inline-skates",
            children: [],
          },
          { title: "Skate Accessories", href: "/deals/accessories/skates" },
          { title: "Inline Skate Wheels", href: "/deals/inline-wheels" },
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
            href: "/deals/protective/cages-and-shields",
            children: [],
          },
          {
            title: "Gloves",
            href: "/deals/protective/gloves",
            children: [],
          },
          {
            title: "Shoulder Pads",
            href: "/deals/protective/shoulder-pads",
            children: [],
          },
          {
            title: "Shin Guards",
            href: "/deals/protective/shin-guards",
            children: [],
          },
          {
            title: "Elbow Pads",
            href: "/deals/protective/elbow-pads",
            children: [],
          },
          {
            title: "Pants",
            href: "/deals/protective/pants",
            children: [],
          },
          {
            title: "Pant Shells",
            href: "/deals/protective/pant-shells",
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
          { title: "Leg Pads", href: "/deals/goalie/leg-pads" },
          { title: "Masks", href: "/deals/goalie/masks" },
          { title: "Blockers", href: "/deals/goalie/blockers" },
          { title: "Chest & Arm", href: "/deals/goalie/chest-and-arm" },
          { title: "Knee Protectors", href: "/deals/goalie/knee-protectors" },
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
    href: "#",
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
          { title: "Headwear", href: "/deals/apparel/headwear" },
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
        title: "Shop By Store",
        href: "#",
        children: [
          { title: "Hockey Monkey", href: "deals/hockey-monkey" },
          { title: "Pure Hockey", href: "deals/pure-hockey" },
          { title: "Discount Hockey", href: "deals/discount-hockey" },
          { title: "Ice Warehouse", href: "deals/ice-warehouse" },
          { title: "CCM", href: "deals/ccm" },
          { title: "Bauer", href: "deals/bauer" },
          { title: "True", href: "deals/true" },
          { title: "Sherwood", href: "deals/sherwood" },
        ],
      },
    ],
  },
  {
    title: "Coupons",
    href: "#",
    children: [
      { title: "COMING SOON!", href: "#" },
      //{ title: "Hockey Monkey", href: "deals/coupons/hockey-monkey" },
      //{ title: "Pure Hockey", href: "deals/coupons/pure-hockey" },
      //{ title: "Ice Warehouse", href: "deals/coupons/ice-warehouse" },
      //{ title: "CCM", href: "deals/coupons/ccm" },
      //{ title: "Bauer", href: "deals/coupons/bauer" },
      //{ title: "True", href: "deals/coupons/true" },
      //{ title: "Sherwood", href: "deals/coupons/sherwood" },
      //{ title: "View All Coupons", href: "deals/coupons" },
    ],
  },
  {
    title: "Promos",
    hred: "#",
    children: [
      { title: "COMING SOON!", href: "#" },
      //{ title: "View All Promos", href: "deals/promos" },
    ],
  },
];
