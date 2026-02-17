import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

type PageHeaderProps = {
  title: string;
  subtitle: string;
  actionLabel?: string;
};

export function PageHeader({ title, subtitle, actionLabel = '+ Новый проект' }: PageHeaderProps) {
  return (
    <div className="mb-6 flex flex-col gap-4 md:mb-8 md:flex-row md:items-start md:justify-between">
      <div>
        <h2 className="text-3xl font-semibold tracking-tight">{title}</h2>
        <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
      </div>
      <Button className="gap-2 self-start">
        <Plus className="h-4 w-4" />
        {actionLabel}
      </Button>
    </div>
  );
}
