import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("planes");

export default function PlanesPage() {
  return <SiteShell initialView="planes" />;
}
