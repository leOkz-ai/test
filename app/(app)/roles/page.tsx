import { Briefcase } from 'lucide-react';
import { EmptyState } from '@/components/layout/empty-state';
import { PageHeader } from '@/components/layout/page-header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { roleRates } from '@/lib/mock-data';

export default function RolesPage() {
  return (
    <div>
      <PageHeader
        title="Роли и ставки"
        subtitle="Матрица ролей для расчёта стоимости"
        actionLabel="Добавить роль"
      />
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0">
          <div>
            <CardTitle>Роли и ставки</CardTitle>
            <CardDescription>Определите ставки для всех участников команды.</CardDescription>
          </div>
          <Button variant="secondary">Добавить роль</Button>
        </CardHeader>
        <CardContent>
          {roleRates.length ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Роль</TableHead>
                  <TableHead className="text-right">Ставка</TableHead>
                  <TableHead className="text-right">Валюта</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {roleRates.map((role) => (
                  <TableRow key={role.id}>
                    <TableCell className="font-medium">{role.role}</TableCell>
                    <TableCell className="text-right">{role.rate}</TableCell>
                    <TableCell className="text-right">{role.currency}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <EmptyState
              icon={Briefcase}
              title="Роли не добавлены"
              description="Добавьте хотя бы одну роль, чтобы рассчитывать стоимость проектов точнее."
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
