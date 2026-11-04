export type Story = {
  id: number;
  title: string;
  slug?: string;
  teaser?: string;
  author?: string;
  last_updated?: string;
  /** Optional image URL for the right panel */
  imageUrl?: string;
};