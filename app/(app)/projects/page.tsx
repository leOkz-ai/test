import { FolderOpen } from 'lucide-react';
import { EmptyState } from '@/components/layout/empty-state';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { projects } from '@/lib/mock-data';

export default function ProjectsPage() {
  return (
    <div>
      <PageHeader title="Проекты" subtitle="Список ИТ-проектов и текущих оценок" />
      <Card>
        <CardHeader>
          <CardTitle>Проекты</CardTitle>
          <CardDescription>Управляйте бэклогом и отслеживайте статусы.</CardDescription>
        </CardHeader>
        <CardContent>
          {projects.length ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Название</TableHead>
                  <TableHead>Клиент</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead className="text-right">Часы</TableHead>
                  <TableHead className="text-right">Стоимость</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {projects.map((project) => (
                  <TableRow key={project.id}>
                    <TableCell className="font-medium">{project.name}</TableCell>
                    <TableCell>{project.client}</TableCell>
                    <TableCell>{project.status}</TableCell>
                    <TableCell className="text-right">{project.hours}</TableCell>
                    <TableCell className="text-right">{project.cost} ₽</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <EmptyState
              icon={FolderOpen}
              title="Пока нет проектов"
              description="Создайте новый проект, чтобы заполнить таблицу и начать планирование."
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
