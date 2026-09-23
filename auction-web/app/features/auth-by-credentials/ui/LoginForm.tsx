import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from 'react-router'; // Хук для навигации в RR v8
import { Button } from '~/shared/ui/Button';
import { cn } from '~/shared/lib/utils';
import { loginSchema, type LoginFormData } from '../model/schema';
import { useAuthStore } from '~/entities/user/model/authStore';

export const LoginForm = () => {
  const navigate = useNavigate();
  // Достаем функцию login из нашего Zustand-стора
  const login = useAuthStore((state) => state.login);

  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting }, 
    reset 
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  // ЕДИНСТВЕННАЯ функция onSubmit
  const onSubmit = async (data: LoginFormData) => {
    try {
      // Имитация успешного ответа от сервера и получения токена
      const fakeToken = "mock-jwt-token-12345";
      
      // 1. Сохраняем токен в Zustand (и в localStorage благодаря persist)
      login(fakeToken);
      
      // 2. Перенаправляем пользователя в профиль
      navigate('/profile');
      
      // 3. Очищаем форму (на случай, если пользователь вернется)
      reset();
    } catch (error) {
      console.error('Ошибка входа:', error);
      alert('Ошибка при входе');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 w-72">
      <div>
        <input
          {...register('login')}
          placeholder="Логин"
          className={cn(
            "w-full border p-2 rounded outline-none focus:ring-2 focus:ring-blue-500",
            errors.login && "border-red-500 focus:ring-red-500"
          )}
        />
        {errors.login && (
          <p className="text-red-500 text-xs mt-1">{errors.login.message}</p>
        )}
      </div>

      <div>
        <input
          {...register('password')}
          type="password"
          placeholder="Пароль"
          className={cn(
            "w-full border p-2 rounded outline-none focus:ring-2 focus:ring-blue-500",
            errors.password && "border-red-500 focus:ring-red-500"
          )}
        />
        {errors.password && (
          <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>
        )}
      </div>

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Вход...' : 'Войти'}
      </Button>
    </form>
  );
};