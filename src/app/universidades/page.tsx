import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("universidades");

export default function UniversidadesPage() {
  return <SiteShell initialView="universidades" />;
}
