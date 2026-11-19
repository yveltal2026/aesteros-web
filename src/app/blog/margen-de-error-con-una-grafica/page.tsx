import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("a-margen");

export default function AMargenPage() {
  return <SiteShell initialView="a-margen" />;
}
