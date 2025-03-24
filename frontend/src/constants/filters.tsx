const categories = {
  id: "category",
  label: "Category",
  children: [
    { id: 1, label: "Sticks", enbaled: false },
    { id: 2, label: "Skates", enbaled: false },
    { id: 3, label: "Helmets", enbaled: false },
    { id: 4, label: "Cages & Shields", enbaled: false },
    { id: 5, label: "Gloves", enbaled: false },
    { id: 6, label: "Shoulder Pads", enbaled: false },
    { id: 7, label: "Shin Guards", enbaled: false },
    { id: 8, label: "Elbow Pads", enbaled: false },
    { id: 9, label: "Pants", enbaled: false },
    { id: 10, label: "Pant Shells", enbaled: false },
    { id: 11, label: "Base", enbaled: false },
    { id: 12, label: "Goalie", enbaled: false },
    { id: 13, label: "Roller", enbaled: false },
  ],
};

const stores = {
  id: "store",
  label: "Stores",
  children: [
    { id: 1, label: "Hockey Monkey", enabled: false },
    { id: 2, label: "Pure Hockey", enabled: false },
    { id: 3, label: "Ice WareHouse", enabled: false },
    { id: 4, label: "CCM", enabled: false },
    { id: 5, label: "Bauer", enabled: false },
    { id: 6, label: "True", enabled: false },
    { id: 7, label: "Sherwood", enabled: false },
  ],
};

const brands = {
  id: "brand",
  label: "Brand",
  children: [
    { id: 1, label: "CCM", enbaled: false },
    { id: 2, label: "Bauer", enbaled: false },
    { id: 3, label: "True", enbaled: false },
    { id: 4, label: "Sherwood", enbaled: false },
    { id: 5, label: "Warrior", enbaled: false },
  ],
};

const sizing = {
  id: "sizing",
  label: "Sizing",
  children: [
    { id: 1, label: "Senior", enbaled: false },
    { id: 2, label: "Intermediate", enbaled: false },
    { id: 3, label: "Junior", enbaled: false },
    { id: 4, label: "Youth", enbaled: false },
  ],
};

export const allDealsFilters = [stores, brands, sizing];
