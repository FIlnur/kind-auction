import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { useAuthStore } from '~/entities/user/model/authStore';
import { Button } from '~/shared/ui/Button';

export default function Profile() {
  const { isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/home', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  if (!isAuthenticated) {
    return <div className="p-10">Перенаправление...</div>;
  }

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold mb-5">Личный кабинет</h1>
      <p className="mb-6 text-green-600">Вы успешно авторизованы! Это защищенная страница.</p>
      
      <Button variant="secondary" onClick={logout}>
        Выйти из аккаунта
      </Button>
    </div>
  );
}