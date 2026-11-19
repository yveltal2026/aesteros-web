import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("agencias");

export default function AgenciasPage() {
  return <SiteShell initialView="agencias" />;
}
