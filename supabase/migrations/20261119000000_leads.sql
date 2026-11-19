-- Tabla para almacenar solicitudes de demostración y registros a la lista de espera desde el sitio público (aesteros-web).
create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  nombre text not null,
  correo text not null,
  org text,
  pregunta text,
  tipo text not null check (tipo in ('u', 'e')),
  espera boolean not null default false,
  ip_hash text,
  user_agent text
);

alter table public.leads enable row level security;

-- Sólo el service_role (desde el endpoint /api/leads) puede insertar o leer leads.
revoke all on table public.leads from anon, authenticated;
