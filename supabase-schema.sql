create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.user_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.time_logs (
  id text primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.reward_events (
  id text primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.sync_mutations (
  id text primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  type text not null,
  payload jsonb,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
alter table public.user_state enable row level security;
alter table public.time_logs enable row level security;
alter table public.reward_events enable row level security;
alter table public.sync_mutations enable row level security;

create policy "profiles owner read" on public.profiles
  for select using (auth.uid() = id);
create policy "profiles owner upsert" on public.profiles
  for all using (auth.uid() = id) with check (auth.uid() = id);

create policy "user_state owner read" on public.user_state
  for select using (auth.uid() = user_id);
create policy "user_state owner upsert" on public.user_state
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "time_logs owner access" on public.time_logs
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "reward_events owner access" on public.reward_events
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "sync_mutations owner access" on public.sync_mutations
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
