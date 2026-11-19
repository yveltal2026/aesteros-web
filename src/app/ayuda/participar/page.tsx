import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("participar");

export default function ParticiparPage() {
  return <SiteShell initialView="participar" />;
}
