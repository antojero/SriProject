export interface CakeItem {
  id: number;
  name: string;
  image: string;
  description: string;
  featured: boolean;
}

export const cakes: CakeItem[] = [
  {
    id: 1,
    name: "Chocolate Truffle",
    image: "/images/cakes/chocolate-truffle.webp",
    description: "A rich chocolate sponge layered with smooth dark chocolate ganache drip and edible gold leaf.",
    featured: true,
  },
  {
    id: 2,
    name: "Red Velvet Dream",
    image: "/images/cakes/red-velvet.webp",
    description: "A soft velvety red sponge cake layered with silky cream cheese frosting and fresh berries.",
    featured: true,
  },
  {
    id: 3,
    name: "Vanilla Berry Bliss",
    image: "/images/cakes/vanilla-berry.webp",
    description: "Light vanilla bean sponge adorned with fresh strawberries, blueberries, and edible flora.",
    featured: true,
  },
  {
    id: 4,
    name: "Royal Dark Chocolate",
    image: "/images/cakes/chocolate-truffle.webp",
    description: "Decadent 70% dark Belgian chocolate drip cake handcrafted for true chocolate enthusiasts.",
    featured: true,
  },
  {
    id: 5,
    name: "Custom Celebration Tier",
    image: "/images/hero-cake.webp",
    description: "Multi-tier bespoke centerpiece cake customized to your celebration theme and flavor preference.",
    featured: true,
  },
  {
    id: 6,
    name: "Classic Strawberry Velvet",
    image: "/images/cakes/red-velvet.webp",
    description: "Rich red sponge whipped with fresh strawberry compote and light vanilla cream frosting.",
    featured: false,
  },
  {
    id: 7,
    name: "Garden Floral Vanilla",
    image: "/images/hero-cake.webp",
    description: "Elegant 3-tier wedding cake with delicate buttercream floral pipes and gold leaf detailing.",
    featured: false,
  },
  {
    id: 8,
    name: "Artisan Chocolate Crunch",
    image: "/images/cakes/chocolate-truffle.webp",
    description: "Layers of fudge chocolate sponge with hazelnut praline crunch and smooth ganache finish.",
    featured: false,
  }
];
