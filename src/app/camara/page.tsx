import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("camara");

export default function CamaraPage() {
  return <SiteShell initialView="camara" />;
}
