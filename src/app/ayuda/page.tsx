import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("ayuda");

export default function AyudaPage() {
  return <SiteShell initialView="ayuda" />;
}
