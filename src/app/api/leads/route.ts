import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
import crypto from "node:crypto";
import { leadSchema } from "@/lib/leads";
import { isSupabaseServerConfigured, publicEnv } from "@/lib/env";
import { rateLimit } from "@/lib/rate-limit";

function getClientIp(req: NextRequest): string {
  const forwarded = req.headers.get("x-forwarded-for");
  if (forwarded) return forwarded.split(",")[0]?.trim() || "0.0.0.0";
  return req.headers.get("x-real-ip") ?? "0.0.0.0";
}

export async function POST(req: NextRequest) {
  const ip = getClientIp(req);
  const rl = rateLimit(`leads:${ip}`, 10, 60_000);
  if (!rl.ok) {
    return NextResponse.json(
      {
        ok: false,
        error: "Demasiados intentos seguidos. Espera un minuto e inténtalo de nuevo.",
      },
      { status: 429 },
    );
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { ok: false, error: "Formato de solicitud inválido." },
      { status: 400 },
    );
  }

  const parsed = leadSchema.safeParse(body);
  if (!parsed.success) {
    const firstIssue = parsed.error.issues[0];
    return NextResponse.json(
      {
        ok: false,
        error: firstIssue?.message ?? "Revisa los datos del formulario.",
        field: firstIssue?.path[0] ?? null,
      },
      { status: 400 },
    );
  }

  const data = parsed.data;
  const ipHash = crypto.createHash("sha256").update(ip).digest("hex").slice(0, 32);
  const userAgent = (req.headers.get("user-agent") ?? "").slice(0, 255);

  let stored = false;
  if (isSupabaseServerConfigured()) {
    try {
      const { supabaseUrl } = publicEnv();
      const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
      const supabase = createClient(supabaseUrl, serviceKey, {
        auth: { persistSession: false, autoRefreshToken: false },
      });
      const { error } = await supabase.from("leads").insert({
        nombre: data.nombre,
        correo: data.correo,
        org: data.org || null,
        pregunta: data.pregunta || null,
        tipo: data.tipo,
        espera: data.espera,
        ip_hash: ipHash,
        user_agent: userAgent || null,
      });
      if (!error) stored = true;
    } catch {
      stored = false;
    }
  }

  const message = data.espera
    ? `Listo, ${data.nombre}. Te avisaremos en ${data.correo} cuando abra el registro y de cada herramienta nueva.`
    : `Gracias, ${data.nombre}. Recibimos tu solicitud y te escribiremos a ${data.correo} para agendar la demostración.`;

  return NextResponse.json({
    ok: true,
    stored,
    message,
  });
}
