import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("a-mapa");

export default function AMapaPage() {
  return <SiteShell initialView="a-mapa" />;
}
