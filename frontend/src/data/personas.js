// Customer personas that mirror the seed data in backend/data/seed_data.py
// Selecting a persona in the header auto fills checkout and review forms
// with the exact name, phone, and address the agent knows from history.

export const GUEST_CUSTOMER = {
  id: "guest",
  name: "",
  phone: "",
  address: "",
  group: "guest",
  label: "Guest (New Customer)",
  hint: "No history. Agent treats you as a new buyer.",
};

export const CUSTOMER_PERSONAS = [
  // Trusted customers
  {
    id: "sarah_mitchell",
    name: "Sarah Mitchell",
    phone: "+1 617-555-0142",
    address: "45 Beacon Street, Boston, MA 02108",
    group: "trusted",
    label: "Sarah Mitchell",
    location: "Boston, MA",
    hint: "5 orders, all approved, family gamer",
  },
  {
    id: "emma_chen",
    name: "Emma Chen",
    phone: "+1 415-555-0177",
    address: "78 Sunset Blvd, San Francisco, CA 94122",
    group: "trusted",
    label: "Emma Chen",
    location: "San Francisco, CA",
    hint: "4 orders, family gamer with kids",
  },
  {
    id: "david_kim",
    name: "David Kim",
    phone: "+1 206-555-0198",
    address: "312 Pine Avenue, Seattle, WA 98101",
    group: "trusted",
    label: "David Kim",
    location: "Seattle, WA",
    hint: "4 orders, adult gamer, 17+ and 18+ titles",
  },
  {
    id: "james_wilson",
    name: "James Wilson",
    phone: "+1 303-555-0134",
    address: "22 Mountain View Rd, Denver, CO 80202",
    group: "trusted",
    label: "James Wilson",
    location: "Denver, CO",
    hint: "4 orders, collector with positive reviews",
  },
  {
    id: "olivia_brown",
    name: "Olivia Brown",
    phone: "+1 512-555-0165",
    address: "890 Oak Lane, Austin, TX 78701",
    group: "trusted",
    label: "Olivia Brown",
    location: "Austin, TX",
    hint: "2 orders, casual buyer",
  },
  {
    id: "sophia_martinez",
    name: "Sophia Martinez",
    phone: "+1 305-555-0189",
    address: "154 Palm Drive, Miami, FL 33139",
    group: "trusted",
    label: "Sophia Martinez",
    location: "Miami, FL",
    hint: "2 orders, family gamer",
  },

  // New customers with clean but short history
  {
    id: "ahmed_hassan",
    name: "Ahmed Hassan",
    phone: "+1 718-555-0121",
    address: "67 Atlantic Ave, Brooklyn, NY 11217",
    group: "new",
    label: "Ahmed Hassan",
    location: "Brooklyn, NY",
    hint: "1 order, first time buyer",
  },
  {
    id: "lucas_garcia",
    name: "Lucas Garcia",
    phone: "+1 619-555-0156",
    address: "425 Harbor Way, San Diego, CA 92101",
    group: "new",
    label: "Lucas Garcia",
    location: "San Diego, CA",
    hint: "1 order, first time buyer",
  },
  {
    id: "isabella_wright",
    name: "Isabella Wright",
    phone: "+1 503-555-0143",
    address: "88 River Street, Portland, OR 97201",
    group: "new",
    label: "Isabella Wright",
    location: "Portland, OR",
    hint: "1 order, first time buyer",
  },

  // Suspicious customers with rejection history
  {
    id: "john_smith",
    name: "John Smith",
    phone: "+1 213-555-9911",
    address: "1200 Industrial Park Dr, Los Angeles, CA 90021",
    group: "suspicious",
    label: "John Smith",
    location: "Los Angeles, CA",
    hint: "1 order, rejected. Address tied to fraud ring.",
  },
  {
    id: "j_smyth",
    name: "J. Smyth",
    phone: "+1 213-555-9912",
    address: "1200 Industrial Park Dr, Los Angeles, CA 90021",
    group: "suspicious",
    label: "J. Smyth",
    location: "Los Angeles, CA",
    hint: "Same address as John Smith, alias",
  },
  {
    id: "jonathan_s",
    name: "Jonathan S.",
    phone: "+1 213-555-9913",
    address: "1200 Industrial Park Dr, Los Angeles, CA 90021",
    group: "suspicious",
    label: "Jonathan S.",
    location: "Los Angeles, CA",
    hint: "Same address as John Smith, third alias",
  },
  {
    id: "michael_chen",
    name: "Michael Chen",
    phone: "+1 646-555-0288",
    address: "500 Commerce Plaza, New York, NY 10013",
    group: "suspicious",
    label: "Michael Chen",
    location: "New York, NY",
    hint: "3 orders, 2 rejected. Console reseller pattern.",
  },
  {
    id: "alex_torres",
    name: "Alex Torres",
    phone: "+1 702-555-0299",
    address: "9800 Desert Rd, Las Vegas, NV 89109",
    group: "suspicious",
    label: "Alex Torres",
    location: "Las Vegas, NV",
    hint: "2 orders, both rejected. High value fraud attempts.",
  },

  // Toxic and spam reviewers (no shipping info needed)
  {
    id: "absolute_trash_reviewer",
    name: "AbsoluteTrashReview",
    phone: "",
    address: "",
    group: "review_offender",
    label: "AbsoluteTrashReview",
    location: "reviews only",
    hint: "5 rejected toxic reviews. Try posting another.",
  },
  {
    id: "spam_bot_99",
    name: "SpamBot99",
    phone: "",
    address: "",
    group: "review_offender",
    label: "SpamBot99",
    location: "reviews only",
    hint: "4 rejected spam reviews with identical text.",
  },
  {
    id: "totally_real_buyer",
    name: "TotallyRealBuyer",
    phone: "",
    address: "",
    group: "review_offender",
    label: "TotallyRealBuyer",
    location: "reviews only",
    hint: "3 rejected fake reviews on unpurchased products.",
  },

  // Edge cases
  {
    id: "rachel_green",
    name: "Rachel Green",
    phone: "+1 212-555-0177",
    address: "90 Central Park West, New York, NY 10023",
    group: "edge",
    label: "Rachel Green",
    location: "New York, NY",
    hint: "3 clean orders. Test how history softens flags.",
  },
  {
    id: "kevin_park",
    name: "Kevin Park",
    phone: "+1 408-555-0166",
    address: "1500 Tech Drive, San Jose, CA 95110",
    group: "edge",
    label: "Kevin Park",
    location: "San Jose, CA",
    hint: "3 orders. One flagged then approved by admin.",
  },
  {
    id: "natalie_foster",
    name: "Natalie Foster",
    phone: "+1 617-555-0201",
    address: "12 Harvard Square, Cambridge, MA 02138",
    group: "edge",
    label: "Natalie Foster",
    location: "Cambridge, MA",
    hint: "2 orders. Post a respectful negative review as her.",
  },
];

export const GROUP_META = {
  guest: { label: "Guest", color: "gray", icon: "?" },
  trusted: { label: "Trusted Customers", color: "emerald", icon: "T" },
  new: { label: "New Customers", color: "blue", icon: "N" },
  suspicious: { label: "Suspicious / Previously Flagged", color: "red", icon: "!" },
  review_offender: { label: "Review Offenders", color: "amber", icon: "R" },
  edge: { label: "Edge Cases", color: "purple", icon: "E" },
};

export function getPersonaById(id) {
  if (id === "guest" || !id) return GUEST_CUSTOMER;
  return CUSTOMER_PERSONAS.find((p) => p.id === id) || GUEST_CUSTOMER;
}

export function groupPersonas() {
  const groups = {};
  CUSTOMER_PERSONAS.forEach((p) => {
    if (!groups[p.group]) groups[p.group] = [];
    groups[p.group].push(p);
  });
  return groups;
}
