import { FolderKanban, Layers3, ReceiptText, Timer } from 'lucide-react';
import { PageHeader } from '@/components/layout/page-header';
import { EmptyState } from '@/components/layout/empty-state';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { projects } from '@/lib/mock-data';

const totalHours = projects.reduce((acc, project) => acc + project.hours, 0);
const totalCost = projects.length ? `${projects.reduce((acc, project) => acc + project.cost, 0)} ₽` : 'NaN ₽';

const kpis = [
  {
    title: 'Всего проектов',
    value: String(projects.length),
    icon: FolderKanban,
    gradient: 'from-violet-600/30 via-violet-500/10 to-transparent'
  },
  {
    title: 'Активных',
    value: String(projects.filter((item) => item.status === 'active').length),
    icon: Layers3,
    gradient: 'from-cyan-500/30 via-emerald-500/10 to-transparent'
  },
  {
    title: 'Всего часов',
    value: String(totalHours),
    icon: Timer,
    gradient: 'from-emerald-500/30 via-lime-500/10 to-transparent'
  },
  {
    title: 'Общая стоимость',
    value: totalCost,
    icon: ReceiptText,
    gradient: 'from-orange-500/30 via-amber-500/10 to-transparent'
  }
];

export default function DashboardPage() {
  return (
    <div>
      <PageHeader title="Дашборд" subtitle="Обзор оценок ИТ-проектов" />

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {kpis.map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.title} className="relative overflow-hidden border-border/70">
              <div className={`absolute inset-0 bg-gradient-to-br ${item.gradient}`} />
              <CardHeader className="relative flex-row items-start justify-between space-y-0">
                <CardDescription>{item.title}</CardDescription>
                <div className="rounded-xl bg-slate-900/70 p-2 text-muted-foreground">
                  <Icon className="h-4 w-4" />
                </div>
              </CardHeader>
              <CardContent className="relative">
                <p className="text-3xl font-semibold tracking-tight">{item.value}</p>
              </CardContent>
            </Card>
          );
        })}
      </section>

      <section className="mt-6 grid gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader>
            <CardTitle>Недавние проекты</CardTitle>
            <CardDescription>Последние изменения по оценкам и статусам проектов.</CardDescription>
          </CardHeader>
          <CardContent>
            <EmptyState
              icon={FolderKanban}
              title="Нет проектов"
              description="Загрузите первое ТЗ, чтобы создать проект и начать оценку."
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Быстрые действия</CardTitle>
            <CardDescription>Запустите основные процессы в один клик.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3">
            <button className="rounded-2xl border border-border/70 bg-muted/20 p-4 text-left transition hover:bg-muted/40">
              <p className="font-medium">Загрузить ТЗ</p>
              <p className="text-sm text-muted-foreground">Импортируйте требования и создайте оценку.</p>
            </button>
            <button className="rounded-2xl border border-border/70 bg-muted/20 p-4 text-left transition hover:bg-muted/40">
              <p className="font-medium">Роли и ставки</p>
              <p className="text-sm text-muted-foreground">Настройте команду и стоимость часа.</p>
            </button>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
