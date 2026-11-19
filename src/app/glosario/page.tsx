import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("glosario");

export default function GlosarioPage() {
  return <SiteShell initialView="glosario" />;
}
