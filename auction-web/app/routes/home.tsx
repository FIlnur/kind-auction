import { useQuery } from '@tanstack/react-query';
import { api } from '~/shared/api/instance';
import { Button } from '~/shared/ui/Button';
import { LotCard } from '~/entities/lot/ui/LotCard';
import { LoginForm } from '~/features/auth-by-credentials/ui/LoginForm';

interface User {
  id: number;
  login: string;
  avatar_url: string;
}

export default function Home() {
  // useQuery сам делает запрос, кэширует данные и возвращает статусы
  const { 
    data: users, 
    isLoading, 
    error 
  } = useQuery({
    queryKey: ['github-users'], // Уникальный ключ для кэша
    queryFn: () => api.get('/users').then((res) => res.data),
  });

  if (isLoading) return <div className="p-10">Загрузка...</div>;
  if (error) return <div className="p-10 text-red-500">Ошибка: {(error as Error).message}</div>;

  return (
    <div className="p-10">
      <h1 className="text-2xl mb-5">Список пользователей GitHub</h1>
      
      <div className="flex flex-wrap gap-4">
        {users.slice(0, 5).map((user: User) => (
          <LotCard
            key={user.id}
            title={user.login}
            price={user.id * 1000}
            imageUrl={user.avatar_url}
          />
        ))}
        <div className="mt-10 p-6 border rounded-lg bg-gray-50 w-fit">
          <h2 className="text-xl font-bold mb-4">Форма входа</h2>
          <LoginForm />
        </div>
      </div>

      <div className="mt-8 flex gap-4">
        <Button>Загрузить еще</Button>
        <Button variant="secondary">Отмена</Button>
      </div>
    </div>
  );
}