'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BarChart3, BriefcaseBusiness, ClipboardList, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { href: '/dashboard', label: 'Дашборд', icon: BarChart3 },
  { href: '/projects', label: 'Проекты', icon: BriefcaseBusiness },
  { href: '/roles', label: 'Роли и ставки', icon: ClipboardList }
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sticky top-0 hidden h-screen w-80 flex-col border-r border-border/70 bg-slate-950/70 p-6 backdrop-blur xl:flex">
      <div>
        <div className="mb-8 flex items-center gap-3">
          <div className="rounded-xl bg-primary/20 p-2 text-primary">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-lg font-semibold">IT Estimator</h1>
            <p className="text-xs text-muted-foreground">Оценка проектов</p>
          </div>
        </div>
        <nav className="space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium text-muted-foreground transition',
                  'hover:bg-muted hover:text-foreground',
                  isActive && 'bg-primary/15 text-primary'
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="mt-auto rounded-2xl border border-border/70 bg-muted/30 p-4">
        <p className="text-sm font-medium">Система оценки v1.0</p>
        <p className="mt-1 text-xs text-muted-foreground">Powered by AI</p>
      </div>
    </aside>
  );
}
