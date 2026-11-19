import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("blog");

export default function BlogPage() {
  return <SiteShell initialView="blog" />;
}
