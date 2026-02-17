export type Project = {
  id: string;
  name: string;
  client: string;
  status: 'active' | 'paused' | 'done';
  hours: number;
  cost: number;
};

export type RoleRate = {
  id: string;
  role: string;
  rate: number;
  currency: string;
};

export const projects: Project[] = [];
export const roleRates: RoleRate[] = [];
