import { z } from 'zod';

export const loginSchema = z.object({
  login: z.string().min(3, 'Логин должен быть не менее 3 символов'),
  password: z.string().min(6, 'Пароль должен быть не менее 6 символов'),
});

export type LoginFormData = z.infer<typeof loginSchema>;