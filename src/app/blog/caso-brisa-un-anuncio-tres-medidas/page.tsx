import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("a-brisa");

export default function ABrisaPage() {
  return <SiteShell initialView="a-brisa" />;
}
