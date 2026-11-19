import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("a-asociacion");

export default function AAsociacionPage() {
  return <SiteShell initialView="a-asociacion" />;
}
